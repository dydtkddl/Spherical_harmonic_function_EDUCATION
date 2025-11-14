# -*- coding: utf-8 -*-
"""
GPU Deep Learning Environment Setup Guide (pip version)
NVIDIA L4 환경에서 pip 중심으로 딥러닝 라이브러리를 설치하는 방법을 정리한 문서
"""

import streamlit as st

st.set_page_config(page_title="GPU Deep Learning Setup Guide (pip)", layout="wide")

st.title("GPU Deep Learning 환경 구축 가이드 (pip 기반)")
st.write(
    "NVIDIA L4 GPU 서버에서 딥러닝 연구 환경을 구성할 때 사용할 pip 기반 설치 절차를 정리했습니다. "
    "기본적인 conda 환경만 만든 뒤 나머지는 모두 pip로 설치하는 방식입니다."
)

st.markdown("---")

# 1. Conda Environment
with st.expander("1. Conda 환경 만들기", expanded=True):
    st.subheader("설치 명령어")
    st.code("""
conda create -n pytorch_gpu python=3.10 -y
conda activate pytorch_gpu
""")

    st.subheader("왜 이렇게 쓰는가")
    st.write(
        "여러 프로젝트를 동시에 관리할 때 각 환경을 독립적으로 유지하는 것이 훨씬 안전합니다. "
        "특히 pip로 여러 GPU 라이브러리를 설치할 때 충돌이 날 수 있으므로, "
        "conda로 기본 틀을 잡고 그 안에서 pip를 사용하는 방식이 가장 안정적입니다."
    )

st.markdown("---")

# 2. PyTorch
with st.expander("2. PyTorch GPU 설치 (pip)", expanded=True):
    st.subheader("설치 명령어")
    st.code("""
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
""")

    st.subheader("왜 필요한가")
    st.write(
        "PyTorch는 연구에서 모델을 직접 설계하고 실험할 때 가장 다루기 쉬운 도구입니다. "
        "처음 아이디어를 구현하거나 구조를 빠르게 바꿔야 하는 상황이 자주 발생하는데, "
        "PyTorch는 이런 반복 작업을 직관적으로 처리할 수 있어 연구에서 많이 사용됩니다."
    )

st.markdown("---")

# 3. TensorFlow
with st.expander("3. TensorFlow GPU 설치 (pip)", expanded=True):
    st.subheader("설치 명령어")
    st.code("""
pip install tensorflow[and-cuda]
""")

    st.subheader("왜 필요한가")
    st.write(
        "TensorFlow는 모델을 실제 서비스 환경에서 사용해야 할 때 안정적이고 확장성이 좋습니다. "
        "최근 버전은 필요한 CUDA 런타임을 함께 제공해서 설치 과정이 간단하고, "
        "연구 단계에서 만든 모델을 배포로 연결시키는 데도 편리합니다."
    )

st.markdown("---")

# 4. JAX
with st.expander("4. JAX GPU 설치 (pip)"):
    st.subheader("설치 명령어")
    st.code("""
pip install -U "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
""")

    st.subheader("왜 필요한가")
    st.write(
        "JAX는 수학적 계산을 빠르게 처리하고 자동 미분이 자연스럽게 적용되어, "
        "새로운 알고리즘을 실험하거나 계산 구조를 반복적으로 바꿔야 할 때 도움이 됩니다. "
        "속도가 빨라서 연산량이 많은 실험에서도 시간을 줄이는 데 유리합니다."
    )

st.markdown("---")

# 5. CUDA Runtime / cuDNN / 기타 GPU 필수 라이브러리
with st.expander("5. NVIDIA CUDA 라이브러리 (pip)"):
    st.subheader("설치 명령어")
    st.code("""
pip install nvidia-cublas-cu12 nvidia-cudnn-cu12 nvidia-cuda-runtime-cu12
pip install nvidia-nccl-cu12 nvidia-curand-cu12 nvidia-cufft-cu12
""")

    st.subheader("왜 필요한가")
    st.write(
        "딥러닝에서 자주 쓰이는 행렬 곱셈, 합성곱 같은 연산은 모두 GPU에서 처리되는데, "
        "실제로 이런 연산을 수행하는 핵심 엔진이 바로 cuBLAS와 cuDNN 같은 CUDA 라이브러리입니다. "
        "프레임워크가 내부적으로 의존하는 부분이라 직접 사용할 일은 없지만, "
        "빠르고 안정적인 연산을 위해서는 꼭 필요한 구성 요소입니다."
    )

st.markdown("---")

# 6. 연구에 자주 쓰이는 Python 패키지
with st.expander("6. 연구용 필수 pip 패키지"):
    st.subheader("설치 명령어")
    st.code("""
pip install numpy scipy pandas scikit-learn matplotlib seaborn
pip install tqdm rich loguru
pip install opencv-python einops
pip install transformers accelerate datasets
pip install wandb tensorboard lightning timm sentencepiece
""")

    st.subheader("왜 필요한가")
    st.write(
        "딥러닝 실험은 모델 학습만으로 끝나는 경우가 거의 없고, "
        "데이터 전처리, 시각화, 로그 기록, 결과 비교 등 다양한 작업이 함께 진행됩니다. "
        "이 패키지들은 그런 부수적인 작업들을 편하게 도와주는 도구들로, "
        "조금만 사용해도 실험 효율이 크게 올라가는 것을 바로 체감할 수 있습니다."
    )

st.markdown("---")

st.write("pip 기반으로 설치할 때는 순서대로 진행하는 것이 가장 안정적입니다.")
