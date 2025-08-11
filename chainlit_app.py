import chainlit as cl
import requests

url = "http://localhost:8000/app/words/"

@cl.on_message
async def on_message(message: cl.Message):
    word = message.content.strip()

    try:
        response = requests.get(url + word)

        if response.status_code == 200:
            result = response.json()

            output = []
            for key, value in result.items():
                if value == None or value == "" or value == [] or value == {}:
                    continue

                if key == "tags":
                    continue

                if key == "mean":
                    line = f"mean: {value}"
                    if "tags" in result and result["tags"]:
                        line += f"  (tags: {', '.join(result['tags'])})"
                    output.append(line)

                elif isinstance(value, list):
                    output.append(f"\n{key}:")
                    for v in value:
                        output.append(f"- {v}")
                else:
                    output.append(f"{key}: {value}")

            await cl.Message(content="\n".join(output)).send()

        else:
            await cl.Message(content="Error: " + response.text).send()

    except Exception as err:
        await cl.Message(content="Connection Error: " + str(err)).send()
