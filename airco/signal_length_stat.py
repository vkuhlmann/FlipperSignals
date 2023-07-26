import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import re
from utils import read_contents
from utils import extract_timings

def plot_signals_individual(signals, signals_even, signals_odd):
    for arr in [signals, signals_even, signals_odd]:
        plt.figure()

        arr = np.array(arr).flatten()
        arr = [a for a in arr if a < 3000]
        # arr = [a for a in arr if a >= 600]
        # arr = [a for a in arr if a < 600]
        plt.hist(arr, bins=100)

    plt.show()

def plot_signals_combined(signals_even, signals_odd):
    plt.figure()

    signals_even = np.array(signals_even).flatten()
    signals_odd = np.array(signals_odd).flatten()

    filter_func = lambda a: a < 2000

    signals_even = list(filter(filter_func, signals_even))
    signals_odd = list(filter(filter_func, signals_odd))

    plt.hist([signals_even, signals_odd], bins=50, label=["pulse", "gap"])
    plt.xlabel("Duration (us)")
    plt.ylabel("Count")
    plt.legend()
    plt.show()


def plot_signals_combined2(signals_even, signals_odd):
    filter_funcs = [
        lambda a: a < 4000,
        lambda a: a >= 200 and a < 500,
        lambda a: a >= 1100 and a < 1400,
        lambda a: a >= 1600 and a < 3500
    ]

    f, ax = plt.subplots(len(filter_funcs), 2, sharex=False, figsize=(8, 10))

    signals_even = np.array(signals_even).flatten()
    signals_odd = np.array(signals_odd).flatten()


    for i, current_ax, filter_func in zip(range(len(ax)), ax, filter_funcs, strict=True):

        signals_even_filtered = list(filter(filter_func, signals_even))
        signals_odd_filtered = list(filter(filter_func, signals_odd))

        for a in current_ax:
            a.hist([signals_even_filtered, signals_odd_filtered], bins=25, label=["pulse", "gap"])

            if i == len(ax) - 1:
                a.set_xlabel("Duration (us)")
                a.set_ylabel("Count")
        current_ax[1].set_yscale("log")
    
        if i == 0:
            current_ax[1].legend()
    # plt.legend()
    plt.show()


def main():
    contents = read_contents("Remote_3.ir")
    timings = extract_timings(contents)

    all_timings = np.concatenate(
        [np.array(a[1]) for a in timings]
    )

    even_timings = np.concatenate(
        [np.array(a[1][::2]) for a in timings]
    )

    odd_timings = np.concatenate(
        [np.array(a[1][1::2]) for a in timings]
    )

    plot_signals_combined2(even_timings, odd_timings)

if __name__ == "__main__":
    main()

