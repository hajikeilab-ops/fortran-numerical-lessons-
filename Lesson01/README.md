# Lesson01: sin(x) の数値微分（前進・後退・中央差分）

Fortran で数値計算を行い、Python で結果をグラフ化する入門例です。

## このレッスンで学ぶこと

- **微分と差分の違い** … コンピュータでは「極限」を使えないので、近くの点の値で傾きを近似する
- **3 つの差分公式**
  - 前進差分: `{ f(x + Δx) - f(x) } / Δx`
  - 後退差分: `{ f(x) - f(x - Δx) } / Δx`
  - 中央差分: `{ f(x + Δx) - f(x - Δx) } / (2Δx)`
- **sin(x) の微分は cos(x)** … 差分の結果が cos(x) にどれだけ近いかを確認する

## フォルダ構成

```
Lesson01_sin_cos/
├── README.md                          … このファイル
├── requirements.txt                   … Python ライブラリ一覧
└── src/
    ├── numerical_differentiation.f95  … Fortran 計算プログラム
    ├── main.py                        … Python 描画プログラム
    ├── output.csv                     … Fortran の出力（実行後に生成）
    └── numerical_differentiation.png  … グラフ画像（Python 実行後に生成）
```

## 必要なソフトウェア

| ソフトウェア | 用途 |
|-------------|------|
| gfortran | Fortran プログラムのコンパイル・実行 |
| Python 3 | グラフ描画 |
| pip | Python ライブラリのインストール |

以下では **macOS / Linux / Windows** それぞれのインストール方法を説明します。  
インストール後、ターミナル（または Windows の MSYS2 ターミナル）で次のコマンドを実行し、バージョンが表示されれば成功です。

```bash
gfortran --version
python --version
pip --version
```

---

## インストール方法

### macOS

#### Python 3

**方法 A: 公式インストーラ（初心者向け・おすすめ）**

