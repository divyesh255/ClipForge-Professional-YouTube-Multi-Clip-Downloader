import subprocess
import re

def fetch_qualities(url: str) -> list:
    try:
        result = subprocess.check_output(
            f'yt-dlp -F "{url}"',
            shell=True,
            text=True
        )

        resolutions = set()

        for line in result.splitlines():
            match = re.search(r'(\d{3,4})p', line)
            if match:
                resolutions.add(match.group(1))

        resolutions = sorted(resolutions, key=int, reverse=True)

        qualities = ["best"]
        qualities.extend(resolutions)

        print("[DEBUG] Parsed qualities:", qualities)

        return qualities

    except Exception as e:
        print("[ERROR fetching qualities]", e)
        return ["best"]
