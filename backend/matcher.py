import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from cleaner import clean_resume_text


def match(df_vac: pd.DataFrame, text: str, top_k: int = 5) -> pd.DataFrame:
    """
    Простое сопоставление резюме и вакансий через TF-IDF.

    df_vac — DataFrame с вакансиями.
    text — сырой текст резюме.
    top_k — количество вакансий в выдаче.

    Возвращает top-k вакансий, отсортированных по tfidf_score.
    """

    df = df_vac.copy()

    # 1. Очищаем текст резюме
    resume_text_clean = clean_resume_text(text)

    # 2. Берем очищенные тексты вакансий
    vacancy_texts = df["text_clean"].fillna("").astype(str).tolist()

    # 3. Собираем общий корпус: резюме + вакансии
    corpus = [resume_text_clean] + vacancy_texts

    # 4. TF-IDF как в baseline
    vectorizer = TfidfVectorizer(
        max_features=20000,
        ngram_range=(1, 1),
        min_df=5,
        max_df=0.9
    )

    tfidf_matrix = vectorizer.fit_transform(corpus)

    # 5. Отделяем вектор резюме и векторы вакансий
    resume_vector = tfidf_matrix[0]
    vacancy_vectors = tfidf_matrix[1:]

    # 6. Считаем cosine similarity
    scores = cosine_similarity(resume_vector, vacancy_vectors).flatten()

    # 7. Добавляем score к вакансиям
    df["tfidf_score"] = scores

    # 8. Сортируем и берем top-k
    result = (
        df.sort_values("tfidf_score", ascending=False)
        .head(top_k)
        .reset_index(drop=True)
    )

    return result


df_vac = pd.DataFrame('df_vac_final.csv')
text = ''

match(df_vac, text)

