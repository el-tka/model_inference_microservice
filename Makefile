.PHONY: install run lint test coverage docker-build docker-up docker-down clean

.DEFAULT_GOAL := test

install:
	poetry install

run: install
	cd app && poetry run python run.py

lint:
	poetry run flake8 app/ tests/

test:
	poetry run pytest tests/ -v

coverage:
	poetry run pytest --cov=app tests/

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

clean:
	poetry run python -c "import pathlib, shutil, os, stat; fix = lambda f: (os.chmod(f, stat.S_IWRITE | stat.S_IREAD), os.unlink(f)); [(shutil.rmtree(p, onerror=lambda func, path, exc: (os.chmod(path, stat.S_IWRITE | stat.S_IREAD), func(path)))) for p in pathlib.Path('.').rglob('__pycache__') if p.exists()]"


