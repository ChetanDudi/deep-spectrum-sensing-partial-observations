from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import torch


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot train/validation loss from a saved checkpoint.")
    parser.add_argument("checkpoint", type=Path, help="Checkpoint path produced by training/train.py")
    parser.add_argument("--save", type=Path, default=None, help="Optional output image path")
    args = parser.parse_args()

    payload = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
    history = payload.get("history", [])
    if not history:
        raise ValueError("Checkpoint does not contain history.")

    epochs = [row["epoch"] for row in history]
    train_loss = [row["train_loss"] for row in history]
    val_loss = [row["val_loss"] for row in history]
    val_acc = [row["val_band_accuracy"] for row in history]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(epochs, train_loss, label="train")
    axes[0].plot(epochs, val_loss, label="val")
    axes[0].set_title("Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].legend()

    axes[1].plot(epochs, val_acc, label="val band accuracy")
    axes[1].set_title("Validation Accuracy")
    axes[1].set_xlabel("Epoch")
    axes[1].legend()

    fig.tight_layout()

    if args.save is not None:
        args.save.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(args.save, dpi=150)
        print(f"Saved plot to {args.save}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
