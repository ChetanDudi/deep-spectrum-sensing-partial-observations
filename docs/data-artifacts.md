# Data Artifacts

## `data/sample_results/` contents

The `data/sample_results/` folder currently stores example PSD logs for multiple modulation types:

- `psd_log_BPSK.csv` / `.pth`
- `psd_log_QPSK.csv` / `.pth`
- `psd_log_8PSK.csv` / `.pth`
- `psd_log_16QAM.csv` / `.pth`
- `psd_binned_by_snr_*.pth`

## CSV format

The capture logger writes four columns:

- `Timestamp`
- `Mean_PSD_dB`
- `SNR_dB`
- `PU_Present`

This is the quick human-readable format for debugging and inspection.

## PTH format

The main `.pth` output is a Python dictionary saved with `torch.save`. In the current logger implementation it stores lists such as:

- `timestamps`
- `snrs`
- `psds`
- `mean_psds`
- `pu_flags`
- `pu_labels`

Each saved PSD is shaped like `(192, 1)`.

## Binned-by-SNR format

The binned `.pth` structure groups examples by nearest SNR bin. It contains:

- `bins`
- `pairs_by_bin`

Each `pairs_by_bin[bin]` entry stores `(psd, label)` pairs.

## Synthetic dataset generator assumptions

`simulation/single_pu_su_to_multi_pu_su_dataset.py` assumes:

- 10 PUs
- 10 SUs
- 20 channels
- 64 frequency bins per channel
- 192-bin PSD inputs split into:
  - left leakage: `0..63`
  - main region: `64..127`
  - right leakage: `128..191`

## New default output locations

To make the project clone-friendly:

- runtime SDR captures now default to `data/runtime_captures/`
- generated synthetic datasets now default to `data/generated_datasets/`

Both directories are ignored in `.gitignore` so future generated files do not clutter the repository.
