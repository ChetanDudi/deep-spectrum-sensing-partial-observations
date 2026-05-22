# Project Structure

This file gives a compact, high-signal overview of the core repository layout.

```text
BTP1/
├── hardware/
│   ├── pu_transmitter/
│   │   ├── primary_user_transmitter.grc
│   │   ├── primary_user_transmitter.py
│   │   └── input_bins/
│   └── su_receiver/
│       ├── secondary_user_receiver.grc
│       └── psd_logger.py
├── simulation/
│   └── single_pu_su_to_multi_pu_su_dataset.py
├── data/
│   ├── sample_results/
│   ├── runtime_captures/        # gitignored
│   └── generated_datasets/      # gitignored
├── models/
│   └── recurrent.py
├── training/
│   ├── train.py
│   ├── evaluate.py
│   ├── dataset.py
│   └── common.py
├── scripts/
├── docs/
│   ├── assets/
│   └── *.md
├── configs/
│   └── train_config.json
├── README.md
├── INSTALL.md
├── CONTRIBUTING.md
├── requirements.txt
├── LICENSE
└── CITATION.cff
```

## Core project path

If someone only wants the main technical flow, the most important folders are:

1. `hardware/`
2. `simulation/`
3. `data/sample_results/`
4. `training/`
5. `models/`
