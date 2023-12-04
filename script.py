from PIL import Image
import subprocess
from config import tokeen
import requests
import time

TELEGRAM_API_URL = "https://api.telegram.org/bot6411496327:AAH2Xs84lg1OYqioAFYJWv2WZPKJfdFgf_E"
def get_updates(offset=None):
    params = {"offset": offset} if offset else {}
    response = requests.get(f"{TELEGRAM_API_URL}/getUpdates", params=params)
    return response.json().get("result", [])

def download_file(file_id, file_path):
    response = requests.get(f"{TELEGRAM_API_URL}/getFile", params={"file_id": file_id})
    file_url = response.json().get("result", {}).get("file_path")
    file_data = requests.get(f"https://api.telegram.org/file/bot6411496327:AAH2Xs84lg1OYqioAFYJWv2WZPKJfdFgf_E/{file_url}")
    with open(file_path, "wb") as f:
        f.write(file_data.content)

def send_message(chat_id, text):
    params = {"chat_id": chat_id, "text": text}
    requests.post(f"{TELEGRAM_API_URL}/sendMessage", params=params)

def extract_colors_from_image(image_path, coordinates):
    img = Image.open(image_path)
    img = img.resize((590, 1280))
    colors = []
    for coord in coordinates:
        color = img.getpixel(coord)
        colors.append('#{:02x}{:02x}{:02x}'.format(*color))
    return colors[:4]

def update_css_file(css_path, colors):
    text_to_write = f''':root {{
        --first: {colors[0]};
        --stripone: {colors[1]};
        --striptwo: {colors[2]};
        --stripthree: {colors[3]};
    }}'''

    with open(css_path, 'w') as file:
        file.write(text_to_write)

def git_push_changes():
    subprocess.run(["cd", r"D:\ticketsystem"], check=True, shell=True)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Updated_colors"], check=True)
    remote_url = f"https://dummytummy123:{tokeen}@github.com/dummytummy123/ticketsystem.git"
    subprocess.run(["git", "push", remote_url, "main"], check=True)

offset = None
while True:
    try:
        updates = get_updates(offset)
    except:
        time.sleep(30)
        continue
    if len(updates) > 0:
        update = updates[-1]
        offset = update["update_id"] + 1
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        file_id = message.get("photo", [{}])[-1].get("file_id")
        if file_id is None:
            file_id = message.get("document", {}).get("file_id")
        if file_id:
            download_file(file_id, "image.jpg")
            image_path = 'image.jpg'
            css_path = 'color.css'
            colors = extract_colors_from_image(image_path, [(535, 535), (57, 240), (57, 600), (57, 960)])
            if colors[2]=="#ffffff":
                colors = extract_colors_from_image(image_path, [(105, 389), (110, 1090), (300, 1090), (475, 1090)])
            update_css_file(css_path, colors)
            git_push_changes()
            send_message(chat_id, "ok")
            get_updates(offset)
    
    print("Sleeping for 30")
    time.sleep(30)