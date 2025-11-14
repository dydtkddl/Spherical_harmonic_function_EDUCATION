# -*- coding: utf-8 -*-
"""
⚛️ QEq (전하 평형화, Charge Equilibration) — 이론적 설명 및 시각화
─────────────────────────────────────────────
ReaxFF에서 전하는 매 시뮬레이션 스텝마다 주변 환경에 따라 스스로 재분배된다.
이 앱은 그 과정을 지배하는 QEq(Charge Equilibration) 알고리즘의
물리적 인과관계, 제약 조건(라그랑주 승수), 그리고 평형의 의미를 시각적으로 보여준다.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────────
st.set_page_config(page_title="QEq 전하 평형화 시각화", layout="wide")
st.title("⚛️ QEq (Charge Equilibration) — 전하 평형화의 물리적 메커니즘과 시각화")

st.markdown("""
**QEq(Charge Equilibration)** 알고리즘은 **ReaxFF** 반응형 포스필드의 근본이 되는 전하 모델이다.  
결합이 생성되거나 끊어질 때마다 각 원자의 **부분 전하(Partial charge)** 가  
주변 환경에 맞게 실시간으로 조정되며, 시스템 전체의 **화학 퍼텐셜이 평형**을 이루는 상태로 수렴한다.  
이 평형 조건은 단순한 수학적 해가 아니라, **전자 이동이 멈춘 물리적 안정 상태**를 뜻한다.
""")

# ─────────────────────────────────────────────
# 이론적 배경
# ─────────────────────────────────────────────
st.markdown("""
전자 분포의 조정은 통계적 현상이 아니라, **에너지 최소화 원리**의 결과다.  
시스템의 총 전기적 에너지는 각 원자의 **전기음성도(χ)**, **자기 경질도(J)**,  
그리고 원자 간의 **쿨롱 상호작용(1/R)** 에 의해 결정된다.
""")

st.latex(r"""
E(\{q_i\}) =
\sum_i \left( \chi_i q_i + \frac{1}{2} J_i q_i^2 \right)
+ \frac{1}{2} \sum_{i \neq j} \frac{q_i q_j}{R_{ij}}
""")

st.markdown("""
- **전기음성도(χ)** 는 전자를 끌어당기려는 경향을 나타낸다.  
  값이 클수록 전자를 강하게 유인하므로, 평형 시 음전하를 띤다.  

- **자기 경질도(J)** 는 전하 변형에 대한 ‘저항’을 뜻한다.  
  전하가 바뀌려면 그만큼 에너지가 필요하다.  
  즉, J가 클수록 전하 이동이 어렵고, J가 작으면 전하 재분포가 쉽게 일어난다.  

이 두 항은 서로 대립한다 —  
χ는 “전하 이동을 유도하는 힘”, J는 “전하 이동을 억제하는 힘”이다.  
QEq는 바로 이 두 힘의 균형점을 찾는 과정이다.
""")

# ─────────────────────────────────────────────
# 라그랑주 승수법과 평형 조건
# ─────────────────────────────────────────────
st.markdown("""
전하의 재분포는 아무렇게나 일어날 수 없다.  
시스템의 전체 전하 \\( Q_{\\text{total}} = \sum_i q_i \\) 은 항상 보존되어야 한다.  
이 제약조건을 포함한 에너지 최소화 문제는 다음과 같은 **라그랑주 승수법(Lagrange multipliers)** 으로 정의된다.
""")

st.latex(r"""
L(\{q_i\}, \lambda)
= E(\{q_i\}) - \lambda \left( \sum_i q_i - Q_{\text{total}} \right)
""")

st.markdown("""
여기서 λ는 **라그랑주 승수(Lagrange multiplier)** 로,  
“총 전하 보존”이라는 제약을 만족시키면서 에너지를 최소화하도록 도와주는 항이다.  

