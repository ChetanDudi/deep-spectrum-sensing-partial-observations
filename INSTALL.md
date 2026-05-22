# Installation And Setup

This guide covers the software environment, PlutoSDR prerequisites, and the main commands needed to run the project from a fresh clone.

## 1. Clone and enter the repository

```powershell
git clone <your-repo-url>
cd BTP1
```

## 2. Create a Python environment

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Install GNU Radio and SDR dependencies

This repository uses GNU Radio flowgraphs and PlutoSDR IIO blocks, so Python packages alone are not enough.

Required system tools:

- GNU Radio `3.10.x`
- PyQt5 compatible with your GNU Radio build
- Analog Devices PlutoSDR drivers
- `libiio`
- GNU Radio IIO blocks / gr-iio

Typical Windows setup:

1. Install GNU Radio with the IIO/Pluto modules enabled.
2. Install Analog Devices PlutoSDR USB/Ethernet drivers.
3. Confirm Pluto connectivity using the IIO tools or GNU Radio device discovery.

## 4. Verify the repository layout

Important paths:

- `hardware/pu_transmitter/primary_user_transmitter.grc`
- `hardware/pu_transmitter/primary_user_transmitter.py`
- `hardware/su_receiver/secondary_user_receiver.grc`
- `hardware/su_receiver/psd_logger.py`
- `simulation/single_pu_su_to_multi_pu_su_dataset.py`
- `data/sample_results/`

## 5. Optional runtime environment variables

The repo now supports portable path overrides:

- `BTP_SYMBOL_FILE`
  Input symbol file for the PU transmitter.

- `BTP_PLUTO_TX_URI`
  PlutoSDR transmitter URI, for example `ip:192.168.2.2`.

- `BTP_OUTPUT_DIR`
  Output directory for receiver capture logs.

- `BTP_CAPTURE_PREFIX`
  Prefix for generated receiver log files.

- `BTP_DATA_DIR`
  Base folder containing modulation `.pth` libraries for dataset generation.

- `BTP_GENERATED_DATA_DIR`
  Output directory for generated synthetic datasets.

Example:

```powershell
$env:BTP_PLUTO_TX_URI="ip:192.168.2.2"
$env:BTP_OUTPUT_DIR="$PWD\\data\\runtime_captures"
```

## 6. Run the PU transmitter

```powershell
cd hardware\pu_transmitter
python primary_user_transmitter.py
```

This uses `input_bins/symbols_01.bin` by default unless `BTP_SYMBOL_FILE` is set.

## 7. Run the SU receiver flowgraph

Use GNU Radio Companion to open and run:

```text
hardware/su_receiver/secondary_user_receiver.grc
```

The custom PSD logger embedded in that flowgraph writes CSV/PTH artifacts. The standalone `psd_logger.py` file is included as the reusable logger implementation reference.

## 8. Generate synthetic datasets

```powershell
cd simulation
python single_pu_su_to_multi_pu_su_dataset.py
```

By default this reads modulation libraries from `data/sample_results/` and saves generated datasets under `data/generated_datasets/`.

## 9. Inspect result files

Example commands:

```powershell
python scripts\inspect_pth.py data\sample_results\psd_log_BPSK.pth
python scripts\summarize_results.py data\sample_results
python scripts\plot_psd_sample.py data\sample_results\psd_log_QPSK.pth --index 0
```

## 10. Train the starter recurrent models

Once you have generated a dataset from `single_pu_su_to_multi_pu_su_dataset.py`, you can use the included starter training pipeline:

```powershell
python training\train.py --dataset <path-to-generated-dataset.pth> --model lstm
python training\evaluate.py --checkpoint checkpoints\latest.pt --dataset <path-to-generated-dataset.pth>
```

## Troubleshooting

- If GNU Radio cannot see PlutoSDR, verify the device URI and IIO driver installation.
- If `torch.load` fails on older `.pth` files, keep `weights_only=False` when reading project data artifacts.
- If plots do not display in PowerShell, use the `--save` option in the plotting script to write an image instead.
