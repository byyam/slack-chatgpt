SLACK_BOT_TOKEN = ""
SLACK_APP_TOKEN = ""
OPENAI_API_KEY = ""

import os
import openai
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
from slack_bolt import App

# Get os env
if SLACK_BOT_TOKEN == "":
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
if SLACK_APP_TOKEN == "":
    SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
if OPENAI_API_KEY == "":
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Event API & Web API
app = App(token=SLACK_BOT_TOKEN)
client = WebClient(SLACK_BOT_TOKEN)


# This gets activated when the bot is tagged in a channel
@app.event("app_mention")
def handle_message_events(body, logger):
    # Log message
    print(str(body["event"]["text"]).split(">")[1])

    # Create prompt for ChatGPT
    prompt = str(body["event"]["text"]).split(">")[1]

    # Let thre user know that we are busy with the request
    response = client.chat_postMessage(channel=body["event"]["channel"],
                                       thread_ts=body["event"]["event_ts"],
                                       text=f"Hello from your bot! :robot_face: \nThanks for your request, I'm on it!")

    # Check ChatGPT
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5).choices[0].text

    # Reply to thread
    response = client.chat_postMessage(channel=body["event"]["channel"],
                                       thread_ts=body["event"]["event_ts"],
                                       text=f"Here you go: \n{response}")


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
