from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import torch


def summarize_value(key: str, value) -> str:
    if isinstance(value, torch.Tensor):
        return f"tensor shape={tuple(value.shape)} dtype={value.dtype}"
    if isinstance(value, np.ndarray):
        return f"ndarray shape={value.shape} dtype={value.dtype}"
    if isinstance(value, list):
        preview = type(value[0]).__name__ if value else "empty"
        return f"list len={len(value)} first_item_type={preview}"
    if isinstance(value, dict):
        return f"dict keys={list(value.keys())[:10]}"
    return f"{type(value).__name__}: {value}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a torch .pth artifact used in the BTP project.")
    parser.add_argument("path", type=Path, help="Path to a .pth file")
    args = parser.parse_args()

    obj = torch.load(args.path, map_location="cpu", weights_only=False)
    print(f"Loaded: {args.path}")
    print(f"Top-level type: {type(obj).__name__}")

    if isinstance(obj, dict):
        for key, value in obj.items():
            print(f"- {key}: {summarize_value(key, value)}")
    else:
        print(obj)


if __name__ == "__main__":
    main()
