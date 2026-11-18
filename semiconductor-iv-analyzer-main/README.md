# 🔬 Semiconductor Device I-V Analyzer & AI Parameter Extractor

반도체 소자(MOSFET)의 측정 데이터로부터 핵심 전기적 파라미터를 자동으로 추출하고, **Gemini AI 소자 엔지니어**를 통해 실시간 소자 특성 및 공정 개선점을 진단하는 Python 기반 지능형 웹 대시보드입니다.

🔗 **Live Demo (웹 서비스 바로가기)**: [https://semiconductor-iv-analyzer-yh7tgnz7nrch2rfkzzuu3v.streamlit.app/](https://semiconductor-iv-analyzer-yh7tgnz7nrch2rfkzzuu3v.streamlit.app/)

---

## 📌 프로젝트 개요 (Overview)
반도체 공정 및 소자 측정 시 발생하는 전압-전류(I-V) 실측 데이터를 파싱하여 소자의 성능을 결정하는 **핵심 파라미터($V_{th}, I_{on}/I_{off}, SS, g_m$)**를 자동으로 계산하고 고해상도(300 DPI) 로그 스케일 그래프로 시각화합니다. 
더불어 최신 **Gemini AI API**를 연동하여 추출된 수치 기반의 소자 양불 판정 및 공정 엔지니어링 피드백을 실시간 제공합니다.

---

## ⚡ 핵심 기능 및 기술 스택

1. **자동 파라미터 추출 엔진:**
  - **문턱전압 ($V_{th}$):** 정전류 기준법(Constant Current Method, $1\mu\text{A}$) 기반 자동 산출
  - **On/Off 전류비 ($I_{on}/I_{off}$):** 최대 구동전류와 최소 누설전류 비율 계산
  - **Subthreshold Swing ($SS$) 및 트랜스콘덕턴스 ($g_m$):** 미분 연산을 통한 스위칭 및 증폭 성능 지표 추출
2. **Gemini AI 지능형 소자 진단 (`gemini-3.8-flash`):**
  - 추출된 파라미터 수치를 프롬프트에 동적으로 바인딩하여 AI 소자 엔지니어가 누설 전류 상태 및 옥사이드/도핑 공정 개선점을 실시간 진단
3. **Streamlit Cloud 웹 대시보드:**
  - 터미널 실행을 넘어 사용자가 브라우저에서 직접 I-V 측정 CSV 파일을 업로드하고, 실시간 $I_d - V_{gs}$ 커브 및 시각화 결과를 확인할 수 있는 직관적인 UI/UX 환경 제공
4. **네트워크 안정성 확보 (Auto-Retry):**
  - 팹/서버 트래픽 과부하 또는 타임아웃 발생 시 최대 3회까지 자동 재시도하는 견고한 예외 처리 로직 구현

---

## 📊 추출 파라미터 및 물리적 의미

| 파라미터 | 추출 방식 | 반도체 소자에서의 물리적 의미 |
| :--- | :--- | :--- |
| **문턱전압 ($V_{th}$)** | 정전류 도달 시점 ($1\mu\text{A}$) | 채널이 반전되어 소자가 켜지는 기준 전압 |
| **On/Off 전류비 ($I_{on}/I_{off}$)** | 최대 전류 / 최소 누설전류 | 스위칭 성능 및 대기 전력(Off-state leakage) 품질 지표 |
| **Subthreshold Swing ($SS$)** | 역기울기 ($[d\log_{10} I_D / dV_{GS}]^{-1}$) | 게이트의 채널 제어력 평가 지표 |
| **트랜스콘덕턴스 ($g_m$)** | $g_m = \partial I_D / \partial V_{GS}$ 최대값 | 게이트 전압에 따른 전류 증폭 성능 |

---

## 🚀 실행 결과 예시 (Output Summary)

```text
============================================================
MOSFET 파라미터 자동 추출 결과
============================================================
▶ 문턱전압 (vth)		: 0.769 V
▶ On/off 전류비 (Ion/Ioff): 7.92e+09
▶ Subthreshold Swing (SS): 71.6 mV/dec
▶ 최대 gm (Transconductance): 1.150 mS
============================================================
🤖 AI 소자 엔지니어 분석 중...
✅ [판정] 실제 데이터 기준 off-state 누설 전류 특성 정상입니다.

============================================================
📊 [Gemini AI 소자 엔지니어 진단 리포트]
============================================================
1) off-state 누설 전류가 1pA 수준으로 매우 낮고 Ion/Ioff 비가 우수하여 스위칭 특성이 안정적입니다.
2) SS 값이 71.6 mV/dec로 이상적인 상온 한계(60)에 근접해 게이트 산화막의 품질이 양호합니다.
3) 추가적인 성능 향상을 위해 고유전율(High-k) 옥사이드 두께 최적화 및 채널 도핑 농도 미세 조정을 권장합니다.
============================================================
---

## 💡 5. 시스템 아키텍처 및 파이프라인 (System Architecture)
```text
[Raw I-V Measurement CSV Data] 
       │
       ▼
[Data Parsing & Preprocessing] 
       │
       ▼
[Parameter Extraction Engine ($V_{th}, I_{on}/I_{off}, SS, g_m$)] 
       │
       ▼
[Log-Scale Visualization (Matplotlib / Seaborn)] 
       │
       ▼
[Gemini AI Device Diagnostic Engine (Auto-Retry)] ──> Expert Process Feedback Report
Developed by 전효재 (Jeon Hyojae) | Suncheon National University, Department of Electronic Engineering