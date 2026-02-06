import subprocess
import datetime


def run_cmd(cmd, log_callback=None):
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # live log streaming
    for line in process.stdout:
        if log_callback:
            log_callback(line.rstrip())

    process.wait()
    return process.returncode


def get_title(url):
    try:
        out = subprocess.check_output(
            ["yt-dlp", "--get-title", url],
            text=True
        ).strip()
        return out.replace("/", "_")
    except:
        return "clip"


def build_format_string(q):
    if not q or q == "best":
        return "bestvideo+bestaudio/best"

    try:
        q = int(q)
        return f"bestvideo[height<={q}]+bestaudio/best[height<={q}]"
    except:
        return "bestvideo+bestaudio/best"


def download_clips(url, clips, quality, log_callback=None):

    title = get_title(url)
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fmt = build_format_string(quality)

    if log_callback:
        log_callback(f"🎬 Title: {title}")
        log_callback(f"🎯 Quality: {quality}")
        log_callback("")

    for i, clip in enumerate(clips, start=1):

        start = clip["start"]
        end = clip["end"]
        filename = f"{title}_{now}_clip_{i}.mp4"

        if log_callback:
            log_callback(f"⬇ Downloading clip {i}: {start} → {end}")

        cmd = [
            "yt-dlp",
            "--downloader", "ffmpeg",
            "--download-sections", f"*{start}-{end}",
            "-f", fmt,
            "-o", filename,
            url
        ]

        code = run_cmd(cmd, log_callback)

        if code != 0:
            if log_callback:
                log_callback(f"❌ Error downloading clip {i}")
            continue

        if log_callback:
            log_callback(f"✅ Done clip {i}\n")

    # FINAL completion return
    return True
