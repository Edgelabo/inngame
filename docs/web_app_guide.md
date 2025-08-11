# NARUTO Hand Sign Detection - Web Application

## 概要

この Web アプリケーションは、ブラウザ上で NARUTO の印（手印）をリアルタイムで検出し、忍術を判定する Web アプリケーションです。元の`Ninjutsu_demo.py`をベースに、FastAPI と WebSocket を使用して Web 版として実装しました。

## 機能

- **リアルタイム印検出**: Web カメラからの映像をリアルタイムで解析
- **忍術判定**: 印の履歴から対応する忍術を自動判定
- **Web UI**: 直感的で美しい Web インターフェース
- **履歴管理**: 印の検出履歴の表示と管理
- **多言語対応**: 日本語・英語での術名表示

## セットアップ

### 1. 依存関係のインストール

```bash
# uvを使用してプロジェクトをセットアップ
uv sync

# または個別に依存関係をインストール
uv add fastapi uvicorn[standard] opencv-python numpy onnxruntime pillow
```

### 2. 必要なファイルの確認

以下のファイルが存在することを確認してください：

- `model/yolox/yolox_nano.onnx` - 訓練済みモデル
- `setting/labels.csv` - 印のラベル定義
- `setting/jutsu.csv` - 忍術の定義
- `utils/font/衡山毛筆フォント.ttf` - 日本語フォント（デスクトップ版で使用）

## 実行方法

### uv を使用

```bash
uv run python web_ninjutsu_app.py
```

### 直接実行

```bash
python web_ninjutsu_app.py
```

### 開発サーバーで実行

```bash
uvicorn web_ninjutsu_app:app --reload --host 0.0.0.0 --port 8000
```

## アクセス方法

アプリケーションを起動後、ブラウザで以下にアクセス：

- ローカル: http://localhost:8000
- ネットワーク内: http://[サーバー IP]:8000

## 使用方法

1. **カメラ開始**: 「カメラ開始」ボタンをクリック
2. **印の検出**: カメラに向かって印を結ぶ
3. **術の確認**: 画面下部で検出された印の履歴と術名を確認
4. **履歴クリア**: 必要に応じて「履歴クリア」ボタンで履歴をリセット

## 技術仕様

### バックエンド

- **Framework**: FastAPI
- **WebSocket**: リアルタイム通信
- **推論エンジン**: ONNX Runtime
- **画像処理**: OpenCV + PIL

### フロントエンド

- **技術**: Vanilla JavaScript + HTML5 Canvas
- **通信**: WebSocket
- **カメラ**: MediaDevices API
- **UI**: レスポンシブデザイン

### API エンドポイント

- `GET /`: メインページ（HTML）
- `WebSocket /ws`: リアルタイム画像処理

## 設定のカスタマイズ

`WebNinjutsuDetector`クラスの初期化部分で以下の設定を変更可能：

```python
# モデル設定
self.score_th = 0.7          # 検出閾値
self.nms_th = 0.45           # NMS閾値
self.sign_interval = 2.0     # 印履歴クリア間隔（秒）
self.jutsu_display_time = 5  # 術名表示時間（秒）
```

## パフォーマンス最適化

- **CPU 使用**: Web 版では安定性を重視して CPU 推論を使用
- **フレーム間隔**: 100ms 間隔で画像処理を実行
- **画像品質**: JPEG 圧縮（品質 80%）で通信量を削減

## トラブルシューティング

### カメラにアクセスできない

- ブラウザでカメラ権限が許可されているか確認
- HTTPS または localhost でのアクセスが必要（セキュリティ要件）

### 推論が遅い

- モデルファイルが正しく配置されているか確認
- CPU リソースが十分にあるか確認

### WebSocket 接続エラー

- ファイアウォール設定を確認
- プロキシ環境の場合は WebSocket 通信を許可

## 開発者向け情報

### 拡張方法

1. **新しい印の追加**: `setting/labels.csv`にラベルを追加
2. **新しい術の追加**: `setting/jutsu.csv`に術の組み合わせを追加
3. **UI のカスタマイズ**: HTML テンプレート内の CSS を修正

### デプロイ

```bash
# 本番環境での実行
uvicorn web_ninjutsu_app:app --host 0.0.0.0 --port 8000 --workers 1

# Dockerを使用する場合
docker run -p 8000:8000 -v $(pwd):/app python:3.10
```

## ライセンス

MIT License - 詳細は`LICENSE`ファイルを参照

## 関連ファイル

- `Ninjutsu_demo.py` - オリジナルのデスクトップ版
- `simple_demo.py` - シンプルな検出デモ
- `docs/project_summary.md` - プロジェクト全体の説明
