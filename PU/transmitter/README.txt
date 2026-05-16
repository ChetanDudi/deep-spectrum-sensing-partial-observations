Transmitter Symbol Data Files
====================================

These files contain randomly generated digital symbols or bits for each modulation scheme.
They are ready to be used as input to your GNU Radio transmitter flowgraph (File Source block).

Files:
------
- bpsk_symbols.bin   → symbol values 0–1
- qpsk_symbols.bin   → symbol values 0–3
- 8psk_symbols.bin   → symbol values 0–7
- qam16_symbols.bin  → symbol values 0–15
- qam64_symbols.bin  → symbol values 0–63
- gfsk_bits.bin      → packed bits (for GFSK modulation)

Usage in GNU Radio Companion:
-----------------------------
Example for QPSK:
    File Source (qpsk_symbols.bin, Repeat=True)
         ↓
    Constellation Object (QPSK)
         ↓
    Constellation Modulator
         ↓
    PlutoSDR Sink (TX)

For GFSK:
    File Source (gfsk_bits.bin, Repeat=True)
         ↓
    Unpack K Bits (8)
         ↓
    GFSK Mod
         ↓
    PlutoSDR Sink

Each file has 2 million random symbols (or bits for GFSK). You can repeat transmission indefinitely.
