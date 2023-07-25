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
src_file = Path("RAW_20230725-164754.sub")

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

def print_signal(buf):
    is_on = False
    s = ""

    for a in buf:
        dur = {
            "0": 1,
            "1": 2
        }[a]
        ch = {
            # False: ".",
            # True: "+"
            False: "0",
            True: "1"
        }[is_on]
        s += ch * dur

        is_on = not is_on

    assert all(a != b for a, b in zip(s[1::2], s[:-1:2], strict=True))
    print(s[::2])



for l in contents.strip().split("\n"):
    m = re.fullmatch(r"RAW_Data:(?P<timings>( -?\d+)+)", l)

    vals = [int(a) for a in m.group("timings").strip().split(" ")]
    # print(vals)
    # print()

    all_vals.extend(vals)

all_vals = np.array(all_vals)

assert np.all(np.sign(all_vals[::2]) == 1)
assert np.all(np.sign(all_vals[1::2]) == -1)

s = None
s_list = []

for v in all_vals:
    # if v < 0:
    #     continue

    a = decode_length(v)
    if len(a) == 1:
        if s is None:
            print(f"Not in signal: {v}")
            continue

        s += a
        continue

    if np.abs(v - 10e3) < 100:
        if s is not None and len(s) > 0:
            print(f"Discarded: {s}")
        s = ""
        # print(a)
        continue
    

    # if s is not None and len(s) > 0:
    #     s_list += [s]
        # s = ""

    if v < -4000:
        if v is None:
            print(a)
            continue

        if s is None or len(s) == 0:
            print(f"Empty package")
            continue

        # assert s is not None and len(s) > 0

        s_list.append(s)
        s = None

        if len(s_list) < 4:
            continue

        # if v < -50e3:
        # if np.abs(np.abs(absv) - 5300) < 400:
        # if len(s_list) == 0:
        #     print(a)
        #     continue

        # if len(s_list)

        consumed = 0

        val = s_list[0]
        while len(s_list) > 0 and s_list[0] == val:
            s_list = s_list[1:]
            consumed += 1

        if consumed != 4:
            print(f"Warning: only got {consumed} packets")

        # assert len(s_list) == 4
        # [val] = set(s_list)

        print_signal(val)
        # print()

        s_list = []

    print(a)

    if v < -10e3:
        print()




