import streamlit as st

st.set_page_config(page_title="Quantum Harmonic Oscillator Suite", layout="centered")

st.title("🔷 Quantum Harmonic Oscillator Interactive Suite")
st.markdown("""
이 앱은 조화진동자 문제의 전 과정을 시각화합니다.  
아래 페이지를 선택해 단계별로 탐색하세요.
""")

st.divider()

st.subheader("📘 페이지 구성")
st.markdown("""
1️⃣ **Hermite Series Solution** — Hermite 미분방정식 해 유도 및 양자화 조건 도출  
2️⃣ **Quantum Harmonic Oscillator** — 고유값 문제 및 에너지 준위 시각화  
3️⃣ **Normalized Wavefunctions** — 정규화된 ψₙ(y)와 확률밀도 함수 시각화
""")
st.info("왼쪽 사이드바를 이용해 원하는 페이지로 이동하세요 👈")

st.caption("Developed by YongSang | Powered by Streamlit")
