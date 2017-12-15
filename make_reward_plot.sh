#!/bin/bash
set -euo pipefail

python run_baseline.py
python run_soso.py
python run_oracle.py
python gen_plot.py
