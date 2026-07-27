PYTHON = python3
PIP = pip3

.PHONY: install run debug clean lint lint-strict

install:
	$(PIP) install --break-system-packages flake8 mypy

run:
	$(PYTHON) main.py $(ARGS)

debug:
	$(PYTHON) -m pdb main.py $(ARGS)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
