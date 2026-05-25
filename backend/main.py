from fastapi import FastAPI, Body, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from models import ResumeModel
from script import get_top_vacancies
from pdf_reader import extract_text_from_pdf


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/get_data")
def get_data(request: ResumeModel):
    """
    Основной endpoint для JSON-запроса с текстом резюме.
    """

    raw_resume = request.resume_text

    try:
        result = get_top_vacancies(raw_resume)
        return result
    except Exception as e:
        print(e)
        return {
            "status": "error",
            "error_code": 600,
            "error_text": "Internal Server Error"
        }


@app.post("/get_data_text")
def get_data_text(raw_resume: str = Body(..., media_type="text/plain")):
    """
    Endpoint для тестирования обычным текстом.
    """

    try:
        result = get_top_vacancies(raw_resume)
        return result
    except Exception as e:
        print(e)
        return {
            "status": "error",
            "error_code": 600,
            "error_text": "Internal Server Error"
        }


@app.post("/get_data_pdf")
async def get_data_pdf(file: UploadFile = File(...)):
    """
    Endpoint для загрузки PDF-резюме.

    Принимает PDF-файл, извлекает из него текст,
    затем запускает ту же логику, что и для обычного текста.
    """

    try:
        if file.content_type != "application/pdf":
            return {
                "status": "error",
                "error_code": 400,
                "error_text": "Файл должен быть в формате PDF"
            }

        file_bytes = await file.read()

        raw_resume = extract_text_from_pdf(file_bytes)

        if not raw_resume:
            return {
                "status": "error",
                "error_code": 422,
                "error_text": "Не удалось извлечь текст из PDF"
            }

        result = get_top_vacancies(raw_resume)

        return result

    except Exception as e:
        print(e)
        return {
            "status": "error",
            "error_code": 600,
            "error_text": "Internal Server Error"
        }