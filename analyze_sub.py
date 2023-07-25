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

# src_file = Path("blinds_sig2.sub")

src_file = Path("blinds_sig4.sub")

with src_file.open("r") as f:
    contents = f.read().replace("\r\n", "\n")

assert contents.startswith(header)
contents = contents[len(header):]

all_vals = []

short_signal = 418
long_signal = 836

def decode_length(val):
    absv = np.abs(val)

    if np.abs(np.abs(absv) - short_signal) < 100:
        return "0"
    
    if np.abs(np.abs(absv) - long_signal) < 100:
        return "1"
    
    return f" ({val}) "



for l in contents.strip().split("\n"):
    m = re.fullmatch(r"RAW_Data:(?P<timings>( -?\d+)+)", l)

    vals = [int(a) for a in m.group("timings").strip().split(" ")]
    # print(vals)
    # print()

    all_vals.extend(vals)

all_vals = np.array(all_vals)

assert np.all(np.sign(all_vals[::2]) == 1)
assert np.all(np.sign(all_vals[1::2]) == -1)


s = ""

def decode_buffer(buf):
    # buf = buf.lstrip("0")
    if buf == "":
        return ""
    
    return buf

    buf += "0" * (8 - len(buf) % 8)

    bin_data = int(buf, 2).to_bytes((len(buf) + 7) // 8, byteorder="big")
    return bin_data.hex()

def flush_s():
    global s
    if len(s) == 0:
        return
    
    print(decode_buffer(s))
    s = ""

for v in all_vals:
    # if v < 0:
    #     continue

    a = decode_length(v)
    if len(a) == 1:
        s += a
        continue

    flush_s()
    print(a)
    if v < -10e3:
        print()
        
flush_s()


def plot_dur_hist(all_vals):
    # excessive = [a for a in all_vals if np.abs(a) > 3000]
    # print(excessive)

    all_vals = np.array([a for a in all_vals if np.abs(a) < 3000])

    plt.hist(all_vals, bins=100)
    plt.xlabel("Time (us)")
    plt.ylabel("Count")
    plt.show()


