import { useMemo, useState } from "react";
import "./styles.css";

function formatScore(value) {
  const number = Number(value || 0);
  return number.toFixed(2);
}

function ScoreBar({ label, value, type }) {
  const percent = Math.max(0, Math.min(100, Number(value || 0) * 100));

  return (
    <div className="score-bar">
      <span className="score-bar__label">{label}</span>

      <div className="score-bar__track">
        <div
          className={`score-bar__fill score-bar__fill--${type}`}
          style={{ width: `${percent}%` }}
        />
      </div>

      <span className="score-bar__value">{formatScore(value)}</span>
    </div>
  );
}

function SkillPill({ children, type }) {
  return (
    <span className={`skill-pill ${type ? `skill-pill--${type}` : ""}`}>
      {children}
    </span>
  );
}

export default function ResumeMatcherTemplate({ data, onBack }) {
  const recommendations = data?.recommendations || [];
  const selectedResume = data?.selectedResume;

  const initialVacancyId =
    data?.selectedVacancyId || recommendations[0]?.id || null;

  const [selectedVacancyId, setSelectedVacancyId] = useState(initialVacancyId);

  const selectedVacancy = useMemo(() => {
    return (
      recommendations.find((vacancy) => vacancy.id === selectedVacancyId) ||
      recommendations[0]
    );
  }, [recommendations, selectedVacancyId]);

  if (!selectedResume || recommendations.length === 0) {
    return (
      <main className="resume-page">
        <div className="resume-page__main">
          <header className="resume-header">
            <h1>Resume Matcher</h1>
            <button className="about-button" onClick={onBack}>
              ← Назад к загрузке
            </button>
          </header>

          <section className="card">
            <div className="card__header">
              <h2>Нет данных для отображения</h2>
            </div>
          </section>
        </div>
      </main>
    );
  }

  const resumeSkills = selectedResume.skills || [];

  const matchedSkills =
    selectedVacancy?.matching?.skillMatch?.matched || [];

  const missingSkills =
    selectedVacancy?.matching?.skillMatch?.missing || [];

  const allResumeSkills =
    selectedVacancy?.matching?.allResumeSkills || resumeSkills;

  const allVacancySkills =
    selectedVacancy?.matching?.allVacancySkills || [];

  return (
    <main className="resume-page">
      <div className="resume-page__layout">
        <section className="resume-page__main">
          <header className="resume-header">
            <h1>Resume Matcher</h1>

            <button className="about-button" onClick={onBack}>
              ← Загрузить другое резюме
            </button>
          </header>

          <section className="selected-resume card">
            <div className="card__header">
              <h2>Выбранное резюме</h2>
            </div>

            <div className="selected-resume__content">
              <div className="selected-resume__main">
                <h3>{selectedResume.title || "Не указано"}</h3>
                <p>
                  Опыт работы:{" "}
                  {selectedResume.experienceYears ?? "не указано"} года
                </p>
              </div>

              <div className="selected-resume__divider" />

              <div className="selected-resume__skills">
                <p>Навыки:</p>

                <div className="skills-list">
                  {resumeSkills.length > 0 ? (
                    resumeSkills.map((skill) => (
                      <SkillPill key={skill}>{skill}</SkillPill>
                    ))
                  ) : (
                    <span>Навыки не найдены</span>
                  )}
                </div>
              </div>
            </div>
          </section>

          <h2 className="section-title">Топ подходящих вакансий</h2>

          <div className="vacancies-list">
            {recommendations.map((vacancy) => (
              <button
                type="button"
                key={vacancy.id}
                className={`vacancy-card card ${
                  vacancy.id === selectedVacancy?.id
                    ? "vacancy-card--active"
                    : ""
                }`}
                onClick={() => setSelectedVacancyId(vacancy.id)}
              >
                <div className="vacancy-card__rank">{vacancy.rank}</div>

                <div className="vacancy-card__info">
                  <h3>{vacancy.title}</h3>
                  <p>
                    Требуемый опыт:{" "}
                    {vacancy.experience?.label || "не указано"}
                  </p>
                </div>

                <div className="vacancy-card__score">
                  {formatScore(vacancy.scores?.totalScore)}
                </div>

                <div className="vacancy-card__metrics">
                  <ScoreBar
                    label="Модель"
                    value={vacancy.scores?.semanticScore}
                    type="semantic"
                  />

                  <ScoreBar
                    label="Навыки"
                    value={vacancy.scores?.skillScore}
                    type="skills"
                  />

                  <ScoreBar
                    label="Опыт"
                    value={vacancy.scores?.experienceScore}
                    type="experience"
                  />
                </div>

                <div className="vacancy-card__arrow">›</div>
              </button>
            ))}
          </div>
        </section>

        <aside className="details-panel">
          <div className="details-panel__header">
            <h2>Детали совпадения</h2>

            <button
              type="button"
              className="details-panel__close"
              onClick={onBack}
            >
              ×
            </button>
          </div>

          <div className="details-panel__title-row">
            <div>
              <h3>{selectedVacancy.title}</h3>
              <p>
                Требуемый опыт:{" "}
                {selectedVacancy.experience?.label || "не указано"}
              </p>
            </div>

            <div className="details-panel__total">
              <strong>
                {formatScore(selectedVacancy.scores?.totalScore)}
              </strong>
              <span>Итоговый score</span>
            </div>
          </div>

          <div className="details-panel__scores">
            <div className="score-box score-box--semantic">
              <span>Модель</span>
              <strong>
                {formatScore(selectedVacancy.scores?.semanticScore)}
              </strong>
            </div>

            <div className="score-box score-box--skills">
              <span>Навыки</span>
              <strong>
                {formatScore(selectedVacancy.scores?.skillScore)}
              </strong>
            </div>

            <div className="score-box score-box--experience">
              <span>Опыт</span>
              <strong>
                {formatScore(selectedVacancy.scores?.experienceScore)}
              </strong>
            </div>
          </div>

          <section className="details-section">
            <h3>Навыки</h3>

            <div className="legend">
              <span>
                <i className="legend__dot legend__dot--match" />
                Совпадает
              </span>

              <span>
                <i className="legend__dot legend__dot--missing" />
                Отсутствует
              </span>
            </div>

            <div className="skills-columns">
              <div className="skills-column">
                <h4>Навыки в резюме</h4>

                <div className="skills-list">
                  {allResumeSkills.map((skill) => (
                    <SkillPill key={skill} type="match">
                      {skill}
                    </SkillPill>
                  ))}
                </div>
              </div>

              <div className="skills-column">
                <h4>Требуемые навыки</h4>

                <div className="skills-list">
                  {allVacancySkills.length > 0 ? (
                    allVacancySkills.map((skill) => {
                      const isMatched = matchedSkills
                        .map((item) => String(item).toLowerCase())
                        .includes(String(skill).toLowerCase());

                      const isMissing = missingSkills
                        .map((item) => String(item).toLowerCase())
                        .includes(String(skill).toLowerCase());

                      return (
                        <SkillPill
                          key={skill}
                          type={isMatched ? "match" : isMissing ? "missing" : ""}
                        >
                          {skill}
                        </SkillPill>
                      );
                    })
                  ) : (
                    <span>Навыки вакансии не указаны</span>
                  )}
                </div>
              </div>
            </div>
          </section>

          <section className="details-section">
            <h3>Опыт работы</h3>

            <div className="experience-info">
              <p>
                Требуемый опыт:{" "}
                {selectedVacancy.matching?.requiredExperienceLabel ||
                  selectedVacancy.experience?.label ||
                  "не указано"}
              </p>

              <p>
                Опыт кандидата:{" "}
                {selectedVacancy.matching?.candidateExperienceYears ??
                  selectedResume.experienceYears ??
                  "не указано"}{" "}
                года
              </p>
            </div>

            <div className="experience-progress">
              <div
                className="experience-progress__fill"
                style={{
                  width: `${Math.max(
                    0,
                    Math.min(
                      100,
                      Number(selectedVacancy.scores?.experienceScore || 0) * 100
                    )
                  )}%`
                }}
              />

              <span>
                {formatScore(selectedVacancy.scores?.experienceScore)}
              </span>
            </div>
          </section>

          {selectedVacancy.url && (
            <section className="details-section">
              <a
                href={selectedVacancy.url}
                target="_blank"
                rel="noreferrer"
                className="about-button"
              >
                Открыть вакансию на hh.ru
              </a>
            </section>
          )}
        </aside>
      </div>
    </main>
  );
}