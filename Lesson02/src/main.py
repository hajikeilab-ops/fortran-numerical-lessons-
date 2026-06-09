"""
Lesson02: 1 次元熱伝導の計算結果をグラフで表示するプログラム

Fortran プログラム (thermal_diffusion.f95) が出力した
grid.csv と output.csv を読み込み、2 枚のグラフを描画する。

  上段: 時間 × 空間のヒートマップ（温度の時間発展を色で表示）
  下段: 初期・中間・最終時刻の温度分布 T(x) を線グラフで比較

【高速化のポイント】
  - Agg バックエンドで PNG 保存のみ（デフォルト。GUI 起動を省略）
  - pandas の代わりに numpy.loadtxt で CSV 読み込み
  - ヒートマップ用データを表示解像度に間引き
  - Fortran 側も output_stride で CSV 行数を削減
"""

import argparse
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

SRC_DIR = Path(__file__).resolve().parent
GRID_FILE = SRC_DIR / "grid.csv"
DATA_FILE = SRC_DIR / "output.csv"
OUTPUT_PNG = SRC_DIR / "thermal_diffusion.png"

MAX_HEATMAP_ROWS = 400


def load_data() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """CSV を numpy で読み込む（pandas より高速）。"""
    x = np.loadtxt(GRID_FILE, delimiter=",", skiprows=1)
    data = np.loadtxt(DATA_FILE, delimiter=",", skiprows=1)
    times = data[:, 0]
    T = data[:, 1:]
    return x, times, T


def downsample_for_heatmap(times: np.ndarray, T: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """ヒートマップ用に時間方向を間引く。"""
    n = len(times)
    if n <= MAX_HEATMAP_ROWS:
        return times, T
    stride = int(np.ceil(n / MAX_HEATMAP_ROWS))
    return times[::stride], T[::stride, :]


def open_image(path: Path) -> None:
    """保存した PNG を OS のビューアで開く。"""
    if sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
    elif sys.platform == "win32":
        subprocess.run(["start", "", str(path)], shell=True, check=False)
    else:
        subprocess.run(["xdg-open", str(path)], check=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson02 熱伝導の結果を描画")
    parser.add_argument(
        "--show",
        action="store_true",
        help="PNG 保存後に画像ビューアで開く",
    )
    args = parser.parse_args()

    x, times, T = load_data()
    times_hm, T_hm = downsample_for_heatmap(times, T)

    fig, axes = plt.subplots(2, 1, figsize=(10, 9))

    im = axes[0].imshow(
        T_hm,
        aspect="auto",
        origin="lower",
        extent=[x.min(), x.max(), times_hm.min(), times_hm.max()],
        cmap="inferno",
        rasterized=True,
        interpolation="nearest",
    )
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("Time [s]")
    axes[0].set_title("1D Heat Diffusion (explicit method)")
    fig.colorbar(im, ax=axes[0], label="Temperature")

    indices = [0, len(times) // 2, len(times) - 1]
    for idx in indices:
        axes[1].plot(x, T[idx], label=f"t = {times[idx]:.3f} s")

    axes[1].set_xlabel("x")
    axes[1].set_ylabel("Temperature")
    axes[1].set_title("Temperature profiles")
    axes[1].legend()
    axes[1].grid()

    plt.tight_layout()
    fig.savefig(OUTPUT_PNG, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"グラフを保存しました: {OUTPUT_PNG}")

    if args.show:
        open_image(OUTPUT_PNG)


if __name__ == "__main__":
    main()
