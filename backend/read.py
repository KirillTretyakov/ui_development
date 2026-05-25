from pypdf import PdfReader
from extract import extract_exp, extract_skills, extract_title
from cleaner import clean_resume_text
from matcher import match
import pandas as pd


def reader(text):
# reader = PdfReader("data/example.pdf")
# text = ""
# for page in reader.pages:
#     text += page.extract_text() + "\n"

    # print(text)
    # print(extract_exp(text))
    # print(extract_skills(text))
    # print(clean_resume_text(text))
    # clean_text = clean_resume_text(text)
    # with open("clean_resume.txt", "w", encoding="utf-8") as file:
    #     file.write(clean_text)
    df_vac = pd.read_csv('df_vac_final_without_score_gt_095.csv')

    title = extract_title(text)
    experience_years = extract_exp(text)
    skills = extract_skills(text)
    clean_text = clean_resume_text(text)
    df_vac_rec = match(df_vac, clean_text)

    return {
        "title": title,
        "experience_years": experience_years,
        "skills": skills,
        "clean_text": clean_text
    }
