from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch


def load_psd_collection(path: Path):
    obj = torch.load(path, map_location="cpu", weights_only=False)
    if isinstance(obj, dict) and "psds" in obj:
        return obj["psds"]
    raise KeyError(f"No 'psds' key found in {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot a PSD sample from a saved .pth file.")
    parser.add_argument("path", type=Path, help="Path to a .pth file with a 'psds' key")
    parser.add_argument("--index", type=int, default=0, help="PSD index to plot")
    parser.add_argument("--save", type=Path, default=None, help="Optional output image path")
    args = parser.parse_args()

    psds = load_psd_collection(args.path)
    sample = np.asarray(psds[args.index]).reshape(-1)

    plt.figure(figsize=(10, 4))
    plt.plot(sample)
    plt.title(f"{args.path.name} - PSD sample {args.index}")
    plt.xlabel("Frequency bin")
    plt.ylabel("PSD (dB)")
    plt.tight_layout()

    if args.save is not None:
        args.save.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(args.save, dpi=150)
        print(f"Saved plot to {args.save}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
