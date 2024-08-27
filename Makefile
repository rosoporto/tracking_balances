install:
	poetry install

load:
	poetry run load

lint:
	poetry run flake8 optima_tg_stock

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl