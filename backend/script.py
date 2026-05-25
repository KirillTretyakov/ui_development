import pandas as pd
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
from matcher import match
import ast

def normalize_skill(skill: str) -> str:
    return str(skill).lower().strip()


def calculate_experience_score(candidate_experience, required_experience):
    """
    Считает соответствие опыта кандидата требованиям вакансии.

    Если требуемый опыт не указан — считаем, что ограничений нет.
    Если опыт кандидата >= требуемого — score = 1.
    Если опыт кандидата меньше — score = candidate / required.
    """

    if candidate_experience is None:
        candidate_experience = 0

    if required_experience is None or pd.isna(required_experience):
        return 1.0

    candidate_experience = float(candidate_experience)
    required_experience = float(required_experience)

    if required_experience == 0:
        return 1.0

    if candidate_experience >= required_experience:
        return 1.0

    return candidate_experience / required_experience


def calculate_skill_match(resume_skills: list, vacancy_skills: list):
    """
    Сопоставляет навыки резюме и вакансии.

    Возвращает:
    - matched_skills: совпавшие навыки
    - missing_skills: навыки вакансии, которых нет в резюме
    - skill_score: доля совпавших навыков
    """

    resume_skills = resume_skills or []
    vacancy_skills = vacancy_skills or []

    # Если навыки вакансии пришли из CSV строкой вида "['sql', 'python']",
    # преобразуем строку в обычный список.
    if isinstance(vacancy_skills, str):
        try:
            vacancy_skills = ast.literal_eval(vacancy_skills)
        except Exception:
            vacancy_skills = [vacancy_skills]

    # Если после преобразования получилось не list, приводим к пустому списку.
    if not isinstance(vacancy_skills, list):
        vacancy_skills = []

    if not isinstance(resume_skills, list):
        resume_skills = []

    resume_map = {
        normalize_skill(skill): skill
        for skill in resume_skills
        if str(skill).strip()
    }

    vacancy_map = {
        normalize_skill(skill): skill
        for skill in vacancy_skills
        if str(skill).strip()
    }

    resume_set = set(resume_map.keys())
    vacancy_set = set(vacancy_map.keys())

    matched_keys = resume_set & vacancy_set
    missing_keys = vacancy_set - resume_set

    matched_skills = [
        vacancy_map[key]
        for key in matched_keys
    ]

    missing_skills = [
        vacancy_map[key]
        for key in missing_keys
    ]

    if vacancy_set:
        skill_score = len(matched_keys) / len(vacancy_set)
    else:
        skill_score = 0

    return matched_skills, missing_skills, skill_score, vacancy_skills


def get_selected_resume(raw_resume: str) -> SelectedResume:
    """
    Обрабатывает текст резюме и формирует объект selectedResume
    для frontend.
    """

    resume_data = reader(raw_resume)

    return SelectedResume(
        id="resume_001",
        title=resume_data["title"],
        experienceYears=float(resume_data["experience_years"]),
        skills=resume_data["skills"],
        clean_text=resume_data["clean_text"],
    )


def get_vacancy_recommendations(
    selected_resume: SelectedResume,
) -> list[VacancyRecommendation]:
    """
    Возвращает top-5 рекомендованных вакансий на основе модели
    TF-IDF + Logistic Regression.
    """

    df_vac = pd.read_csv("df_vac_final_without_score_gt_095.csv")
    vac_df = match(
        df_vac=df_vac,
        text=selected_resume.clean_text,
        top_k=5
    )

    vacancies = []

    for idx, row in vac_df.iterrows():
        vacancy_skills = row.get("skills_final") or []

        matched_skills, missing_skills, skill_score, vacancy_skills = calculate_skill_match(
            resume_skills=selected_resume.skills,
            vacancy_skills=vacancy_skills,
        )

        experience_min = row.get("experience_years_min")

        if pd.isna(experience_min):
            min_years = None
            experience_label = "не указано"
        else:
            min_years = float(experience_min)
            experience_label = f"от {min_years:g} лет"

        experience_score = calculate_experience_score(
            candidate_experience=selected_resume.experienceYears,
            required_experience=min_years
        )

        model_score = float(row.get("model_score", 0))

        vacancy = VacancyRecommendation(
            id=str(row.get("id")),
            rank=idx + 1,

            title=str(row.get("vacancy_name")),
            company=None,
            city=None,

            url=row.get("vacancy_url"),
            source="hh.ru",
            format=None,

            experience=VacancyExperience(
                label=experience_label,
                minYears=min_years,
                maxYears=None,
            ),

            scores=VacancyScores(
                totalScore=round(model_score, 4),
                semanticScore=round(model_score, 4),
                skillScore=round(skill_score, 4),
                experienceScore=round(experience_score, 4),
            ),

            matching=VacancyMatching(
                skillMatch=SkillMatch(
                    matched=matched_skills,
                    partial=[],
                    missing=missing_skills,
                ),
                candidateExperienceYears=selected_resume.experienceYears,
                requiredExperienceLabel=experience_label,
                experienceComment=(
                    "Опыт кандидата соответствует требованиям вакансии"
                    if experience_score == 1
                    else "Опыт кандидата ниже минимальных требований вакансии"
                ),
                allResumeSkills=selected_resume.skills,
                allVacancySkills=vacancy_skills,
            ),
        )

        vacancies.append(vacancy)

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
        selected_resume=selected_resume, 
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