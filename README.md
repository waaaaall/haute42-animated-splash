# Haute42 Animated Splash Screen for GP2040-CE

[English](#english) | [日本語](#日本語)

Play custom 128×64 animated GIF splash screens on your **Haute42** and RP2040-based arcade controllers running **GP2040-CE**.  
Upload, preview, and update animations directly from your web browser without entering BOOTSEL mode or re-flashing firmware.

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
  <em>Real Hardware Demo on Haute42 G16: <a href="https://x.com/good_wall/status/2101679788842996177">Watch on X (Twitter)</a></em>
</p>

---

<a name="english"></a>
## English

### Features
- **Browser-Based Upload**: Upload any animated GIF through the WebConfig interface (`http://192.168.7.1`) directly into controller Flash memory.
- **OLED Simulator**: Real-time 128×64 pixel preview with native frame timings, brightness threshold adjustment, and black/white inversion.
- **Single Initial Flash**: Flashing via BOOTSEL is only required once during initial setup. Subsequent animation updates are handled entirely through WebConfig.
- **Zero Input Latency**: The microcontroller performs zero runtime GIF decoding. Frame data is pre-processed into raw 1-bit monochrome buffers on the client side and streamed from Flash with minimal memory copies.
- **Continuous Looping**: Supports continuous animated playback without transitioning to the default input display.
- **Automatic Formatting**: Automatically scales, centers, and binarizes arbitrary GIF dimensions into 128×64 monochrome frames.
- **Included Sample**: Bundles a ready-to-use leverless command input animation (CC0 / Public Domain).

---

### How It Works

In standard GP2040-CE firmware, dynamic GIF playback was considered impractical due to RP2040 microcontroller constraints (limited SRAM and CPU overhead required for decompression, which risks input latency).

This project resolves those limitations through client-side pre-processing:

```
[User GIF]
   │
   ▼
[Browser / WebConfig]
   ├─ Decodes GIF frames and timing metadata
   ├─ Resizes and centers onto 128×64 canvas
   ├─ Binarizes pixels with user-selected threshold / inversion
   └─ Packs frames into 1-bit monochrome buffers (1,024 bytes per frame)
   │
   ▼ (HTTP REST API chunks)
[RP2040 Flash Memory] (Allocated splash region, up to 512 KB)
   │
   ▼ (Zero-overhead memcpy per frame delay)
[OLED Display (SSD1306 / SH1106)]
```

1. **Client-Side Conversion**: The browser decodes GIF frames, applies contrast thresholding, and converts each frame into a raw 1,024-byte 1-bit monochrome bitmap.
2. **Direct Flash Storage**: The pre-converted payload is written directly to a dedicated 512 KB sector of RP2040 Flash memory via WebConfig HTTP API endpoints.
3. **Zero MCU Decoding Overhead**: During playback, the RP2040 does not parse GIF headers or perform image decoding. It reads raw display buffers directly from Flash memory into the OLED driver, maintaining complete isolation from button polling and USB input handling.

---

### Quick Start Guide

#### Step 1: Initial Firmware Setup (One Time Only)
Flashing via BOOTSEL mode is only necessary for the initial installation.

1. Download **`haute42_animated_splash_v1.1.0.uf2`** from [GitHub Releases](https://github.com/waaaaall/haute42-animated-splash/releases).
2. Connect your controller in **BOOTSEL mode**:
   - **Hardware BOOT Button (Recommended)**: While holding the **BOOT** button (or pinhole switch) on the controller, plug the USB cable into your PC.
   - **Button Shortcut**: With the controller plugged in normally, hold **`Start + X + Y`** (or `Start + Select + Up`) for 5 seconds until the display halts.
   - **WebConfig**: Hold **START** while plugging in the USB cable, navigate to `http://192.168.7.1` in your browser, and select **Reboot > Bootsel**.
3. A mass storage device named **`RPI-RP2`** will appear on your computer. Copy the downloaded `.uf2` file to the root of this drive.
4. The controller will disconnect automatically and reboot with animated splash support enabled.

#### Step 2: Upload Animations via WebConfig
Once the firmware is installed, manage animations directly in your browser:

<p align="center">
  <img src="assets/webconfig_upload_demo.gif" alt="WebConfig Animated Splash Screen Upload Demo" width="760" />
  <br>
  <em>WebConfig Interface: Selecting GIF, real-time OLED simulation, and writing to Flash memory</em>
</p>

1. Hold the **START** button while plugging the controller into your PC.
2. Open **`http://192.168.7.1`** in your web browser.
3. Navigate to **Configuration** → **Display Configuration**.
4. Scroll down to the **Animated Splash Screen (GIF Direct Upload)** section.
5. Click **Choose File** and select your GIF:
   - **OLED Simulator**: Preview playback at native frame rates with play/pause controls.
   - **Brightness Threshold**: Adjust monochrome conversion contrast (0–255) with instant visual feedback.
   - **Invert Black/White**: Toggle pixel inversion for dark-on-light or light-on-dark display styles.
   - **Flash Info**: Review frame count, duration, and Flash memory consumption.
6. Click **Write Animation to Flash** and wait for the upload progress bar to complete.
7. Reconnect or reboot your controller. The new animation will play on startup.
   - To remove the custom animation, click **Clear Animation from Flash**.

#### Step 3: Configure Continuous Looping (Optional)
To keep the animation looping indefinitely instead of switching to the input display:

<p align="center">
  <img src="assets/webconfig_display_settings.png" alt="WebConfig Display Configuration Settings" width="680" />
</p>

1. Open WebConfig (`http://192.168.7.1`) by holding **START** while plugging in the controller.
2. Navigate to **Configuration** → **Display Configuration**.
3. Configure the following parameters:
   - **Hardware Options > Enabled**: `Enabled`
   - **Splash Mode**: `Enabled (Custom Splash Screen)`
   - **Splash Duration (seconds, 0 for Always On)**: Set to `0`  
     *(Setting this value to `0` enables Always-On mode, preventing transition to the button state screen.)*
   - **Display Saver Timeout (minutes)**: Set to `0` (disables automatic screen sleep)
4. Click **Save** at the bottom of the page and reconnect the controller.

*(Note: Command-line utilities `patch_splash.py` and `upload_to_controller.py` are also provided in the repository for automated or headless workflows.)*

---

### GIF Specifications & Recommendations
- **Resolution**: 128 × 64 pixels (exact match avoids downscaling artifacts).
- **Color Format**: 1-bit monochrome (white foreground on black background recommended).
- **Frame Count**: Up to 128 frames (16 to 48 frames yield optimal balance between file size and smoothness).
- **Storage Limit**: Maximum 512 KB Flash payload (~128 frames at 1,024 bytes/frame + header).
- Refer to [`sample_gif/README.md`](sample_gif/README.md) for frame design tips and examples.

---

### Compatibility & Other RP2040 Controllers
While the pre-compiled binary targets **Haute42 controllers** (G16, B16, T16, S16, etc. using the `Haute42COSMOX` board profile), the animation engine is compatible with **any RP2040 arcade controller running GP2040-CE**.

#### Hardware Requirements
1. **RP2040 Microcontroller** with 2 MB or more Flash memory.
2. **128×64 Monochrome OLED Display** (SSD1306 or SH1106 via I2C or SPI).  
   *(Displays with 128×32 resolution will show the upper 32 lines of the animation).*

#### Compatible Hardware Examples
- **Flatbox** (Rev 4 / Rev 5 with OLED display addon)
- **Fightbox** (RP2040 / B1-PC OLED models)
- **Pico Fighting Board** / **RP2040 Advanced Breakout Board** custom enclosures
- **Sallybox**, **BentoBox**, **Mavercade** GP2040-CE variants
- DIY builds combining a Raspberry Pi Pico or RP2040 Pro Micro with a 0.96-inch OLED module

#### Building for Other Targets
To build firmware for a different board target:
```bash
export PICO_BOARD=FlatboxRev5  # Specify target board
cmake -B build -DPICO_BOARD=$PICO_BOARD
cmake --build build
```
Flash the generated `.uf2` file once via BOOTSEL. All WebConfig upload and preview capabilities operate identically across targets.

---

### Troubleshooting & FAQ

#### Q: The animation stops and switches to the button layout after a few seconds.
Set **Splash Duration** to `0` under **Configuration** → **Display Configuration** in WebConfig. A value of `0` designates infinite looping.

#### Q: The OLED display turns black after a few minutes of inactivity.
The screen saver is active. In **Configuration** → **Display Configuration**, set **Display Saver Timeout** to `0` to keep the display continuously active.

#### Q: Unable to access `http://192.168.7.1`.
1. Verify that the **START** button was held down while connecting the USB cable to enter WebConfig mode.
2. Ensure no third-party VPN, firewall, or virtual network adapter conflicts with the `192.168.7.x` subnet.
3. Check that the controller appears in your operating system as an RNDIS/Ethernet gadget.

#### Q: How can I revert to the default splash screen or stock firmware?
- To restore the default splash: In WebConfig, click **Clear Animation from Flash** in the Animated Splash Screen section.
- To restore stock GP2040-CE: Download the official firmware UF2 for your board from the [GP2040-CE Releases page](https://github.com/OpenStickCommunity/GP2040-CE/releases) and flash it via BOOTSEL.

---

<a name="日本語"></a>
## 日本語

### 特徴
- **WebConfig からの直接アップロード**: コントローラーの設定画面（`http://192.168.7.1`）から、ブラウザ経由で直接 Flash メモリへ GIF アニメーションを書き込めます。
- **リアルタイム OLED シミュレータ**: 実機相当の 128×64 ピクセル表示、フレーム間隔（ディレイ）、二値化しきい値調整、白黒反転をブラウザ上でプレビューできます。
- **初回導入のみで運用可能**: BOOTSEL モードを用いたファームウェア書き込みは初回の1度のみです。日常のアニメーション変更は WebConfig 上で完結します。
- **入力遅延への影響ゼロ**: マイコン側での動的な GIF デコード処理を行いません。ブラウザ側で 1-bit モノクロ配列に事前変換し、Flash メモリから単純なメモリ転送（memcpy）のみで描画するため、ボタン入力ポーリングや USB 転送を阻害しません。
- **常時ループ再生に対応**: 起動後に入力表示画面へ遷移させず、アニメーションを無限ループ再生させることが可能です。
- **自動フォーマット機能**: アスペクト比や解像度の異なる GIF を、128×64 サイズの中央配置・モノクロ 2 値データへ自動調整します。
- **サンプル同梱**: レバーレスの波動拳コマンド入力アニメーション（CC0 / パブリックドメイン）を同梱しています。

---

### 動作原理とアーキテクチャ

GP2040-CE 公式リポジトリの Issue #407 では、アニメーション GIF サポートの要望に対し、RP2040 マイコンの Flash 容量や RAM 制約、デコード負荷による入力遅延の懸念から対応が見送られた経緯があります。

本プロジェクトでは、デコード処理をクライアント（ブラウザ）側に逃がすアーキテクチャを採用することでこの制約を解消しています。

```
[GIF 画像]
   │
   ▼
[WebConfig (ブラウザ)]
   ├─ フレーム展開および表示時間（delay）の解析
   ├─ 128×64 キャンバスへの中央配置・スケーリング
   ├─ 任意しきい値によるモノクロ 2 値化および白黒反転
   └─ 1 フレームあたり 1,024 バイトの 1-bit 配列へパック化
   │
   ▼ (HTTP REST API 経由で分割送信)
[RP2040 Flash メモリ] (スプラッシュ専用領域、最大 512 KB)
   │
   ▼ (フレームごとのディレイに応じた低負荷 memcpy)
[OLED ディスプレイ (SSD1306 / SH1106)]
```

1. **ブラウザ側での前処理**: WebConfig の JavaScript が GIF をデコードし、128×64 ピクセルのモノクロビットマップデータ（1フレーム＝1,024バイト）へ変換します。
2. **Flash への直接書き込み**: 変換済みバイナリを、WebConfig の REST API を経由して RP2040 の Flash メモリ（最大 512 KB 領域）へ直接書き込みます。
3. **マイコン負荷ゼロの描画**: 再生時、RP2040 は GIF フォーマットの解析や画像伸張処理を行いません。Flash 上に並ぶ展開済みバッファをタイマーに合わせて OLED ドライバへ転送するだけであるため、入力処理に負荷を与えません。

---

### クイックスタートガイド

#### Step 1: 初回セットアップ（ファームウェア書き込み：最初の一度のみ）
BOOTSEL モードでの書き込みは、初回のファームウェア導入時のみ必要です。

1. [GitHub Releases](https://github.com/waaaaall/haute42-animated-splash/releases) から **`haute42_animated_splash_v1.1.0.uf2`** をダウンロードします。
2. コントローラーを **BOOTSEL モード** で PC に接続します：
   - **BOOT ボタン（推奨）**: コントローラーの BOOT ボタン（またはピンホールスイッチ）を押しながら USB ケーブルを接続します。
   - **ボタンショートカット**: 通常接続した状態で、**`Start + X + Y`**（または `Start + Select + Up`）を 5 秒以上長押しします。
   - **WebConfig**: START ボタンを押しながら接続し、ブラウザで `http://192.168.7.1` を開いて **「Reboot」→「Bootsel」** を選択します。
3. PC に認識された **`RPI-RP2`** ドライブ直下に、ダウンロードした `.uf2` ファイルをコピーします。
4. 書き込み完了後、ドライブが自動で切断され、アニメーション機能が有効化された状態で再起動します。

#### Step 2: WebConfig からアニメーションを登録
ファームウェア導入後は、ブラウザからアニメーションの更新を行えます：

<p align="center">
  <img src="assets/webconfig_upload_demo.gif" alt="WebConfig アニメーション直接アップロード デモ" width="760" />
  <br>
  <em>WebConfig 画面: GIF 選択、リアルタイム OLED プレビュー、Flash への書き込み</em>
</p>

1. **START ボタン** を押しながらコントローラーの USB ケーブルを PC に接続します。
2. Web ブラウザで **`http://192.168.7.1`** を開きます。
3. メニューの **「Configuration」** → **「Display Configuration」** に移動します。
4. ページ下部の **Animated Splash Screen (GIF Direct Upload)** セクションへ進みます。
5. **「ファイルを選択」** から任意の GIF アニメーションを選択します：
   - **OLED シミュレータ**: 実機同様のフレームレートとドット表示でプレビュー再生されます。
   - **Brightness Threshold**: 白黒判定のしきい値（0〜255）をスライダーでリアルタイムに調整できます。
   - **Invert Black/White**: 背景色と描画色の反転を切り替えられます。
   - **Flash 情報**: フレーム数、再生時間、Flash 使用量が表示されます。
6. **「Write Animation to Flash」** をクリックします。プログレスバーが完了するまで待ちます。
7. コントローラーを再接続すると、登録したアニメーションが再生されます。
   - 登録したアニメーションを削除したい場合は、**「Clear Animation from Flash」** をクリックします。

#### Step 3: 常時ループ再生の設定（推奨）
起動後に入力受付画面へ切り替えず、アニメーションを常時ループ再生させる場合の設定です：

<p align="center">
  <img src="assets/webconfig_display_settings.png" alt="WebConfig ディスプレイ設定画面" width="680" />
</p>

1. START ボタンを押しながらコントローラーを接続し、WebConfig（`http://192.168.7.1`）を開きます。
2. **「Configuration」** → **「Display Configuration」** を開きます。
3. 以下の項目を設定します：
   - **Hardware Options > Enabled**: `Enabled`
   - **Splash Mode**: `Enabled (Custom Splash Screen)`
   - **Splash Duration (seconds, 0 for Always On)**: **`0`**  
     *（`0` に設定することで Always-On モードとなり、ボタン入力画面に遷移せず無限ループします）*
   - **Display Saver Timeout (minutes)**: **`0`**（無操作時の画面自動消灯を無効化）
4. ページ下部の **「Save」** ボタンを押し、コントローラーを再接続します。

*(※補足: Python CLI スクリプト `patch_splash.py` および `upload_to_controller.py` もリポジトリ内に同梱されており、自動化スクリプト等からの書き込みも可能です。)*

---

### GIF の仕様と推奨設定
- **解像度**: 128 × 64 ピクセル（縮小によるジャギーを防ぐため実寸での作成を推奨）。
- **カラーフォーマット**: モノクロ 2 値（黒背景に白描画を推奨）。
- **フレーム数**: 最大 128 フレーム（滑らかさとデータ容量の観点から 16〜48 フレーム程度が扱いやすい形式です）。
- **データサイズ上限**: Flash 領域は最大 512 KB（1 フレームあたり 1,024 バイト＋ヘッダ構造）。
- 作成のコツやサンプル詳細は [`sample_gif/README.md`](sample_gif/README.md) を参照してください。

---

### 他の RP2040 コントローラーでの利用
本リポジトリでは **Haute42 シリーズ**（G16 / B16 / T16 / S16 等、`Haute42COSMOX` ターゲット）向けにビルド済みファームウェアを提供していますが、アニメーション機能自体は **GP2040-CE を搭載した任意の RP2040 コントローラー** で動作します。

#### 動作条件
1. **RP2040 マイコン**（Flash メモリ 2 MB 以上）を搭載していること。
2. **128×64 モノクロ OLED ディスプレイ**（SSD1306 / SH1106）を搭載していること。  
   *（128×32 画面のコントローラーでは上半分 32 行が表示されます）*

#### 対応可能なコントローラー例
- **Flatbox**（Rev 4 / Rev 5 OLED 搭載型）
- **Fightbox**（RP2040 / B1-PC OLED 搭載モデル）
- **Pico Fighting Board** / **RP2040 Advanced Breakout Board** を用いた自作コントローラー
- **Sallybox**, **BentoBox**, **Mavercade** などの各種 GP2040-CE 採用レバーレス
- Raspberry Pi Pico や RP2040 Pro Micro に 0.96 インチ OLED を接続した自作機全般

#### 他のボード向けビルド手順
コントローラーごとに GPIO ピン定義が異なるため、対象ボードを指定してビルドを行います：
```bash
export PICO_BOARD=FlatboxRev5  # 対象のボード名を指定
cmake -B build -DPICO_BOARD=$PICO_BOARD
cmake --build build
```
生成された `.uf2` を一度書き込めば、WebConfig からの GIF 直接アップロード機能は同一の操作感で利用できます。

---

### トラブルシューティング & FAQ

#### Q: 数秒経過するとアニメーションが停止し、ボタン入力画面に切り替わってしまう
WebConfig の **「Configuration」** → **「Display Configuration」** 内にある **Splash Duration** を **`0`** に設定してください。`0` に設定することで Always-On（常時表示）モードとなり、自動遷移が無効化されます。

#### Q: しばらく操作しないと画面が消灯してしまう
画面焼き付き防止用のスクリーンセーバーが動作しています。**「Display Configuration」** の **Display Saver Timeout** を **`0`** に設定することで、自動消灯を無効化できます。

#### Q: `http://192.168.7.1` にアクセスできない
1. コントローラーの **START ボタン** を押しながら USB ケーブルを接続したか確認してください（通常接続ではコントローラーとして認識され、WebConfig サーバーは起動しません）。
2. PC 側の VPN や仮想ネットワークアダプタが `192.168.7.x` 帯と競合していないか確認してください。
3. デバイスマネージャー等でコントローラーが RNDIS / Ethernet ガジェットとして認識されているか確認してください。

#### Q: 初期の静止画スプラッシュや公式ファームウェアに戻したい
- 静止画に戻す場合: WebConfig の Animated Splash Screen 項目にある **「Clear Animation from Flash」** をクリックしてください。
- 公式ファームウェアに戻す場合: [GP2040-CE 公式リリースページ](https://github.com/OpenStickCommunity/GP2040-CE/releases) からお使いのボード用の UF2 ファイルをダウンロードし、BOOTSEL モードで書き直してください。

---

## ⚠️ Disclaimer / 免責事項
- This project is an independent community project and is not officially affiliated with Haute42 or the GP2040-CE project.
- Flashing firmware involves risks. Please ensure you have a backup of your original controller firmware and settings.
- Users are solely responsible for ensuring they possess the necessary rights and permissions for any animated assets uploaded to their hardware.
- 本プロジェクトは個人によるコミュニティプロジェクトであり、Haute42 公式および GP2040-CE 公式とは直接の関係はありません。
- ファームウェアの書き込みには潜在的なリスクが伴います。必要に応じて既存の設定やファームウェアのバックアップを保持した上で実施してください。
- コントローラーへ導入する画像・アニメーション素材の著作権および利用許諾については、利用者の責任において管理してください。

---

## 📜 License & Credits
- **Source Code & Tools**: Licensed under the [MIT License](LICENSE).
- **Sample Animation (`sample_gif/leverless_hadouken_loop.gif`)**: Dedicated to the public domain under **CC0 1.0 Universal**.
- **Base Firmware**: Derived from [GP2040-CE](https://github.com/OpenStickCommunity/GP2040-CE) (MIT License, Copyright (c) 2024 OpenStickCommunity).

