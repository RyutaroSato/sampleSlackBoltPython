# -*- coding: utf-8 -*-

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

# FaaS で実行するときは process_before_response を True にする必要があります
app = App(process_before_response=True)

def respond_to_slack_within_3_seconds(body, ack):
    text = body.get("text")
    if text is None or len(text) == 0:
        ack(":x: Usage: /start-process (description here)")
    else:
        ack(f"Accepted! (task: {body['text']})")

import time
def run_long_process(respond, body):
    time.sleep(5)  # 3 秒より長い時間を指定します
    respond(f"Completed! (task: {body['text']})")

app.command("/start-process")(
    ack=respond_to_slack_within_3_seconds,  # `ack()` の呼び出しを担当します
    lazy=[run_long_process]  # `ack()` の呼び出しはできません。複数の関数を持たせることができます。
)

## "おはよう"が含まれるメッセージに対する処理
@app.message("おはよう")
def say_hello(client, message):
    time_stamp = message["ts"]
    emoji_name = 'dragon'
    channel_id = message["channel"]

    # 即座にリアクションすると怪しまれるかもしれないので10秒待ちましょう()笑)
    time.sleep(10)

    client.reactions_add(
        channel=channel_id,
        name=emoji_name,
        timestamp=time_stamp
    )

def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
