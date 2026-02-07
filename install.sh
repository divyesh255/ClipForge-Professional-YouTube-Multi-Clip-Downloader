#!/bin/bash

echo "----------------------------------"
echo " ClipForge Installer / Updater"
echo "----------------------------------"

echo "Updating system..."
sudo apt update -y
sudo apt upgrade -y

echo "Installing dependencies..."
sudo apt install python3 python3-pip ffmpeg nodejs -y

echo "Updating python libraries..."
pip3 install -U yt-dlp textual rich

echo ""
echo "----------------------------------"
echo " ClipForge Ready / Updated"
echo "----------------------------------"
echo ""
echo "Run tool:"
echo "python3 main.py"
echo ""
