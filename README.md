# レシピ動画スライド自動生成ツール

YouTube の料理レシピ動画から、材料リスト・手順サマリー・画像付き詳細手順を自動生成し、スマートフォンで見やすい Web スライドとして出力するツールです。

## 機能

- **URL入力のみ**: YouTube動画URLを入力するだけでレシピを自動生成
- **AI解析**: OpenAI GPT-4を使用して材料と手順を自動抽出
- **モバイル最適化**: スマホ縦画面に最適化されたUI
- **3つのビュー**:
  - 材料リスト（チェックボックス付き）
  - 手順サマリー
  - 画像付き詳細手順（スワイプ操作対応）
- **Screen Wake Lock**: 調理中の画面スリープ防止

## 技術スタック

- **Backend**: Python, FastAPI, yt-dlp, OpenAI API, ffmpeg
- **Frontend**: React, Vite, Swiper.js
- **Deployment**: Docker, Render

## セットアップ（ローカル開発）

### 前提条件

- Python 3.11+
- Node.js 18+
- ffmpeg（画像抽出用）

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd 料理レシピ動画
```

### 2. バックエンドのセットアップ

```bash
# 依存関係のインストール
pip install -r backend/requirements.txt

# .envファイルの作成
cp backend/.env.example backend/.env
# backend/.env を編集してOpenAI APIキーを設定
```

### 3. フロントエンドのセットアップ

```bash
cd frontend
npm install
npm run build
cd ..
```

### 4. サーバーの起動

```bash
uvicorn backend.main:app --reload
```

ブラウザで `http://localhost:8000` にアクセス

## デプロイ（Render）

### 1. Renderアカウントの作成

[Render](https://render.com) でアカウントを作成

### 2. 新しいWebサービスの作成

- **Type**: Web Service
- **Build Command**: `docker build -t recipe-app .`
- **Start Command**: Docker（自動検出）

### 3. 環境変数の設定

Renderのダッシュボードで以下の環境変数を設定:

- `OPENAI_API_KEY`: OpenAI APIキー

### 4. デプロイ

Renderが自動的にDockerイメージをビルドしてデプロイします。

## 使い方

1. トップページでYouTube動画のURLを入力
2. 「レシピを生成」ボタンをクリック
3. 解析が完了するまで待機（数分かかる場合があります）
4. 生成されたレシピを3つのタブで確認:
   - **材料**: チェックボックスで準備状況を管理
   - **サマリー**: 全体の流れを確認
   - **手順**: 画像付きの詳細手順をスワイプで確認

## 既知の制限事項

- クラウド環境からのYouTubeアクセスはブロックされる可能性があります
- 動画の解析には数分かかる場合があります
- 画像抽出の精度は動画の品質に依存します

## ライセンス

私的利用のみ。著作権に注意してください。
