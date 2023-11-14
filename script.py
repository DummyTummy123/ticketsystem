from PIL import Image
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

def git_push_changes(repo_path, commit_message, file_path, git_access_token):
    repo = Repo(repo_path)
    git = repo.git
    git.add(file_path)
    git.commit('-m', commit_message)
    git.push('https://' + git_access_token + '@github.com/DummyTummy123/ticketsystem.git', repo.active_branch.name)

image_path = 'image.jpg'
css_path = 'color.css'
pinpoints = [(309, 428), (57, 240), (57, 600), (57, 960)]
colors = extract_colors_from_image(image_path, pinpoints)
update_css_file(css_path, colors)
# git_push_changes("D:/ticketsystem", "Updated colors in CSS variables", css_path, "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")