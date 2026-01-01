#!/data/data/com.termux/files/usr/bin/sh

termux-wake-lock

PROJECT_DIR="${PROJECT_DIR:-$(cd "$(dirname "$0")" && pwd)}"
cd "$PROJECT_DIR"

. "$PROJECT_DIR/.venv/bin/activate"

LOG_FILE="$PROJECT_DIR/server.log"
echo "서버 시작 $(date)" >> "$LOG_FILE"
python main.py >> "$LOG_FILE" 2>&1 &

sleep 20
am start -W --user 0 -n com.example/.MainActivity >> "$LOG_FILE" 2>&1
echo "am rc=$?" >> "$LOG_FILE"
