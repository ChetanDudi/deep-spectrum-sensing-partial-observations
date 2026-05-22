# Contributing

This project mixes GNU Radio flowgraphs, SDR capture utilities, synthetic dataset generation, and PyTorch-based baselines. Keep changes small, documented, and easy to verify.

## Recommended workflow

1. Update or add documentation when folder names, commands, or outputs change.
2. Keep generated data out of Git-tracked folders unless it is an intentional sample artifact.
3. Prefer portable paths over machine-specific absolute paths.
4. Validate artifacts with:

```powershell
python scripts\validate_artifacts.py data\sample_results
```

5. Syntax-check edited Python files before committing.

## Directory ownership

- `hardware/`
  GNU Radio and SDR-side files.

- `simulation/`
  Synthetic dataset generation pipeline.

- `training/` and `models/`
  Reconstructed ML baseline code.

- `data/`
  Checked-in example artifacts and ignored runtime/generated outputs.

- `docs/`
  Repository documentation and report assets.

## Style expectations

- Use clear, descriptive names.
- Avoid hardcoded local filesystem paths.
- Keep scripts runnable from the repository root when possible.
- Document environment variables when introducing them.
