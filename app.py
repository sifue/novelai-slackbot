from asyncio import run
from boilerplate import API
from novelai_api.ImagePreset import ImageModel, ImagePreset, ImageResolution, UCPreset
from dotenv import load_dotenv
load_dotenv()
import re
import os
import json
import datetime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.getenv('SLACK_BOT_TOKEN'))

GENERATED_FILEPATH = "./generated.png"
EXECUTABLE_COUNT_SETTING_FILEPATH = "./executable_count_setting.json"

# 生成可能回数の初期値設定
last_execute_date = datetime.datetime.now()
executable_count = 0
day_increment = 0

# 起動時に実行可能回数の設定を読み込む
with open(EXECUTABLE_COUNT_SETTING_FILEPATH) as f:
    setting = json.load(f)
    last_execute_date = datetime.datetime.strptime(setting["date"], "%Y-%m-%d")
    executable_count = setting["count"]
    day_increment = setting["day_increment"]

# 実行可能回数の設定を保存する
def save_executable_count_setting():
    executable_count_setting = { "date": last_execute_date.strftime("%Y-%m-%d"), "count" : executable_count, "day_increment": day_increment}
    with open(EXECUTABLE_COUNT_SETTING_FILEPATH, 'w') as f:
        json.dump(executable_count_setting, f, indent=4)

# 一日に生成できる回数の上限を再設定
def update_executable_count():
    now = datetime.datetime.now()
    global last_execute_date
    global executable_count
    date_diff = now - last_execute_date
    if date_diff.days > 0:
        executable_count += day_increment * date_diff.days
        last_execute_date = now
        save_executable_count_setting()

async def genarate(prompt):
    async with API() as api_handler:
        api = api_handler.api
        preset = ImagePreset()
        preset["n_samples"] = 1
        preset["resolution"] = (512, 512)
        preset["quality_toggle"] = False
        async for img in api.high_level.generate_image(prompt, ImageModel.Anime_Curated, preset):
            with open(GENERATED_FILEPATH, "wb") as f:
                f.write(img)

@app.message(re.compile(r"^!img ([ a-zA-Z0-9!-/:-@¥[-`'{-~]+)$"))
def message_img(client, message, say, context):
    usingUser = None
    try:
        global executable_count
        update_executable_count()

        if usingUser is not None:
            say(f"<@{usingUser}> さんが画像を生成中ですのでしばらくお待ちください。")

        elif executable_count <= 0:
            say(f"今日の生成回数の上限に達しました。明日もう一度お試しください。")

        else:
            usingUser = message['user']
            prompt = context['matches'][0]

            # 可能な限りの問題回避ワードの置換
            ngs = ["nsfw", "nude", "fuck ", "fucked "]
            for ng in ngs:
                prompt = prompt.replace(ng, "")

            say(f"<@{message['user']}> さんのプロンプト `{prompt}` で画像を生成します。数秒程度お待ちください。")
            run(genarate(prompt))

            client.files_upload(
                channels=message['channel'],
                file=GENERATED_FILEPATH,
                title=prompt
            )

            executable_count -= 1
            save_executable_count_setting()

            say(f"<@{message['user']}> さんのプロンプト `{prompt}` の画像の生成が終わりました。あと `{executable_count}` 回生成できます。")
            usingUser = None
    except Exception as e:
        usingUser = None
        print(e)
        say(f"エラーが発生しました。やり方を変えて試してみてください。 Error: {e}")

@app.message(re.compile(r"^!img-ct$"))
def message_ct(client, message, say, context):
    update_executable_count()
    say(f"本日は、あと `{executable_count}` 回生成できます。日が変わると `{day_increment}` 回増えます。") 

@app.message(re.compile(r"^!img-help$"))
def message_help(client, message, say, context):
    update_executable_count()
    say("`!img [半角英数字記号で構成されるプロンプト]` の形式で画像の生成ができます。\n" +
    f"`!img-ct` で残りの生成可能回数を確認できます。\n" +
    "生成には数秒程度の時間がかかります。絶対にエログロ画像などは生成しないようにしてください。停止することになります。" +
    "また、誰かが生成している際には実行できません。内部的にはNovelAIというWebサービスを有償利用しています。" +
    "そのため生成した画像のライセンスはCC0 1.0 Universal Public Domain Dedicationとなり、誰にも著作権は発生しません。" +
    "またプロンプト探しには https://p1atdev.notion.site/5d32c4e0eafe4e6997573e937bef120d をご利用ください。")

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.getenv('SLACK_APP_TOKEN')).start()