이제 이를 최소화하려면 다음 조건을 동시에 만족해야 한다:
""")

st.latex(r"""
\frac{\partial L}{\partial q_i} = 0,
\quad
\frac{\partial L}{\partial \lambda} = 0
""")

st.markdown("""
이때 첫 번째 조건을 전개하면
""")

st.latex(r"""
\frac{\partial L}{\partial q_i}
= \frac{\partial E}{\partial q_i} - \lambda = 0
\quad \Rightarrow \quad
\frac{\partial E}{\partial q_i} = \lambda
""")

st.markdown("""
즉, 각 원자의 국소적인 화학 퍼텐셜(∂E/∂q_i)이 모두 λ와 같아져야 한다.  
두 번째 조건은 전체 전하 보존을 보장한다:
""")

st.latex(r"""
\sum_i q_i = Q_{\text{total}}
""")

st.markdown("""
따라서 λ는 단순한 수학적 상수가 아니라,  
모든 원자가 공유하는 **공통 화학 퍼텐셜(chemical potential)** 로서  
시스템 전체가 더 이상 전자를 교환하지 않는 상태를 의미한다.
""")

st.markdown("""
다시 말해,  
> 전기화학 퍼텐셜이 다른 원자들 사이에서는 전자가 이동하지만,  
> 모든 원자의 퍼텐셜이 동일해지면 더 이상 전하 이동이 일어나지 않는다.  
> 이때의 공통 퍼텐셜 λ가 바로 평형을 규정하는 지표다.
""")

st.markdown("""
이를 선형 방정식으로 표현하면 다음과 같다:
""")

st.latex(r"""
\chi_i + J_i q_i + \sum_{j \neq i} \frac{q_j}{R_{ij}} = \lambda
""")

st.markdown("""
즉, 각 원자의 전하 \\(q_i\\)는 χ, J, 그리고 이웃 원자들의 상호작용(1/R)에 의해 조정되어  
λ이라는 하나의 공통 평형 퍼텐셜에 맞춰진다.  
이것이 바로 QEq의 본질이다.
""")

# ─────────────────────────────────────────────
# QEq 계산 함수
# ─────────────────────────────────────────────
def solve_qeq(chi, J, R, Q_total=0.0):
    N = len(chi)
    A = np.zeros((N + 1, N + 1))
    b = np.zeros(N + 1)

    for i in range(N):
        for j in range(N):
            A[i, j] = J[i] if i == j else 1.0 / R[i, j]
        A[i, -1] = 1.0
        A[-1, i] = 1.0
        b[i] = -chi[i]
    b[-1] = Q_total

    q_lambda = np.linalg.solve(A, b)
    return q_lambda[:-1], q_lambda[-1]

# ─────────────────────────────────────────────
# 사용자 입력
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader("변수 설정 및 계산")

col1, col2 = st.columns(2)
N = col1.slider("원자 개수", 2, 4, 3)

chi = np.array([col1.slider(f"χ{i+1} (전기음성도)", -5.0, 5.0, val, 0.1)
                for i, val in enumerate(np.linspace(-1, 1, N))])
J = np.array([col2.slider(f"J{i+1} (자기 경질도)", 0.1, 10.0, 5.0, 0.1)
              for i in range(N)])

# 거리 행렬
R = np.ones((N, N))
for i in range(N):
    for j in range(N):
        if i != j:
            R[i, j] = np.abs(i - j) + 1.0

Q_total = st.number_input("총 전하 Q_total", value=0.0, step=0.1)

q, lam = solve_qeq(chi, J, R, Q_total)

st.markdown("""
**계산 결과:**  
각 원자의 전하는 다음과 같이 평형화된다.  
λ은 모든 원자가 공유하는 공통 화학 퍼텐셜(전기화학 평형점)을 나타낸다.
""")
st.write({f"원자 {i+1}": round(qi, 4) for i, qi in enumerate(q)})
st.write(f"λ (공통 화학 퍼텐셜): {lam:.4f}")

# ─────────────────────────────────────────────
# 전하 재분포 시각화
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader("전하 재분포 시각화")

st.markdown("""
전기음성도가 높은 원자는 전자를 끌어당겨 음전하를,  
전기음성도가 낮은 원자는 상대적으로 양전하를 띠게 된다.  
막대의 색상은 전하의 부호를, 높이는 전하의 크기를 나타낸다.
""")

fig, ax = plt.subplots(figsize=(7, 4))
normed = (q - min(q)) / (max(q) - min(q) + 1e-6)
colors = plt.cm.coolwarm(normed)
ax.bar(range(1, N + 1), q, color=colors, edgecolor='black')
ax.set_xlabel("원자 번호")
ax.set_ylabel("전하 (q_i)")
ax.set_title("전하 평형화 후 원자별 전하 분포")
st.pyplot(fig)

# ─────────────────────────────────────────────
# 에너지 곡선 시각화
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader("단일 원자의 전하–에너지 곡선")

st.markdown("""
각 원자의 에너지는 전기음성도와 경질도의 경쟁으로 결정된다.
""")

st.latex(r"""
E_i(q_i) = \chi_i q_i + \frac{1}{2} J_i q_i^2
""")

st.markdown("""
χ는 에너지의 기울기를, J는 곡률을 결정한다.  
χ가 크면 기울기가 커져 전자를 끌어당기며,  
J가 크면 곡선이 가팔라져 전하 이동이 어렵다.  
따라서 평형 전하는 χ/J 비율의 균형점에서 결정된다.
""")

q_space = np.linspace(-2, 2, 200)
fig2, ax2 = plt.subplots(figsize=(7, 4))
for i in range(N):
    E = chi[i] * q_space + 0.5 * J[i] * q_space ** 2
    ax2.plot(q_space, E, label=f'원자 {i+1}')
ax2.set_xlabel("시도 전하 q_i")
ax2.set_ylabel("에너지 E_i(q_i)")
ax2.set_title("각 원자의 에너지 곡선 (χ–J 상호작용)")
ax2.legend()
st.pyplot(fig2)

# ─────────────────────────────────────────────
# 물리적 해석 및 결론
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader("물리적 해석과 결론")

st.markdown("""
QEq에서의 λ는 단순한 수학적 상수가 아니라 **물리적 균형점(chemical potential equalization point)** 이다.  
전기음성도 χ가 큰 원자는 전자를 더 끌어당기려 하고,  
χ가 작은 원자는 전자를 잃으려 한다.  
이 전자 이동은 서로 다른 퍼텐셜(∂E/∂q_i) 간의 차이로 인해 발생하며,  
그 차이가 0이 되는 순간, 즉 모든 원자의 ∂E/∂q_i가 동일해질 때 전자 이동이 멈춘다.

이때의 공통 퍼텐셜이 λ이며, 이는 시스템 전체가 **전기적 평형 상태**에 도달했음을 의미한다.  
결국 QEq의 목표는 ‘모든 원자가 동일한 화학 퍼텐셜을 가지도록 전하를 재분배하는 것’이다.

이 모델은 선형 근사를 기반으로 하지만,  
실시간으로 결합 형성·파괴 중 전하 이동을 반영할 수 있다는 점에서  
ReaxFF의 반응성 시뮬레이션을 가능하게 만든 핵심 구성요소다.
""")

st.success("🔹 λ는 단순한 상수가 아니라 ‘전하 이동이 멈춘 상태를 규정하는 공통 화학 퍼텐셜’이며, QEq는 바로 그 λ를 찾아가는 알고리즘이다.")
