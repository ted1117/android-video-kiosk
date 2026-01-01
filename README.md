# Grandma Tablet Video Kiosk

안드로이드 태블릿을 키오스크 모드로 고정하여 할머니께서 **정해진 동영상만 선택·재생**할 수 있도록 만드는 프로젝트입니다.

Termux 환경에서 FastAPI 서버를 실행하고, 키오스크 WebView 앱에서 `localhost`로 접속하는 구조입니다.

---

## 개요

- Android 태블릿 (Android 15 기준)
- 내부 저장소 동영상만 노출
- 주소 입력 및 다른 앱 전환 불가
- FastAPI 기반 단순 웹 UI
- `/stream/{path}` 방식 스트리밍

---

## 요구사항

- Android 태블릿
- Termux (F-Droid 버전 권장)
- Termux:Boot
- Git

---

## 설치 방법

### 1) Termux 초기 설정

- Play Store보다 F-Droid 버전 권장: https://f-droid.org/en/packages/com.termux/
- 저장소 접근 권한을 허용합니다.

```bash
termux-setup-storage
```

### 2) 필수 패키지 설치

```bash
pkg update && pkg upgrade -y
pkg install python git -y
```

설치 확인:

```bash
python --version
git --version
```

### 3) 프로젝트 클론

- Termux 홈 디렉토리에서 진행합니다.

```bash
git clone https://github.com/ted1117/android-video-kiosk <PROJECT_DIR>
cd <PROJECT_DIR>
```

### 4) Python 가상환경 생성 및 활성화

```bash
python -m venv .venv
source .venv/bin/activate
```

### 5) 의존성 설치

```bash
pip install -r requirements.txt
```

### 6) 서버 실행

```bash
python main.py
```

---

## 부팅 후 자동 실행 (선택)

### 1) Termux:Boot 초기 설정

- F-Droid에서 Termux:Boot 설치
- 설치 후 앱을 한 번 실행

```bash
mkdir ~/.termux/boot/
```

### 2) start-server.sh 준비

```bash
cp ~/android-video-kiosk/start-server.sh ~/.termux/boot/
cd ~/.termux/boot/
nano start-server.sh
```

`com.example/.MainActivity`는 실행하려는 앱의 패키지명과 액티비티명으로 교체합니다.

```bash
chmod +x start-server.sh
```
