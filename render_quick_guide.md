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

**対策済み:**
- **アーキテクチャ変更**: 動画ファイルをダウンロードせず、字幕データとメタデータのみを使用するように変更しました。
- これにより、YouTubeのBot検出を回避しやすくなりました。
- 副次効果として、画像は動画のサムネイルのみになります（各ステップの個別画像抽出は無効化）。

**動作しやすい動画の特徴:**
- 字幕（手動または自動生成）がある動画
- 公開設定の動画