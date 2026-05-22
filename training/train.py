from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import torch
from torch import nn
from torch.utils.data import DataLoader, random_split

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from models.recurrent import RecurrentSpectrumModel
from training.common import ensure_dir, load_json, set_seed
from training.dataset import SpectrumDataset


def evaluate(model: nn.Module, loader: DataLoader, device: torch.device) -> dict:
    criterion = nn.BCEWithLogitsLoss()
    model.eval()
    total_loss = 0.0
    total_correct = 0
    total_elements = 0

    with torch.no_grad():
        for inputs, labels in loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            logits = model(inputs)
            loss = criterion(logits, labels)
            total_loss += loss.item() * inputs.size(0)

            preds = (torch.sigmoid(logits) >= 0.5).float()
            total_correct += (preds == labels).sum().item()
            total_elements += labels.numel()

    return {
        "loss": total_loss / max(len(loader.dataset), 1),
        "band_accuracy": total_correct / max(total_elements, 1),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a recurrent baseline on a generated BTP dataset.")
    parser.add_argument("--dataset", required=True, help="Path to the generated dataset .pth file")
    parser.add_argument("--config", default="configs/train_config.json", help="Path to a JSON config file")
    parser.add_argument("--model", default=None, help="Override model type: lstm, bilstm, gru, rnn")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--output-dir", default="checkpoints")
    args = parser.parse_args()

    config = load_json(args.config)
    if args.model is not None:
        config["model"] = args.model

    set_seed(int(config["seed"]))
    device = torch.device(args.device)

    full_dataset = SpectrumDataset(args.dataset, split="training")
    train_size = int(len(full_dataset) * float(config["train_split"]))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=int(config["batch_size"]), shuffle=True, num_workers=int(config["num_workers"]))
    val_loader = DataLoader(val_dataset, batch_size=int(config["batch_size"]), shuffle=False, num_workers=int(config["num_workers"]))

    model = RecurrentSpectrumModel(
        model_type=config["model"],
        hidden_size=int(config["hidden_size"]),
        num_layers=int(config["num_layers"]),
        dropout=float(config["dropout"]),
    ).to(device)

    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=float(config["learning_rate"]),
        weight_decay=float(config["weight_decay"]),
    )

    history = []
    best_val_loss = float("inf")
    output_dir = ensure_dir(args.output_dir)
    checkpoint_path = output_dir / f"{config['model']}_latest.pt"

    for epoch in range(1, int(config["epochs"]) + 1):
        model.train()
        running_loss = 0.0

        for inputs, labels in train_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            logits = model(inputs)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)

        train_loss = running_loss / max(len(train_loader.dataset), 1)
        val_metrics = evaluate(model, val_loader, device)
        epoch_metrics = {
            "epoch": epoch,
            "train_loss": train_loss,
            "val_loss": val_metrics["loss"],
            "val_band_accuracy": val_metrics["band_accuracy"],
        }
        history.append(epoch_metrics)
        print(json.dumps(epoch_metrics))

        payload = {
            "model_state": model.state_dict(),
            "config": config,
            "history": history,
        }
        torch.save(payload, checkpoint_path)

        if val_metrics["loss"] < best_val_loss:
            best_val_loss = val_metrics["loss"]
            torch.save(payload, output_dir / f"{config['model']}_best.pt")


if __name__ == "__main__":
    main()
