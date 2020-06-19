CODE = exchange
TESTS = tests

ALL = $(CODE) $(TESTS)

VENV ?= .venv

venv:
	python3 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install poetry
	$(VENV)/bin/poetry install
	$(VENV)/bin/python setup.py install

currencies:
	$(VENV)/bin/add_default_currencies

test:
	$(VENV)/bin/pytest -v tests

lint:
	$(VENV)/bin/flake8 --jobs 4 --statistics --show-source $(ALL)
	$(VENV)/bin/pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	$(VENV)/bin/black --skip-string-normalization --check $(ALL)
	$(VENV)/bin/mypy $(CODE)

format:
	$(VENV)/bin/isort --apply --recursive $(ALL)
	$(VENV)/bin/black --skip-string-normalization $(ALL)
	$(VENV)/bin/autoflake --recursive --in-place --remove-all-unused-imports $(ALL)
	$(VENV)/bin/unify --in-place --recursive $(ALL)

up:
	FLASK_APP=$(CODE)/app flask run --host 0.0.0.0

db_clear:
	$(VENV)/bin/clear_db


ci:	lint test
