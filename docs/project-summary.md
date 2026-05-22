# Project Summary

## Problem

The project studies wideband spectrum sensing in cognitive radio networks when each Secondary User (SU) observes only part of the spectrum. The core challenge is detecting Primary User (PU) activity reliably at low SNR under partial observations.

## Main idea

The work combines two pieces:

1. A real SDR measurement pipeline using ADALM-Pluto and GNU Radio.
2. A synthetic dataset generator that expands real captured PSD traces into larger multi-user datasets for deep learning experiments.

## What the report/slides say the project covers

- Recurrent deep learning models for PU detection: `RNN`, `LSTM`, `Bi-LSTM`, `GRU`, and an enhanced gated LSTM.
- Comparison against collaborative CNN-style ideas from the literature.
- Real over-the-air capture of modulation-specific PSDs using PlutoSDR.
- Conversion of real PSD libraries into larger datasets with realistic wireless impairments.

## What is actually present in this repository

- GNU Radio transmitter flowgraph and generated Python for the PU side.
- GNU Radio receiver-side custom PSD logging block.
- A simulation script that creates synthetic multi-PU/multi-SU datasets from saved PSD libraries.
- Example `.csv` and `.pth` capture artifacts.
- Mid-semester PDF, final report PDF, and end-semester presentation.

## What is not present in this snapshot

The training and evaluation scripts for the deep learning models mentioned in the report are not included here. If you later add them, this repository structure is already set up to document them cleanly.
