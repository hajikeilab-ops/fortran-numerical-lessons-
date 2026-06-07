"""
Lesson01: sin(x) の数値微分結果をグラフで表示するプログラム

Fortran プログラム (numerical_differentiation.f95) が出力した
output.csv を読み込み、2 枚のグラフを描画する。

  上段: sin(x) の曲線と、Fortran で計算に使ったサンプリング点
  下段: 真の微分 cos(x) と、3 つの差分による近似値の比較
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# このスクリプトと同じフォルダ (src/) にあるファイルを参照する
DATA_FILE = Path(__file__).resolve().parent / "output.csv"
OUTPUT_PNG = Path(__file__).resolve().parent / "numerical_differentiation.png"


def main() -> None:
    # ------------------------------------------------------------------
    # ステップ1: Fortran が出力した CSV を読み込む
    # ------------------------------------------------------------------
    df = pd.read_csv(DATA_FILE)

    # 滑らかな sin(x) 曲線を描くための補助データ（100 点）
    x_fine = np.linspace(0, np.pi, 100)
    sin_fine = np.sin(x_fine)

    # 上下 2 段のグラフを用意する
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))

    # ------------------------------------------------------------------
    # 上段: sin(x) の曲線とサンプリング点
    # ------------------------------------------------------------------
    axes[0].plot(x_fine, sin_fine, label="sin(x)", linewidth=2, color="blue")
    axes[0].scatter(df["x"], df["sin(x)"], color="red", label="Sampled points", zorder=3)
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("sin(x)")
    axes[0].set_title("sin(x) and Sampled Points")
    axes[0].legend()
    axes[0].grid()

    # ------------------------------------------------------------------
    # 下段: 数値微分の結果と真値 cos(x) の比較
    #
    # 中央差分（緑の三角）が cos(x)（黒の破線）に最も近いはず。
    # 前進差分・後退差分は片側の点だけを使うため、ずれが大きい。
    # ------------------------------------------------------------------
    axes[1].plot(
        df["x"], df["cos(x)"],
        label="Exact cos(x)", linestyle="dashed", linewidth=2, color="black",
    )
    axes[1].plot(
        df["x"], df["Forward Diff"],
        label="Forward Difference", marker="o", linestyle="dotted",
    )
    axes[1].plot(
        df["x"], df["Backward Diff"],
        label="Backward Difference", marker="s", linestyle="dotted",
    )
    axes[1].plot(
        df["x"], df["Central Diff"],
        label="Central Difference", marker="^", linestyle="solid",
    )
    axes[1].set_xlabel("x")
    axes[1].set_ylabel("Derivative Value")
    axes[1].set_title("Numerical Differentiation of sin(x)")
    axes[1].legend()
    axes[1].grid()

    plt.tight_layout()
    fig.savefig(OUTPUT_PNG, dpi=150)
    print(f"グラフを保存しました: {OUTPUT_PNG}")
    plt.show()


if __name__ == "__main__":
    main()
