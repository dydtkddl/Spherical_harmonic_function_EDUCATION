# -*- coding: utf-8 -*-
"""
고급형 맥스웰–볼츠만 분포 시각화 튜토리얼 (Streamlit)
────────────────────────────────────────────
• LaTeX 렌더링 오류 방지 (raw string)
• Plotly 기반 인터랙티브 시각화
• 축 범위 고정 (정적 xlim, ylim)
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ─────────────────────────────────────────────
st.set_page_config(page_title="Maxwell–Boltzmann Distribution", layout="wide")

st.title("🌡️ Maxwell–Boltzmann Distribution — A Statistical Window into Molecular Motion")

# ─────────────────────────────────────────────
st.markdown(r"""
### 1️⃣ 물리적 배경: 무질서 속의 규칙성  
기체를 구성하는 분자는 끊임없이 움직이지만, 각각의 운동은 불규칙하고 예측 불가능해 보입니다. 그러나 수많은 입자의 집합적 행동을 통계적으로 바라보면 놀라울 만큼 규칙적인 패턴이 나타납니다. 바로 **맥스웰–볼츠만 분포(Maxwell–Boltzmann Distribution)** 가 그것입니다. 이 분포는 “혼돈 속 질서”의 대표적 사례로, 미시적 무작위 운동이 거시적 물리량(온도, 압력, 에너지)을 어떻게 결정하는지를 보여줍니다.  

### 2️⃣ 수학적 표현과 근본 가정  
이 분포는 고전 통계역학의 가장 단순한 형태, 즉 양자적 제약이 무시될 만큼 충분히 **고온·저밀도** 조건을 전제로 합니다. 이상기체 내의 한 입자에 대한 속도 확률밀도는 다음 식으로 주어집니다:  

$$
f(v) = 4\pi \left(\frac{m}{2\pi k_B T}\right)^{3/2} v^2 e^{-\\frac{mv^2}{2k_BT}}
$$  

여기서 \\(m\\)은 입자 질량, \\(T\\)는 절대온도, \\(k_B\\)는 볼츠만 상수입니다. 지수항은 빠른 입자가 지닐 확률이 급격히 감소함을, 앞의 \\(v^2\\) 항은 느린 입자보다 중간속도의 입자가 더 많음을 의미합니다.  

### 3️⃣ 온도와 질량이 만드는 동적 균형  
낮은 온도에서는 분포가 뾰족하고 좁으며, 대부분의 입자가 유사한 속도를 가집니다. 반대로 온도가 높아질수록 지수 감쇠 항의 영향이 완화되어, 더 많은 입자가 높은 속도를 가질 확률이 증가합니다. 즉, **온도 상승 → 평균 운동에너지 증가 → 분포의 우측 이동 및 평탄화**라는 인과적 연쇄가 발생합니다. 한편 질량이 클수록 속도가 느려지고, 분포의 중심은 왼쪽으로 이동합니다.  

