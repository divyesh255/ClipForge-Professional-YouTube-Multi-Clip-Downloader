import re

def validate_url(url: str) -> bool:
    if not url:
        return False
    return "youtube.com" in url or "youtu.be" in url


def validate_time_format(t: str) -> bool:
    if not t:
        return False
    pattern = r'^(\d{1,2}:)?\d{1,2}:\d{2}$'
    return re.match(pattern, t) is not None


def time_to_seconds(t: str) -> int:
    parts = [int(p) for p in t.split(":")]

    if len(parts) == 3:
        h, m, s = parts
    else:
        h = 0
        m, s = parts

    return h*3600 + m*60 + s


def validate_clip(start: str, end: str):

    if not validate_time_format(start):
        return False, f"Invalid start time: {start}"

    if not validate_time_format(end):
        return False, f"Invalid end time: {end}"

    s = time_to_seconds(start)
    e = time_to_seconds(end)

    if e <= s:
        return False, "End time must be greater than start time"

    return True, "ok"
