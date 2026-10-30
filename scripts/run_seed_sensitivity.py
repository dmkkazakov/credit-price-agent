"""Run all five prespecified seeds and retain their complete outputs."""
import hashlib
import gzip
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn

ROOT = Path(__file__).resolve().parents[1]
SEEDS = [42, 43, 44, 45, 46]
OUT = ROOT / 'results' / 'seed_sensitivity'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONPATH=str(ROOT / 'src'), OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    runs = []
    for seed in SEEDS:
        dest = OUT / f'seed_{seed}'
        subprocess.run([sys.executable, str(ROOT / 'scripts/run_experiment.py'),
                        '--seed', str(seed), '--output-dir', str(dest)], check=True, env=env)
        runs.append(json.loads((dest / 'metrics.json').read_text()))
    values = [m['agent_vs_risk_only_ev_pct'] for m in runs]
    report = {
        'seeds': SEEDS, 'n_per_seed': 30000,
        'mean_agent_vs_risk_only_ev_pct': float(np.mean(values)),
        'min_agent_vs_risk_only_ev_pct': float(min(values)),
        'max_agent_vs_risk_only_ev_pct': float(max(values)),
        'runs': runs,
        'scope': 'Seed sensitivity under one fixed synthetic DGP; no parameter robustness or real-bank validation.',
        'evaluation': 'Structural acceptance with a shared estimated PD, not fully structural counterfactual default evaluation.',
        'environment': {'python': platform.python_version(), 'numpy': np.__version__,
                        'pandas': pd.__version__, 'scikit_learn': sklearn.__version__},
    }
    (OUT / 'summary.json').write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    # Lossless, deterministic compression keeps all policy rows economical to archive.
    for csv_path in OUT.rglob('*.csv'):
        compressed = csv_path.with_suffix('.csv.gz')
        compressed.write_bytes(gzip.compress(csv_path.read_bytes(), mtime=0))
        csv_path.unlink()
    sources = sorted((ROOT / 'src').rglob('*.py')) + sorted((ROOT / 'scripts').glob('*.py'))
    artifacts = sorted(OUT.rglob('*.json')) + sorted(OUT.rglob('*.csv.gz'))
    manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sources + artifacts if p.name != 'manifest.json'}
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'runs'}, indent=2))


if __name__ == '__main__':
    main()
