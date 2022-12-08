from asyncio import run
from boilerplate import API
from novelai_api.ImagePreset import ImageModel, ImagePreset, ImageResolution, UCPreset
from dotenv import load_dotenv
load_dotenv()
import re
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.getenv('SLACK_BOT_TOKEN'))

GENERATED_FILEPATH = "./generated.png"

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
        if usingUser is not None:
            say(f"<@{usingUser}> さんが画像を生成中ですのでしばらくお待ちください。")

        else:
            usingUser = message['user']
            prompt = context['matches'][0]
            say(f"<@{message['user']}> さんのプロンプト `{prompt}` で画像を生成します。数秒程度お待ちください。")
            run(genarate(prompt))

            client.files_upload(
                channels=message['channel'],
                file=GENERATED_FILEPATH,
                title=prompt
            )

            say(f"<@{message['user']}> さんのプロンプト `{prompt}` の画像の生成が終わりました。")
            usingUser = None
    except Exception as e:
        usingUser = None
        print(e)
        say(f"エラーが発生しました。やり方を変えて試してみてください。 Error: {e}")

@app.message(re.compile(r"^!img-help$"))
def message_help(client, message, say, context):
    say("`!img [半角英数字記号で構成されるプロンプト]` の形式で画像の生成ができます。") 

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.getenv('SLACK_APP_TOKEN')).start()