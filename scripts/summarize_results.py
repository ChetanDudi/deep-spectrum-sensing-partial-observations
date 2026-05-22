from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean

import torch


def summarize_csv(path: Path) -> None:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    print(f"[CSV] {path.name}")
    columns = list(rows[0].keys()) if rows else []
    print(f"  rows={len(rows)} columns={columns}")
    if rows and {"Mean_PSD_dB", "SNR_dB", "PU_Present"}.issubset(columns):
        mean_psd = mean(float(row["Mean_PSD_dB"]) for row in rows)
        mean_snr = mean(float(row["SNR_dB"]) for row in rows)
        pu_rate = mean(float(row["PU_Present"]) for row in rows)
        print(
            "  "
            f"mean_psd={mean_psd:.3f} "
            f"mean_snr={mean_snr:.3f} "
            f"pu_rate={pu_rate:.3f}"
        )


def summarize_pth(path: Path) -> None:
    obj = torch.load(path, map_location="cpu", weights_only=False)
    print(f"[PTH] {path.name}")
    if isinstance(obj, dict):
        print(f"  keys={list(obj.keys())}")
        if "psds" in obj:
            print(f"  psd_examples={len(obj['psds'])}")
        if "snrs" in obj and obj["snrs"]:
            snrs = [float(snr) for snr in obj["snrs"]]
            print(f"  snr_range=({min(snrs):.3f}, {max(snrs):.3f}) mean={mean(snrs):.3f}")
        if "pairs_by_bin" in obj:
            print(f"  bins={list(obj.get('bins', []))[:10]}")
            print(f"  total_pairs={sum(len(v) for v in obj['pairs_by_bin'].values())}")
        if "training data list" in obj:
            print(f"  train_samples={len(obj['training data list'])}")
            print(f"  test_samples={len(obj.get('testing data list', []))}")
    else:
        print(f"  type={type(obj).__name__}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize BTP result artifacts in a folder.")
    parser.add_argument("path", type=Path, help="A result file or directory")
    args = parser.parse_args()

    if args.path.is_file():
        paths = [args.path]
    else:
        paths = sorted(p for p in args.path.iterdir() if p.suffix.lower() in {".csv", ".pth"})

    for path in paths:
        if path.suffix.lower() == ".csv":
            summarize_csv(path)
        elif path.suffix.lower() == ".pth":
            summarize_pth(path)


if __name__ == "__main__":
    main()
