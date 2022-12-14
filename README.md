# NovelAI Slackbot
Slackを通じてAIアート生成するNovelAIを利用するためのBot

<kbd><img src="image/usage.png"></kbd><br>

## ボットの使い方
- 画像の生成: !img \[半角英数字記号で構成されるプロンプト\]
- 残りの生成可能回数を表示: !img-ct
- 使い方を表示: !img-help

## 環境構築
### NovelAIのアカウントの用意 (ID/PASSWOARD形式)
[NovelAI](https://novelai.net/)にアクセスしてID/PASSWOARD形式でアカウント作成。
画像生成を行うには、Tablet以上の課金プランに入会し、Anlasを得ている必要がある。

なおREST APIを利用したアクセスに関しては個人利用の範囲ではOKであると、NovelAIの開発者より[利用規約](https://novelai.net/terms)を確認した上で[サポートDiscord](https://discord.com/invite/novelai)にて[許可](https://discord.com/channels/836774308772446268/1020000423228215306/threads/1027326619595067465)がある。

<kbd><img src="image/restapi.png"></kbd><br>

### Slack Botのトークンの用意
[Bolt 入門ガイド](https://slack.dev/bolt-python/ja-jp/tutorial/getting-started)に準拠。

- SLACK_BOT_TOKEN
- SLACK_APP_TOKEN

を取得しておく。

#### SLACK_BOT_TOKENで要求するスコープ
- chat:write
- files:write
- files:read

#### Event SubscriptionsのSubscribe to Bot Events で要求するスコープ
- message.channels
- message.groups
- message.im
- message.mpim 

### インストール方法、起動方法
Docker Engine (バージョン3のdocker-composeに対応の必要あり)およびDocker Composeプラグインのインストール。(Docker version 20.10.22, build 3a2c30bで確認済み)

`opt/.env` ファイルを実行フォルダ内に作成して、自分のクレデンシャル情報を記述

```
NAI_USERNAME=xxxxxxx@example.com
NAI_PASSWORD=password999999
SLACK_BOT_TOKEN=xoxb-999999999999999999999999
SLACK_APP_TOKEN=xapp-999999999999999999999999
```

`opt/executable_count_setting.json` を作成して、

- date: 日付
- count: その日付時点の実行可能回数
- day_increment: 1日で増加する実行可能回数

を設定して上限実行回数を記述。

```json
{
    "date": "2022-12-07",
    "count": 2000,
    "day_increment": 20
}
```

あとは以下を実行してイメージをビルド&実行。

```sh
docker compose up -d --build
```

以上で起動。

```
docker compose down
```

で停止。なお、novelai-apiはアップデートがよくあるため、その時には、`docker rmi [イメージID]` でDockerイメージを削除し、再度ビルドしなおすとよい。

## LICNESE
MIT
