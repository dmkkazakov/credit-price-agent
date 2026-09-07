install:
	pip install -e .[dev]

experiment:
	PYTHONPATH=src python scripts/run_experiment.py

test:
	PYTHONPATH=src pytest -q
