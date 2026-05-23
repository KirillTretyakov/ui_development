from typing import List, Optional
from pydantic import BaseModel, Field


# ============================================================
# Request schemas
# ============================================================

class RecommendationRequest(BaseModel):
    """
    Запрос на получение рекомендаций.

    На первом этапе можно использовать resumeId,
    если резюме уже есть в базе.

    Если позже пользователь будет загружать текст резюме,
    можно использовать resumeText.
    """

    resumeId: Optional[str] = None
    resumeText: Optional[str] = None
    topK: int = 5


# ============================================================
# Resume schemas
# ============================================================

class SelectedResume(BaseModel):
    """
    Данные выбранного резюме.
    Используются в верхнем блоке интерфейса.
    """

    id: Optional[str] = None
    title: str
    experienceYears: float
    skills: List[str] = Field(default_factory=list)


# ============================================================
# Vacancy schemas
# ============================================================

class VacancyExperience(BaseModel):
    """
    Требуемый опыт по вакансии.
    label нужен для красивого отображения на фронтенде.
    """

    label: str
    minYears: Optional[float] = None
    maxYears: Optional[float] = None


class VacancyScores(BaseModel):
    """
    Оценки соответствия резюме и вакансии.

    totalScore — итоговый score, по которому сортируются вакансии.
    semanticScore — семантическое сходство текстов.
    skillScore — совпадение навыков.
    experienceScore — соответствие опыта.
    """

    totalScore: float
    semanticScore: float
    skillScore: float
    experienceScore: float


class SkillMatch(BaseModel):
    """
    Детализация совпадения навыков.

    matched — навыки, которые совпали.
    partial — частично похожие или близкие навыки.
    missing — навыки, которых не хватает в резюме.
    """

    matched: List[str] = Field(default_factory=list)
    partial: List[str] = Field(default_factory=list)
    missing: List[str] = Field(default_factory=list)


class VacancyMatching(BaseModel):
    """
    Детали совпадения для правой панели интерфейса.
    """

    skillMatch: SkillMatch

    candidateExperienceYears: Optional[float] = None
    requiredExperienceLabel: Optional[str] = None
    experienceComment: Optional[str] = None

    allResumeSkills: List[str] = Field(default_factory=list)
    allVacancySkills: List[str] = Field(default_factory=list)


class VacancyRecommendation(BaseModel):
    """
    Одна вакансия из top-5 рекомендаций.
    """

    id: str
    rank: int

    title: str
    company: Optional[str] = None
    city: Optional[str] = None

    url: Optional[str] = None
    source: Optional[str] = "hh.ru"

    format: Optional[str] = None

    experience: VacancyExperience
    scores: VacancyScores
    matching: VacancyMatching


# ============================================================
# Metrics schemas
# ============================================================

class Metrics(BaseModel):
    """
    Метрики качества, которые отображаются в интерфейсе.
    Можно оставить Optional, если не всегда хочешь их возвращать.
    """

    goodMatchRateAt5: Optional[float] = None
    experienceFitRateAt5: Optional[float] = None
    meanSemanticScoreAt5: Optional[float] = None


# ============================================================
# Meta schemas
# ============================================================

class ResponseMeta(BaseModel):
    """
    Техническая информация об ответе.
    """

    modelName: Optional[str] = None
    topK: int = 5
    generatedAt: Optional[str] = None


# ============================================================
# Main response schema
# ============================================================

class RecommendationResponse(BaseModel):
    """
    Главный JSON, который backend возвращает на frontend.
    """

    selectedResume: SelectedResume

    recommendations: List[VacancyRecommendation] = Field(
        default_factory=list,
        min_length=1,
        max_length=5
    )

    selectedVacancyId: Optional[str] = None

    metrics: Optional[Metrics] = None
    meta: Optional[ResponseMeta] = None