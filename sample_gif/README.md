# Sample GIF Specifications / サンプルGIF仕様

## `leverless_hadouken_loop.gif`
- **Resolution / 解像度**: 128 x 64 pixels (1-bit monochrome / モノクロ白黒)
- **Frames / フレーム数**: 32 frames (32フレーム)
- **Frame Duration / 1フレーム時間**: 80 ms (Total 2,560 ms cycle / 1周期約2.56秒)
- **Theme / テーマ**:
  - Leverless controller Hadouken command input (2 -> 3 -> 6 + P) followed by energy fireball projectile.
  - レバーレスコントローラーのボタン入力（波動拳コマンド：↓ ↘ → ＋ 弱P）と波動弾射出のアトラクト・ループアニメーション。
- **License / ライセンス**:
  - **CC0 1.0 Universal (Public Domain / 権利放棄・フリー素材)**
  - Free to use, modify, distribute, and embed for any purpose without attribution.
  - 商用・非商用問わず自由に使用・改変・再配布可能。

---

## Tips for Creating Your Own GIF / 自作GIF作成のコツ

1. **Resolution / 解像度**:
   - Recommended: **128 x 64 pixels**.
   - If other resolutions are used, WebConfig automatically scales and centers it with nearest-neighbor interpolation.
   - 推奨解像度は **128 x 64 ピクセル** です。異なるサイズの場合も自動でセンタリング＆アスペクト比維持で縮小配置されます。

2. **Color Mode / カラー**:
   - Monochrome 1-bit (White on Black background is recommended for OLED).
   - OLEDディスプレイの特性上、**黒背景に白ピクセル** が最も映え、視認性が高くなります。
   - グレースケールやカラーGIFの場合、自動で閾値（デフォルト128）による白黒2値化が行われます。

3. **Frame Count & Duration / フレーム数と遅延**:
   - Up to 128 frames are supported (usually 16 to 48 frames are ideal for smooth 1-3 second loops).
   - Variable frame delays are fully supported.
   - 最大128フレームまで対応（推奨は16〜48フレーム程度）。各フレームごとの個別ディレイ（緩急）も忠実に反映されます。
