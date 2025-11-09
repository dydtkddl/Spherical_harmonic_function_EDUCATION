# -*- coding: utf-8 -*-
"""
조화진동자 대응원리 인과관계 시각화 (x₀ 확장 설명 포함)
────────────────────────────────────────────
• Classical vs Quantum Probability
• Plotly 인터랙티브 시각화
• n 증가에 따른 x₀ 확장 인과관계 해설
"""

import streamlit as st
import numpy as np
import math
import plotly.graph_objects as go
from scipy.special import eval_hermite
from matplotlib import font_manager

# ─────────────────────────────────────────────
# ✅ 한글 + LaTeX 폰트 설정
def set_font():
    import matplotlib.pyplot as plt
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["mathtext.fontset"] = "stix"
    available_fonts = [f.name for f in font_manager.fontManager.ttflist]
    if "Malgun Gothic" in available_fonts:
        plt.rcParams["font.family"] = "Malgun Gothic"
    elif "AppleGothic" in available_fonts:
        plt.rcParams["font.family"] = "AppleGothic"
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"
set_font()

# ─────────────────────────────────────────────
st.set_page_config(page_title="조화진동자 대응원리", layout="wide")
st.title("⚛️ 조화진동자 & 대응원리 (Quantum–Classical Correspondence)")
st.caption("양자 확률밀도 |ψₙ(x)|²가 고전 확률밀도 P(x)로 수렴하는 과정을 시각·이론적으로 해석")

ħ, m, ω = 1.0, 1.0, 1.0
np.seterr(all="ignore")

# ─────────────────────────────────────────────
# ✅ 파동함수 계산 함수 (고속 캐시)
@st.cache_data(show_spinner=False)
def compute_probabilities(n, ħ, m, ω, x0):
    xv = np.linspace(-1.2*x0, 1.2*x0, 1500)

    # Classical Probability
    P_classical = np.zeros_like(xv)
    mask = np.abs(xv) <= x0
    P_classical[mask] = 1 / (np.pi * np.sqrt(x0**2 - xv[mask]**2))
    P_classical /= np.trapz(P_classical, xv)

    # Quantum Probability (작은 n)
    if n <= 500:
        Nn = (m*ω/(np.pi*ħ))**0.25 / np.sqrt(2.0**n * math.factorial(n))
        ψ = Nn * eval_hermite(n, np.sqrt(m*ω/ħ) * xv) * np.exp(-m*ω*xv**2 / (2*ħ))
        ψ2 = np.abs(ψ)**2
        ψ2 /= np.trapz(ψ2, xv)
    else:
        # n이 매우 클 경우 근사적으로 classical 분포로 전환
        ψ2 = P_classical.copy()

    return xv, ψ2, P_classical

# ─────────────────────────────────────────────
# 수식 표시
st.markdown(r"""
**고전 확률밀도:**  
$$
P(x) = \frac{1}{\pi\sqrt{x_0^2 - x^2}},\quad |x|\le x_0
$$  

**양자 확률밀도:**  
$$
|\psi_n(x)|^2 =
\left|
\frac{1}{\sqrt{2^n n!}}
\left(\frac{m\omega}{\pi\hbar}\right)^{1/4}
H_n\!\left(\sqrt{\frac{m\omega}{\hbar}}x\right)
e^{-\frac{m\omega x^2}{2\hbar}}
\right|^2
$$  

이때 \(n \to \infty\) 일수록,  
$$
|\psi_n(x)|^2 \approx P(x)
$$
으로 수렴한다.
""")

# ─────────────────────────────────────────────
st.markdown("### 🎚️ 양자수 조절")
col_slider, col_buttons = st.columns([3, 2])

with col_slider:
    n = st.slider("세밀 조정 (1~100)", 1, 100, 10)
with col_buttons:
    st.write("**큰 n 선택 (극한 근사)**")
    c1, c2, c3 = st.columns(3)
    if c1.button("n = 1000"):
        n = 1000
    if c2.button("n = 10000"):
        n = 10000
    if c3.button("n = 100000"):
        n = 100000

# 고전 진폭 (x₀)
x0 = np.sqrt(2*(n+0.5)*ħ/(m*ω))
st.markdown(f"현재 선택된 양자수: **n = {n}**,  고전 진폭: **x₀ = {x0:.3f}**")

# 계산
xv, ψ2, P_classical = compute_probabilities(n, ħ, m, ω, x0)

# ─────────────────────────────────────────────
# Plotly 그래프
fig = go.Figure()

# Classical 영역 강조 (±x₀)
fig.add_vrect(
    x0=-x0, x1=x0,
    fillcolor="lightgray", opacity=0.2, line_width=0,
    annotation_text="고전적으로 허용된 영역 (±x₀)",
    annotation_position="top left"
)

