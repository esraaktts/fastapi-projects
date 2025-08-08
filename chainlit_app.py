import chainlit as cl
import requests
import json

url = "http://localhost:8000/app/words/"

@cl.on_message
async def on_message(message: cl.Message):
    path = message.content.strip()

    try:
        res = requests.get(f"{url}{path}")

        if res.ok:
            formatted_json = json.dumps(res.json())
            await cl.Message(content=formatted_json).send()
        else:
            await cl.Message(content=res.text).send()

    except Exception as e:
        await cl.Message(content=str(e)).send()
