import streamlit as st
from streamlit_mic_recorder import mic_recorder
from engine import InterviewEngine
from style import apply_custom_style
import os

# 페이지 설정
st.set_page_config(page_title="2026 임용 마스터", layout="wide")
apply_custom_style()

# 세션 상태 초기화
if "question" not in st.session_state:
    st.session_state.question = ""
if "evaluation" not in st.session_state:
    st.session_state.evaluation = None

# 상단 타이틀
st.markdown("<h1 style='text-align: center; color: #003366;'>🚀 2026 임용 마스터</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>2026학년도 중등교사 임용시험 AI 면접 코치</p>", unsafe_allow_html=True)

# 사이드바: 설정 및 필터
with st.sidebar:
    st.header("⚙️ 설정")
    
    # st.secrets 또는 환경변수에서 API 키 확인
    if "GEMINI_API_KEY" in st.secrets or os.getenv("GEMINI_API_KEY"):
        st.success("✅ API 키가 설정되었습니다.")
        engine = InterviewEngine()
    else:
        st.error("❌ API 키가 설정되지 않았습니다.")
        st.info("`.streamlit/secrets.toml` 파일이나 Streamlit Cloud의 Secrets 설정에 `GEMINI_API_KEY`를 추가해주세요.")
        engine = None

    region = st.selectbox("지원 지역", ["서울", "경기"])
    topic = st.selectbox("핵심 주제", [
        "공동체형 인성", 
        "AI·디지털 리터러시", 
        "학생 마음건강",
        "수업 설계 및 교육과정",
        "생활지도 및 상담"
    ])

    st.divider()
    with st.expander("🛠️ 디버그 정보"):
        import google.generativeai as genai_ver
        st.caption(f"SDK Version: {genai_ver.__version__}")
        if st.button("사용 가능 모델 확인"):
            if engine:
                models = engine.get_available_models()
                st.write(models)
            else:
                st.error("API 키가 설정되지 않았습니다.")

    if st.button("새 문항 생성", type="primary"):
        if engine:
            # API 키가 초기값인지 확인
            if "your_actual_api_key_here" in str(st.secrets.get("GEMINI_API_KEY", "")):
                st.warning("⚠️ `.streamlit/secrets.toml` 파일에 실제 Gemini API 키를 입력해주세요.")
            else:
                with st.spinner("문제를 생성 중입니다..."):
                    result = engine.generate_question(region, topic)
                    if result.startswith("❌") or result.startswith("⚠️"):
                        st.error(result)
                    else:
                        st.session_state.question = result
                        st.session_state.evaluation = None
        else:
            st.error("먼저 API 키를 입력해주세요.")

# 메인 레이아웃: 좌우 분할
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='section-header'>📍 면접 문항</div>", unsafe_allow_html=True)
    if st.session_state.question:
        st.markdown(f"<div class='report-card'>{st.session_state.question}</div>", unsafe_allow_html=True)
    else:
        st.info("왼쪽 사이드바에서 '새 문항 생성' 버튼을 눌러주세요.")

with col2:
    st.markdown("<div class='section-header'>✍️ 답변 입력</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["텍스트 입력", "음성 녹음"])
    
    with tab1:
        answer_text = st.text_area("답변을 입력하세요", height=250, placeholder="여기에 답변을 작성하거나 음성 보드를 이용하세요.")
    
    with tab2:
        st.write("마이크 버튼을 눌러 답변을 녹음하세요.")
        audio_response = mic_recorder(
            start_prompt="🔴 녹음 시작",
            stop_prompt="⏹️ 녹음 중지",
            key='recorder'
        )
        
        if audio_response:
            st.audio(audio_response['bytes'])
            st.info("음성 인식을 위해서는 Gemini API의 오디오 분석 기능을 사용합니다. '평가하기' 버튼을 누르면 처리가 시작됩니다.")

    if st.button("🔍 평가하기", use_container_width=True):
        if not st.session_state.question:
            st.error("문제가 없습니다. 먼저 문제를 생성해주세요.")
        elif not engine:
            st.error("API 키가 필요합니다.")
        else:
            target_answer = answer_text
            # 음성 데이터가 있는 경우 (간이 처리: 실제 구현 시 bytes 전달 필요)
            # 여기서는 텍스트 우선, 음성 지원 안내만 포함
            with st.spinner("AI가 답변을 분석 중입니다..."):
                result = engine.evaluate_answer(st.session_state.question, target_answer)
                if result.startswith("❌") or result.startswith("⚠️"):
                    st.error(result)
                else:
                    st.session_state.evaluation = result

# 결과 대시보드
if st.session_state.evaluation:
    st.divider()
    st.markdown("<h2 style='color: #003366;'>📊 분석 결과 리포트</h2>", unsafe_allow_html=True)
    
    eval_text = st.session_state.evaluation
    
    # 간단한 파싱 (Level 추출 등)
    level = "N/A"
    if "Level:" in eval_text:
        level = eval_text.split("Level:")[1].split("\n")[0].strip()
    
    st.markdown(f"<div class='level-badge'>평가 등급: {level}</div>", unsafe_allow_html=True)
    
    with st.expander("📝 상세 피드백 보기", expanded=True):
        st.markdown(f"<div class='report-card'>{eval_text}</div>", unsafe_allow_html=True)
        
    st.success("등급이 낮다면 아래의 'Recommended Revision'을 참고하여 답변을 보완해보세요!")
