# Lesson02: 1 次元熱伝導
# Fortran で計算 → Python で描画（plplot 不要）

F95      ?= gfortran
F95FLAGS ?= -O2

SRC_DIR  = src
SOURCE   = $(SRC_DIR)/thermal_diffusion.f95
TARGET   = $(SRC_DIR)/thermal_diffusion

PYTHON   ?= python3

.DEFAULT_GOAL := all

.PHONY: all deps run plot plot-show all-results clean

all: $(TARGET)

$(TARGET): $(SOURCE)
	@echo "$(F95) $(F95FLAGS) -o $@ $<"
	@NIX_CFLAGS_COMPILE= NIX_LDFLAGS= $(F95) $(F95FLAGS) -o $@ $<

# Python ライブラリのインストール
# Nix devShell (~/aqwa) では pythonEnv に同梱済み → make deps 不要
deps:
	@if $(PYTHON) -c "import matplotlib, pandas, numpy" 2>/dev/null; then \
		echo "matplotlib / pandas / numpy は既に利用可能です（make deps 不要）。"; \
	elif $(PYTHON) -m pip --version >/dev/null 2>&1; then \
		$(PYTHON) -m pip install -r requirements.txt; \
	else \
		echo "pip が見つかりません。Nix では: cd ~/aqwa && nix develop"; \
		exit 1; \
	fi

run: $(TARGET)
	cd $(SRC_DIR) && ./thermal_diffusion

plot:
	cd $(SRC_DIR) && $(PYTHON) main.py

# 描画後に画像ビューアで開く
plot-show:
	cd $(SRC_DIR) && $(PYTHON) main.py --show

all-results: run plot

clean:
	rm -f $(TARGET) thermal_diffusion
	rm -f $(SRC_DIR)/grid.csv $(SRC_DIR)/output.csv $(SRC_DIR)/thermal_diffusion.png
