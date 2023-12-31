from pathlib import Path
import numpy as np

from utils import header, get_data_dir

signal = "93cfe01c9f0000c0003210303c0009fce18100009f0f80"

dst_file = get_data_dir() / "blinds_sig1_again.sub"

with dst_file.open("w", encoding="ascii") as f:
    f.write(header)

    signal = bytes.fromhex(signal)
    signal = int.from_bytes(signal, byteorder="big", signed=False)
    signal = [int(a) for a in f"{signal:08b}"]

    signal_bits = np.array(signal).reshape(-1, 2)
    signal_bits = (signal_bits + 1) * 418
    signal_bits[:,1] *= -1

    val = [
        10e3 + 50,
        -418,
        418,
        -418,
        *signal_bits.flatten()
    ]

    assert val[-1] < 0

    # for i in range(0, len(signal), 2):
    #     f.write(f"RAW_Data: {signal[i:i+2]}\n")

    signal_line = " ".join(str(a) for a in val * 4)
    f.write(f"RAW_Data: {signal_line}\n")




