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
    <img src="assets/hardware_demo.gif" alt="Watch Real Hardware Demo on Haute42 G16" width="280" />
  </a>
  <br>
  <em>🎬 <strong>Real Hardware Demo / 実機動作デモ:</strong> <a href="https://x.com/good_wall/status/2101679788842996177">Watch on X (Twitter)</a></em>
</p>

---

<a name="english"></a>
## English

### ✨ Features
- **WebConfig GUI Direct Upload**: Upload animated GIFs directly through your browser (`http://192.168.7.1`) into controller Flash memory with real-time OLED simulation preview—no firmware reflashing or BOOTSEL button required!
- **No Compilation Needed**: Pre-patched firmware or 1-second Python offline patcher—no C++ compiler, CMake, or Pico SDK required.
- **Easy Windows Workflow**: Place your GIF into `custom_gif/` and double-click `generate_firmware.bat` for offline `.uf2` generation.
- **Infinite Looping Splash**: Plays smooth animated loops continuously without exiting to the button display.
- **Variable Frame Delay**: Accurately preserves individual frame timings from your GIF.
- **Auto-Formatting**: Automatically scales, centers, and binarizes arbitrary GIFs into 128x64 1-bit monochrome.
- **Pre-packaged Sample**: Includes a ready-to-flash Hadouken leverless input animation (CC0 / Public Domain).

### 🚀 Usage Methods

You can update animations using either **Method A (WebConfig GUI)** or **Method B (UF2 File Flash)**:

---

#### 🌐 Method A: WebConfig GUI Direct Upload (Recommended — No Re-flashing Needed!)

Once the base animated splash firmware is installed on your controller, you never need to enter BOOTSEL mode or drag-and-drop `.uf2` files again!

1. Hold the **START** button while plugging the controller into your PC via USB.
2. Open **`http://192.168.7.1`** in any web browser.
3. Navigate to **Configuration** → **Display Configuration**.
4. Scroll down to the **Animated Splash Screen (GIF Direct Upload)** section.
5. Click **Choose File** and select your favorite animated GIF:
   - The interactive preview will simulate your OLED display in real time with the actual frame delay.
   - Adjust the **Brightness Threshold** slider or toggle **Invert Black/White** if needed.
6. Click **Write Animation to Flash**. The progress bar will indicate flash sector erase and chunk programming progress.
7. Replug or restart your controller—your new animation plays immediately upon boot!
   - You can also click **Clear Animation from Flash** anytime to revert to the default static splash screen.

---

#### 📦 Method B: UF2 Firmware Patcher (Offline Flashing)

If you prefer flashing a standalone `.uf2` binary file:

