from schema import (
    RecommendationResponse,
    SelectedResume,
    VacancyRecommendation,
    VacancyExperience,
    VacancyScores,
    VacancyMatching,
    SkillMatch,
    Metrics,
    ResponseMeta,
)
from read import reader


def get_selected_resume(raw_resume: str) -> SelectedResume:
    """
    Обрабатывает текст резюме и формирует объект selectedResume
    для frontend.
    """

    resume_data = reader(raw_resume)

    return SelectedResume(
        id="resume_001",
        title=resume_data["title"],
        experienceYears=resume_data["experience_years"],
        skills=resume_data["skills"],
    )


def get_vacancy_recommendations(selected_resume: SelectedResume) -> list[VacancyRecommendation]:
    """
    Возвращает top-5 рекомендованных вакансий.

    Сейчас данные тестовые.
    Позже здесь будет вызов модели сопоставления резюме и вакансий.
    """

    vacancies = [
        VacancyRecommendation(
            id="vacancy_001",
            rank=1,
            title="Data Analyst",
            company="Яндекс",
            city="Москва",
            url="https://hh.ru/vacancy/111111",
            source="hh.ru",
            format="офис",
            experience=VacancyExperience(
                label="2-4 года",
                minYears=2,
                maxYears=4,
            ),
            scores=VacancyScores(
                totalScore=0.83,
                semanticScore=0.76,
                skillScore=0.85,
                experienceScore=0.90,
            ),
            matching=VacancyMatching(
                skillMatch=SkillMatch(
                    matched=[
                        "Python",
                        "SQL",
                        "Pandas",
                        "Machine Learning",
                        "Statistics",
                    ],
                    partial=[
                        "NumPy",
                        "Data Analysis",
                        "Excel",
                        "Data Visualization",
                    ],
                    missing=[
                        "Git",
                    ],
                ),
                candidateExperienceYears=selected_resume.experienceYears,
                requiredExperienceLabel="2-4 года",
                experienceComment="Опыт кандидата соответствует требованиям вакансии",
                allResumeSkills=selected_resume.skills,
                allVacancySkills=[
                    "Python",
                    "SQL",
                    "Pandas",
                    "Machine Learning",
                    "Statistics",
                    "NumPy",
                    "Data Analysis",
                    "Excel",
                    "Data Visualization",
                    "Git",
                ],
            ),
        ),
        VacancyRecommendation(
            id="vacancy_002",
            rank=2,
            title="Junior Data Analyst",
            company="Сбер",
            city="Москва",
            url="https://hh.ru/vacancy/222222",
            source="hh.ru",
            format="гибрид",
            experience=VacancyExperience(
                label="1-3 года",
                minYears=1,
                maxYears=3,
            ),
            scores=VacancyScores(
                totalScore=0.76,
                semanticScore=0.76,
                skillScore=0.80,
                experienceScore=0.75,
            ),
            matching=VacancyMatching(
                skillMatch=SkillMatch(
                    matched=[
                        "Python",
                        "SQL",
                        "Pandas",
                        "Excel",
                    ],
                    partial=[
                        "Data Analysis",
                        "Statistics",
                    ],
                    missing=[
                        "Power BI",
                    ],
                ),
                candidateExperienceYears=selected_resume.experienceYears,
                requiredExperienceLabel="1-3 года",
                experienceComment="Опыт кандидата подходит под требования вакансии",
                allResumeSkills=selected_resume.skills,
                allVacancySkills=[
                    "Python",
                    "SQL",
                    "Pandas",
                    "Excel",
                    "Power BI",
                    "Data Analysis",
                    "Statistics",
                ],
            ),
        ),
        VacancyRecommendation(
            id="vacancy_003",
            rank=3,
            title="BI Analyst",
            company="Тинькофф",
            city="Москва",
            url="https://hh.ru/vacancy/333333",
            source="hh.ru",
            format="офис",
            experience=VacancyExperience(
                label="2-3 года",
                minYears=2,
                maxYears=3,
            ),
            scores=VacancyScores(
                totalScore=0.72,
                semanticScore=0.72,
                skillScore=0.75,
                experienceScore=0.72,
            ),
            matching=VacancyMatching(
                skillMatch=SkillMatch(
                    matched=[
                        "SQL",
                        "Excel",
                        "Data Visualization",
                        "Statistics",
                    ],
                    partial=[
                        "Data Analysis",
                    ],
                    missing=[
                        "Power BI",
                        "Tableau",
                    ],
                ),
                candidateExperienceYears=selected_resume.experienceYears,
                requiredExperienceLabel="2-3 года",
                experienceComment="Опыт кандидата находится в допустимом диапазоне",
                allResumeSkills=selected_resume.skills,
                allVacancySkills=[
                    "SQL",
                    "Excel",
                    "Power BI",
                    "Tableau",
                    "Data Visualization",
                    "Statistics",
                    "Data Analysis",
                ],
            ),
        ),
        VacancyRecommendation(
            id="vacancy_004",
            rank=4,
            title="Data Engineer",
            company="Контур",
            city="Москва",
            url="https://hh.ru/vacancy/444444",
            source="hh.ru",
            format="офис",
            experience=VacancyExperience(
                label="3-5 лет",
                minYears=3,
                maxYears=5,
            ),
            scores=VacancyScores(
                totalScore=0.64,
                semanticScore=0.64,
                skillScore=0.60,
                experienceScore=0.70,
            ),
            matching=VacancyMatching(
                skillMatch=SkillMatch(
                    matched=[
                        "Python",
                        "SQL",
                    ],
                    partial=[
                        "Pandas",
                    ],
                    missing=[
                        "Airflow",
                        "Docker",
                        "Spark",
                    ],
                ),
                candidateExperienceYears=selected_resume.experienceYears,
                requiredExperienceLabel="3-5 лет",
                experienceComment="Опыт кандидата находится на нижней границе требований",
                allResumeSkills=selected_resume.skills,
                allVacancySkills=[
                    "Python",
                    "SQL",
                    "Airflow",
                    "Docker",
                    "Spark",
                    "Pandas",
                ],
            ),
        ),
        VacancyRecommendation(
            id="vacancy_005",
            rank=5,
            title="ML Analyst",
            company="Ozon",
            city="Москва",
            url="https://hh.ru/vacancy/555555",
            source="hh.ru",
            format="гибрид",
            experience=VacancyExperience(
                label="2-4 года",
                minYears=2,
                maxYears=4,
            ),
            scores=VacancyScores(
                totalScore=0.58,
                semanticScore=0.58,
                skillScore=0.55,
                experienceScore=0.60,
            ),
            matching=VacancyMatching(
                skillMatch=SkillMatch(
                    matched=[
                        "Python",
                        "Machine Learning",
                        "Statistics",
                    ],
                    partial=[
                        "Pandas",
                        "NumPy",
                    ],
                    missing=[
                        "PyTorch",
                        "NLP",
                        "Docker",
                    ],
                ),
                candidateExperienceYears=selected_resume.experienceYears,
                requiredExperienceLabel="2-4 года",
                experienceComment="Опыт кандидата подходит, но есть недостающие навыки",
                allResumeSkills=selected_resume.skills,
                allVacancySkills=[
                    "Python",
                    "Machine Learning",
                    "Statistics",
                    "Pandas",
                    "NumPy",
                    "PyTorch",
                    "NLP",
                    "Docker",
                ],
            ),
        ),
    ]

    return vacancies


def get_metrics() -> Metrics:
    """
    Возвращает метрики качества для отображения на странице.
    """

    return Metrics(
        goodMatchRateAt5=0.68,
        experienceFitRateAt5=0.72,
        meanSemanticScoreAt5=0.71,
    )


def get_top_vacancies(raw_resume: str) -> RecommendationResponse:
    """
    Основная функция, которую можно вызывать из FastAPI endpoint.

    На вход получает текст резюме.
    На выход возвращает готовую структуру для frontend.
    """

    selected_resume = get_selected_resume(raw_resume)

    recommendations = get_vacancy_recommendations(
        selected_resume=selected_resume
    )

    metrics = get_metrics()

    response = RecommendationResponse(
        selectedResume=selected_resume,
        recommendations=recommendations,
        selectedVacancyId=recommendations[0].id if recommendations else None,
        metrics=metrics,
        meta=ResponseMeta(
            modelName="TF-IDF + Logistic Regression",
            topK=5,
            generatedAt="2026-05-23T12:00:00",
        ),
    )

    return response