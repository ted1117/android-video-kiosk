# Termux (Android) Setup Guide

이 프로젝트는 Termux에서 FastAPI 서버(`main.py`)를 실행해, 안드로이드 기기(폰/태블릿)에서 동영상 목록을 웹으로 보여주고 `/stream/...`로 재생합니다.

## 요구사항

- Android + Termux (F-Droid 버전 권장)
- `git`, `python`

## 1) Termux 초기 설정

```bash
termux-setup-storage
pkg update && pkg upgrade -y
pkg install -y python git
python -m pip install --upgrade pip
```

## 2) 설치 (git clone)

공유 저장소(파일앱에서 접근 쉬움)에 두고 싶으면:

```bash
cd ~/storage/shared
git clone <YOUR_REPO_URL> android-video-kiosk
cd android-video-kiosk
```

## 3) 가상환경 + 의존성 설치

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

## 4) 동영상 폴더 준비

`main.py`는 기본적으로 안드로이드 동영상 폴더를 사용합니다:

- 기본 경로: `/storage/emulated/0/Movies`

위 폴더가 없으면, 프로젝트 내부 `videos/` 폴더로 자동 폴백합니다.

## 5) 실행

```bash
python main.py
```

브라우저에서 접속:

- 같은 기기: `http://localhost:8000`
- 같은 Wi‑Fi의 다른 기기: `http://<폰/태블릿IP>:8000`

## 자주 겪는 문제

### `/storage/...` 접근이 안 돼요

- `termux-setup-storage`를 실행했고 권한을 허용했는지 확인하세요.
- 안드로이드 버전에 따라 “모든 파일 접근” 권한 정책이 달라질 수 있어, 가장 확실한 방법은 프로젝트의 `videos/` 폴더에 파일을 두는 것입니다.

### 화면이 꺼지면 서버가 멈춰요

```bash
termux-wake-lock
```

## (선택) uvicorn으로 실행

`python main.py` 대신 다음도 가능합니다:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```
