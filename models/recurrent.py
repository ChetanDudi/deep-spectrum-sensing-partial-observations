from __future__ import annotations

import torch
from torch import nn


class RecurrentSpectrumModel(nn.Module):
    def __init__(
        self,
        model_type: str = "lstm",
        input_size: int = 64,
        hidden_size: int = 128,
        num_layers: int = 2,
        num_bands: int = 20,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        self.model_type = model_type.lower()
        self.num_bands = num_bands

        rnn_kwargs = {
            "input_size": input_size,
            "hidden_size": hidden_size,
            "num_layers": num_layers,
            "batch_first": True,
            "dropout": dropout if num_layers > 1 else 0.0,
        }

        if self.model_type == "rnn":
            self.encoder = nn.RNN(**rnn_kwargs)
            output_size = hidden_size
        elif self.model_type == "gru":
            self.encoder = nn.GRU(**rnn_kwargs)
            output_size = hidden_size
        elif self.model_type == "bilstm":
            self.encoder = nn.LSTM(bidirectional=True, **rnn_kwargs)
            output_size = hidden_size * 2
        else:
            self.encoder = nn.LSTM(**rnn_kwargs)
            output_size = hidden_size

        self.head = nn.Sequential(
            nn.LayerNorm(output_size),
            nn.Linear(output_size, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [batch, num_su, num_bands, bins]
        if x.dim() != 4:
            raise ValueError(f"Expected input shape [batch, su, bands, bins], got {tuple(x.shape)}")

        # Average across SUs to create a collaborative summary per band.
        x = x.mean(dim=1)
        encoded, _ = self.encoder(x)
        logits = self.head(encoded).squeeze(-1)
        return logits
