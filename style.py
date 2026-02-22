import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Noto+Sans+KR', sans-serif;
        }
        
        .main {
            background-color: #f8f9fa;
        }
        
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            height: 2.5em;
            background-color: #003366;
            color: white;
            font-weight: bold;
            border: none;
            transition: 0.3s;
        }
        
        .stButton>button:hover {
            background-color: #004080;
            border: none;
            color: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .report-card {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            border-left: 5px solid #003366;
        }
        
        .level-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            background-color: #003366;
            color: white;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .section-header {
            color: #003366;
            font-weight: bold;
            margin-top: 15px;
            margin-bottom: 5px;
            border-bottom: 1px solid #eee;
        }
        
        .policy-keyword {
            background-color: #e3f2fd;
            color: #0d47a1;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)
