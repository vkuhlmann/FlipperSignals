from pathlib import Path
import re
import matplotlib.pyplot as plt
import numpy as np
from utils import read_contents, extract_timings

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

def print_signals(all_values: list[int]):
    s = None
    s_list = []

    for v in all_values:
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

        if v < -4000:
            if v is None:
                print(a)
                continue

            if s is None or len(s) == 0:
                print(f"Empty package")
                continue

            s_list.append(s)
            s = None

            if len(s_list) < 4:
                continue

            consumed = 0

            val = s_list[0]
            while len(s_list) > 0 and s_list[0] == val:
                s_list = s_list[1:]
                consumed += 1

            if consumed != 4:
                print(f"Warning: only got {consumed} packets")

            print_signal(val)
            s_list = []

        print(a)

        if v < -10e3:
            print()

def main():
    # contents = read_contents("Blinds.sub")
    # contents = read_contents("blinds_sig4.sub")
    contents = read_contents("RAW_20230725-164754.sub")
    all_vals = extract_timings(contents)

    print_signals(all_vals)

if __name__ == "__main__":
    main()
