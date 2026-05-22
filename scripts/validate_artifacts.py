from __future__ import annotations

import argparse
import csv
from pathlib import Path

import torch


def validate_csv(path: Path) -> list[str]:
    issues: list[str] = []
    with open(path, "r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        issues.append("empty csv")
        return issues

    required = {"Timestamp", "Mean_PSD_dB", "SNR_dB", "PU_Present"}
    missing = required.difference(rows[0].keys())
    if missing:
        issues.append(f"missing columns: {sorted(missing)}")
    return issues


def validate_pth(path: Path) -> list[str]:
    issues: list[str] = []
    obj = torch.load(path, map_location="cpu", weights_only=False)
    if not isinstance(obj, dict):
        return [f"unexpected top-level type: {type(obj).__name__}"]

    if "psds" in obj:
        psd_count = len(obj["psds"])
        snr_count = len(obj.get("snrs", []))
        if psd_count == 0:
            issues.append("no PSD examples")
        if snr_count and psd_count != snr_count:
            issues.append(f"psd/snrs mismatch: {psd_count}/{snr_count}")

    if "pairs_by_bin" in obj:
        total_pairs = sum(len(v) for v in obj["pairs_by_bin"].values())
        if total_pairs == 0:
            issues.append("no binned pairs")

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate PSD CSV/PTH artifacts for obvious issues.")
    parser.add_argument("path", type=Path, help="A file or directory to validate")
    args = parser.parse_args()

    paths = [args.path] if args.path.is_file() else sorted(
        p for p in args.path.iterdir() if p.suffix.lower() in {".csv", ".pth"}
    )

    had_issue = False
    for path in paths:
        if path.suffix.lower() == ".csv":
            issues = validate_csv(path)
        else:
            issues = validate_pth(path)

        if issues:
            had_issue = True
            print(f"[WARN] {path.name}: " + "; ".join(issues))
        else:
            print(f"[OK]   {path.name}")

    if had_issue:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
