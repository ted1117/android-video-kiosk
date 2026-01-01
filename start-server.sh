#!/data/data/com.termux/files/usr/bin/sh

termux-wake-lock

cd ~/MyDevFolder/testProject

. ~/.venv/testProject/bin/activate

echo "서버 시작 $(date)" >> server.log
python main.py >> server.log 2>&1 &

sleep 20
am start -W --user 0 -n com.example/.MainActivity >> server.log 2>&1
echo "am rc=$?" >> server.log
