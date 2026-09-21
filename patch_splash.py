#!/usr/bin/env python3
"""
Haute42 Animated Splash UF2 Patcher
===================================
Injects custom 128x64 animated GIF splash screens directly into GP2040-CE base firmware.
No C++ compiler or Pico SDK required.

License: MIT License
"""

import os
import sys
import glob
import struct
import argparse
from typing import List, Tuple, Optional
from PIL import Image, ImageSequence, ImageOps

# Constants for Flash splash structure
FLASH_SPLASH_MAGIC = 0x53504C53  # "SPLS" in Little Endian
FLASH_SPLASH_ADDR  = 0x10100000  # 1MB offset in RP2040 Flash

# Constants for UF2 format
UF2_MAGIC_START0    = 0x0A324655
UF2_MAGIC_START1    = 0x9E5D5157
UF2_MAGIC_END       = 0x0AB16F30
UF2_FLAG_FAMILY_ID  = 0x00002000
RP2040_FAMILY_ID    = 0xE48BFF56
PAYLOAD_SIZE        = 256
UF2_BLOCK_SIZE      = 512


def convert_gif_to_anim_payload(
    gif_path: str,
    threshold: int = 128,
    dither: bool = False,
    invert: bool = False,
    min_delay_ms: int = 20,
    max_frames: int = 128
) -> Tuple[bytes, int, int]:
    """
    Parse animated GIF and generate binary payload conforming to FlashSplashHeader.
    Returns: (payload_bytes, frame_count, total_duration_ms)
    """
    if not os.path.exists(gif_path):
        raise FileNotFoundError(f"GIF file not found: {gif_path}")

    frames_raw = []
    delays = []

    with Image.open(gif_path) as img:
        frame_idx = 0
        for frame in ImageSequence.Iterator(img):
            if frame_idx >= max_frames:
                print(f"[WARN] Reached maximum frame limit ({max_frames}). Truncating further frames.")
                break

            # Duration
            duration = frame.info.get("duration", 100)
            if duration is None or duration <= 0:
                duration = 100
            if duration < min_delay_ms:
                duration = min_delay_ms
            delays.append(int(duration))

            # Convert to RGBA for transparency handling
            rgba = frame.convert("RGBA")
            target_w, target_h = 128, 64
            canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 255))

            # Preserve aspect ratio with crisp nearest-neighbor scaling
            src_w, src_h = rgba.size
            scale = min(target_w / src_w, target_h / src_h)
            new_w = max(1, int(round(src_w * scale)))
            new_h = max(1, int(round(src_h * scale)))
            scaled = rgba.resize((new_w, new_h), Image.Resampling.NEAREST)

            # Center on 128x64 canvas
            off_x = (target_w - new_w) // 2
            off_y = (target_h - new_h) // 2
            canvas.paste(scaled, (off_x, off_y), scaled)

            gray = canvas.convert("L")
            if dither:
                mono = gray.convert("1", dither=Image.Dither.FLOYDSTEINBERG)
            else:
                mono = gray.point(lambda p: 255 if p >= threshold else 0, mode="1")

            if invert:
                mono = ImageOps.invert(mono.convert("L")).convert("1")

            raw_bytes = mono.tobytes()
            if len(raw_bytes) != 1024:
                raise ValueError(f"Unexpected frame byte size {len(raw_bytes)}, expected 1024")
            frames_raw.append(raw_bytes)
            frame_idx += 1

    total_frames = len(frames_raw)
    if total_frames == 0:
        raise ValueError("No frames found in GIF")

    total_duration = sum(delays)
    cumulative = []
    curr = 0
    for d in delays:
        curr += d
        cumulative.append(curr)

    # Pack FlashSplashHeader (20 bytes)
    # magic: uint32, version: uint16, frame_count: uint16, total_duration: uint32,
    # width: uint16, height: uint16, frame_size: uint16, reserved: uint16
    header_bytes = struct.pack(
        "<IHHIHHHH",
        FLASH_SPLASH_MAGIC,
        1,  # version
        total_frames,
        total_duration,
        128,  # width
        64,   # height
        1024, # frame_size
        0     # reserved
    )

    # Pack cumulative times: uint32[total_frames]
    cum_bytes = struct.pack(f"<{total_frames}I", *cumulative)

    # Pack all raw frame bytes
    all_frames_bytes = b"".join(frames_raw)

    payload = header_bytes + cum_bytes + all_frames_bytes
    return payload, total_frames, total_duration


