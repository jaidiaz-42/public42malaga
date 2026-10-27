.DEFAULT_GOAL := help
MSG ?= Actualizacion automatica

.PHONY: install run debug clean lint lint-strict


export UV_CACHE_DIR := $(shell [ -d /sgoinfre/students/$(USER) ] && echo /sgoinfre/students/$(USER)/uv-cache || echo $(HOME)/.cache/uv)
export HF_HOME := $(shell [ -d /sgoinfre/students/$(USER) ] && echo /sgoinfre/students/$(USER)/hf-cache || echo $(HOME)/.cache/huggingface)

install:
	mkdir -p $(UV_CACHE_DIR)
	uv sync

run:
	mkdir -p $(HF_HOME)
	uv run python -m src

gitup: 
	make clean
	git add .
	git commit -m "$(MSG)"
	git push

debug:
	mkdir -p $(HF_HOME)
	uv run python -m pdb -m src

clean:
	rm -rf __pycache__ src/__pycache__ .mypy_cache .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict

help:
	@echo "Available targets:"
	@echo "  install      - Install dependencies"
	@echo "  run          - Run the application"
	@echo "  debug        - Run the application in debug mode"
	@echo "  clean        - Clean up temporary files"
	@echo "  lint         - Run linting and type checking"
	@echo "  lint-strict  - Run strict linting and type checking"
	@echo "  gitup        - Commit and push changes"
	@echo "  help         - Show this help message"