##### Step 1: Prepare the `.uf2` Firmware File
- **Pre-built Sample**: Download `firmware_hadouken_sample.uf2` from [GitHub Releases](https://github.com/waaaaall/haute42-animated-splash/releases).
- **Your Own Custom GIF**:
  1. Clone or download this repository.
  2. Put your animated GIF into `custom_gif/` (e.g. `custom_gif/my_animation.gif`).
  3. Double-click `generate_firmware.bat` (or run `python patch_splash.py`).
  4. Your custom `firmware_custom.uf2` will be generated in the root directory!

##### Step 2: Put Controller into BOOTSEL (`RPI-RP2`) Mode
Choose any of the following official methods to enter bootloader mode:
- **Method 1 (Hardware BOOT Button - Recommended)**:
  Unplug the controller. Locate the small **BOOT button** (or pinhole on the back/side). Hold it down while plugging the USB cable into your PC.
- **Method 2 (Button Shortcut)**:
  While connected normally, press and hold **`Start + X + Y`** (or **`Start + Select + Up`**) for 5+ seconds until the screen freezes into boot mode.
- **Method 3 (WebConfig)**:
  Hold the **START** button while plugging in USB, open `http://192.168.7.1` in your browser, and click **Reboot > Bootsel**.

##### Step 3: Copy Firmware
1. Your PC will recognize the controller as a USB drive named **`RPI-RP2`**.
2. **Drag and drop** your `.uf2` file into the `RPI-RP2` drive.
3. The drive will automatically disconnect, and the controller will reboot into your new animated splash!

> 💡 **Notes & Troubleshooting:**
> - Always use a **data-capable USB Type-C cable** (charging-only cables won't work).
> - If Windows prompts you to "format the drive", **DO NOT FORMAT**. Simply copy the `.uf2` file.

### ⚙️ WebConfig Settings (Display Configuration for Always-On Animation)
If your screen switches to the button layout display (e.g. after 5 seconds) instead of continuously looping the animation, configure these options in WebConfig:

1. Hold the **START** button while plugging the controller into your PC via USB.
2. Open **`http://192.168.7.1`** in any web browser.
3. Navigate to **Configuration** → **Display Configuration**.
4. Configure the following options:
   - **Hardware Options > Enabled**: `Enabled`
   - **Splash Mode**: **`Enabled (Custom Splash Screen)`**
   - **Splash Duration (seconds, 0 for Always On)**: Set to **`0`**  
     *(⚠️ Critical: Setting this to `0` enables "Always On" mode so the animation loops infinitely and never transitions to the button screen!)*
   - **Display Saver Timeout (minutes)**: Set to **`0`** (prevents screen from turning off)
5. Click **Save** at the bottom of the page and replug your controller.

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
- **WebConfig GUI からの直接アップロード**: 一度導入すれば、次回以降はブラウザ画面（`http://192.168.7.1`）から直接GIFを選択・OLEDシミュレーションプレビューしながらFlashメモリへ直接書き込み可能！BOOTSELモードや再フラッシュは一切不要。
- **環境構築ゼロ**: C++コンパイラやPico SDK、CMakeは一切不要。Pythonスクリプトがビルド済みベースファームウェアに1秒で直接パッチを適用（オフライン作成も可能）。
- **直感的な操作**: `custom_gif/` フォルダにお好みのGIFを入れて `generate_firmware.bat` をダブルクリックするだけでも `.uf2` を生成可能。
- **常時ループ再生**: 起動後もボタン画面に遷移せず、滑らかなアニメーションを常時無限ループ再生します。
- **可変フレームレート対応**: GIF本来のコマごとのディレイ（緩急）を忠実に再現。
- **自動フォーマット**: 異なるサイズのGIFでも、128x64の中央配置・モノクロ2値化へ自動変換。
- **安全なオリジナルサンプル同梱**: 権利フリー（CC0）な「波動拳コマンド入力アニメーション」を同梱。

### 🚀 アニメーション更新方法

アニメーションの更新は **方法A（WebConfig GUIからの直接更新）** または **方法B（UF2ファイルによる一括書き込み）** のどちらでも行えます：

---

#### 🌐 方法A: WebConfig GUI からの直接アップロード（推奨・再フラッシュ不要！）

本ファームウェア導入後は、**BOOTSELボタンを押してファームウェアを書き直す必要はありません**。普段お使いのWebブラウザから直接アニメーションを入れ替えられます：

1. **START ボタン** を押しながらコントローラーのUSBケーブルをPCに接続します。
2. ブラウザで **`http://192.168.7.1`** を開きます。
3. **Configuration** → **Display Configuration** に移動します。
4. ページ下部の **Animated Splash Screen (GIF Direct Upload)** セクションへ進みます。
5. **ファイルを選択** でお好きなGIFアニメーションを選択します。
   - 画面上のOLEDシミュレータで、実際のフレーム速度に合わせたリアルタイムプレビューが再生されます。
   - 必要に応じて **Brightness Threshold（二値化しきい値）** スライダーや **Invert Black/White（白黒反転）** を調整できます。
6. **Write Animation to Flash** ボタンをクリックします。プログレスバーが表示され、Flashメモリへ分割転送されます。
7. 書き込み完了！コントローラーを再接続（または再起動）すると、アップロードしたアニメーションが即座に再生されます。
   - 初期状態（静止画ロゴ）に戻したい時は **Clear Animation from Flash** ボタンを押すだけでいつでも初期化できます。

---

#### 📦 方法B: UF2 パッチャーによる一括書き込み（オフライン）

単体の `.uf2` ファームウェアファイルとして書き込みたい場合の手順です：

##### Step 1: ファームウェア（`.uf2`）を用意する
- **完成品サンプルをすぐ試す場合**:
  [GitHub Releases](https://github.com/waaaaall/haute42-animated-splash/releases) から `firmware_hadouken_sample.uf2` をダウンロードします。
- **自作GIFでファームウェアを作成する場合**:
  1. 本リポジトリをダウンロード（ZIP解凍または `git clone`）します。
  2. `custom_gif/` フォルダにお好みのGIF画像を置きます（例: `custom_gif/my_animation.gif`）。
  3. **`generate_firmware.bat`** をダブルクリックして実行します（CLIの場合は `python patch_splash.py`）。
  4. フォルダ直下に **`firmware_custom.uf2`** が生成されます。

##### Step 2: Haute42 を BOOTSEL（`RPI-RP2`）モードで接続する
以下のいずれかの方法でコントローラーをブートローダーモードにします（PC上に `RPI-RP2` ドライブが認識されます）：
- **方法1（BOOTボタン・公式推奨）**:
  USBケーブルを抜いた状態で、背面またはUSB端子付近にある小さな **BOOTボタン**（またはピンホール）を爪楊枝や指で押しながら、PCにUSBケーブルを接続します。
- **方法2（ボタン長押しショートカット）**:
  通常接続した状態で、**`Start + X + Y`**（または **`Start + Select + Up`**）を5秒以上長押しします。画面がフリーズしてブートモードに入ります。
- **方法3（WebConfig経由）**:
  **STARTボタン**を押しながらUSB接続し、ブラウザで `http://192.168.7.1` を開いて **「Reboot」→「Bootsel」** を選択します（物理ボタンが押しづらい場合に便利です）。

##### Step 3: ファームウェアを書き込む
1. PCに認識された **`RPI-RP2`** ドライブ直下に、用意した `.uf2` ファイルをドラッグ＆ドロップ（コピー）します。
2. コピー完了と同時にドライブが自動で切断され、コントローラーが再起動してアニメーションが再生されます！

> 💡 **注意事項・トラブルシューティング:**
> - 必ず**データ転送に対応したUSB Type-Cケーブル**をご使用ください（充電専用ケーブルでは認識されません）。
> - Windowsから「ドライブをフォーマットしますか？」等の警告が出ても、**絶対にフォーマットしないでください**。そのまま `.uf2` をコピーすれば完了します。

### ⚙️ WebConfig の設定（常時ループ再生・画面遷移防止）
もしファームウェア書き込み後に数秒（5秒など）でボタン入力画面に切り替わってしまう場合は、本体側のスプラッシュ時間設定を確認・変更してください：

1. **STARTボタン** を押しながらPCにUSBケーブルを接続します。
2. Webブラウザで **`http://192.168.7.1`** にアクセスします。
3. メニューの **「Configuration」** → **「Display Configuration」** を開きます。
4. 以下の項目を設定します：
   - **Hardware Options > Enabled**: `Enabled`
   - **Splash Mode**: **`Enabled (Custom Splash Screen)`**
   - **Splash Duration (seconds, 0 for Always On)**: **`0`** に設定  
     *（⚠️ 最重要: ここを `0` にすることで「Always On（常時表示）」となり、ボタン画面に切り替わらずアニメーションがずっとループ再生され続けます）*
   - **Display Saver Timeout (minutes)**: **`0`**（画面が自動消灯するのを防ぐ場合は `0`）
5. ページ下部の **「Save」** ボタンを押し、コントローラーを再接続します。

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
