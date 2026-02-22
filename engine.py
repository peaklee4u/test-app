import google.generativeai as genai
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, QUESTION_GEN_PROMPT

load_dotenv()

import streamlit as st

# API 키 설정 (Streamlit secrets를 우선적으로 사용)
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
elif os.getenv("GEMINI_API_KEY"):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
else:
    GEMINI_API_KEY = None

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class InterviewEngine:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model = genai.GenerativeModel(model_name)
    
    def generate_question(self, region, topic):
        prompt = QUESTION_GEN_PROMPT.format(region=region, topic=topic)
        response = self.model.generate_content(prompt)
        return response.text.strip()
    
    def evaluate_answer(self, question, answer):
        prompt = f"{SYSTEM_PROMPT}\n\n[Question]\n{question}\n\n[User Answer]\n{answer}"
        response = self.model.generate_content(prompt)
        return response.text.strip()
