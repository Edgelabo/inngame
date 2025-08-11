#!/bin/bash

# NARUTO Hand Sign Detection Web App 起動スクリプト

echo "🥷 NARUTO Hand Sign Detection Web App 🥷"
echo "========================================"

# 依存関係のチェック
echo "依存関係をチェックしています..."

# uvがインストールされているかチェック
if ! command -v uv &> /dev/null; then
    echo "エラー: uvがインストールされていません。"
    echo "uvをインストールしてください: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 必要なファイルの存在確認
echo "必要なファイルの存在を確認しています..."

required_files=(
    "model/yolox/yolox_nano.onnx"
    "setting/labels.csv"
    "setting/jutsu.csv"
    "web_ninjutsu_app.py"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "エラー: 必要なファイルが見つかりません: $file"
        exit 1
    fi
done

echo "✅ 全ての必要なファイルが見つかりました"

# 依存関係のインストール
echo "依存関係をインストールしています..."

# Python仮想環境を作成・アクティベート
if [ ! -d ".venv" ]; then
    echo "仮想環境を作成しています..."
    python3 -m venv .venv
fi

# 仮想環境をアクティベート
source .venv/bin/activate

# 依存関係をインストール
pip install fastapi uvicorn opencv-python numpy onnxruntime pillow websockets

if [ $? -ne 0 ]; then
    echo "エラー: 依存関係のインストールに失敗しました"
    exit 1
fi

echo "✅ 依存関係のインストールが完了しました"

# アプリケーションの起動
echo "Webアプリケーションを起動しています..."
echo "ブラウザで以下のURLにアクセスしてください:"
echo "  http://localhost:8000"
echo ""
echo "停止するには Ctrl+C を押してください"
echo ""

python web_ninjutsu_app.py
