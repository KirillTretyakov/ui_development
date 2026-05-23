from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from models import ResumeModel
from script import get_top_vacancies


app = FastAPI()


# Нужно будет для подключения frontend
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
    Основной endpoint для frontend.

    Принимает JSON:
    {
        "resume_text": "..."
    }
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
    Дополнительный endpoint для тестирования в Swagger.

    Позволяет вставлять обычный многострочный текст резюме,
    без JSON и без экранирования переносов строк через \\n.
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