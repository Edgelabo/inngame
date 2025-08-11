# NARUTO Hand Sign Detection - Vercel デプロイガイド

## 概要
この文書では、NARUTO Hand Sign Detection WebアプリをVercelにデプロイする方法を説明します。

## 🚀 Vercelデプロイ手順

### 1. Vercelアカウントの準備
1. [Vercel](https://vercel.com)にアクセス
2. GitHubアカウントでサインアップ/ログイン

### 2. プロジェクトの準備
以下のファイルが含まれていることを確認：
- `vercel.json` - Vercel設定ファイル
- `requirements.txt` - Python依存関係
- `runtime.txt` - Python バージョン指定
- `api/main.py` - メインアプリケーション
- `.vercelignore` - デプロイ除外ファイル

### 3. GitHubリポジトリの作成
```bash
# プロジェクトをGitリポジトリとして初期化
git init
git add .
git commit -m "Initial commit for Vercel deployment"

# GitHubに新しいリポジトリを作成してプッシュ
git remote add origin git@github.com:Edgelabo/inngame.git
git branch -M main
git push -u origin main
```

### 4. Vercelでのデプロイ
1. Vercelダッシュボードで「New Project」をクリック
2. GitHubリポジトリを選択
3. プロジェクト設定：
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: (空白のまま)
   - Output Directory: (空白のまま)
   - Install Command: pip install -r requirements.txt

### 5. 環境変数の設定（必要に応じて）
Vercelダッシュボードで以下の環境変数を設定：
- `PYTHON_VERSION`: 3.10
- `PYTHONPATH`: .

## 📁 Vercel用ファイル構成

```
project/
├── vercel.json              # Vercel設定
├── requirements.txt         # Python依存関係
├── runtime.txt             # Python バージョン
├── .vercelignore           # デプロイ除外ファイル
├── api/
│   └── main.py             # FastAPI アプリケーション
└── setting/                # 設定ファイル（オプション）
    ├── labels.csv
    └── jutsu.csv
```

## ⚠️ 制限事項

### Vercel環境での制限
1. **ファイルサイズ制限**: 大きなモデルファイル（.onnx）は含められません
2. **実行時間制限**: 長時間の処理は制限されます
3. **メモリ制限**: 大きなモデルの読み込みは制限されます

### デモモードの機能
- カメラアクセス: ✅ 利用可能
- WebSocket通信: ✅ 利用可能  
- AI印検出: ❌ 制限（スタブ実装）
- 忍術判定: ❌ 制限（デモデータ）

## 🔧 カスタマイズ

### UIの変更
`api/main.py`のHTMLテンプレート部分を編集してUIをカスタマイズできます。

### 機能の追加
WebSocket エンドポイントに新しい機能を追加することで、リアルタイム機能を拡張できます。

## 🌐 デプロイ後のアクセス

デプロイ完了後、Vercelから提供されるURLでアプリケーションにアクセス可能：
- `https://your-project-name.vercel.app`

## 🔍 トラブルシューティング

### よくある問題
1. **ビルドエラー**: requirements.txtの依存関係を確認
2. **404エラー**: vercel.jsonのルーティング設定を確認
3. **WebSocketエラー**: HTTPSでのWebSocket接続を確認

### ログの確認
Vercelダッシュボードの「Functions」タブでログを確認できます。

## 📝 メンテナンス

### アップデート方法
1. ローカルで変更を加える
2. GitHubにプッシュ
3. Vercelが自動でデプロイ

### パフォーマンス監視
Vercelダッシュボードでパフォーマンス metrics を確認できます。

## 🆚 ローカル版との違い

| 機能 | ローカル版 | Vercel版 |
|------|-----------|----------|
| AI印検出 | ✅ 完全対応 | ❌ デモのみ |
| 忍術判定 | ✅ 完全対応 | ❌ デモのみ |
| UI/UX | ✅ 完全対応 | ✅ 完全対応 |
| カメラアクセス | ✅ 対応 | ✅ 対応 |
| リアルタイム通信 | ✅ 対応 | ✅ 対応 |

完全な機能を体験するには、ローカル環境での実行をお勧めします。
