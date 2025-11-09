# hermite_wavefunction_with_normalization.py
# ─────────────────────────────────────────────
import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.cm import get_cmap
from matplotlib import font_manager

# ─────────────────────────────────────────────
def set_font():
    available_fonts = [f.name for f in font_manager.fontManager.ttflist]

    if "Malgun Gothic" in available_fonts:
        base_font = "Malgun Gothic"
    elif "AppleGothic" in available_fonts:
        base_font = "AppleGothic"
    else:
        base_font = "NanumGothic"

    plt.rcParams.update({
        "text.usetex": False,             # LaTeX 미사용
        "font.family": base_font,         # 한글 표시용
        "axes.unicode_minus": False,
        "mathtext.fontset": "stix",       # ✅ STIX 폰트로 수식 전용 폰트 변경
        "mathtext.rm": "serif",
        "mathtext.it": "serif:italic",
        "mathtext.bf": "serif:bold",
        "font.size": 11,
    })
    matplotlib.rcParams["figure.dpi"] = 150

set_font()

# ─────────────────────────────────────────────
st.set_page_config(page_title="Hermite Wavefunction Normalization", layout="centered")
st.title("🎓 Hermite 다항식으로부터 조화진동자 파동함수 도출 및 정규화")
st.caption("Hermite 미분방정식 → 양자화 조건 → ψₙ(y) 정규화 및 에너지 준위 시각화")

st.divider()

# ─────────────────────────────────────────────
st.header("1️⃣ 수학적 다항식에서 물리적 파동함수로")

st.markdown(r"""
이전 단계에서 Hermite 미분방정식으로부터  
**양자화 조건** \(\lambda = 2n\) 과 **Hermite 다항식 \(H_n(y)\)** 를 얻었다.  

하지만 실제 물리적으로 의미 있는 것은 입자의 **파동함수 \(\psi_n(y)\)** 이다.  
이 파동함수는 공간 내 확률 분포를 기술한다.

---

📘 **조화진동자 해의 구조**

$$
\psi_n(y) = N_n\, H_n(y)\, e^{-y^2/2}
$$

- \(H_n(y)\): Hermite 다항식 — 파동의 진동 형태 결정  
- \(e^{-y^2/2}\): 가우시안 감쇠 항 — 국소화  
- \(N_n\): 정규화 상수 — 확률 총합(=1) 보장  
""")

# ─────────────────────────────────────────────
st.header("2️⃣ 정규화 조건 — 확률 총합이 1이 되도록")

st.markdown(r"""
파동함수는 확률 진폭이므로 전체 확률은 항상 1이어야 한다.

$$
\int_{-\infty}^{\infty} |\psi_n(y)|^2\,dy = 1
$$

Hermite 다항식의 직교성 관계로부터,

$$
\int_{-\infty}^{\infty} H_n(y)H_m(y)e^{-y^2}\,dy = 2^n n!\sqrt{\pi}\,\delta_{nm}
$$

따라서,

$$
N_n = \frac{1}{\sqrt{2^n n! \sqrt{\pi}}}
$$
""")

st.info("Hermite 다항식은 정규화되어 있지 않으며, "
        "이 상수를 곱해야 실제 확률 조건(∫|ψ|²=1)을 만족한다.")

# ─────────────────────────────────────────────
st.header("3️⃣ 정규화 검증 — 기본상태 ψ₀(y)")

y = sp.Symbol("y", real=True)
psi0 = (1/sp.sqrt(sp.sqrt(sp.pi))) * sp.exp(-y**2/2)
integral_check = sp.integrate(psi0**2, (y, -sp.oo, sp.oo))

st.latex(
    r"\int_{-\infty}^{\infty} |\psi_0(y)|^2\,dy = " + sp.latex(sp.simplify(integral_check))
)
st.caption("결과적으로 1이 되어, ψ₀(y)는 완벽히 정규화되어 있음을 확인할 수 있다.")

# ─── 시각화: |ψ₀|² 확률밀도
ys = np.linspace(-4, 4, 400)
psi0_func = np.exp(-ys**2 / 2) / (np.pi ** 0.25)
density = psi0_func**2

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(ys, density, color="navy", lw=2, label=r"$|\psi_0(y)|^2$")
ax.fill_between(ys, density, color="royalblue", alpha=0.3)
ax.set_title("기본상태 확률밀도 |ψ₀(y)|² (면적=1)", fontsize=13)
ax.set_xlabel("y (무차원 좌표)")
ax.set_ylabel("확률밀도")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig)

# ─────────────────────────────────────────────
st.header("4️⃣ 정규화된 파동함수 ψₙ(y) 자동 계산 (n=0~9)")

psi_exprs = []
for n in range(10):
    Hn = sp.hermite(n, y)
    Nn = 1/sp.sqrt(2**n * sp.factorial(n) * sp.sqrt(sp.pi))
    psi_n = sp.simplify(Nn * Hn * sp.exp(-y**2/2))
    psi_exprs.append(psi_n)

