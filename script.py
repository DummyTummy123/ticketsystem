from PIL import Image
import subprocess
from git import Repo, GitCommandError

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
    remote_url = f"https://dummytummy123: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@github.com/dummytummy123/ticketsystem.git"
    subprocess.run(["git", "push", remote_url, "main"], check=True)

image_path = 'image.jpg'
css_path = 'color.css'
pinpoints = [(309, 428), (57, 240), (57, 600), (57, 960)]
colors = extract_colors_from_image(image_path, pinpoints)
update_css_file(css_path, colors)
git_push_changes()