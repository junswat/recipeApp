# Renderデプロイクイックガイド

## ステップ1: Renderアカウント作成

1. https://render.com にアクセス
2. **Get Started for Free** または **Sign Up** をクリック
3. **GitHub** アカウントでサインアップ
4. GitHubの認証を許可

## ステップ2: 新しいWebサービスを作成

1. Renderダッシュボードで **New +** → **Web Service** をクリック
2. **Connect a repository** で GitHub を選択
3. リポジトリ一覧から **recipeApp** を選択
4. **Connect** をクリック

## ステップ3: サービス設定

以下の項目を設定:

| 項目 | 設定値 |
|------|--------|
| **Name** | `recipe-video-slides`（任意） |
| **Region** | `Singapore` または `Oregon` |
| **Branch** | `main` |
| **Root Directory** | （空欄） |
| **Runtime** | `Docker`（自動検出） |
| **Instance Type** | `Free` |

## ステップ4: 環境変数の設定

**Environment Variables** セクションで:

1. **Add Environment Variable** をクリック
2. 以下を入力:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: `your-openai-api-key-here`

## ステップ5: デプロイ開始

1. **Create Web Service** ボタンをクリック
2. ビルドログを確認（5〜10分かかります）
3. 完了すると URL が表示されます

## 注意点

- 初回ビルドは時間がかかります（10分程度）
- エラーが発生した場合はログを確認
- RenderのFreeプランは非アクティブ時にスリープします

## トラブルシューティング

### YouTube動画のダウンロードエラー

**エラー内容:**
```
ERROR: [youtube] Sign in to confirm you're not a bot
```

**原因:**
YouTubeがクラウドサーバー（データセンターIP）からのアクセスをBot判定してブロックしています。

**対策済み:**
- 最新版のyt-dlpを使用
- Androidクライアントを模倣するオプションを追加
- User-Agentをブラウザに偽装

**それでもエラーが出る場合:**
1. **別の動画で試す**: 一部の動画は制限が厳しい場合があります
2. **時間をおく**: 短時間に複数回試すとブロックされやすくなります
3. **代替案を検討**: 
   - 他のホスティングサービス（Railway、Fly.io等）を試す
   - ローカル環境で実行する（PC起動が必要）

**動作しやすい動画の特徴:**
- 公開されて時間が経っている動画
- 再生回数が多い人気動画
- 年齢制限やログイン制限がない動画