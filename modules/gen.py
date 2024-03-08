import time

from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from utils.scripts import interact_with, interact_with_to_delete, format_exc

import requests
import replicate
import os
import time

prompt = ""


async def gen(prompt):
    print("Generating...")
    output = replicate.run(
        "playgroundai/playground-v2-1024px-aesthetic:42fe626e41cc811eaf02c94b892774839268ce1994ea778eba97103fe1ef51b8",
        input={
            "width": 1024,
            "height": 1024,
            "prompt": prompt,
            "scheduler": "K_EULER_ANCESTRAL",
            "guidance_scale": 3,
            "apply_watermark": False,
            "negative_prompt": "",
            "num_inference_steps": 50
        }
    )

    print("Line 28")

    if output:
        output_url = output[0]
        print("Output URL:", output_url)

        while True:
            response = requests.get(output_url)
            if response.status_code == 200:
                print("Image found. Downloading...")
                with open("image.png", "wb") as f:
                    f.write(response.content)
                break
            else:
                print("Image not ready. Waiting...")
                time.sleep(5)  # Почекайте 5 секунд перед повторною перевіркою
    else:
        print("No output URL found. Exiting.")

    print("Process completed.")


@Client.on_message(filters.command("gen", prefix) & filters.me)
async def generate(client: Client, message: Message):
    if len(message.command) > 1:
        prompt = message.text.split(maxsplit=1)[1]
    elif message.reply_to_message:
        prompt = message.reply_to_message.text
    else:
        await message.edit("<b>Prompt isn't provided</b>")
        return

    try:
        await message.edit("<b>Generating...</b>")
        await gen(prompt=prompt)
        await message.delete()
        await client.send_photo(message.chat.id, "image.png", caption=f"🖼 Prompt: <b>{prompt}</b>")
    except Exception as e:
        await message.edit(format_exc(e))


modules_help["gen"] = {
    "gen [link|reply]*": "generate a photo by AI",
}
