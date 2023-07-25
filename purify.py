from pathlib import Path
import re
import matplotlib.pyplot as plt
import numpy as np

header = """Filetype: Flipper SubGhz RAW File
Version: 1
Frequency: 868950000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
"""

src_file = Path("Blinds.sub")
dst_file = Path("blinds_sig3.sub")

# src_file = Path("blinds_sig2.sub")

with src_file.open("r") as f:
    contents = f.read().replace("\r\n", "\n")

assert contents.startswith(header)
contents = contents[len(header):]

# all_vals = []

short_signal = 418
long_signal = 836

def decode_length(val):
    absv = np.abs(val)

    if np.abs(np.abs(absv) - short_signal) < 100:
        return "0"
    
    if np.abs(np.abs(absv) - long_signal) < 100:
        return "1"
    
    return f" ({val}) "

def cast_lengths(val):
    absv = np.abs(val)

    if np.abs(np.abs(absv) - short_signal) < 100:
        return short_signal * np.sign(val)
    
    if np.abs(np.abs(absv) - long_signal) < 100:
        return long_signal * np.sign(val)
    
    if np.abs(np.abs(absv) - 5300) < 400:
        return 5300 * np.sign(val)
    
    if np.abs(np.abs(absv) - 10e3) < 100:
        return int(10e3) * np.sign(val)
    
    assert val < -50e3
    return val

with dst_file.open("w", encoding="ascii") as f:
    f.write(header)

    for l in contents.strip().split("\n"):
        m = re.fullmatch(r"RAW_Data:(?P<timings>( -?\d+)+)", l)

        vals = [int(a) for a in m.group("timings").strip().split(" ")]
        new_vals = [cast_lengths(a) for a in vals]

        data_line = " ".join(str(a) for a in new_vals)

        f.write(f"RAW_Data: {data_line}\n")

    # print(vals)
    # print()

    # all_vals.extend(vals)


