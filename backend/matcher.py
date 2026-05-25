import os
import joblib
import pandas as pd

from cleaner import clean_resume_text


def match(df_vac: pd.DataFrame, text: str, top_k: int = 5) -> pd.DataFrame:
    """
    Сопоставление резюме и вакансий через сохранённую модель:
    TF-IDF + Logistic Regression.

    df_vac — DataFrame с вакансиями.
    text — сырой текст резюме.
    top_k — количество вакансий в выдаче.

    Возвращает top-k вакансий, отсортированных по model_score.
    """

    tfidf_logreg = joblib.load("tfidf_logreg.joblib")
    logreg_model = joblib.load("logreg_model.joblib")

    df = df_vac.copy()

    # 1. Очищаем текст резюме
    resume_text_clean = clean_resume_text(text)

    # 2. Подготавливаем тексты вакансий
    df["text_clean"] = df["text_clean"].fillna("").astype(str)

    # 3. Формируем pair_text так же, как в baseline
    df["pair_text"] = (
        resume_text_clean
        + " [sep] "
        + df["text_clean"]
    )

    # 4. Преобразуем пары в TF-IDF-признаки
    X = tfidf_logreg.transform(df["pair_text"])

    # 5. Получаем вероятность класса 1
    # 5. Получаем вероятность класса 1
    df["model_score"] = logreg_model.predict_proba(X)[:, 1]

    


    # 7. Сортируем и берем top-k
    result = (
        df.sort_values("model_score", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )


    df.to_csv(
        "test.csv",
        encoding="utf-8-sig",
        sep=";"
    )

    return result