rows = []
for n, psi in enumerate(psi_exprs):
    latex_expr = sp.latex(psi).replace(r"\mathrm{e}", "e").replace(r"\left", "").replace(r"\right", "")
    rows.append(f"| {n} | $\\psi_{{{n}}}(y)={latex_expr}$ |")

table_md = "| n | 정규화된 파동함수 ψₙ(y) |\n|:-:|:--|\n" + "\n".join(rows)
with st.expander("정규화된 파동함수 ψₙ(y) 보기 (n=0~9)"):
    st.markdown(table_md, unsafe_allow_html=True)
st.caption("각 ψₙ(y)는 서로 직교하며, ∫ψₙψₘ dy = δₙₘ을 만족한다.")

# ─────────────────────────────────────────────
st.header("5️⃣ 조화진동자 퍼텐셜과 파동함수 시각화 (에너지 스케일 적용)")

st.markdown(r"""
조화진동자 퍼텐셜과 에너지 준위는 다음과 같다:

$$
V(y) = \frac{1}{2}m\omega^2y^2,\qquad
E_n = \left(n + \frac{1}{2}\right)\hbar\omega
$$

여기서는 \(m = \hbar = 1\) 로 두고, \(\omega = 2\) 로 설정하여  
단위 없는 무차원 형태로 표현한다.
""")

ħ = 1.0
ω = 2.0
m = 1.0
ys = np.linspace(-4, 4, 600)
V = 0.5 * m * ω**2 * ys**2

# ──────────────── [Figure 1: ψₙ(y)] ────────────────
fig1, ax1 = plt.subplots(figsize=(9, 6), facecolor="#fafafa")
ax1.plot(ys, V, color="red", lw=2.5, label="퍼텐셜 V(y)=½y²")
cmap = get_cmap("viridis")
scale_factor = 1.2

for n in range(10):
    f = sp.lambdify(y, psi_exprs[n], "numpy")
    psi_y = f(ys)
    E_n = (n + 0.5) * ħ * ω
    color = cmap(n / 10)
    ax1.plot(ys, psi_y * scale_factor + E_n, color=color, lw=1.8, alpha=0.85, label=f"n={n}")
    ax1.axhline(E_n, color="gray", linestyle="--", lw=0.6, alpha=0.4)

ax1.set_xlim(-4, 4)
ax1.set_ylim(-0.5, 15)
ax1.set_xlabel("y (무차원 위치)")
ax1.set_ylabel("에너지 Eₙ = (n+½)ħω")
ax1.set_title("정규화된 파동함수 ψₙ(y) — 조화진동자 퍼텐셜 위", fontsize=14, fontweight="bold", pad=10)
ax1.grid(True, linestyle="--", alpha=0.4)
ax1.axvline(0, color="black", lw=1)
ax1.legend(loc="upper right", ncol=2, fontsize=8)
st.pyplot(fig1)

# ──────────────── [Figure 2: |ψₙ(y)|²] ────────────────
fig2, ax2 = plt.subplots(figsize=(9, 6), facecolor="#fafafa")
ax2.plot(ys, V, color="red", lw=2.5, label="퍼텐셜 V(y)=½y²")

for n in range(10):
    f = sp.lambdify(y, psi_exprs[n], "numpy")
    psi_y = f(ys)
    prob = psi_y**2
    E_n = (n + 0.5) * ħ * ω
    color = cmap(n / 10)
    ax2.plot(ys, prob * 3 + E_n, color=color, lw=1.8, alpha=0.75)
    ax2.axhline(E_n, color="gray", linestyle="--", lw=0.6, alpha=0.3)

ax2.set_xlim(-4, 4)
ax2.set_ylim(-0.5, 15)
ax2.set_xlabel("y (무차원 위치)")
ax2.set_ylabel("에너지 Eₙ = (n+½)ħω")
ax2.set_title("|ψ_n(y)|² — 에너지 준위별 공간 확률 분포", fontsize=14, fontweight="bold", pad=10)
ax2.grid(True, linestyle="--", alpha=0.4)
ax2.axvline(0, color="black", lw=1)
st.pyplot(fig2)

# ─────────────────────────────────────────────
st.markdown(r"""
📘 **그래프 해석 요약**

- ψₙ(y): 파동함수의 위상 구조 (진폭, 노드 수)
- |ψₙ(y)|²: 입자의 존재 확률 분포
- 빨강선: 퍼텐셜 V(y)
- 회색 점선: 각 에너지 준위 Eₙ
- 색상 구분: n값에 따른 고유 파동함수

🎯 결론적으로, Hermite 다항식으로부터 유도된 ψₙ(y)는  
양자 조화진동자의 실제 물리적 상태를 정확히 기술하며,  
에너지 준위별로 파동의 공간 확률 분포를 시각적으로 보여준다.
""")

