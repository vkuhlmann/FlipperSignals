import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import re

matcher_name = re.compile(r"\nname: (?P<name>[^\n]+)\n")
matcher = re.compile(r"\ndata: (?P<data>[^\n]+)\n")

with Path("airco/Remote.ir").open("r") as f:
    contents = f.read()

signals = []

signals_even = []
signals_odd = []


def map_dur(dur):
    # if dur >= 390 and dur < 406:
    if dur >= 360 and dur < 406:
        return "."
    
    # if dur >= 420 and dur < 450:
    if dur >= 410 and dur < 465:
        return "."
        # return "1"
    
    # if dur >= 1200 and dur < 1239:
    if dur >= 1100 and dur < 1239:
        return "x"
    
    if dur >= 1240 and dur < 1290:
        return "x"
    
    return f" ({dur}) "


names = (a.group("name") for a in matcher_name.finditer(contents))

for name, data in zip(names, matcher.finditer(contents), strict=True):
    data = data.group("data")
    data = data.split(" ")
    data = [int(a) for a in data]

    # print(len(data))
    print()

    signals.append(data)
    signals_even.append(data[::2])
    signals_odd.append(data[1::2])

    s = []

    for a in data:
        s.append(map_dur(a))

    line1 = ""
    line2 = ""
    pulse_dur = s[::2]
    gap_dur = s[1::2]

    if len(pulse_dur) < len(gap_dur):
        pulse_dur.append("")

    if len(gap_dur) < len(pulse_dur):
        gap_dur.append("")

    for a, b in zip(pulse_dur, gap_dur, strict=True):
        val1 = str(a)
        val2 = str(b)
        length = max(len(val1), len(val2))

        line1 += val1.rjust(length)
        line2 += val2.rjust(length)

        # s += f"{a:08b}"

    # print(s[::2])
    # print(s[1::2])
    print(f"\n{name}:")
    print(f"  Pulse: {line1}")
    print(f"  Gap:   {line2}")
    print()

def plot_signals():
    # all_signals = np.array(signals).flatten()
    # all_signals = [a for a in all_signals if a < 3000]
    # all_signals = [a for a in all_signals if a < 600]
    # plt.hist(all_signals, bins=100)
    # plt.show()

    for arr in [signals, signals_even, signals_odd]:
        plt.figure()

        arr = np.array(signals).flatten()
        arr = [a for a in arr if a < 3000]

        arr = [a for a in arr if a >= 600]

        # arr = [a for a in arr if a < 600]
        plt.hist(arr, bins=100)

    plt.show()


    # signals_even = np.array(signals_even).flatten()
    # all_signals = [a for a in all_signals if a < 3000]
    # all_signals = [a for a in all_signals if a < 600]
    # plt.hist(all_signals, bins=100)
    # plt.show()


