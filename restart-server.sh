#!/data/data/com.termux/files/usr/bin/sh

PROJECT_DIR="$HOME/<PROJECT_DIR>" # TODO: replace <PROJECT_DIR> with your project folder
export PROJECT_DIR

pkill -f "python main.py" 2>/dev/null
pkill -f "uvicorn" 2>/dev/null

sleep 1

sh "$HOME/.termux/boot/start-server.sh"