def parse_uf2_blocks(uf2_bytes: bytes) -> List[dict]:
    """Parse raw UF2 binary into a list of block dictionaries."""
    blocks = []
    num_blocks = len(uf2_bytes) // UF2_BLOCK_SIZE
    for i in range(num_blocks):
        chunk = uf2_bytes[i * UF2_BLOCK_SIZE : (i + 1) * UF2_BLOCK_SIZE]
        magic0, magic1, flags, target_addr, num_bytes, block_no, total_blocks, family_id = struct.unpack(
            "<IIIIIIII", chunk[:32]
        )
        magic_end = struct.unpack("<I", chunk[508:512])[0]
        if magic0 != UF2_MAGIC_START0 or magic1 != UF2_MAGIC_START1 or magic_end != UF2_MAGIC_END:
            raise ValueError(f"Corrupt UF2 block detected at block index {i}")

        blocks.append({
            "flags": flags,
            "target_addr": target_addr,
            "num_bytes": num_bytes,
            "family_id": family_id,
            "data": chunk[32 : 32 + num_bytes],
        })
    return blocks


def create_uf2_blocks(payload: bytes, start_addr: int = FLASH_SPLASH_ADDR) -> List[dict]:
    """Convert raw byte payload into UF2 block structures."""
    blocks = []
    # RP2040 BootROM requires payloadSize to be exactly 256 bytes per block.
    # Pad payload to an exact multiple of PAYLOAD_SIZE (256) with 0xFF (flash erased state).
    remainder = len(payload) % PAYLOAD_SIZE
    padded_payload = payload
    if remainder != 0:
        padded_payload += b"\xff" * (PAYLOAD_SIZE - remainder)

    offset = 0
    cur_addr = start_addr
    while offset < len(padded_payload):
        chunk = padded_payload[offset : offset + PAYLOAD_SIZE]
        blocks.append({
            "flags": UF2_FLAG_FAMILY_ID,
            "target_addr": cur_addr,
            "num_bytes": PAYLOAD_SIZE,
            "family_id": RP2040_FAMILY_ID,
            "data": chunk,
        })
        cur_addr += PAYLOAD_SIZE
        offset += PAYLOAD_SIZE
    return blocks


def build_patched_uf2(base_uf2_bytes: Optional[bytes], anim_blocks: List[dict]) -> bytes:
    """
    Merge base UF2 blocks with animation blocks and produce a valid unified UF2 binary.
    If base_uf2_bytes is None, outputs standalone animation UF2.
    """
    combined_blocks = []
    if base_uf2_bytes:
        combined_blocks.extend(parse_uf2_blocks(base_uf2_bytes))

    combined_blocks.extend(anim_blocks)
    total_blocks = len(combined_blocks)

    output = bytearray()
    for block_no, b in enumerate(combined_blocks):
        # 476 bytes payload space (padded with 0x00)
        padded_data = b["data"].ljust(476, b"\x00")
        header = struct.pack(
            "<IIIIIIII",
            UF2_MAGIC_START0,
            UF2_MAGIC_START1,
            b["flags"],
            b["target_addr"],
            b["num_bytes"],
            block_no,
            total_blocks,
            b["family_id"],
        )
        end = struct.pack("<I", UF2_MAGIC_END)
        output.extend(header + padded_data + end)

    return bytes(output)


