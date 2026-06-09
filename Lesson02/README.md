# Lesson02: 1 次元熱伝導（显式差分法）

Fortran で熱伝導方程式を数値計算し、Python で結果をグラフ化する例です。  
Lesson01 と同様、**計算は Fortran・描画は Python** の役割分担です（plplot は使いません）。

## このレッスンで学ぶこと

- **1 次元熱伝導方程式** … `∂T/∂t = κ ∂²T/∂x²`
- **显式差分法（フォワード・オイラー）** … 時間を少しずつ進めて温度分布を更新する
- **ディリクレ境界条件** … 両端の温度を固定する
- **初期条件** … 三角形分布から拡散がどう進むかを観察する
- **Fortran と Python の連携** … CSV を介して計算結果を可視化する

## フォルダ構成

```
Lesson02/
├── README.md                 … このファイル
├── Makefile                  … ビルド・実行・描画の自動化
├── requirements.txt          … Python ライブラリ一覧
└── src/
    ├── thermal_diffusion.f95 … Fortran 計算プログラム
    ├── main.py               … Python 描画プログラム
    ├── grid.csv              … 空間座標（実行後に生成）
    ├── output.csv            … 温度の時系列（実行後に生成）
    └── thermal_diffusion.png … グラフ画像（Python 実行後に生成）
```

## 必要なソフトウェア

| ソフトウェア | 用途 |
|-------------|------|
| gfortran | Fortran プログラムのコンパイル・実行 |
| make（任意） | Makefile による一括実行 |
| Python 3 | グラフ描画 |
| matplotlib, numpy | 描画・データ読み込み（`requirements.txt` 参照） |

gfortran / Python のインストール手順は [Lesson01 の README](../Lesson01/README.md#インストール方法) を参照してください。

---

## 実行手順

### 方法 A: Makefile を使う（おすすめ）

`Lesson02/` フォルダで実行します。

```bash
cd Lesson02

# 1. Fortran をビルド
make

# 2. 計算実行（grid.csv, output.csv を生成）
make run

# 3. グラフ描画（thermal_diffusion.png を保存）
make plot

# または 2〜3 を一括
make all-results
```

| コマンド | 内容 |
|---------|------|
| `make` | Fortran プログラムをコンパイル |
| `make run` | 熱伝導の時間発展を計算 |
| `make plot` | PNG を保存（高速。ウィンドウは開かない） |
| `make plot-show` | PNG 保存後、画像ビューアで開く |
| `make clean` | 実行ファイルと生成ファイルを削除 |
| `make deps` | Python ライブラリを pip でインストール |

### 方法 B: コマンドを直接実行する

```bash
cd Lesson02/src

# Fortran
gfortran -O2 -o thermal_diffusion thermal_diffusion.f95
./thermal_diffusion

# Python
pip install -r ../requirements.txt   # 初回のみ
python main.py
python main.py --show                # 保存後にビューアで開く
```

### macOS / Linux / WSL2

上記の手順がそのまま使えます。WSL2 では **WSL 内のターミナル**で実行してください。

### Windows（ネイティブ）

PowerShell 単体では Makefile がそのまま動きません。次のいずれかを使ってください。

| 方法 | 説明 |
|------|------|
| **WSL2**（推奨） | Linux と同じ手順。`make` が使える |
| **MSYS2 UCRT64** | `make` と `gfortran` を入れて実行。実行ファイルは `.exe` |

MSYS2 の例:

```bash
gfortran -O2 -o thermal_diffusion.exe thermal_diffusion.f95
./thermal_diffusion.exe
python main.py
```

---

## 結果の見方

### 上段: ヒートマップ（時間 × 空間）

- **横軸** … 空間座標 x
- **縦軸** … 時間 t
- **色** … 温度 T（明るいほど高温）

三角形の初期分布が、時間とともに拡散・平滑化していく様子がわかります。

### 下段: 温度分布の断面

- **3 本の曲線** … 初期・中間・最終時刻の T(x)
- ピークが低くなり、分布が広がっていれば計算は妥当と考えられます

---

## パラメータの変更

`src/thermal_diffusion.f95` の先頭付近で変更できます。

```fortran
integer, parameter :: iend = 100          ! 空間分割数
integer, parameter :: nend = 2500           ! 時間ステップ数
integer, parameter :: output_stride = 10    ! CSV 出力間隔（描画用）
real(8), parameter :: kp     = 1.0d0        ! 熱拡散係数 κ
real(8), parameter :: length = 10.0d0       ! 領域長
real(8), parameter :: dt     = 0.004d0      ! 時間刻み Δt
```

| パラメータ | 意味 | 変更の目安 |
|-----------|------|-----------|
| `iend` | 空間の格子点数 | 大きいほど空間分解能が上がる |
| `nend` | 時間ステップ数 | 大きいほど長く計算する |
| `output_stride` | CSV の出力間隔 | 大きいほどファイルが小さく描画が速い |
| `kp` | 拡散係数 | 大きいほど拡散が速い |
| `dt` | 時間刻み | 大きすぎると显式法が不安定になりやすい |

変更後は、再度 `make`（または `gfortran` でコンパイル）から実行してください。

### 安定条件の目安

显式差分法では、おおよそ次を満たす必要があります。

```
κ * Δt / Δx² ≤ 1/2
```

不安定になった場合は `dt` を小さくするか、`iend` を増やして `Δx` を小さくしてください。

---

## よくある質問

### Q. `ModuleNotFoundError: No module named 'matplotlib'`

Python ライブラリが未インストールです。

```bash
pip install -r requirements.txt
# または
python -m pip install -r requirements.txt
# または
make deps
```

### Q. 描画が遅い

次を試してください。

1. `output_stride` を大きくする（例: `20`）
2. `make plot` を使う（`plt.show()` ではなく PNG 保存のみ）
3. Fortran を再実行して CSV を再生成する

### Q. Lesson01 との違いは？

| 項目 | Lesson01 | Lesson02 |
|------|----------|----------|
| テーマ | 数値微分 | 熱伝導（時間発展） |
| 出力 | `output.csv` | `grid.csv` + `output.csv` |
| グラフ | sin(x) と微分の比較 | ヒートマップ + 断面 |
| ビルド | 手動 `gfortran` | Makefile 対応 |

---

## 参考リンク

### 熱伝導・差分法

| サイト | 内容 |
|--------|------|
| [熱伝導方程式 — Wikipedia（日本語）](https://ja.wikipedia.org/wiki/%E7%86%B1%E4%BC%9D%E5%B0%8E%E6%96%B9%E7%A8%8B%E5%BC%8F) | 方程式の概要 |
| [有限差分法 — Wikipedia（日本語）](https://ja.wikipedia.org/wiki/%E6%9C%89%E9%99%90%E5%B7%AE%E5%88%86%E6%B3%95) | 差分法の基本概念 |

### Python ライブラリ

| サイト | 内容 |
|--------|------|
| [Matplotlib チュートリアル](https://matplotlib.org/stable/tutorials/index.html) | グラフ描画 |
| [NumPy ユーザーガイド](https://numpy.org/doc/stable/user/index.html) | 数値配列の操作 |

### 開発環境

| サイト | 内容 |
|--------|------|
| [Lesson01 README](../Lesson01/README.md) | gfortran / Python のインストール手順 |
| [MSYS2](https://www.msys2.org/) | Windows 向け gfortran 環境 |
| [WSL インストール — Microsoft Learn](https://learn.microsoft.com/ja-jp/windows/wsl/install) | Windows 上で Linux 環境を使う |
