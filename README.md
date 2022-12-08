# NovelAI Slackbot
Slackを通じてAIアート生成するNovelAIを利用するためのBot

## 環境構築
### NovelAIのアカウントの用意 (ID/PASSWOARD形式)
[NovelAI](https://novelai.net/)にアクセスしてID/PASSWOARD形式でアカウント作成。
画像生成を行うには、Tablet以上の課金プランに入会し、クレジットを払っている必要がある。

なおREST APIを利用したアクセスに関しては個人利用の範囲ではOKであると、NovelAIの開発者より[利用規約](https://novelai.net/terms)を確認した上で[サポートDiscord](https://discord.com/invite/novelai)にて[許可](https://discord.com/channels/836774308772446268/1020000423228215306/threads/1027326619595067465)をもらっています。

<kbd><img src="image/restapi.png"></kbd><br>

## Slackのアプリに必要な権限
アプリの作り方は[このドキュメント](https://slack.dev/bolt-python/ja-jp/tutorial/getting-started)に準拠。
必要権限は以下。

### OAuth & Permissions - Bot Token Scopes
- chat:write
- files:write
- files:read

### Event Subscriptions
- message.channels
- message.groups
- message.im
- message.mpim 

### インストール方法、起動方法
Python3.9.6以上で動作を確認済み。

.env ファイルを実行フォルダ内に作成して、自分のクレデンシャル情報を記述

```
NAI_USERNAME=xxxxxxx@example.com
NAI_PASSWORD=password999999
SLACK_BOT_TOKEN=xoxb-999999999999999999999999
SLACK_APP_TOKEN=xapp-999999999999999999999999
```

executable_count_setting.json を作成して、

- date: 日付
- count: その日付時点の実行可能回数
- day_increment: 1日で増加する実行可能回数

を設定して記述しておきます。

```json
{
    "date": "2022-12-07",
    "count": 2000,
    "day_increment": 20
}
```

あとは以下を実行。

```sh
pip3 install python-dotenv --upgrade
pip3 install novelai-api --upgrade
pip3 install slack_bolt --upgrade
pip3 list # python-dotenv と novelai-api と slack-bolt と slack-sdkを確認
python3 app.py
```

以上で起動。tmuxなどのセッションを維持するツールで起動することを前提としている。

なお、novelai-apiはアップデートがよくあるため、

```sh
pip3 install novelai-api --upgrade
```

は時折実行して再起動する必要がある。動作確認バージョンは、novelai-api v0.10.2

## LICNESE
MIT
