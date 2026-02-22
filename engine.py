import google.generativeai as genai
from google.api_core import exceptions
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
    def __init__(self, model_name="gemini-2.0-flash"):
        self.model = genai.GenerativeModel(model_name)
    
    def get_available_models(self):
        try:
            models = [m.name for m in genai.list_models()]
            return models
        except Exception as e:
            return [f"Error listing models: {str(e)}"]

    def generate_question(self, region, topic):
        try:
            prompt = QUESTION_GEN_PROMPT.format(region=region, topic=topic)
            response = self.model.generate_content(prompt)
            
            if not response.text:
                if response.candidates and response.candidates[0].finish_reason != 1:
                    return f"⚠️ 문제가 생성되지 않았습니다. (사유: {response.candidates[0].finish_reason})"
                return "⚠️ 응답이 비어있습니다. 다시 시도해주세요."
                
            return response.text.strip()
        except Exception as e:
            return f"❌ 오류 발생: {str(e)}"
    
    def evaluate_answer(self, question, answer):
        try:
            if not answer or len(answer.strip()) < 5:
                return "⚠️ 답변이 너무 짧습니다. 조금 더 자세히 입력해주세요."
                
            prompt = f"{SYSTEM_PROMPT}\n\n[Question]\n{question}\n\n[User Answer]\n{answer}"
            response = self.model.generate_content(prompt)
            
            if not response.text:
                return "⚠️ 평가 결과를 가져오지 못했습니다. 안전 필터에 의해 차단되었을 수 있습니다."
                
            return response.text.strip()
        except Exception as e:
            return f"❌ 분석 중 오류가 발생했습니다: {str(e)}"