# Quantum
fig.add_trace(go.Scatter(
    x=xv, y=ψ2, mode="lines",
    line=dict(color="royalblue", width=3),
    name=f"|ψₙ|² (n={n})"
))
# Classical
fig.add_trace(go.Scatter(
    x=xv, y=P_classical, mode="lines",
    line=dict(color="red", width=3, dash="dot"),
    name="고전확률 P(x)"
))

# y축 제한 및 설정
fig.update_layout(
    title=f"조화진동자 대응원리 — Quantum vs Classical (n={n})",
    xaxis_title="x (무차원)",
    yaxis_title="확률밀도",
    yaxis=dict(range=[0, 0.7]),
    template="plotly_white",
    font=dict(size=15),
    legend=dict(x=0.02, y=0.98),
    margin=dict(t=60, l=20, r=20, b=40),
)

st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
st.divider()
st.header("📖 단계별 인과관계 해설")

with st.expander("1️⃣ 왜 양자수가 커질수록 x₀(진폭)이 달라지는가?"):
    st.markdown(r"""
조화진동자의 에너지 준위는  
$$
E_n = \hbar \omega \left( n + \frac{1}{2} \right)
$$  
으로 \(n\)이 커질수록 에너지가 증가한다.

고전적으로 입자가 도달할 수 있는 최대 변위 \(x_0\)는  
$$
E_n = \frac{1}{2}m\omega^2 x_0^2
\Rightarrow
x_0 = \sqrt{\frac{2E_n}{m\omega^2}} 
= \sqrt{\frac{2\hbar}{m\omega}\left(n + \frac{1}{2}\right)}
$$  
따라서  
\[
x_0 \propto \sqrt{n}
\]
즉, 양자수가 커질수록 입자가 ‘더 넓은 공간에서 진동’하게 되고  
파동함수의 확률밀도 역시 더 멀리까지 퍼지게 된다.
""")

with st.expander("2️⃣ 고전 조화진동자의 확률밀도는 왜 이런 형태인가?"):
    st.markdown(r"""
입자는 진폭 \(x_0\) 사이를 왕복 운동한다.  
속도 \(v(x) = \omega\sqrt{x_0^2 - x^2}\) 이므로,  
속도가 느린 구간(끝점)에 더 오래 머문다 → 확률 ↑.  

결국,
$$
P(x) = \frac{1}{\pi\sqrt{x_0^2 - x^2}},\quad |x|\le x_0
$$
중심에서는 빠르게 지나가므로 확률이 작고, 끝점에서는 발산형으로 높다.
""")

with st.expander("3️⃣ 양자 확률밀도는 어떻게 생기는가?"):
    st.markdown(r"""
양자역학에서는 입자의 상태가 **파동함수 \(\psi_n(x)\)** 로 표현된다:
$$
\left[-\frac{\hbar^2}{2m}\frac{d^2}{dx^2} + \frac{1}{2}m\omega^2x^2\right]\psi_n = E_n\psi_n
$$

해는 Hermite 다항식으로 주어지며,
$$
\psi_n(x) = 
\frac{1}{\sqrt{2^n n!}}\left(\frac{m\omega}{\pi\hbar}\right)^{1/4}
H_n\!\left(\sqrt{\frac{m\omega}{\hbar}}x\right)
e^{-\frac{m\omega x^2}{2\hbar}}
$$

여기서 \(H_n(x)\)는 파동의 진동 형태를,  
가우시안 \(e^{-x^2/2}\)는 감쇠를 결정한다.
""")

with st.expander("4️⃣ 왜 n이 커질수록 고전확률에 수렴하는가? (보어의 대응원리)"):
    st.markdown(r"""
n이 커질수록 파동의 노드(진동)가 많아지고,  
\(|\psi_n|^2\)의 세밀한 진동은 평균적으로 \(P(x)\)와 같은 형태로 분포한다.

즉, 빠른 진동의 평균 확률이 **고전적 체류시간 분포**와 같아진다:
$$
\lim_{n\to\infty} |\psi_n(x)|^2 = P(x)
$$
""")

with st.expander("5️⃣ 물리적 해석 요약"):
    st.markdown(r"""
| 구분 | 고전 확률밀도 \(P(x)\) | 양자 확률밀도 \(|\psi_n(x)|^2\) |
|:--:|:--|:--|
| 정의 | 시간체류 확률 | 파동함수 제곱 |
| 중심부 | 속도 빠름 → 확률 작음 | 파동 진폭 작음 |
| 끝점부 | 속도 느림 → 확률 큼 | 평균 확률 큼 |
| 형태 | 부드러운 곡선 | 진동 + 감쇠 |
| \(n \to \infty\) | — | 평균이 \(P(x)\)에 수렴 |

즉, 둘 다 "입자가 어디에 오래 존재하는가"를 표현하며,  
양자확률이 고전확률로 부드럽게 이어지는 것이 바로 **대응원리**이다.
""")

