#!/data/data/com.termux/files/usr/bin/sh

PROJECT_DIR="$(pwd)"
export PROJECT_DIR

pkill -f "python main.py" 2>/dev/null
pkill -f "uvicorn" 2>/dev/null

sleep 1

sh "$HOME/.termux/boot/start-server.sh"
