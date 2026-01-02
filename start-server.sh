#!/data/data/com.termux/files/usr/bin/sh

termux-wake-lock

SCRIPT_PATH="$0"
if command -v readlink >/dev/null 2>&1; then
  SCRIPT_PATH="$(readlink -f "$0")"
fi

PROJECT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
LOG_FILE="$PROJECT_DIR/server.log"

cd "$PROJECT_DIR" || exit 1

. "$PROJECT_DIR/.venv/bin/activate"

echo "서버 시작 $(date)" >> "$LOG_FILE"
python main.py >> "$LOG_FILE" 2>&1 &

sleep 20
am start -W --user 0 -n com.example/.MainActivity >> "$LOG_FILE" 2>&1
