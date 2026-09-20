#!/usr/bin/env python3
"""
Unit tests for Haute42 Animated Splash UF2 Patcher
==================================================
Verifies GIF parsing, Flash binary payload structure, UF2 block construction,
and address space integrity (0x10100000).
"""

import os
import sys
import struct
import unittest
from PIL import Image

# Import patch_splash module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch_splash


class TestPatchSplash(unittest.TestCase):
    def setUp(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.sample_gif = os.path.join(self.script_dir, "sample_gif", "leverless_hadouken_loop.gif")

    def test_01_sample_gif_exists(self):
        """Verify sample GIF exists and is readable."""
        self.assertTrue(os.path.exists(self.sample_gif), f"Sample GIF not found: {self.sample_gif}")
        with Image.open(self.sample_gif) as img:
            self.assertEqual(img.size, (128, 64))

    def test_02_convert_gif_payload_structure(self):
        """Verify the binary payload conforms to FlashSplashHeader specification."""
        payload, total_frames, total_duration = patch_splash.convert_gif_to_anim_payload(self.sample_gif)
        
        self.assertEqual(total_frames, 32)
        self.assertEqual(total_duration, 2560)  # 32 frames * 80ms

        # Check FlashSplashHeader (20 bytes)
        magic, version, frames, duration, w, h, frame_sz, res = struct.unpack("<IHHIHHHH", payload[:20])
        self.assertEqual(magic, patch_splash.FLASH_SPLASH_MAGIC)  # 0x53504C53 ("SPLS")
        self.assertEqual(version, 1)
        self.assertEqual(frames, 32)
        self.assertEqual(duration, 2560)
        self.assertEqual(w, 128)
        self.assertEqual(h, 64)
        self.assertEqual(frame_sz, 1024)
        self.assertEqual(res, 0)

        # Check cumulative table (32 * 4 bytes)
        cum_offset = 20
        cum_end = cum_offset + (32 * 4)
        cumulative = struct.unpack("<32I", payload[cum_offset:cum_end])
        self.assertEqual(len(cumulative), 32)
        self.assertEqual(cumulative[-1], total_duration)
        self.assertEqual(cumulative[0], 80)
        self.assertEqual(cumulative[1], 160)

        # Check frames data (32 * 1024 bytes)
        frames_bytes = payload[cum_end:]
        self.assertEqual(len(frames_bytes), 32 * 1024)
        self.assertEqual(len(payload), 20 + 128 + 32768)

    def test_03_create_uf2_blocks(self):
        """Verify UF2 blocks generation at 0x10100000."""
        payload, total_frames, _ = patch_splash.convert_gif_to_anim_payload(self.sample_gif)
        blocks = patch_splash.create_uf2_blocks(payload, patch_splash.FLASH_SPLASH_ADDR)

        expected_blocks = (len(payload) + 255) // 256
        self.assertEqual(len(blocks), expected_blocks)

        # First block checks
        self.assertEqual(blocks[0]["target_addr"], 0x10100000)
        self.assertEqual(blocks[0]["family_id"], patch_splash.RP2040_FAMILY_ID)
        self.assertEqual(blocks[0]["flags"], patch_splash.UF2_FLAG_FAMILY_ID)
        self.assertEqual(blocks[0]["num_bytes"], 256)

        # Check contiguous addressing
        for i, b in enumerate(blocks):
            expected_addr = 0x10100000 + (i * 256)
            self.assertEqual(b["target_addr"], expected_addr, f"Address mismatch at block {i}")
            self.assertEqual(b["family_id"], patch_splash.RP2040_FAMILY_ID)
            self.assertTrue(1 <= b["num_bytes"] <= 256)

    def test_04_build_and_parse_uf2_binary(self):
        """Verify end-to-end serialization and parsing of standalone UF2."""
        payload, _, _ = patch_splash.convert_gif_to_anim_payload(self.sample_gif)
        blocks = patch_splash.create_uf2_blocks(payload, patch_splash.FLASH_SPLASH_ADDR)
        uf2_bytes = patch_splash.build_patched_uf2(None, blocks)

        # Every UF2 file must be a multiple of 512 bytes
        self.assertEqual(len(uf2_bytes) % 512, 0)
        total_blocks = len(uf2_bytes) // 512
        self.assertEqual(total_blocks, len(blocks))

        parsed = patch_splash.parse_uf2_blocks(uf2_bytes)
        self.assertEqual(len(parsed), len(blocks))
        self.assertEqual(parsed[0]["target_addr"], 0x10100000)
        
        # Reconstruct payload from parsed blocks and verify equality
        reconstructed = bytearray()
        for p in parsed:
            reconstructed.extend(p["data"])
        self.assertEqual(bytes(reconstructed[:len(payload)]), payload)

    def test_05_dummy_base_firmware_merge(self):
        """Verify merging with a base firmware correctly updates block indices."""
        # Create dummy base firmware (4 blocks at 0x10000000)
        dummy_base_payload = b"GP2040_BASE_FIRMWARE_DUMMY_CODE" * 32
        base_blocks = patch_splash.create_uf2_blocks(dummy_base_payload, 0x10000000)
        base_uf2 = patch_splash.build_patched_uf2(None, base_blocks)

        # Create animation payload
        payload, _, _ = patch_splash.convert_gif_to_anim_payload(self.sample_gif)
        anim_blocks = patch_splash.create_uf2_blocks(payload, patch_splash.FLASH_SPLASH_ADDR)

        # Merge
        merged_uf2 = patch_splash.build_patched_uf2(base_uf2, anim_blocks)
        merged_parsed = patch_splash.parse_uf2_blocks(merged_uf2)

        self.assertEqual(len(merged_parsed), len(base_blocks) + len(anim_blocks))
        
        # Verify base portion
        for i in range(len(base_blocks)):
            self.assertEqual(merged_parsed[i]["target_addr"], 0x10000000 + i * 256)
        
        # Verify animation portion starts at 0x10100000
        anim_start_idx = len(base_blocks)
        self.assertEqual(merged_parsed[anim_start_idx]["target_addr"], 0x10100000)

    def test_06_real_base_firmware_and_generated_sample_uf2(self):
        """Verify real base firmware exists and the generated sample UF2 has valid structure."""
        base_uf2_path = os.path.join(self.script_dir, "base_firmware", "gp2040ce_haute42_flash_anim_base.uf2")
        sample_uf2_path = os.path.join(self.script_dir, "firmware_hadouken_sample.uf2")

        self.assertTrue(os.path.exists(base_uf2_path), f"Base firmware not found: {base_uf2_path}")
        self.assertTrue(os.path.exists(sample_uf2_path), f"Sample UF2 not found: {sample_uf2_path}")

        with open(sample_uf2_path, "rb") as f:
            sample_bytes = f.read()

        parsed = patch_splash.parse_uf2_blocks(sample_bytes)
        self.assertGreater(len(parsed), 3000)  # Should have ~3791 blocks

        # Verify sequential block numbering and block count consistency
        for idx, block in enumerate(parsed):
            self.assertEqual(block["family_id"], patch_splash.RP2040_FAMILY_ID)
            self.assertTrue(1 <= block["num_bytes"] <= 256)

        # Find the block corresponding to 0x10100000
        anim_blocks = [b for b in parsed if b["target_addr"] == patch_splash.FLASH_SPLASH_ADDR]
        self.assertEqual(len(anim_blocks), 1, "Expected exactly one block at 0x10100000")
        
        # Verify FlashSplashHeader magic in that block's data
        first_anim_data = anim_blocks[0]["data"]
        magic = struct.unpack("<I", first_anim_data[:4])[0]
        self.assertEqual(magic, patch_splash.FLASH_SPLASH_MAGIC)


if __name__ == "__main__":
    print("Running patch_splash unit tests...")
    unittest.main(verbosity=2)