def find_default_gif(default_path: str = "sample_gif/leverless_hadouken_loop.gif") -> str:
    """Find default sample GIF."""
    if os.path.exists(default_path):
        return default_path
    raise FileNotFoundError(f"Default sample GIF not found at: {default_path}")


def find_base_uf2(search_dir: str = "base_firmware") -> Optional[str]:
    """Find the GP2040-CE base .uf2 firmware in search_dir."""
    if os.path.exists(search_dir):
        uf2s = glob.glob(os.path.join(search_dir, "*.uf2"))
        if uf2s:
            return uf2s[0]
    return None


def main():
    parser = argparse.ArgumentParser(description="Haute42 Animated Splash Screen UF2 Patcher")
    parser.add_argument("--gif", "-g", help="Path to input GIF file")
    parser.add_argument("--base-uf2", "-b", help="Path to base GP2040-CE UF2 firmware")
    parser.add_argument("--output", "-o", default="firmware_custom.uf2", help="Path to output UF2 file")
    parser.add_argument("--standalone", action="store_true", help="Output only the animation UF2 blocks without base firmware")
    parser.add_argument("--threshold", type=int, default=128, help="Binarization threshold (0-255)")
    parser.add_argument("--dither", action="store_true", help="Use Floyd-Steinberg dithering")
    parser.add_argument("--invert", action="store_true", help="Invert monochrome colors")
    parser.add_argument("--max-frames", type=int, default=128, help="Maximum frame limit")

    args = parser.parse_args()

    # Determine input GIF
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = args.gif
    if not gif_path:
        default_sample = os.path.join(script_dir, "sample_gif", "leverless_hadouken_loop.gif")
        gif_path = find_default_gif(default_sample)

    print("==================================================")
    print("   Haute42 Animated Splash UF2 Patcher")
    print("==================================================")
    print(f"[INFO] Input GIF       : {gif_path}")

    # Convert GIF
    payload, total_frames, total_duration = convert_gif_to_anim_payload(
        gif_path,
        threshold=args.threshold,
        dither=args.dither,
        invert=args.invert,
        max_frames=args.max_frames
    )
    print(f"[INFO] Animation parsed: {total_frames} frames, {total_duration} ms total duration")
    print(f"[INFO] Payload size    : {len(payload)} bytes")

    # Generate animation UF2 blocks
    anim_blocks = create_uf2_blocks(payload, FLASH_SPLASH_ADDR)
    print(f"[INFO] Flash address   : 0x{FLASH_SPLASH_ADDR:08X}")
    print(f"[INFO] Anim UF2 blocks : {len(anim_blocks)} blocks ({len(anim_blocks) * UF2_BLOCK_SIZE} bytes)")

    # Handle Base Firmware
    base_uf2_bytes = None
    if not args.standalone:
        base_uf2_path = args.base_uf2
        if not base_uf2_path:
            base_uf2_path = find_base_uf2(os.path.join(script_dir, "base_firmware"))

        if base_uf2_path and os.path.exists(base_uf2_path):
            print(f"[INFO] Base firmware   : {base_uf2_path}")
            with open(base_uf2_path, "rb") as f:
                base_uf2_bytes = f.read()
        else:
            print("[WARN] Base firmware not found in base_firmware/. Generating standalone animation UF2.")

    # Output
    out_path = os.path.abspath(args.output)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    patched_bytes = build_patched_uf2(base_uf2_bytes, anim_blocks)
    with open(out_path, "wb") as f:
        f.write(patched_bytes)

    print("--------------------------------------------------")
    print(f"[SUCCESS] Generated    : {out_path}")
    print(f"[SUCCESS] File size    : {len(patched_bytes):,} bytes ({len(patched_bytes) // UF2_BLOCK_SIZE} UF2 blocks)")
    print("==================================================")
    print("Ready to flash! Drag & drop to your RPI-RP2 drive.")


if __name__ == "__main__":
    main()
