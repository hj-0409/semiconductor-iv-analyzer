import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def analyze_mosfet(csv_file="sample_data.csv"):
    # 1. 측정 데이터 로드
    df = pd.read_csv(csv_file)
    vg = df["Vgs"].values
    id_cur = df["Id"].values

    # 2. 파라미터 계산
    # (1) On/Off Current Ratio
    id_max = np.max(id_cur)
    id_min = np.min(id_cur[id_cur > 0])
    on_off_ratio = id_max / id_min

    # (2) Transconductance (gm = dId / dVg)
    gm = np.gradient(id_cur, vg)
    max_gm_idx = np.argmax(gm)
    max_gm = gm[max_gm_idx]
    vg_max_gm = vg[max_gm_idx]
    id_max_gm = id_cur[max_gm_idx]

    # (3) Threshold Voltage (Vth) - 선형 외삽법 (Linear Extrapolation)
    vth = vg_max_gm - (id_max_gm / max_gm)

    # (4) Subthreshold Swing (SS = [d(log10 Id) / dVg]^-1)
    log_id = np.log10(np.maximum(id_cur, 1e-15))
    d_log_id = np.gradient(log_id, vg)
    sub_mask = (vg < vth) & (vg > 0.0)
    if np.any(sub_mask):
        ss_val = (1.0 / np.max(d_log_id[sub_mask])) * 1000  # 단위: mV/dec
    else:
        ss_val = 0.0

    # 3. 결과 터미널 출력
    print("=" * 45)
    print("       MOSFET 파라미터 자동 추출 결과       ")
    print("=" * 45)
    print(f"▶ 문턱전압 (Vth)        : {vth:.3f} V")
    print(f"▶ On/Off 전류비 (Ion/Ioff): {on_off_ratio:.2e}")
    print(f"▶ Subthreshold Swing (SS): {ss_val:.1f} mV/dec")
    print(f"▶ 최대 gm (Transconductance): {max_gm*1000:.3f} mS")
    print("=" * 45)

    # 4. 듀얼 그래프 플롯팅 (Linear & Semi-log)
    fig, ax1 = plt.subplots(figsize=(8, 6))

    # 왼쪽 축: Linear scale
    color = "tab:blue"
    ax1.set_xlabel("Gate Voltage $V_{GS}$ [V]", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Drain Current $I_D$ [A] (Linear)", color=color, fontsize=12, fontweight="bold")
    ax1.plot(vg, id_cur, color=color, linewidth=2.5, label="$I_D$ (Linear)")
    ax1.tick_params(axis="y", labelcolor=color)

    # Vth 접선 표시
    tangent_vg = np.linspace(vth, vg_max_gm + 0.3, 50)
    tangent_id = max_gm * (tangent_vg - vth)
    ax1.plot(tangent_vg, tangent_id, "--", color="red", label=f"Extrapolation ($V_{{th}}$={vth:.2f}V)")
    ax1.axvline(x=vth, color="red", linestyle=":", alpha=0.7)

    # 오른쪽 축: Log scale
    ax2 = ax1.twinx()
    color = "tab:green"
    ax2.set_ylabel("Drain Current $I_D$ [A] (Log Scale)", color=color, fontsize=12, fontweight="bold")
    ax2.semilogy(vg, id_cur, color=color, linewidth=2.5, linestyle="-.", label="$I_D$ (Log)")
    ax2.tick_params(axis="y", labelcolor=color)

    plt.title("MOSFET Transfer Characteristics ($I_D - V_{GS}$)", fontsize=14, fontweight="bold", pad=15)
    fig.tight_layout()
    plt.grid(True, which="both", alpha=0.3)
    
    # 그래프 이미지로 자동 저장
    plt.savefig("mosfet_transfer_curve.png", dpi=300)
    print("▶ 분석 그래프 저장 완료: mosfet_transfer_curve.png")

if __name__ == "__main__":
    analyze_mosfet()
