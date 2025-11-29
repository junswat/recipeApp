# デプロイ手順ガイド

## ステップ1: GitHubリポジトリの作成

### 1.1 GitHubにログイン
ブラウザで https://github.com/login にアクセスし、ログインしてください。

### 1.2 新しいリポジトリの作成
1. https://github.com/new にアクセス
2. 以下の情報を入力:
   - **Repository name**: `recipe-video-slides` (または任意の名前)
   - **Description**: `レシピ動画スライド自動生成ツール`
   - **Public / Private**: Private を推奨（個人利用のため）
   - **Initialize this repository with**: **何もチェックしない**（既存のコードをプッシュするため）
3. **Create repository** ボタンをクリック

### 1.3 リポジトリにプッシュ
作成されたリポジトリページに表示されるコマンドを使用します。

ターミナルで以下を実行:

```powershell
# リモートリポジトリを追加（URLは自分のリポジトリURLに置き換え）
git remote add origin https://github.com/YOUR_USERNAME/recipe-video-slides.git

# ブランチ名を main に変更（Renderは main ブランチを期待）
git branch -M main

# プッシュ
git push -u origin main
```

**重要**: `YOUR_USERNAME` は自分のGitHubユーザー名に置き換えてください。

---

## ステップ2: Renderへのデプロイ

### 2.1 Renderアカウントの作成
1. https://render.com にアクセス
2. **Get Started for Free** をクリック
3. GitHubアカウントでサインアップ/ログイン

### 2.2 新しいWebサービスの作成
1. Renderダッシュボードで **New +** → **Web Service** をクリック
2. GitHubリポジトリの接続を許可
3. 作成したリポジトリ（`recipe-video-slides`）を選択

### 2.3 サービス設定
以下の設定を入力:

- **Name**: `recipe-video-slides`（任意）
- **Region**: `Singapore` または `Oregon`（日本に近いリージョン）
- **Branch**: `main`
- **Root Directory**: （空欄のまま）
- **Runtime**: `Docker`（自動検出されるはず）
- **Instance Type**: `Free`（無料プラン）

### 2.4 環境変数の設定
**Environment Variables** セクションで **Add Environment Variable** をクリック:

- **Key**: `OPENAI_API_KEY`
- **Value**: `your-openai-api-key-here`

### 2.5 デプロイの開始
**Create Web Service** ボタンをクリック

---

## ステップ3: デプロイの確認

### 3.1 ビルドログの確認
Renderが自動的にDockerイメージをビルドします（5〜10分かかります）。

ログに以下が表示されれば成功:
```
==> Your service is live 🎉
```

### 3.2 URLの取得
デプロイが完了すると、Renderが自動的にURLを生成します:
```
https://recipe-video-slides-xxxx.onrender.com
```

### 3.3 動作確認
1. 生成されたURLにアクセス
2. YouTube動画のURL（例: 料理レシピ動画）を入力
3. 「レシピを生成」ボタンをクリック
4. 解析が完了するまで待機（数分）
5. 生成されたレシピを確認

### 3.4 スマホでの確認
スマホブラウザからURLにアクセスし、以下を確認:
- タブの切り替え（材料・サマリー・手順）
- スライドのスワイプ操作
- Screen Wake Lock（調理中に画面が消えないこと）

---

## トラブルシューティング

### YouTube動画がダウンロードできない
**症状**: ダウンロードエラーが発生
**原因**: RenderのIPがYouTubeにブロックされている
**対処法**:
1. クッキーを使用する（要実装）
2. プロキシを経由する（要実装）
3. 別のホスティングサービスを検討（Railway, Flyなど）

### ビルドが失敗する
**症状**: Dockerビルドエラー
**確認点**:
- `Dockerfile` の内容が正しいか
- `frontend/dist` フォルダが存在するか（ローカルで `npm run build` 実行）

### 画像抽出が動作しない
**症状**: 手順に画像が表示されない
**原因**: ffmpegのインストールエラー、またはタイムスタンプが不正
**対処法**: Renderのログを確認し、エラー内容を特定

---

## 完了！

これでレシピ動画スライド自動生成ツールがクラウドにデプロイされ、スマホからいつでもアクセスできるようになりました！🎉
