# Changelog / 更新履歴

All notable changes to the Haute42 Animated Splash project are documented in this file.  
本プロジェクトにおける主なバージョン更新履歴を記載しています。

---

## [v1.1.0] - 2026-09-21

### 🚀 Major Architecture Upgrade / メジャーアップデート
- **WebConfig Direct Upload GUI / ブラウザ直接アップロード**:
  - WebConfig（`http://192.168.7.1`）から、ブラウザ経由で直接 Flash メモリへ GIF アニメーションを書き込める GUI を実装。
  - 初回ファームウェア導入以降、アニメーション変更時に BOOTSEL ボタンを押したり UF2 を再フラッシュする必要がなくなりました。
- **Interactive OLED Simulator / リアルタイムOLEDシミュレータ**:
  - 128×64 ドットの忠実なディスプレイ表示、コマごとの可変ディレイ（フレームレート）、再生/一時停止プレビューをブラウザ上に搭載。
  - 二値化しきい値スライダー（0〜255）および白黒反転トグルをリアルタイムプレビュー可能に。
- **Zero Runtime MCU Overhead / 入力遅延ゼロ設計**:
  - ブラウザ側で GIF をデコードし、1 フレームあたり 1,024 バイトの 1-bit モノクロビットマップ配列へ事前変換。
  - RP2040 マイコン側は Flash からの低負荷 `memcpy` のみで描画するため、デコード負荷や動的メモリ確保を排除し、対戦プレイ時の入力処理を一切阻害しません。
- **REST API Endpoints / Web API 対応**:
  - WebConfig バックエンドにアニメーション情報取得・チャンク書き込み・初期化 API（`/api/getSplashAnimationInfo`, `/api/writeSplashChunk`, `/api/clearSplashAnimation`）を追加。

---

## [v1.0.0] - Initial Release / 初期リリース

### ✨ Initial Features / 初期機能
- **Offline UF2 Patcher (`patch_splash.py`) / オフラインパッチ方式**:
  - C++ コンパイラや Pico SDK をインストールすることなく、配布済み UF2 ファームウェアに Python スクリプトで直接 GIF アニメーションを注入するパッチャーを提供。
  - 最大 128 フレームのモノクロアニメーションおよび可変フレームレートに対応。
- **Infinite Looping Engine / 常時ループ再生エンジン**:
  - 起動後もボタン入力画面へ遷移せず、アニメーションを無限ループ再生するカスタム表示ロジックを実装。
- **Leverless Hadouken Sample / サンプルアニメーション同梱**:
  - 権利フリー（CC0 1.0 Universal）なレバーレス波動拳コマンド入力アニメーション（`sample_gif/leverless_hadouken_loop.gif`）を同梱。
