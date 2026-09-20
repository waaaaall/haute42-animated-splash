# Haute42 Animated Splash Screen UF2 Patcher

[English](#english) | [日本語](#日本語)

Easily inject custom 128x64 animated GIF splash screens into your **Haute42 G16** (and Haute42 COSMOX OLED 128x64 controllers) running **GP2040-CE v0.7.9**.  
**No C++ compiler, CMake, or Raspberry Pi Pico SDK required!**

<p align="center">
  <img src="sample_gif/leverless_hadouken_preview_4x.gif" alt="Hadouken Leverless Splash Animation" width="400" />
  <br>
  <em>Sample: Leverless Hadouken (236+P) Animation (CC0 / Public Domain)</em>
</p>

<p align="center">
  <a href="https://x.com/good_wall/status/2101679788842996177" target="_blank">
    <img src="assets/hardware_demo.gif" alt="Watch Real Hardware Demo on X" width="260" />
  </a>
  <br>
  <em>🎬 <strong>Real Hardware Demo / 実機動作デモ:</strong> <a href="https://x.com/good_wall/status/2101679788842996177">Watch on X (Twitter)</a></em>
</p>

---

<a name="english"></a>
## English

### ✨ Features
- **No Compilation Needed**: Automatically patches pre-compiled GP2040-CE firmware in under 1 second.
- **Easy Windows Workflow**: Place your GIF into `custom_gif/` and double-click `generate_firmware.bat`.
- **Infinite Looping Splash**: Plays smooth animated loops continuously without exiting to the button display.
- **Variable Frame Delay**: Accurately preserves individual frame timings from your GIF.
- **Auto-Formatting**: Automatically scales, centers, and binarizes arbitrary GIFs into 128x64 1-bit monochrome.
- **Pre-packaged Sample**: Includes a ready-to-flash Hadouken leverless input animation (CC0 / Public Domain).

### 🚀 Quick Start

#### Option A: Flash Pre-built Sample Firmware (Fastest)
1. Download `firmware_hadouken_sample.uf2` from [GitHub Releases](https://github.com/waaaaall/haute42-animated-splash/releases).
2. Unplug your Haute42 controller.
3. Hold down the **BOOTSEL** button (or UP/BOOT button depending on model) and connect the USB cable to your PC.
4. A USB storage drive named `RPI-RP2` will appear.
5. Drag and drop the `.uf2` file into the `RPI-RP2` drive.
6. The controller will reboot automatically into your new animated splash screen!

#### Option B: Use Your Own Animated GIF
1. Download or clone this repository:
   ```bash
   git clone https://github.com/waaaaall/haute42-animated-splash.git
   ```
2. Put your animated GIF into the `custom_gif/` folder (e.g. `custom_gif/my_cool_anim.gif`).
3. Double-click **`generate_firmware.bat`** (Windows) or run:
   ```bash
   python patch_splash.py
   ```
4. A newly created **`firmware_custom.uf2`** will appear in the folder!
5. Flash it to your Haute42 controller following the BOOTSEL instructions above.

### 🎨 GIF Requirements & Recommendations
- **Resolution**: 128 x 64 pixels (recommended).
- **Color**: Monochrome 1-bit (White on black background recommended).
- **Frames**: Up to 128 frames (16 to 48 frames recommended).
- For details and tips, see [`sample_gif/README.md`](sample_gif/README.md).

---

<a name="日本語"></a>
## 日本語

### 📺 実機デモ
実際の Haute42 G16 でアニメーションが点灯・常時再生されている様子はこちらのポストをご覧ください：  
👉 **[X (Twitter) で実機動画を見る](https://x.com/good_wall/status/2101679788842996177)**

### ✨ 特徴
- **環境構築ゼロ**: C++コンパイラやPico SDK、CMakeは一切不要。Pythonスクリプトがビルド済みベースファームウェアに1秒で直接パッチを適用します。
- **直感的な操作**: `custom_gif/` フォルダにお好みのGIFを入れて `generate_firmware.bat` をダブルクリックするだけ。
- **常時ループ再生**: 起動後もボタン画面に遷移せず、滑らかなアニメーションを常時無限ループ再生します。
- **可変フレームレート対応**: GIF本来のコマごとのディレイ（緩急）を忠実に再現。
- **自動フォーマット**: 異なるサイズのGIFでも、128x64の中央配置・モノクロ2値化へ自動変換。
- **安全なオリジナルサンプル同梱**: 権利フリー（CC0）な「波動拳コマンド入力アニメーション」を同梱。

### 🚀 クイックスタート

#### 方法A: 完成品サンプルをすぐ試す（最も簡単）
1. [GitHub Releases](https://github.com/waaaaall/haute42-animated-splash/releases) から `firmware_hadouken_sample.uf2` をダウンロードします。
2. Haute42 コントローラーのUSBケーブルを抜きます。
3. **BOOTSELボタン**（または天面BOOTキー／上ボタン）を押しながらPCにUSB接続します。
4. PC上に `RPI-RP2` というUSBドライブが認識されます。
5. ダウンロードした `.uf2` ファイルを `RPI-RP2` ドライブへドラッグ＆ドロップします。
6. コントローラーが自動再起動し、アニメーションが再生されます！

#### 方法B: 自作GIFでファームウェアを作成する
1. 本リポジトリをダウンロード（ZIP解凍または `git clone`）します。
2. `custom_gif/` フォルダにお好みのGIF画像を置きます（例: `custom_gif/my_animation.gif`）。
3. **`generate_firmware.bat`** をダブルクリックして実行します（CLIの場合は `python patch_splash.py`）。
4. フォルダ直下に **`firmware_custom.uf2`** が生成されます！
5. 上記の手順に従って `RPI-RP2` ドライブへ書き込んでください。

---

## ⚠️ Disclaimer / 免責事項
- This project is not officially affiliated with Haute42 or the GP2040-CE project.
- Flashing firmware is done at your own risk. Always ensure you have a backup of your original controller firmware.
- Users are solely responsible for ensuring they hold the necessary rights or permissions for any custom GIF animations they create and flash for personal use.
- 本プロジェクトは Haute42 公式および GP2040-CE 公式とは独立した有志プロジェクトです。
- ファームウェアの書き込みは自己責任で行ってください。必要に応じて元のファームウェアをバックアップしてください。
- ユーザーが独自に導入するアニメーション素材の著作権については、私的使用の範囲を含め利用者の自己責任において管理してください。

---

## 📜 License & Credits
- **Patch Tool & Sample**: Licensed under the [MIT License](LICENSE).
- **Sample Animation (`sample_gif/leverless_hadouken_loop.gif`)**: Dedicated to the public domain under **CC0 1.0**.
- **Base Firmware**: Derived from [GP2040-CE](https://github.com/OpenStickCommunity/GP2040-CE) (MIT License, Copyright (c) 2024 OpenStickCommunity).
