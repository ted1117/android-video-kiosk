#!/data/data/com.termux/files/usr/bin/sh

termux-wake-lock

PROJECT_DIR="$HOME/<PROJECT_DIR>" # TODO: replace <PROJECT_DIR> with your project folder
LOG_FILE="$PROJECT_DIR/server.log"

cd "$PROJECT_DIR" || exit 1

. "$PROJECT_DIR/.venv/bin/activate"

echo "서버 시작 $(date)" >> "$LOG_FILE"
python main.py >> "$LOG_FILE" 2>&1 &

sleep 20
am start -W --user 0 -n com.example/.MainActivity >> "$LOG_FILE" 2>&1
