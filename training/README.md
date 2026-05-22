# Training Scaffold

This folder contains a starter training pipeline added to align the repository with the project report.

## What it does

- loads generated datasets saved by `simulation/single_pu_su_to_multi_pu_su_dataset.py`
- converts each sample into a collaborative tensor of shape:
  - `num_su x num_bands x bins`
- trains a recurrent per-band classifier
- saves checkpoints and basic validation history

## Included model variants

- `lstm`
- `bilstm`
- `gru`
- `rnn`

## Important note

These scripts are baseline scaffolding for this repository snapshot. They are not guaranteed to be the exact original experiment code used for the final report.
