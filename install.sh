#!/bin/bash

echo "----------------------------------"
echo " ClipForge Installer / Updater"
echo "----------------------------------"

# TERMUX
if [ -d "/data/data/com.termux/files/usr" ]; then
    echo "Termux detected"

    pkg update -y
    pkg upgrade -y

    pkg install python ffmpeg curl unzip -y

    echo "Updating python libs..."
    pip install --upgrade pip
    pip install -U yt-dlp textual rich

    echo "Updating deno..."
    if command -v deno &> /dev/null
    then
        deno upgrade
    else
        curl -fsSL https://deno.land/install.sh | sh
        export PATH="$HOME/.deno/bin:$PATH"
    fi

# LINUX
else
    echo "Linux detected"

    sudo apt update -y
    sudo apt upgrade -y

    sudo apt install python3 python3-pip ffmpeg curl unzip -y

    echo "Updating python libs..."
    pip3 install --upgrade pip
    pip3 install -U yt-dlp textual rich

    echo "Updating deno..."
    if command -v deno &> /dev/null
    then
        deno upgrade
    else
        curl -fsSL https://deno.land/install.sh | sh
        export PATH="$HOME/.deno/bin:$PATH"
    fi
fi

echo ""
echo "----------------------------------"
echo " ClipForge Ready / Updated"
echo "----------------------------------"
echo ""
echo "Run tool:"
echo "python3 main.py"
echo ""