1. [Python 公式ダウンロードページ](https://www.python.org/downloads/) を開く
2. 「Download Python 3.x.x」をクリックして `.pkg` をダウンロード
3. ダウンロードしたファイルをダブルクリックし、画面の指示に従ってインストール

**方法 B: Homebrew（コマンドラインに慣れている方向け）**

Homebrew が未インストールの場合は、[Homebrew 公式サイト](https://brew.sh/) の手順で先にインストールしてください。

```bash
brew install python
```

#### gfortran（Fortran コンパイラ）

**方法 A: Homebrew（おすすめ）**

```bash
brew install gcc
```

`gcc` パッケージに `gfortran` が含まれます。

**方法 B: 公式に近いスタンドアロンインストーラ**

Homebrew を使わない場合は、[gfortran for macOS (GitHub)](https://github.com/fxcoudert/gfortran-for-macOS/releases) から、お使いの macOS バージョンと CPU（Apple Silicon / Intel）に合った `.dmg` をダウンロードしてインストールしてください。

#### macOS での動作確認

```bash
gfortran --version
python3 --version
pip3 --version
```

---

### Linux

Linux では、ディストリビューションごとにパッケージ管理コマンドが異なります。  
お使いの Linux に合った方法を選んでください。

#### Python 3

多くの Linux には Python 3 が最初から入っています。まず確認してください。

```bash
python3 --version
```

入っていない場合は、ディストリビューションに応じてインストールします。

**Debian / Ubuntu / Mint など（apt）**

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Fedora / RHEL 8 以降 / CentOS Stream など（dnf）**

```bash
sudo dnf install python3 python3-pip
```

**Arch Linux / Manjaro など（pacman）**

```bash
sudo pacman -S python python-pip
```

#### gfortran（Fortran コンパイラ）

**Debian / Ubuntu / Mint など（apt）**

```bash
sudo apt update
sudo apt install gfortran
```

**Fedora / RHEL 8 以降 など（dnf）**

```bash
sudo dnf install gcc-gfortran
```

**Arch Linux / Manjaro など（pacman）**

```bash
sudo pacman -S gcc-fortran
```

#### Linux での動作確認

```bash
gfortran --version
python3 --version
pip3 --version
```

---

### Windows

Windows では **MSYS2** を使う方法が最も一般的です。  
Linux/macOS と同じ `gfortran` コマンドでコンパイルできます。

#### Python 3

1. [Python 公式ダウンロードページ](https://www.python.org/downloads/) を開く
2. 「Download Python 3.x.x」をクリック
3. インストーラを実行する
4. **重要:** 最初の画面で **「Add python.exe to PATH」** にチェックを入れてから「Install Now」をクリック

詳細は [Python on Windows 公式ドキュメント](https://docs.python.org/3/using/windows.html) も参照してください。

#### gfortran（Fortran コンパイラ）— MSYS2 を使う方法

1. [MSYS2 公式サイト](https://www.msys2.org/) からインストーラをダウンロード
2. インストーラを実行し、画面の指示に従う
3. スタートメニューから **「MSYS2 UCRT64」** を開く
4. パッケージデータベースを更新する（初回のみ）

```bash
pacman -Syu
```

ターミナルが閉じるよう指示されたら閉じ、再度 **「MSYS2 UCRT64」** を開いて続けます。

5. gfortran をインストールする

```bash
pacman -S mingw-w64-ucrt-x86_64-gcc-fortran
```

6. インストール確認

```bash
gfortran --version
```

> **補足:** Fortran のコンパイルと実行は **MSYS2 UCRT64** ターミナル内で行ってください。  
> 通常の PowerShell やコマンドプロンプトでは `gfortran` が使えない場合があります。

#### Windows 向けの別の選択肢

| 方法 | 説明 |
|------|------|
| [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/ja-jp/windows/wsl/install) | Windows 上で Linux 環境を動かす。Linux 向け手順（apt など）が使える |
| [equation.com](http://www.equation.com/) | インストーラ形式の GCC/gfortran（32/64 bit） |
| [MinGW-w64](https://www.mingw-w64.org/) | MSYS2 の基盤。詳細は [Getting Started with MSYS2](https://www.mingw-w64.org/getting-started/msys2/) |

#### Windows での動作確認

**PowerShell / コマンドプロンプト（Python）**

```powershell
python --version
pip --version
```

**MSYS2 UCRT64 ターミナル（gfortran）**

```bash
gfortran --version
```

---

### Python ライブラリのインストール（全 OS 共通）

プロジェクトのルートフォルダ (`Lesson01_sin_cos`) で実行してください。

```bash
pip install -r requirements.txt
```

Linux / macOS で `pip` が見つからない場合は `pip3` を使ってください。

```bash
pip3 install -r requirements.txt
```

---

## 実行手順

### macOS / Linux

`src` フォルダに移動してから実行します。

```bash
cd src
```

#### ステップ 1: Fortran をコンパイルする

ソースコード (`.f95`) を、コンピュータが実行できる形式 (実行ファイル) に変換します。

```bash
gfortran -O2 -o numerical_differentiation numerical_differentiation.f95
```

- `gfortran` … Fortran コンパイラ
- `-O2` … 最適化オプション（計算を少し速くする）
- `-o numerical_differentiation` … 出力する実行ファイルの名前
- 最後の引数 … コンパイルするソースファイル

#### ステップ 2: Fortran プログラムを実行する

```bash
./numerical_differentiation
```

成功すると、同じフォルダに `output.csv` が作成されます。

```
計算結果を output.csv に保存しました。
```

#### ステップ 3: Python でグラフを描画する

```bash
python main.py
```

macOS / Linux では `python3 main.py` の場合もあります。

---

### Windows（MSYS2 UCRT64 ターミナル）

1. **MSYS2 UCRT64** を開く
2. プロジェクトの `src` フォルダに移動する

```bash
cd /c/Users/あなたのユーザー名/Desktop/96_Program/FortranHandbook-Programs/Fortran/Lesson01_sin_cos/src
```

> パスは環境に合わせて変更してください。`C:\` は MSYS2 では `/c/` と書きます。

3. Fortran をコンパイル・実行する

```bash
gfortran -O2 -o numerical_differentiation.exe numerical_differentiation.f95
./numerical_differentiation.exe
```

4. Python でグラフを描画する（PowerShell でも可）

```powershell
cd src
python main.py
```

グラフウィンドウが開き、同時に `numerical_differentiation.png` も保存されます。

---

## 結果の見方

### 上段のグラフ: sin(x) とサンプリング点

- 青い曲線 … 本来の sin(x)
- 赤い点 … Fortran が計算に使った 10 個の点

点の間隔が広いほど、差分の近似精度は下がります。

### 下段のグラフ: 微分の比較

- 黒い破線 … 真の微分 cos(x)
- 青丸 … 前進差分（右側の点だけ使用 → ややずれる）
- 橙四角 … 後退差分（左側の点だけ使用 → ややずれる）
- 緑三角 … 中央差分（左右両方使用 → cos(x) に最も近い）

**中央差分が最も精度が高い** ことがグラフで確認できます。

---

## よくある質問

### Q. `gfortran: command not found` と出る

gfortran がインストールされていないか、PATH が通っていません。  
上記の [インストール方法](#インストール方法) を参照してください。

- **macOS:** `brew install gcc`
- **Linux (Ubuntu):** `sudo apt install gfortran`
- **Windows:** MSYS2 UCRT64 ターミナルで `pacman -S mingw-w64-ucrt-x86_64-gcc-fortran`

### Q. `python: command not found` と出る

- **macOS / Linux:** `python3` を試してください
- **Windows:** Python インストール時に「Add python.exe to PATH」にチェックを入れ直すか、再インストールしてください

### Q. `ModuleNotFoundError: No module named 'pandas'` と出る

Python ライブラリが未インストールです。ルートフォルダで次を実行してください。

```bash
pip install -r requirements.txt
```

### Q. サンプリング点数を変えたい

`src/numerical_differentiation.f95` の次の行を変更します。

```fortran
integer, parameter :: n  = 10     ! ← この数字を変更（例: 20, 50）
```

変更後は、再度コンパイル（ステップ 1）から実行してください。

### Q. 端点で差分が 0 になっている

端点では片側の点しか存在しないため、前進・後退・中央差分のいずれかが計算できません。プログラムでは計算不可の場合に 0 を出力しています。

---

## 参考: 差分の精度

| 差分の種類 | 精度 | 使う点 |
|-----------|------|--------|
| 前進差分 | 1 次 | 右側 1 点 |
| 後退差分 | 1 次 | 左側 1 点 |
| 中央差分 | 2 次 | 左右 2 点 |

「1 次精度」「2 次精度」とは、誤差が Δx に比例するか、Δx² に比例するかの違いです。中央差分の方が Δx を小さくしたときに誤差が早く減ります。

---

## 参考リンク

### Fortran / gfortran

| サイト | 内容 |
|--------|------|
| [Installing GFortran — fortran-lang.org](https://fortran-lang.org/learn/os_setup/install_gfortran/) | OS 別 gfortran インストールガイド（英語・初心者向け） |
| [GNU Fortran — GNU Project](https://www.gnu.org/software/gcc/fortran/) | GFortran 公式プロジェクトページ |
| [GFortran Binaries — GCC Wiki](https://gcc.gnu.org/wiki/GFortranBinaries) | 非公式バイナリ配布の一覧 |
| [gfortran for macOS (GitHub)](https://github.com/fxcoudert/gfortran-for-macOS/releases) | macOS 向けスタンドアロン gfortran インストーラ |
| [Homebrew](https://brew.sh/) | macOS 用パッケージマネージャ |
| [MSYS2](https://www.msys2.org/) | Windows 向け開発環境（gfortran 含む） |
| [MinGW-w64 — Getting Started with MSYS2](https://www.mingw-w64.org/getting-started/msys2/) | MSYS2 で GCC/gfortran を使う手順 |
| [WSL インストール — Microsoft Learn](https://learn.microsoft.com/ja-jp/windows/wsl/install) | Windows 上で Linux 開発環境を使う方法 |

### Python

| サイト | 内容 |
|--------|------|
| [Download Python — python.org](https://www.python.org/downloads/) | Python 公式ダウンロード |
| [Python ドキュメント — 目次](https://docs.python.org/ja/3/) | Python 公式ドキュメント（日本語） |
| [Python on Windows](https://docs.python.org/3/using/windows.html) | Windows 向け Python 利用ガイド |
| [Python on macOS](https://docs.python.org/3/using/mac.html) | macOS 向け Python 利用ガイド |
| [pip ユーザーガイド](https://pip.pypa.io/en/stable/user_guide/) | pip（ライブラリ管理）の使い方 |

### 本レッスンで使う Python ライブラリ

| サイト | 内容 |
|--------|------|
| [NumPy ユーザーガイド](https://numpy.org/doc/stable/user/index.html) | 数値計算ライブラリ |
| [pandas ドキュメント](https://pandas.pydata.org/docs/) | CSV 読み込み・データ操作 |
| [Matplotlib チュートリアル](https://matplotlib.org/stable/tutorials/index.html) | グラフ描画 |

### 数値計算・差分法（学習の参考）

| サイト | 内容 |
|--------|------|
| [有限差分法 — Wikipedia（日本語）](https://ja.wikipedia.org/wiki/%E6%9C%89%E9%99%90%E5%B7%AE%E5%88%86%E6%B3%95) | 差分法の概要 |
| [数値微分 — Wikipedia（日本語）](https://ja.wikipedia.org/wiki/%E6%95%B0%E5%80%A4%E5%BE%AE%E5%88%86) | 数値微分の基本概念 |
| [Fortran 入門 — 国立天文台](https://www.nao.ac.jp/contents/about-naoj/reports/fortran/fortran.html) | Fortran 文法の日本語解説 |
