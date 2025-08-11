# NARUTO Hand Sign Detection - プロジェクトサマリー

## 概要

このプロジェクトは、コンピュータビジョンとディープラーニングを使用して NARUTO の印（手印）を検出し、忍術を識別するアプリケーションです。YOLOX-Nano モデルを使用してリアルタイムで手印を検出し、印の履歴から対応する忍術を判定します。

## プロジェクト構造

### ルートディレクトリ

- `pyproject.toml` - uv パッケージマネージャーの設定ファイル
- `README.md`, `README_EN.md` - プロジェクトの説明（日本語・英語）
- `LICENSE` - ライセンスファイル

### メインアプリケーション

- `Ninjutsu_demo.py` - 忍術判定機能付きのフルデモアプリケーション
- `simple_demo.py` - シンプルな印検出デモ
- `simple_demo_without_post.py` - 後処理なしのシンプルデモ

### モデル関連 (`model/`)

- `yolox/`
  - `yolox_nano.onnx` - 訓練済み YOLOX-Nano モデル
  - `yolox_nano_with_post.onnx` - 後処理込みモデル
  - `yolox_onnx.py` - ONNX モデルの推論クラス
  - `yolox_onnx_without_post.py` - 後処理なし推論クラス

### データ・設定 (`setting/`)

- `labels.csv` - 印のラベル定義（英語・日本語）
- `jutsu.csv` - 忍術の定義と必要な印の組み合わせ

### ユーティリティ (`utils/`)

- `cvfpscalc.py` - FPS 計測モジュール
- `cvdrawtext.py` - 日本語テキスト描画モジュール
- `font/衡山毛筆フォント.ttf` - 日本語フォント

### ツール (`post_process_gen_tools/`)

- ONNX モデルに後処理を統合するためのスクリプト群
- NMS、座標変換、スコア計算などの後処理機能

### レガシー (`_legacy/`)

- 旧バージョンのコード（v2）
- EfficientDet、MobileNetV2 SSD などの過去のモデル

## 検出可能な印

14 種類の印を検出可能：

- 十二支: 子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥
- その他: 壬、合掌

## 主要機能

### 1. 印検出機能

- YOLOX-Nano を使用したリアルタイム印検出
- バウンディングボックス表示
- 信頼度スコア表示

### 2. 忍術判定機能

- 印の履歴から忍術を自動判定
- jutsu.csv に定義された術の組み合わせでマッチング
- 術名の表示（日本語・英語対応）

### 3. カスタマイズ機能

- カメラ設定の調整
- 検出閾値の調整
- 表示オプションの切り替え
- フルスクリーン表示対応

## 技術スタック

- **推論エンジン**: ONNX Runtime
- **画像処理**: OpenCV
- **言語**: Python 3.10+
- **パッケージ管理**: uv
- **モデル**: YOLOX-Nano

## 依存関係

- onnxruntime >= 1.10.0
- opencv-python >= 3.4.2
- Pillow >= 6.1.0
- numpy

## 実行方法

```bash
# シンプルデモ
python simple_demo.py

# 忍術判定デモ
python Ninjutsu_demo.py

# オプション例
python Ninjutsu_demo.py --device 0 --score_th 0.7 --use_jutsu_lang_en True
```

## 特徴的な実装

1. **リアルタイム処理**: 効率的なフレーム処理と FPS 制御
2. **印履歴管理**: deque を使用した効率的な履歴管理
3. **チャタリング対策**: 連続検出による誤検出防止
4. **多言語対応**: 日本語・英語の表示切り替え
5. **カスタムフォント**: 日本語表示用の毛筆フォント使用

## アプリケーション事例

- 忍認証システム
- 忍者アカデミー試験対策
- インタラクティブゲーム「印 VADERS」

このプロジェクトは、エンターテイメントと教育を組み合わせた革新的なコンピュータビジョンアプリケーションの例として設計されています。
