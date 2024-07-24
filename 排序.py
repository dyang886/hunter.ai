import fitz  # PyMuPDF
import openai
from dotenv import load_dotenv
import os
import sys

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_path, '.env')
load_dotenv(env_path)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GPT_VERSION = "gpt-4o-mini"

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Function to rank resumes using OpenAI API
def rank_resumes(resume_texts):
    openai.api_key = OPENAI_API_KEY

    prompt = "Rank the following resumes from best to worst, give reasons:\n\n"
    for i, text in enumerate(resume_texts):
        prompt += f"Resume {i+1}:\n{text}\n\n"

    response = openai.chat.completions.create(
        model=GPT_VERSION,
        messages=[
            {"role": "system", "content": "You are a hiring manager evaluating resumes."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


pdf_paths = [f"resume samples/resume{i+1}.pdf" for i in range(10)]
resume_texts = [extract_text_from_pdf(pdf_path) for pdf_path in pdf_paths]
ranked_resumes = rank_resumes(resume_texts)
print(ranked_resumes)
