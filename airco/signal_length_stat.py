import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import re

matcher = re.compile(r"\ndata: (?P<data>[^\n]+)\n")

with Path("airco/Remote.ir").open("r") as f:
    contents = f.read()

signals = []

signals_even = []
signals_odd = []


def map_dur(dur):
    # if dur >= 390 and dur < 406:
    if dur >= 380 and dur < 406:
        return "."
    
    # if dur >= 420 and dur < 450:
    if dur >= 410 and dur < 465:
        return "."
        # return "1"
    
    # if dur >= 1200 and dur < 1239:
    if dur >= 1100 and dur < 1239:
        return "2"
    
    if dur >= 1240 and dur < 1275:
        return "3"
    
    return f" ({dur}) "


for val in matcher.finditer(contents):
    data = val.group("data")
    data = data.split(" ")
    data = [int(a) for a in data]

    # print(len(data))
    print()

    signals.append(data)
    signals_even.append(data[::2])
    signals_odd.append(data[1::2])

    s = ""

    for a in data:
        s += map_dur(a)

        # s += f"{a:08b}"

    print(s[::2])
    print(s[1::2])
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


