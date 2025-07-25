# Reproducibility Instructions for `ratesb_python` vs `SBMLKinetics` Benchmark

This document provides step-by-step instructions to **replicate the performance comparison** between `ratesb_python` and `SBMLKinetics`, as discussed in the paper titled:

> **"ratesb_python: A Python Package for Analyzing Rate Laws in Biological Models"**

---

## 📦 Environment Setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv benchmark_env
source benchmark_env/bin/activate
```

# Install required packages
```bash
pip install -r requirements.txt
```

benchmark/
├── models/
│   ├── mass_action.ant
│   ├── reversible_mm.ant
│   ├── product_rate.ant
│   ├── custom_law.ant
│   └── ... (more test models)
├── benchmark.py
├── utils.py
├── requirements.txt
└── README.md

To run the benchmark on all test cases:
```bash
python benchmark.py
```
