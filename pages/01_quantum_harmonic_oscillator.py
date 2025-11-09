# quantum_harmonic_oscillator.py
import streamlit as st
import logging
from tqdm import tqdm
import time

# ─────────────────────────────────────────────
# Logging 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler("qho_solver.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
st.set_page_config(page_title="Quantum Harmonic Oscillator", layout="centered")

st.title("🧩 Quantum Harmonic Oscillator (QHO)")
st.caption("1단계: 슈뢰딩거 방정식의 미분방정식 형태 전개")

st.divider()

# ─────────────────────────────────────────────
sections = [
    "1️⃣ 슈뢰딩거 방정식",
    "2️⃣ 무차원화 (Dimensionless Substitution)",
    "3️⃣ 큰 y에서의 해 근사",
    "4️⃣ Hermite 방정식 도출",
    "5️⃣ 에너지 고유값과 고유함수",
    "📘 전체 요약",
]

for step in tqdm(sections, desc="Rendering Sections"):
    logger.info(f"Rendering section: {step}")
    time.sleep(0.3)

# ─────────────────────────────────────────────
with st.expander("1️⃣ 슈뢰딩거 방정식"):
    st.markdown("조화 진동자의 퍼텐셜 에너지는 다음과 같습니다:")
    st.latex(r"V(x) = \frac{1}{2} k x^2")

    st.markdown("시간에 무관한 슈뢰딩거 방정식은 다음과 같습니다:")
    st.latex(
        r"-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2} + \frac{1}{2}kx^2\psi = E\psi"
    )
    st.markdown("여기서:")
    st.latex(r"\omega = \sqrt{\frac{k}{m}}")

# ─────────────────────────────────────────────
with st.expander("2️⃣ 무차원화 (Dimensionless Substitution)"):
    st.markdown("새로운 변수를 도입합니다:")
    st.latex(r"y = \sqrt{\frac{m\omega}{\hbar}}x, \quad \alpha = \frac{2E}{\hbar \omega}")

    st.markdown("미분 항 변환:")
    st.latex(r"\frac{d}{dx} = \sqrt{\frac{m\omega}{\hbar}}\frac{d}{dy}")
    st.latex(r"\frac{d^2}{dx^2} = \frac{m\omega}{\hbar}\frac{d^2}{dy^2}")

    st.markdown("대입하면 표준형 식을 얻습니다:")
    st.latex(r"\frac{d^2\psi}{dy^2} + (\alpha - y^2)\psi = 0")

# ─────────────────────────────────────────────
with st.expander("3️⃣ 큰 y에서의 해 근사"):
    st.markdown("큰 y에 대해 \(y^2\psi\)항이 우세하므로:")
    st.latex(r"\frac{d^2\psi}{dy^2} - y^2\psi = 0")
    st.markdown("따라서 해의 형태는:")
    st.latex(r"\psi \sim e^{\pm \frac{1}{2}y^2}")
    st.markdown("정규화 가능한 해만 남기면:")
    st.latex(r"\psi(y) \sim e^{-\frac{1}{2}y^2}")

# ─────────────────────────────────────────────
with st.expander("4️⃣ Hermite 방정식 도출"):
    st.markdown("새로운 함수 \(H(y)\)를 정의합니다:")
    st.latex(r"\psi(y) = H(y)e^{-\frac{1}{2}y^2}")

    st.markdown("이를 원래 방정식에 대입하면 Hermite 미분방정식이 됩니다:")
    st.latex(r"H'' - 2yH' + (\alpha - 1)H = 0")

    st.markdown("Hermite 표준형과 비교하면:")
    st.latex(r"H'' - 2yH' + 2nH = 0")
    st.latex(r"\Rightarrow \alpha - 1 = 2n")

# ─────────────────────────────────────────────
with st.expander("5️⃣ 에너지 고유값과 고유함수"):
    st.markdown("에너지 양자화 조건은 다음과 같습니다:")
    st.latex(r"\alpha = 2n + 1")
    st.latex(r"E_n = \left(n + \frac{1}{2}\right)\hbar\omega")

    st.markdown("고유함수는 다음과 같습니다:")
    st.latex(r"\psi_n(y) = N_n\,H_n(y)e^{-\frac{1}{2}y^2}")
    st.markdown("Hermite 다항식의 정의:")
    st.latex(r"H_n(y) = (-1)^n e^{y^2}\frac{d^n}{dy^n}(e^{-y^2})")

# ─────────────────────────────────────────────
with st.expander("📘 전체 요약"):
    st.table(
        {
            "단계": [
                "1. 원래 식",
                "2. 무차원화",
                "3. 표준형",
                "4. Hermite 방정식",
                "5. 에너지/고유함수",
            ],
            "수식": [
                r"-\frac{\hbar^2}{2m}\psi'' + \frac{1}{2}kx^2\psi = E\psi",
                r"y=\sqrt{\frac{m\omega}{\hbar}}x,\quad \alpha=\frac{2E}{\hbar\omega}",
                r"\psi'' + (\alpha - y^2)\psi=0",
                r"H'' - 2yH' + (\alpha-1)H=0",
                r"E_n=(n+\frac{1}{2})\hbar\omega,\quad \psi_n=N_nH_n e^{-\frac{1}{2}y^2}",
            ],
        }
    )

