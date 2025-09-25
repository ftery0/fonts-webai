from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn
import os
import io
import base64
from pydantic import BaseModel
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from infer import InferencePipeline

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
_pipeline: InferencePipeline = None  # lazy init

class GenerateRequest(BaseModel):
    text: str
    lang: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    lang: str = Form(...),  
):
    try:
        file_location = os.path.join(UPLOAD_DIR, f"{lang}_{file.filename}")

        # 파일 저장
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        # 여기서 lang 값에 따라 분석 로직 분기 가능
        if lang == "kor":
            message = f"한글 손글씨 파일 '{file.filename}'이 성공적으로 업로드 및 분석되었습니다."
        else:
            message = f"영어 손글씨 파일 '{file.filename}'이 성공적으로 업로드 및 분석되었습니다."

        return JSONResponse(
            content={
                "filename": file.filename,
                "lang": lang,
                "message": message,
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, status_code=500
        )

def _find_font_path_for_lang(lang: str) -> Optional[str]:
    # macOS 기본 한글/영문 글꼴 추정 경로
    candidates = []
    if lang == "kor":
        candidates.extend([
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",
            "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        ])
    else:
        candidates.extend([
            "/System/Library/Fonts/SFNS.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ])
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

@app.post("/generate")
def generate(req: GenerateRequest):
    try:
        text = req.text[:200]
        lang = req.lang

        # 간단 베이스라인: 시스템 폰트로 128x128 타일 생성 후, 추론 파이프라인을 통해 스타일 변환
        font_path = _find_font_path_for_lang(lang)
        base_font = ImageFont.truetype(font_path, 96) if font_path else ImageFont.load_default()

        tiles = []
        for ch in text:
            # 128x128 캔버스에 문자 렌더링
            canvas = Image.new("L", (128, 128), 255)
            draw = ImageDraw.Draw(canvas)
            bbox = draw.textbbox((0, 0), ch, font=base_font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            x = max(0, (128 - tw) // 2)
            y = max(0, (128 - th) // 2)
            draw.text((x, y), ch, font=base_font, fill=0)
            tiles.append(canvas)

        # 추론 파이프라인 준비
        global _pipeline
        if _pipeline is None:
            _pipeline = InferencePipeline(ckpt_dir="checkpoints", num_styles=25)

        out_tiles = []
        for t in tiles:
            y_img = _pipeline.infer_image(t, target_style_id=0)
            out_tiles.append(y_img)

        # 타일들을 가로로 이어붙이기 (미리보기용)
        if not out_tiles:
            return JSONResponse(content={"error": "empty input"}, status_code=400)
        tile_w, tile_h = out_tiles[0].size
        concat = Image.new("L", (tile_w * len(out_tiles), tile_h), 255)
        for i, img in enumerate(out_tiles):
            concat.paste(img, (i * tile_w, 0))

        buf = io.BytesIO()
        concat.save(buf, format="PNG")
        buf.seek(0)
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return {"image_base64": f"data:image/png;base64,{b64}", "lang": lang}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
