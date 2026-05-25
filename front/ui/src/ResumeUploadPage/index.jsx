import { useRef, useState } from "react";
import TopSkillsChart from "../components/TopSkillsChart";
import "./styles.css";
import TopResumeTitlesChart from "../components/TopResumeTitlesChart";
import VacancyWordCloud from "../components/VacancyWordCloud";
import ModelComparisonChart from "../components/ModelComparisonChart";

export default function ResumeUploadPage({ onMatchResult }) {
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorText, setErrorText] = useState("");

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setSelectedFile(file);
    setErrorText("");
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      setErrorText("Сначала выберите файл с резюме");
      return;
    }

    try {
      setLoading(true);
      setErrorText("");

      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch("http://localhost:8000/get_data_pdf", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Backend вернул ошибку: ${response.status}`);
      }

      const data = await response.json();

      if (data.status === "error") {
        throw new Error(data.error_text || "Ошибка backend");
      }

      console.log("Ответ backend:", data);

      onMatchResult(data);
    } catch (error) {
      console.error(error);
      setErrorText(
        "Ошибка при подборе вакансий. Проверь, запущен ли backend и доступен ли endpoint /get_data_pdf."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="upload-page">
      <div className="upload-page__content">
        <header className="upload-header">
          <h1>Система сопоставления резюме и вакансий</h1>
          <p>
            Загрузите резюме в текстовом формате. Система обработает данные и
            подберет наиболее подходящие вакансии.
          </p>
        </header>

        <section className="upload-card">
          <div className="upload-card__icon">📄</div>

          <h2>Загрузка резюме</h2>

          <p className="upload-card__description">
            Загрузите PDF-файл резюме. Backend извлечет текст из файла и подберет подходящие вакансии.
          </p>

          <input
            ref={fileInputRef}
            type="file"
            className="upload-input"
            accept=".pdf"
            onChange={handleFileChange}
          />

          <button
            type="button"
            className="upload-button"
            onClick={handleUploadClick}
          >
            Выбрать файл
          </button>

          {selectedFile && (
            <div className="selected-file">
              <span>Выбран файл:</span>
              <strong>{selectedFile.name}</strong>
            </div>
          )}

          <button
            type="button"
            className="submit-button"
            onClick={handleSubmit}
            disabled={!selectedFile || loading}
          >
            {loading ? "Идет подбор..." : "Подобрать вакансии"}
          </button>

          {errorText && (
            <p
              style={{
                marginTop: "16px",
                color: "#ef4444",
                fontWeight: 700
              }}
            >
              {errorText}
            </p>
          )}
        </section>

        <section className="info-card">
          <h2>Как работает система</h2>
          <p>
            Backend очищает текст резюме, извлекает признаки и ранжирует
            вакансии с помощью модели TF-IDF + Logistic Regression.
          </p>

          <div className="info-grid">
            <div className="info-item">
              <h3>1. Загрузка</h3>
              <p>
                Пользователь загружает текст резюме.
              </p>
            </div>

            <div className="info-item">
              <h3>2. Обработка</h3>
              <p>
                Из текста извлекаются должность, опыт работы, навыки и очищенное
                описание, производится сопоставление.
              </p>
            </div>

            <div className="info-item">
              <h3>3. Рекомендации</h3>
              <p>
                Система возвращает top-5 вакансий с итоговой оценкой
                соответствия.
              </p>
            </div>
          </div>
        </section>
        <section className="eda-section">
          <h2>Анализ данных</h2>
          <p>
            Ниже представлены некоторые характеристики данных, использованных при
            построении модели сопоставления резюме и вакансий.
          </p>

          <div className="eda-charts-grid">
            <TopSkillsChart />
            <TopResumeTitlesChart />
          </div>
            <VacancyWordCloud />
        </section>

        <section className="about-project-section">
          <h2>О проекте</h2>
          <p className="about-project-lead">
            Система предназначена для автоматизированного сопоставления резюме и вакансий
            в условиях отсутствия заранее размеченных данных.
          </p>

          <div className="about-project-card">
            <div className="about-project-item">
              <span className="about-dot"></span>
              <div>
                <h3>Данные hh.ru</h3>
                <p>
                  В работе используются тексты резюме и вакансий, очищенные от служебных
                  и нерелевантных фрагментов.
                </p>
              </div>
            </div>

            <div className="about-project-item">
              <span className="about-dot"></span>
              <div>
                <h3>Псевдоразметка</h3>
                <p>
                  Так как экспертная разметка отсутствует, таргет формируется на основе
                  соответствия навыков и опыта работы.
                </p>
              </div>
            </div>

            <div className="about-project-item">
              <span className="about-dot"></span>
              <div>
                <h3>Ранжирование вакансий</h3>
                <p>
                  Модель TF-IDF + Logistic Regression возвращает top-5 вакансий с
                  итоговой оценкой соответствия (вероятностью logreg).
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="tools-section">
  <h2>Использованные инструменты</h2>
  <p className="tools-lead">
    В проекте использовались инструменты для сбора данных, хранения, обработки,
    построения модели, визуализации и разработки веб-интерфейса.
  </p>

  <div className="tools-card">
    <div className="tool-item">
      <span className="tool-dot"></span>
      <div>
        <h3>Python</h3>
        <p>Основной язык разработки для обработки данных, очистки текстов, построения модели и backend-логики.</p>
      </div>
    </div>

    <div className="tool-item">
      <span className="tool-dot"></span>
      <div>
        <h3>Apache Airflow</h3>
        <p>Использовался для автоматизации процессов сбора данных и регулярного запуска задач парсинга.</p>
      </div>
    </div>

    <div className="tool-item">
      <span className="tool-dot"></span>
      <div>
        <h3>PostgreSQL</h3>
        <p>Применялся для хранения собранных резюме, вакансий и промежуточных данных проекта.</p>
      </div>
    </div>

    <div className="tool-item">
      <span className="tool-dot"></span>
      <div>
        <h3>Docker</h3>
        <p>Использовался для контейнеризации сервисов и настройки воспроизводимого окружения.</p>
      </div>
    </div>

    <div className="tool-item">
      <span className="tool-dot"></span>
      <div>
        <h3>Yandex Cloud VM</h3>
        <p>Виртуальная машина использовалась для размещения инфраструктуры проекта и хранения данных.</p>
      </div>
    </div>

    <div className="tool-item">
      <span className="tool-dot"></span>
      <div>
        <h3>Selenium</h3>
        <p>Использовался для автоматизированного сбора данных с веб-страниц резюме и вакансий.</p>
      </div>
    </div>

    <div className="tool-item">
      <span className="tool-dot"></span>
      <div>
        <h3>Pandas / NumPy</h3>
        <p>Применялись для анализа данных, преобразования таблиц, расчета признаков и подготовки выборок.</p>
      </div>
    </div>

    <div className="tool-item">
      <span className="tool-dot"></span>
      <div>
        <h3>Scikit-learn</h3>
        <p>Использовался для TF-IDF-векторизации, обучения Logistic Regression и расчета метрик качества.</p>
      </div>
    </div>

    <div className="tool-item">
      <span className="tool-dot"></span>
      <div>
        <h3>re</h3>
        <p>Библиотека регулярных выражений применялась для очистки текстов и извлечения признаков из резюме и вакансий.</p>
      </div>
    </div>

    <div className="tool-item">
      <span className="tool-dot"></span>
      <div>
        <h3>Matplotlib</h3>
        <p>Использовался для построения графиков и визуального анализа данных на этапе EDA.</p>
      </div>
    </div>

    <div className="tool-item">
      <span className="tool-dot"></span>
      <div>
        <h3>FastAPI</h3>
        <p>Применялся для реализации backend-сервиса, принимающего резюме и возвращающего рекомендации вакансий.</p>
      </div>
    </div>

    <div className="tool-item">
      <span className="tool-dot"></span>
      <div>
        <h3>React</h3>
        <p>Использовался для разработки демонстрационного веб-интерфейса системы сопоставления.</p>
      </div>
    </div>

    <div className="tool-item">
      <span className="tool-dot"></span>
      <div>
        <h3>Recharts</h3>
        <p>Применялся для отображения графиков и характеристик данных внутри веб-интерфейса.</p>
      </div>
    </div>

    <div className="tool-item">
      <span className="tool-dot"></span>
      <div>
        <h3>Вспомогательные библиотеки</h3>
        <p>Дополнительно использовались библиотеки для работы с файлами, сериализации моделей и подготовки данных.</p>
      </div>
    </div>
  </div>
</section>
          <ModelComparisonChart />
                
      </div>
    </main>
  );
}