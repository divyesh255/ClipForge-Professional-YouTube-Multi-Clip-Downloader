import subprocess
import datetime
import re

def clean_title(title: str) -> str:
    title = title.replace(" ", "_")
    title = re.sub(r'[^a-zA-Z0-9_\-]', '', title)
    return title


def get_video_title(url: str) -> str:
    try:
        title = subprocess.check_output(
            f'yt-dlp --get-title "{url}"',
            shell=True,
            text=True
        ).strip()
        return clean_title(title)
    except:
        return "video"


def build_base_filename(url: str) -> str:
    title = get_video_title(url)

    now = datetime.datetime.now()
    stamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    return f"{title}_{stamp}"

