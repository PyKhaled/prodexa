# ─────────────────────────────────────────────
# Prodexa Makefile
# ─────────────────────────────────────────────

APP_NAME := Prodexa
PACKAGE := prodexa
ENTRY := $(PACKAGE)/__main__.py
DIST_DIR := dist
BUILD_DIR := build
ICON_DIR := $(PACKAGE)/assets/icons

PYTHON := python
VERSION := $(shell $(PYTHON) -c "from prodexa.__version__ import __version__; print(__version__)")

OS := $(shell uname -s)

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

.PHONY: help
help:
	@echo "Prodexa build commands:"
	@echo ""
	@echo "  make run        Run app locally"
	@echo "  make build      Build standalone app"
	@echo "  make clean      Remove build artifacts"
	@echo "  make version    Print current version"
	@echo ""

# ─────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────

.PHONY: run
run:
	$(PYTHON) -m $(PACKAGE)

# ─────────────────────────────────────────────
# Build
# ─────────────────────────────────────────────

.PHONY: build
build:
	@echo "🔧 Building $(APP_NAME) v$(VERSION)"
	@mkdir -p $(DIST_DIR) $(BUILD_DIR)

ifeq ($(OS),Darwin)
	$(PYTHON) -m PyInstaller \
		--name $(APP_NAME)-$(VERSION) \
		--windowed \
		--icon $(ICON_DIR)/app.icns \
		--clean \
		--noconfirm \
		--distpath $(DIST_DIR) \
		--workpath $(BUILD_DIR) \
		--add-data "$(PACKAGE)/assets:$(PACKAGE)/assets" \
		--add-data "$(PACKAGE)/resources:$(PACKAGE)/resources" \
		$(ENTRY)
else ifeq ($(OS),Linux)
	$(PYTHON) -m PyInstaller \
		--name $(APP_NAME)-$(VERSION) \
		--clean \
		--noconfirm \
		--distpath $(DIST_DIR) \
		--workpath $(BUILD_DIR) \
		--add-data "$(PACKAGE)/assets:$(PACKAGE)/assets" \
		--add-data "$(PACKAGE)/resources:$(PACKAGE)/resources" \
		$(ENTRY)
else
	$(PYTHON) -m PyInstaller \
		--name $(APP_NAME)-$(VERSION) \
		--windowed \
		--icon $(ICON_DIR)/app.ico \
		--clean \
		--noconfirm \
		--distpath $(DIST_DIR) \
		--workpath $(BUILD_DIR) \
		--add-data "$(PACKAGE)/assets;$(PACKAGE)/assets" \
		--add-data "$(PACKAGE)/resources;$(PACKAGE)/resources" \
		$(ENTRY)
endif

	@echo "✅ Build finished: $(DIST_DIR)/$(APP_NAME)-$(VERSION)"

# ─────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────

.PHONY: clean
clean:
	rm -rf $(DIST_DIR) $(BUILD_DIR) *.spec

.PHONY: version
version:
	@echo $(VERSION)