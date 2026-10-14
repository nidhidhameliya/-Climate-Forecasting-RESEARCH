"""A recurrent ConvLSTM baseline for gridded sequence forecasting."""

from __future__ import annotations

import torch
from torch import nn


class ConvLSTMCell(nn.Module):
    """Single ConvLSTM cell with convolutional input-to-state transitions."""

    def __init__(self, input_channels: int, hidden_channels: int, kernel_size: int = 3):
        super().__init__()
        if kernel_size % 2 == 0:
            raise ValueError("kernel_size must be odd to preserve spatial dimensions")
        self.hidden_channels = hidden_channels
        self.gates = nn.Conv2d(
            input_channels + hidden_channels,
            4 * hidden_channels,
            kernel_size=kernel_size,
            padding=kernel_size // 2,
        )

    def forward(self, x: torch.Tensor, state: tuple[torch.Tensor, torch.Tensor]):
        hidden, cell = state
        input_gate, forget_gate, output_gate, candidate = self.gates(
            torch.cat((x, hidden), dim=1)
        ).chunk(4, dim=1)
        input_gate = torch.sigmoid(input_gate)
        forget_gate = torch.sigmoid(forget_gate)
        output_gate = torch.sigmoid(output_gate)
        candidate = torch.tanh(candidate)
        cell = forget_gate * cell + input_gate * candidate
        hidden = output_gate * torch.tanh(cell)
        return hidden, cell


class RecurrentConvLSTM(nn.Module):
    """One-layer recurrent ConvLSTM baseline followed by a spatial projection.

    Input shape is (batch, time, channels, height, width), matching the
    repository's saved seven-day temperature tensors.
    """

    def __init__(self, config: dict):
        super().__init__()
        hidden_channels = int(config["model"].get("hidden_dim", 32))
        self.cell = ConvLSTMCell(input_channels=1, hidden_channels=hidden_channels)
        self.projection = nn.Conv2d(hidden_channels, 1, kernel_size=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.ndim != 5 or x.shape[2] != 1:
            raise ValueError(f"Expected (B,T,1,H,W) input, got {tuple(x.shape)}")
        batch, _, _, height, width = x.shape
        hidden = x.new_zeros((batch, self.cell.hidden_channels, height, width))
        cell = torch.zeros_like(hidden)
        for time_index in range(x.shape[1]):
            hidden, cell = self.cell(x[:, time_index], (hidden, cell))
        return self.projection(hidden)
