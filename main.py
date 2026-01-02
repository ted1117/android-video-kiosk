import mimetypes
import os
import urllib.parse
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ==========================================
# 1. 앱 설정 및 경로 초기화
# ==========================================
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# [핵심] 현재 파일(main.py)이 있는 위치를 기준으로 templates 폴더 찾기
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
VIDEO_FOLDER = "/storage/emulated/0/Movies"  # 안드로이드 동영상 폴더

# 템플릿 폴더 존재 확인
if not TEMPLATES_DIR.exists():
    print("\n[오류] templates 폴더가 없습니다!")
    print(f"경로: {TEMPLATES_DIR}\n")
    # 폴더가 없으면 에러가 나므로 임시로 현재 폴더 지정 (에러 방지용)
    templates = Jinja2Templates(directory=".")
else:
    print(f"템플릿 폴더 연결: {TEMPLATES_DIR}")
    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# 동영상 폴더가 없으면 생성 (에러 방지)
if not os.path.exists(VIDEO_FOLDER):
    os.makedirs("videos", exist_ok=True)
    VIDEO_FOLDER = "videos"

# 지원할 확장자
VIDEO_EXTENSIONS = {".mp4", ".webm", ".ogg"}


# ==========================================
# 2. 유틸/스트리밍
# ==========================================
def _resolve_video_path(requested_path: str) -> str:
    decoded = urllib.parse.unquote(requested_path)
    normalized = os.path.normpath(decoded).lstrip(os.sep)
    full_path = os.path.realpath(os.path.join(VIDEO_FOLDER, normalized))
    base_path = os.path.realpath(VIDEO_FOLDER)
    if os.path.commonpath([full_path, base_path]) != base_path:
        raise HTTPException(status_code=404, detail="Not Found")
    return full_path


def _parse_range(range_header: str, file_size: int):
    if not range_header.startswith("bytes="):
        return None
    range_value = range_header.replace("bytes=", "", 1).strip()
    if not range_value:
        return None
    if "," in range_value:
        range_value = range_value.split(",", 1)[0].strip()
    start_str, sep, end_str = range_value.partition("-")
    if sep != "-":
        return None

    try:
        if start_str == "" and end_str == "":
            return None
        if start_str == "":
            suffix_length = int(end_str)
            if suffix_length <= 0:
                return None
            start = max(file_size - suffix_length, 0)
            end = file_size - 1
        else:
            start = int(start_str)
            end = file_size - 1 if end_str == "" else int(end_str)
            if start > end:
                return None
    except ValueError:
        return None

    if start >= file_size:
        return None
    end = min(end, file_size - 1)
    return start, end


def _iter_file(path: str, start: int, end: int, chunk_size: int = 64 * 1024):
    with open(path, "rb") as file_obj:
        file_obj.seek(start)
        remaining = end - start + 1
        while remaining > 0:
            read_size = min(chunk_size, remaining)
            data = file_obj.read(read_size)
            if not data:
                break
            remaining -= len(data)
            yield data


@app.get("/stream/{path:path}")
async def stream_video(path: str, request: Request):
    full_path = _resolve_video_path(path)
    if not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail="Not Found")

    file_size = os.path.getsize(full_path)
    media_type = mimetypes.guess_type(full_path)[0] or "application/octet-stream"
    range_header = request.headers.get("range")

    if file_size == 0:
        headers = {"Accept-Ranges": "bytes", "Content-Length": "0"}
        return Response(status_code=200, headers=headers, media_type=media_type)

    if range_header:
        parsed = _parse_range(range_header, file_size)
        if parsed is None:
            headers = {"Content-Range": f"bytes */{file_size}"}
            raise HTTPException(
                status_code=416, detail="Range Not Satisfiable", headers=headers
            )
        start, end = parsed
        status_code = 206
    else:
        start, end = 0, file_size - 1
        status_code = 200

    headers = {
        "Accept-Ranges": "bytes",
        "Content-Length": str(end - start + 1),
    }
    if status_code == 206:
        headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"

    if request.method == "HEAD":
        return Response(status_code=status_code, headers=headers, media_type=media_type)

    return StreamingResponse(
        _iter_file(full_path, start, end),
        status_code=status_code,
        headers=headers,
        media_type=media_type,
    )


# ==========================================
# 3. 메인 로직
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


if __name__ == "__main__":
    uvicorn.run(app)
