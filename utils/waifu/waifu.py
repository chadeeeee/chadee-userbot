import requests

APIURL = "https://api.waifu.pics"

ENDPOINTS = {
    "SFW": [
        ["waifu", "/sfw/waifu"],
        ["neko", "/sfw/neko"],
        ["shinobu", "/sfw/shinobu"],
        ["megumin", "/sfw/megumin"],
        ["bully", "/sfw/bully"],
        ["cuddle", "/sfw/cuddle"],
        ["cry", "/sfw/cry"],
        ["hug", "/sfw/hug"],
        ["awoo", "/sfw/awoo"],
        ["kiss", "/sfw/kiss"],
        ["lick", "/sfw/lick"],
        ["pat", "/sfw/pat"],
        ["smug", "/sfw/smug"],
        ["bonk", "/sfw/bonk"],
        ["yeet", "/sfw/yeet"],
        ["blush", "/sfw/blush"],
        ["smile", "/sfw/smile"],
        ["wave", "/sfw/wave"],
        ["highfive", "/sfw/highfive"],
        ["handhold", "/sfw/handhold"],
        ["nom", "/sfw/nom"],
        ["bite", "/sfw/bite"],
        ["glomp", "/sfw/glomp"],
        ["slap", "/sfw/slap"],
        ["kill", "/sfw/kill"],
        ["kick", "/sfw/kick"],
        ["happy", "/sfw/happy"],
        ["wink", "/sfw/wink"],
        ["poke", "/sfw/poke"],
        ["dance", "/sfw/dance"],
        ["cringe", "/sfw/cringe"]
    ],
    "NSFW": [
        ["waifu", "/nsfw/waifu"],
        ["neko", "/nsfw/neko"],
        ["trap", "/nsfw/trap"],
        ["blowjob", "/nsfw/blowjob"]
    ]
}

def fetch_image_url(url):
    try:
        response = requests.get(f"{APIURL}{url}")
        if response.status_code == 200:
            data = response.json()
            return data.get("url")  # Возвращает только URL изображения
        else:
            return {"error": "Failed to fetch image."}
    except Exception as e:
        return {"error": str(e)}

def get_item_url(category, item_name):
    for item in ENDPOINTS.get(category, []):
        if item[0] == item_name:
            return item[1]
    return None

if __name__ == "__main__":
    category = "SFW"  # Замените на желаемую категорию ("SFW" или "NSFW")
    item_name = "neko"  # Замените на желаемое имя элемента
    item_url = get_item_url(category, item_name)

    if item_url:
        print(f"Category: {category}")
        print(f"Name: {item_name}")
        print(f"URL: {item_url}")
        image_url = fetch_image_url(item_url)
        print(f"Fetched Image URL: {image_url}")
    else:
        print(f"Item not found in category: {category}")
