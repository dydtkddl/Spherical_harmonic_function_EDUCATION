# -*- coding: utf-8 -*-
"""
2D Quantum Harmonic Oscillator Visualization
--------------------------------------------
단계:
1~6 : 수학적 유도
7   : 정규화
8   : 파동함수 확률밀도(|ψ|²) 3D 시각화 (Plotly)
"""

import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────
# ✅ 한글 + LaTeX 폰트 설정
def set_font():
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["mathtext.fontset"] = "dejavusans"
    plt.rcParams["font.size"] = 12
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    if "Malgun Gothic" in available_fonts:
        plt.rcParams["font.family"] = "Malgun Gothic"
    elif "AppleGothic" in available_fonts:
        plt.rcParams["font.family"] = "AppleGothic"
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"

set_font()

# ─────────────────────────────────────────────
st.set_page_config(page_title="2D 조화진동자 시각화", layout="wide")
st.title("🎓 2차원 양자 조화진동자 (2D Quantum Harmonic Oscillator)")
st.caption("Hermite 다항식 기반 파동함수 해석 및 확률밀도 시각화")

st.divider()
st.header("1️⃣~6️⃣ 수학적 배경 요약")

st.markdown(r"""
$$
H = -\frac{\hbar^2}{2m}\left(\frac{\partial^2}{\partial x^2}+\frac{\partial^2}{\partial y^2}\right)
+ \frac{1}{2}m\omega^2(x^2+y^2)
$$

$$
\Psi(x,y)=\psi_x(x)\psi_y(y), \quad
H_x\psi_x=E_x\psi_x,\quad H_y\psi_y=E_y\psi_y,\quad E=E_x+E_y
$$

각 축의 해는 1D 조화진동자의 해와 동일하다:
$$
\psi_n(x)=N_n e^{-\frac{m\omega x^2}{2\hbar}}H_n\left(\sqrt{\frac{m\omega}{\hbar}}x\right)
$$

따라서 2D 파동함수:
$$
\Psi_{n_x,n_y}(x,y)=N_{n_x,n_y}
e^{-\frac{m\omega(x^2+y^2)}{2\hbar}}
H_{n_x}\!\left(\sqrt{\frac{m\omega}{\hbar}}x\right)
H_{n_y}\!\left(\sqrt{\frac{m\omega}{\hbar}}y\right)
$$

$$
E_{n_x,n_y}=(n_x+n_y+1)\hbar\omega
$$
""")

# ─────────────────────────────────────────────
st.header("7️⃣ 정규화")

st.markdown(r"""
정규화 조건:
$$
\iint |\Psi_{n_x,n_y}(x,y)|^2 dx\,dy = 1
$$

Hermite 다항식의 직교성으로부터
$$
N_{n_x,n_y}=
\sqrt{\frac{1}{2^{n_x+n_y} n_x! n_y! \pi}}
\left(\frac{m\omega}{\hbar}\right)^{1/2}
$$
""")

# ─────────────────────────────────────────────
st.header("8️⃣ 시각화 — |ψₙₓₙᵧ(x,y)|² 3D 확률밀도")

ħ = 1.0
m = 1.0
ω = 1.0

nx = st.slider("nₓ (0~4)", 0, 4, 1)
ny = st.slider("nᵧ (0~4)", 0, 4, 1)

# 변수 및 파동함수 계산
x = sp.Symbol("x", real=True)
y = sp.Symbol("y", real=True)

ξx = sp.sqrt(m*ω/ħ)*x
ξy = sp.sqrt(m*ω/ħ)*y

Hx = sp.hermite(nx, ξx)
Hy = sp.hermite(ny, ξy)
N = sp.sqrt((m*ω/ħ)/(2**(nx+ny)*sp.factorial(nx)*sp.factorial(ny)*sp.pi))

Ψ_expr = N * sp.exp(-m*ω*(x**2+y**2)/(2*ħ)) * Hx * Hy
Ψ_func = sp.lambdify((x,y), Ψ_expr, "numpy")

# Grid 생성
X = np.linspace(-3, 3, 120)
Y = np.linspace(-3, 3, 120)
X, Y = np.meshgrid(X, Y)
Z = np.abs(Ψ_func(X, Y))**2

# ─────────────────────────────────────────────
# Plotly 3D Surface
fig = go.Figure()

fig.add_trace(go.Surface(
    x=X, y=Y, z=Z,
    colorscale="Viridis",
    contours={"z": {"show": True, "usecolormap": True, "highlightcolor": "limegreen"}},
    lighting=dict(ambient=0.7, diffuse=0.7, roughness=0.3, specular=0.4),
    opacity=0.95
))

fig.update_layout(
    title=f"2D 조화진동자 확률밀도 |Ψₙₓₙᵧ(x,y)|² (nₓ={nx}, nᵧ={ny})",
    scene=dict(
        xaxis_title="x (무차원)",
        yaxis_title="y (무차원)",
        zaxis_title="|ψ|²",
        xaxis=dict(showbackground=True, backgroundcolor="rgba(230,230,230,0.5)"),
        yaxis=dict(showbackground=True, backgroundcolor="rgba(230,230,230,0.5)"),
        zaxis=dict(showbackground=True, backgroundcolor="rgba(250,250,250,0.5)"),
    ),
    template="plotly_white",
    margin=dict(l=10, r=10, b=10, t=40)
)

st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
st.markdown(r"""
🎨 **시각화 해석**
- 높이(Z)는 확률밀도 \(|\Psi(x,y)|^2\)를 나타냄  
- 중심으로 갈수록 확률이 높음  
- nₓ, nᵧ가 커질수록 노드(진폭=0인 지점) 증가  
- 색상은 진폭의 공간적 변화를 시각적으로 표현

💡 슬라이더로 \(nₓ, nᵧ\) 값을 바꿔서 모드별 파동함수 형태를 직접 관찰하세요!
""")

