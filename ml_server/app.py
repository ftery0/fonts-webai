from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import uvicorn
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
