import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
import urllib.parse
import socket

# ==========================================
# 1. 앱 설정 및 경로 초기화
# ==========================================
app = FastAPI()

# CORS 허용 (태블릿 등 다른 기기 접속 시 필요)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# [핵심] 현재 파일(main.py)이 있는 위치를 기준으로 templates 폴더 찾기
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
VIDEO_FOLDER = "/storage/emulated/0/Movies"  # 안드로이드 동영상 폴더

# 템플릿 폴더 존재 확인
if not TEMPLATES_DIR.exists():
    print(f"\n❌ [오류] templates 폴더가 없습니다!")
    print(f"👉 경로: {TEMPLATES_DIR}\n")
    # 폴더가 없으면 에러가 나므로 임시로 현재 폴더 지정 (에러 방지용)
    templates = Jinja2Templates(directory=".")
else:
    print(f"✅ 템플릿 폴더 연결: {TEMPLATES_DIR}")
    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# 동영상 폴더가 없으면 생성 (에러 방지)
if not os.path.exists(VIDEO_FOLDER):
    os.makedirs("videos", exist_ok=True)
    VIDEO_FOLDER = "videos"

# [핵심] 정적 파일 마운트 (동영상 스트리밍/이어보기 지원)
app.mount("/stream", StaticFiles(directory=VIDEO_FOLDER), name="stream")

# 지원할 확장자
VIDEO_EXTENSIONS = {".mp4", ".webm", ".ogg"}


# ==========================================
# 2. 메인 로직
# ==========================================
@app.get("/")
async def index(request: Request):
    videos = []
    warnings = []

    # 폴더 탐색
    for root, dirs, files in os.walk(VIDEO_FOLDER):
        for file in files:
            path_obj = Path(file)
            ext = path_obj.suffix.lower()

            if ext in VIDEO_EXTENSIONS:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, VIDEO_FOLDER)
                # 윈도우(\) -> 웹(/) 경로 변환
                web_path = rel_path.replace(os.sep, "/")

                videos.append(
                    {
                        # URL 인코딩 (한글, 공백 처리)
                        "path": urllib.parse.quote(web_path),
                        "name": path_obj.stem,
                    }
                )
            elif ext in {".mkv", ".avi", ".wmv", ".flv"}:
                warnings.append(file)

    # 이름순 정렬
    videos.sort(key=lambda x: x["name"])

    # HTML 템플릿 렌더링
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "videos": videos,
            "warnings": warnings,
            "folder": VIDEO_FOLDER,
        },
    )


# ==========================================
# 3. 내부 IP 찾기 (접속 주소 안내용)
# ==========================================
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


if __name__ == "__main__":
    ip_address = get_ip()
    print("=" * 50)
    print(f"🚀 서버 실행 중!")
    print(f"📂 동영상 폴더: {VIDEO_FOLDER}")
    print(f"📱 내 폰에서 접속: http://localhost:8000")
    print(f"📺 다른 기기 접속: http://{ip_address}:8000")
    print("=" * 50)

    # aiofiles 경고 무시 및 실행
    uvicorn.run(app, host="0.0.0.0", port=8000)
