# Deep Learning-Based Spectrum Sensing under Partial Observations

This repository contains a B.Tech. project on cognitive radio spectrum sensing using PlutoSDR/GNU Radio experimentation, PSD logging, synthetic dataset generation, and starter deep-learning baselines.

## Highlights

- PlutoSDR + GNU Radio transmitter/receiver flowgraphs for real spectrum capture
- Custom PSD logger that exports CSV and PyTorch `.pth` artifacts
- Synthetic multi-PU/multi-SU dataset generation based on measured PSD libraries
- Starter recurrent training pipeline aligned with the report narrative
- Utility scripts and notebooks for quick result inspection

## Repository Status

- `hardware/` contains the SDR-side GNU Radio assets.
- `simulation/` and `data/` cover dataset generation and checked-in sample artifacts.
- `training/` provides a baseline reconstruction for reproducible experimentation.
- `docs/assets/` preserves the submitted project report and presentation.

## System Overview

```mermaid
flowchart LR
    A[Symbol Binaries] --> B[Primary User Transmitter]
    B --> C[PlutoSDR Air Interface]
    C --> D[Secondary User Receiver]
    D --> E[PSD Logger]
    E --> F[data/sample_results]
    F --> G[single_pu_su_to_multi_pu_su_dataset.py]
    G --> H[data/generated_datasets]
    H --> I[training/train.py]
    I --> J[Checkpoints and Metrics]
```

## What is in this repo

- `hardware/`: GNU Radio transmitter/receiver assets for the Primary User and Secondary User sides.
- `simulation/`: synthetic dataset generation from real PSD captures.
- `data/`: sample result artifacts plus ignored runtime/generated data directories.
- `models/` and `training/`: starter recurrent baselines for generated datasets.
- `scripts/`: artifact inspection and plotting utilities.
- `notebooks/`: quick PSD exploration notebook.
- `docs/`: project guides plus submitted report/presentation assets.

## Project workflow

1. A Primary User transmitter sends modulated symbols with PlutoSDR.
2. A Secondary User receiver captures complex I/Q samples using PlutoSDR.
3. A custom logger computes PSD, estimates SNR, and stores CSV/PyTorch outputs.
4. Real PSD captures are reused as a library to generate larger synthetic multi-user datasets with path loss, shadowing, frequency drift, and AWGN.
5. Those datasets are intended for recurrent spectrum-sensing models discussed in the report.

## Repository layout

```text
BTP1/
├── hardware/
├── simulation/
├── data/
├── models/
├── training/
├── scripts/
├── notebooks/
├── docs/
├── configs/
├── requirements.txt
└── README.md
```

## Quick start

### 1. Review the documentation

- Start with [`docs/project-summary.md`](docs/project-summary.md)
- Then read [`docs/hardware-and-data-flow.md`](docs/hardware-and-data-flow.md)
- For file formats and outputs, see [`docs/data-artifacts.md`](docs/data-artifacts.md)
- For reproducibility and structure, see [`docs/reproducibility.md`](docs/reproducibility.md) and [`docs/repo-map.md`](docs/repo-map.md)

### 2. Install dependencies

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

For GNU Radio, PlutoSDR, and driver setup, use [`INSTALL.md`](INSTALL.md).

### 3. Run the PU transmitter

The generated Python script now uses a relative symbol file by default:

```powershell
cd hardware\pu_transmitter
python primary_user_transmitter.py
```

Optional environment variables:

- `BTP_SYMBOL_FILE`: choose a different input symbol file
- `BTP_PLUTO_TX_URI`: override the PlutoSDR TX URI

### 4. Run the SU receiver flowgraph

Use `hardware/su_receiver/secondary_user_receiver.grc` as the main GNU Radio receiver flowgraph. The standalone `psd_logger.py` file is the reusable logger-block implementation/reference, and its output paths now default to `data/runtime_captures/`.

Optional environment variables:

- `BTP_OUTPUT_DIR`: where CSV/PTH capture files should be saved
- `BTP_CAPTURE_PREFIX`: filename prefix for the capture set

### 5. Generate synthetic datasets

`simulation/single_pu_su_to_multi_pu_su_dataset.py` reads input PSD libraries from `data/sample_results/` by default and writes generated datasets to `data/generated_datasets/`.

```powershell
cd simulation
python single_pu_su_to_multi_pu_su_dataset.py
```

Optional environment variables:

- `BTP_DATA_DIR`: base folder containing the modulation `.pth` libraries
- `BTP_GENERATED_DATA_DIR`: output folder for generated datasets

### 6. Use the helper utilities

```powershell
python scripts\inspect_pth.py data\sample_results\psd_log_BPSK.pth
python scripts\summarize_results.py data\sample_results
python scripts\plot_psd_sample.py data\sample_results\psd_log_QPSK.pth --index 0
python scripts\validate_artifacts.py data\sample_results
python scripts\plot_training_history.py checkpoints\lstm_best.pt --save artifacts\lstm_history.png
```

## Data Quality Note

The checked-in sample artifacts are mostly consistent, but `psd_log_16QAM.pth` and `psd_binned_by_snr_16QAM.pth` appear incomplete compared to the corresponding CSV. The validator script reports this explicitly so future users do not assume every sample artifact is equally complete.

### 7. Train the starter recurrent baseline

```powershell
python training\train.py --dataset <generated-dataset.pth> --model lstm
python training\evaluate.py --checkpoint checkpoints\lstm_best.pt --dataset <generated-dataset.pth>
```

## Important note on scope

The report and slides describe a broader research codebase than the files originally present here. The added `models/` and `training/` folders provide a clean baseline scaffold so the repository is runnable and easier to extend, but they should be treated as reconstructed starter code rather than a verified copy of the exact original experiment scripts.

## Hardware/software dependencies

- ADALM-Pluto SDR
- GNU Radio 3.10.x
- PyQt5
- libiio / GNU Radio IIO blocks
- Python 3
- `numpy`, `torch`

## Reproducibility files

- [`requirements.txt`](requirements.txt)
- [`INSTALL.md`](INSTALL.md)
- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md)
- [`configs/train_config.json`](configs/train_config.json)
- [`CITATION.cff`](CITATION.cff)
- [`LICENSE`](LICENSE)

## Included Project Assets

- [`docs/assets/reports/final_report.pdf`](docs/assets/reports/final_report.pdf)
- [`docs/assets/reports/midsem_report.pdf`](docs/assets/reports/midsem_report.pdf)
- [`docs/assets/presentations/endsem_presentation.pptx`](docs/assets/presentations/endsem_presentation.pptx)

## Supporting documents

- [`docs/project-summary.md`](docs/project-summary.md)
- [`docs/hardware-and-data-flow.md`](docs/hardware-and-data-flow.md)
- [`docs/data-artifacts.md`](docs/data-artifacts.md)
- [`docs/reproducibility.md`](docs/reproducibility.md)
- [`docs/repo-map.md`](docs/repo-map.md)
- [`docs/references.md`](docs/references.md)
