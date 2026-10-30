install:
	pip install -e .[dev]

experiment:
	PYTHONPATH=src python scripts/run_experiment.py

test:
	PYTHONPATH=src python -m unittest discover -s tests -v


sensitivity:
	PYTHONPATH=src python scripts/run_seed_sensitivity.py
