# -*- coding: utf-8 -*-
"""
Nose–Hoover Thermostat & Tdamp Visualization (LaTeX-safe)
────────────────────────────────────────────
• 완전 LaTeX-safe (raw string 처리)
• Plotly 시각화 포함
• 6문단 이상의 인과적 설명
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ─────────────────────────────────────────────
st.set_page_config(page_title="Nose–Hoover Thermostat", layout="wide")

st.title("🌡️ Nose–Hoover Thermostat & Temperature Damping Time (Tdamp)")

# ─────────────────────────────────────────────
st.markdown(r"""
### 1️⃣ 서론 — 온도 제어의 필요성  
분자동역학 시뮬레이션(MD)에서는 각 입자의 운동방정식만으로는 **미시계의 에너지가 일정**하게 유지됩니다.  
하지만 실험적 시스템은 열탕, 진공, 외부 환경 등과 에너지를 교환하며 온도를 일정하게 유지하죠.  
이를 모사하기 위해 ‘열저장소(heat bath)’를 모사하는 **온도 조절 장치(thermostat)** 가 필요합니다.  
그중 **Nose–Hoover thermostat**은 **에너지를 보존하면서도 평균적으로 목표 온도를 유지하는 대표적 방법**입니다.  

### 2️⃣ Nose–Hoover의 기본 아이디어  
기존의 단순한 속도 재스케일링 방법은 온도를 빠르게 맞추지만, 동역학의 자연스러움이 사라집니다.  
Nose–Hoover는 계(system)에 **가상의 자유도(ζ)** 를 도입하여, 입자 속도를 물리적으로 감쇠하거나 가속하는 방식으로 온도를 조절합니다.  
즉, 시스템이 너무 뜨거우면 ζ가 양의 값을 가져 속도를 줄이고, 너무 차가우면 음의 값을 가져 속도를 늘립니다.  
이 방식은 온도 조절이 “물리적으로 연속적”이기 때문에 canonical ensemble (NVT)을 자연스럽게 구현할 수 있습니다.  

### 3️⃣ Nose–Hoover 운동방정식  
가상의 변수 ζ(제어 변수)의 동역학은 다음과 같은 연립 방정식으로 기술됩니다:  

$$
m_i \frac{d^2 r_i}{dt^2} = F_i - \zeta m_i \frac{d r_i}{dt} \\
\frac{d\zeta}{dt} = \frac{1}{Q}\left(\sum_i \frac{m_i v_i^2}{k_B T} - g \right)
$$  

여기서 \(Q\)는 thermostat의 “관성 매개변수(thermal mass)”이며,  
\(g\)는 자유도의 수, 즉 3N을 의미합니다.  
\(\zeta\)는 마치 점성항처럼 작용하여 계의 속도를 온도 변화에 따라 부드럽게 조절합니다.  

### 4️⃣ Tdamp의 물리적 의미와 조정  
LAMMPS에서 사용되는 **Tdamp (temperature damping time)** 은 바로 이 \(Q\)와 관련이 있습니다.  
$$ Q \propto g k_B T \times (Tdamp)^2 $$  
Tdamp가 클수록 열저장소의 반응이 느려지고, 작을수록 빠르게 온도가 조정됩니다.  
즉, **Tdamp는 thermostat이 시스템의 에너지 진동을 얼마나 빠르게 완화할지 결정하는 시간 상수**입니다.  
너무 작으면 온도가 진동하며 비물리적, 너무 크면 평형에 도달하는 데 오래 걸립니다.  

### 5️⃣ 인과관계 — Tdamp와 온도 안정성  
Tdamp가 너무 작으면 thermostat이 강제로 속도를 조절하므로 실제 동역학이 왜곡됩니다.  
반면 너무 크면 시스템은 실제 목표 온도에 도달하지 못하고 진동하게 됩니다.  
따라서 **적절한 Tdamp는 시스템의 진동 주기보다 5~10배 이상 큰 값**으로 설정하는 것이 경험적으로 안정적입니다.  
이는 thermostat이 입자의 자연 진동보다 훨씬 느리게 작동해야 한다는 “시간 스케일 분리 원리”에 근거합니다.  

### 6️⃣ Nose–Hoover의 물리적 결과  
Nose–Hoover thermostat은 canonical ensemble의 분포함수를 만족시키며,  
평균 에너지는 다음과 같이 안정화됩니다:  
$$ \langle E \rangle = \frac{3}{2}Nk_B T $$.  
즉, thermostat은 열적 평형 상태에서 기대되는 평균 에너지를 정확히 재현합니다.  
따라서 Tdamp를 적절히 조정하면, 시뮬레이션이 물리적이며 부드럽게 수렴하고,  
온도 진동이 과도하지 않게 제어됩니다.  
""")

# ─────────────────────────────────────────────
# Tdamp effect visualization
st.markdown(r"### 🔬 Tdamp에 따른 온도 안정화 시뮬레이션 예시")

time = np.linspace(0, 10, 300)
T_target = 300

# 세 가지 Tdamp에 따른 가상의 온도 진동 모델
def temp_profile(t, Tdamp):
    return T_target + 40*np.exp(-t/Tdamp)*np.cos(6*np.pi*t/Tdamp)

Tdamp_values = [0.5, 2, 5]
colors = ['red', 'green', 'blue']

fig = go.Figure()
for Tdamp, c in zip(Tdamp_values, colors):
    fig.add_trace(go.Scatter(
        x=time,
        y=temp_profile(time, Tdamp),
        mode='lines',
        line=dict(width=3, color=c),
        name=f"Tdamp={Tdamp}"
    ))

fig.add_hline(y=T_target, line=dict(color='black', dash='dash'), annotation_text="Target Temp")

fig.update_layout(
    title="Nose–Hoover 온도 안정화 시뮬레이션 (가상 데이터)",
    xaxis_title="시간 (ps)",
    yaxis_title="온도 (K)",
    template="plotly_white",
    xaxis=dict(range=[0, 10], fixedrange=True),
    yaxis=dict(range=[200, 360], fixedrange=True)
)
st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
st.markdown(r"""
### 7️⃣ 결론  
Nose–Hoover thermostat은 단순한 수학적 도구가 아니라,  
**에너지 교환을 미시적으로 모사하는 물리적 장치**입니다.  
온도 감쇠 시간 Tdamp는 그 장치의 ‘반응 속도’를 결정하며,  
적절히 선택된 Tdamp는 시뮬레이션의 안정성과 물리적 신뢰성을 동시에 보장합니다.  
즉, Nose–Hoover의 핵심은 “온도를 조절하되 동역학은 왜곡하지 않는다”는 균형의 예술이라 할 수 있습니다.
""")
