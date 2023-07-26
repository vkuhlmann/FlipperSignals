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

def decode_buffer(buf):
    # buf = buf.lstrip("0")
    if buf == "":
        return ""
    
    return buf

    buf += "0" * (8 - len(buf) % 8)

    bin_data = int(buf, 2).to_bytes((len(buf) + 7) // 8, byteorder="big")
    return bin_data.hex()

def print_signal(all_vals):
    s = ""

    def flush_s():
        nonlocal s
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


def main():
    contents = read_contents("blinds_sig4.sub")
    all_vals = extract_timings(contents)
    plot_dur_hist(all_vals)
    print_signal(all_vals)

if __name__ == "__main__":
    main()


