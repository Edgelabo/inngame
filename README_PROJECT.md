# NARUTO Hand Sign Detection Project

## 📋 プロジェクト概要

このプロジェクトは、AI とコンピュータビジョンを使用して NARUTO の印（手印）を検出し、忍術を判定するアプリケーションです。デスクトップ版と Web 版の両方を提供しています。

## 🏗️ プロジェクト構造

```
naruto/
├── 📁 docs/                          # ドキュメント
│   ├── project_summary.md            # プロジェクト全体の詳細説明
│   └── web_app_guide.md             # Webアプリケーションガイド
├── 📁 model/                         # AIモデル
│   └── yolox/
│       ├── yolox_nano.onnx          # 訓練済みYOLOXモデル
│       └── yolox_onnx.py            # モデル推論クラス
├── 📁 setting/                       # 設定ファイル
│   ├── labels.csv                    # 印のラベル定義
│   └── jutsu.csv                     # 忍術の定義
├── 📁 utils/                         # ユーティリティ
│   ├── cvfpscalc.py                 # FPS計測
│   ├── cvdrawtext.py                # 日本語テキスト描画
│   └── font/衡山毛筆フォント.ttf     # 日本語フォント
├── 🖥️ Ninjutsu_demo.py              # デスクトップ版（メイン）
├── 🖥️ simple_demo.py                # シンプル検出デモ
├── 🌐 web_ninjutsu_app.py           # Webアプリケーション版
├── 🚀 start_web_app.sh              # Web版起動スクリプト
├── 📋 pyproject.toml                # プロジェクト設定（uv）
└── 📝 README.md                     # このファイル
```

## 🚀 クイックスタート

### 前提条件

- Python 3.10+
- uv パッケージマネージャー
- Web カメラ（カメラを使用する場合）

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/Kazuhito00/NARUTO-HandSignDetection.git
cd NARUTO-HandSignDetection

# 依存関係をインストール
uv sync
```

## 📱 アプリケーション版

### 1. デスクトップ版（推奨）

最も機能が豊富で安定したバージョンです。

```bash
# 忍術判定デモ（フル機能）
uv run python Ninjutsu_demo.py

# シンプル検出デモ
uv run python simple_demo.py
```

### 2. Web アプリケーション版（新機能！）

ブラウザで動作する Web 版です。

```bash
# 簡単起動
./start_web_app.sh

# または直接実行
uv run python web_ninjutsu_app.py
```

その後、ブラウザで `http://localhost:8000` にアクセス

## 🎯 主要機能

### 印検出機能

- 14 種類の印を検出（子〜亥、壬、合掌）
- リアルタイム処理
- 高精度な YOLOX-Nano モデル

### 忍術判定機能

- 印の履歴から忍術を自動判定
- 50 以上の忍術に対応
- 日本語・英語表示切り替え

### カスタマイズ機能

- 検出閾値の調整
- 表示オプションの切り替え
- フルスクリーン表示対応

## 📊 対応忍術例

| 術名       | 必要な印                         | 分類     |
| ---------- | -------------------------------- | -------- |
| 豪火球の術 | 巳 → 寅 → 申 → 亥 → 午 → 寅      | 火遁     |
| 分身の術   | 未 → 巳 → 寅                     | 基本忍術 |
| 水鮫弾の術 | 寅 → 丑 → 辰 → 卯 → 酉 → 辰 → 未 | 水遁     |

## 🎮 使用方法

### デスクトップ版

1. アプリケーションを起動
2. カメラに向かって印を結ぶ
3. 画面下部で印の履歴と術名を確認
4. `C`キーで履歴クリア、`ESC`キーで終了

### Web 版

1. ブラウザでアプリケーションにアクセス
2. 「カメラ開始」ボタンをクリック
3. カメラに向かって印を結ぶ
4. リアルタイムで印と術名が表示される

## ⚙️ 高度な設定

### コマンドラインオプション（デスクトップ版）

```bash
python Ninjutsu_demo.py \
  --device 0 \
  --score_th 0.7 \
  --use_jutsu_lang_en True \
  --use_fullscreen True
```

### 設定ファイルのカスタマイズ

- `setting/labels.csv`: 新しい印の追加
- `setting/jutsu.csv`: 新しい忍術の追加

## 🛠️ 開発情報

### 技術スタック

- **AI/ML**: YOLOX-Nano, ONNX Runtime
- **画像処理**: OpenCV
- **Web**: FastAPI, WebSocket
- **パッケージ管理**: uv
- **言語**: Python 3.10+

### アーキテクチャ

- **推論エンジン**: ONNX Runtime
- **前処理**: OpenCV
- **後処理**: カスタム NMS 実装
- **通信**: WebSocket（Web 版）

## 🎨 UI/UX 特徴

### デスクトップ版

- 日本語フォント対応
- リアルタイム FPS 表示
- バウンディングボックス表示
- フルスクリーン対応

### Web 版

- レスポンシブデザイン
- 美しいグラデーション背景
- リアルタイム更新
- モバイル対応

## 📈 パフォーマンス

- **推論速度**: 30+ FPS（CPU）
- **検出精度**: 高精度（YOLOX-Nano）
- **レイテンシ**: 低遅延リアルタイム処理
- **メモリ使用量**: 軽量設計

## 🤝 貢献

プロジェクトへの貢献を歓迎します：

1. Issue でバグ報告や機能提案
2. 新しい印のデータ提供
3. 翻訳の改善
4. パフォーマンス最適化

## 📄 ライセンス

MIT License - 詳細は`LICENSE`ファイルを参照

## 🙏 謝辞

- オリジナルプロジェクト: [Kazuhito00/NARUTO-HandSignDetection](https://github.com/Kazuhito00/NARUTO-HandSignDetection)
- フォント: 衡山毛筆フォント
- データセット: naruto-hand-sign-dataset (Kaggle)

## 📞 サポート

- 📖 詳細ドキュメント: `docs/project_summary.md`
- 🌐 Web 版ガイド: `docs/web_app_guide.md`
- 🐛 Issues: GitHub の Issue ページ

---

**Deep 写輪眼で忍術をマスターしよう！** 🥷✨
