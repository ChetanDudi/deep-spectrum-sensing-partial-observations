from __future__ import annotations

from pathlib import Path
from typing import Tuple

import torch
from torch.utils.data import Dataset


def _normalize_su_tensor(su_tensor: torch.Tensor) -> torch.Tensor:
    tensor = torch.as_tensor(su_tensor, dtype=torch.float32)
    if tensor.dim() == 3 and tensor.shape[0] == 1:
        tensor = tensor.squeeze(0)
    if tensor.shape != (64, 20):
        raise ValueError(f"Expected SU tensor shape (64, 20), got {tuple(tensor.shape)}")
    return tensor.transpose(0, 1).contiguous()


def _normalize_sample(sample) -> torch.Tensor:
    su_tensors = [_normalize_su_tensor(su) for su in sample]
    return torch.stack(su_tensors, dim=0)


class SpectrumDataset(Dataset):
    def __init__(self, dataset_path: str | Path, split: str = "training") -> None:
        dataset_path = Path(dataset_path)
        data = torch.load(dataset_path, map_location="cpu", weights_only=False)

        if split == "training":
            samples = data["training data list"]
            labels = data["training label list"]
        elif split == "testing":
            samples = data["testing data list"]
            labels = data["testing label list"]
        else:
            raise ValueError("split must be 'training' or 'testing'")

        self.inputs = [_normalize_sample(sample) for sample in samples]
        self.labels = [torch.as_tensor(label, dtype=torch.float32) for label in labels]

    def __len__(self) -> int:
        return len(self.inputs)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.inputs[index], self.labels[index]
