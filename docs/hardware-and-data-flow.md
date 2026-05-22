# Hardware And Data Flow

## End-to-end pipeline

1. `hardware/pu_transmitter/primary_user_transmitter.grc` and `primary_user_transmitter.py` generate and transmit modulated symbols.
2. `hardware/su_receiver/secondary_user_receiver.grc` receives the signal using PlutoSDR.
3. The custom Python block in `hardware/su_receiver/secondary_user_receiver.grc` / `psd_logger.py` computes PSD and SNR.
4. Outputs are saved as:
   - CSV logs for quick inspection
   - `.pth` files for downstream ML/data processing
   - SNR-binned `.pth` files for grouped training inputs
5. `simulation/single_pu_su_to_multi_pu_su_dataset.py` uses the captured PSD libraries to generate larger realistic datasets.

## PU transmitter

Path: `hardware/pu_transmitter/`

Key points:

- Uses a `File Source` with pre-generated symbol binaries.
- Applies digital modulation.
- Sends the resulting complex baseband stream to PlutoSDR.
- Also shows the spectrum on a Qt frequency sink for monitoring.

Current default runtime settings from the generated Python:

- Center frequency: `2.4 GHz`
- Sample rate: `1.024 MHz`
- Pluto URI: `ip:192.168.2.2`

## SU receiver and logger

Path: `hardware/su_receiver/`

Key points:

- Receives complex I/Q samples from PlutoSDR.
- Computes a 192-bin PSD by taking a short FFT and applying `fftshift`.
- Estimates SNR as:
  - `mean_psd - 10th_percentile_noise_floor`
- Declares PU presence using a threshold-based rule.
- Periodically saves cumulative logs to disk.

Receiver values visible in the provided flowgraph/slides:

- Center frequency: `2.4 GHz`
- Sample rate: about `1.024 MHz`
- RF bandwidth: `20 MHz`

## Why the simulation exists

The real SDR setup is enough to validate a single PU-to-SU link, but it does not create enough diversity or scale for large deep learning experiments. The simulator reuses measured PSD shapes and adds:

- channel gain / path loss
- log-normal shadowing
- frequency drift
- AWGN
- partial observation constraints across SUs

That makes it possible to synthesize multi-user occupancy datasets while keeping the spectra closer to real captures than purely artificial signals.
