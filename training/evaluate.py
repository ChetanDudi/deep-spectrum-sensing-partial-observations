from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np
import torch
from torch.utils.data import DataLoader

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from models.recurrent import RecurrentSpectrumModel
from training.dataset import SpectrumDataset


def binary_auc(y_true: np.ndarray, y_score: np.ndarray) -> float:
    positives = y_true.sum()
    negatives = len(y_true) - positives
    if positives == 0 or negatives == 0:
        return float("nan")

    order = np.argsort(-y_score)
    y_true = y_true[order]
    y_score = y_score[order]

    tps = np.cumsum(y_true)
    fps = np.cumsum(1 - y_true)
    tpr = tps / positives
    fpr = fps / negatives

    tpr = np.concatenate([[0.0], tpr, [1.0]])
    fpr = np.concatenate([[0.0], fpr, [1.0]])
    return float(np.trapezoid(tpr, fpr))


def macro_auc(y_true: np.ndarray, y_score: np.ndarray) -> float:
    aucs = []
    for band in range(y_true.shape[1]):
        auc = binary_auc(y_true[:, band], y_score[:, band])
        if not np.isnan(auc):
            aucs.append(auc)
    return float(np.mean(aucs)) if aucs else float("nan")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a saved recurrent baseline checkpoint.")
    parser.add_argument("--checkpoint", required=True, help="Path to a saved .pt checkpoint")
    parser.add_argument("--dataset", required=True, help="Path to the generated dataset .pth file")
    parser.add_argument("--split", default="testing", choices=["training", "testing"])
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    payload = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
    config = payload["config"]

    device = torch.device(args.device)
    dataset = SpectrumDataset(args.dataset, split=args.split)
    loader = DataLoader(dataset, batch_size=int(config["batch_size"]), shuffle=False)

    model = RecurrentSpectrumModel(
        model_type=config["model"],
        hidden_size=int(config["hidden_size"]),
        num_layers=int(config["num_layers"]),
        dropout=float(config["dropout"]),
    ).to(device)
    model.load_state_dict(payload["model_state"])
    model.eval()

    all_logits = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in loader:
            logits = model(inputs.to(device))
            all_logits.append(logits.cpu())
            all_labels.append(labels)

    logits = torch.cat(all_logits, dim=0)
    labels = torch.cat(all_labels, dim=0)
    probs = torch.sigmoid(logits)
    preds = (probs >= 0.5).float()

    metrics = {
        "band_accuracy": float((preds == labels).float().mean().item()),
        "macro_auc": macro_auc(labels.numpy(), probs.numpy()),
        "num_samples": int(labels.shape[0]),
        "num_bands": int(labels.shape[1]),
    }
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