### 4️⃣ 세 가지 특성속도와 비대칭성  
분포에는 세 가지 대표 속도가 존재합니다.  
$$v_{mp} = \sqrt{\\frac{2k_BT}{m}}, \quad v_{mean} = \sqrt{\\frac{8k_BT}{\\pi m}}, \quad v_{rms} = \sqrt{\\frac{3k_BT}{m}}$$  
이들은 각각 “가장 많은 입자가 가지는 속도”, “평균 속도”, “평균 에너지에 대응하는 속도”를 뜻합니다. 모든 경우에 \\(v_{mp} < v_{mean} < v_{rms}\\)이며, 이는 속도 분포가 완전한 대칭이 아님을 의미합니다.
""")

# ─────────────────────────────────────────────
T = st.slider("Temperature (K)", 100, 1200, 300, 50)
m = st.slider("Particle mass (kg)", 1e-27, 1e-25, 4.65e-26, format="%.2e")

kB = 1.380649e-23
v = np.linspace(0, 4000, 600)

# Maxwell–Boltzmann PDF
f_v = 4 * np.pi * (m / (2 * np.pi * kB * T)) ** (3 / 2) * v ** 2 * np.exp(-m * v ** 2 / (2 * kB * T))

v_mp = np.sqrt(2 * kB * T / m)
v_mean = np.sqrt(8 * kB * T / (np.pi * m))
v_rms = np.sqrt(3 * kB * T / m)

# ─────────────────────────────────────────────
# Plotly figure (축 범위 고정)
fig = go.Figure()
fig.add_trace(go.Scatter(x=v, y=f_v, mode='lines', name='f(v)', line=dict(width=3)))
fig.add_vline(x=v_mp, line=dict(color='red', dash='dash'), annotation_text="v_mp")
fig.add_vline(x=v_mean, line=dict(color='green', dash='dot'), annotation_text="v_mean")
fig.add_vline(x=v_rms, line=dict(color='blue', dash='dot'), annotation_text="v_rms")

fig.update_layout(
    title=f"맥스웰–볼츠만 속도 분포 (T={T} K, m={m:.2e} kg)",
    xaxis_title="속도 v (m/s)",
    yaxis_title="확률밀도 f(v)",
    template="plotly_white",
    xaxis=dict(range=[0, 4000], fixedrange=True),  # ✅ xlim 고정
    # yaxis=dict(range=[0, np.max(f_v)*1.1 if np.max(f_v) < 0.005 else 0.005], fixedrange=True)  # ✅ ylim 상한 고정
    yaxis=dict(range=[0,  0.005], fixedrange=True)  # ✅ ylim 상한 고정
)
st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
st.markdown(r"""
### 5️⃣ 통계적 의미와 에너지 등분배  
맥스웰–볼츠만 분포는 **에너지 등분배 정리**의 직접적인 결과로, 각 자유도당 평균 에너지가 \(\frac{1}{2}k_BT\)임을 보여줍니다.  
3차원 입자의 평균 운동에너지는 \(\langle E \rangle = \frac{3}{2}k_BT\)이며, 이는 온도 자체가 입자 운동의 평균 무질서 정도를 나타내는 물리량임을 의미합니다.  

### 6️⃣ 이상기체 법칙으로의 연결  
이 분포를 이용하면 이상기체 방정식 \(PV = Nk_BT\)이 자연스럽게 도출됩니다.  
분자 충돌에 의한 평균 운동량 전달과 충돌 빈도를 적분하면 거시적 압력이 계산되며,  
그 결과가 바로 이상기체식입니다.  

### 7️⃣ 화학반응속도론과 활성화 에너지  
화학반응은 특정 활성화 에너지 \(E_a\) 이상을 가진 입자만 참여할 수 있습니다.  
맥스웰–볼츠만 분포에서 \(E > E_a\) 구간의 면적은 반응 가능한 입자의 비율을 의미하며,  
이 비율이 아레니우스식의 지수항 \(e^{-E_a/k_BT}\)로 이어집니다.  
따라서 **온도 상승 → 고에너지 분자 비율 증가 → 반응속도 증가**라는 실험적 법칙의 이론적 근거가  
이 분포로부터 유도됩니다.  

### 8️⃣ 양자적 한계와 확장  
낮은 온도나 높은 밀도에서는 입자의 파동성이 뚜렷해져 맥스웰–볼츠만 통계가 붕괴합니다.  
전자는 **페르미–디랙 통계**, 보손은 **보즈–아인슈타인 통계**로 대체되며,  
맥스웰–볼츠만 분포는 양자 통계의 고온 극한에서 수렴하는 고전 근사입니다.  

### 9️⃣ 천체물리학적 응용  
별의 대기층, 행성 대기 탈출, 플라즈마 내 전자 온도 분포 등에서도 이 분포가 핵심적으로 등장합니다.  
예를 들어, 지구 대기에서 헬륨이 사라지는 이유는,  
맥스웰–볼츠만 분포의 꼬리 부분에 탈출속도(≈11.2 km/s)를 넘는 입자들이 존재하기 때문입니다.  

### 🔟 결론  
맥스웰–볼츠만 분포는 단순한 속도함수가 아니라,  
**무질서한 미시 세계가 거시적 법칙으로 수렴하는 통계적 다리**입니다.  
이 개념을 이해하면, 기체역학, 반응속도론, 열역학, 플라즈마물리 등 수많은 현상을 하나의 언어로 해석할 수 있습니다.
""")

