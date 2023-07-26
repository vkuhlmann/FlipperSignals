import numpy as np
import re

# The other file in the same directory
from airco_signal import AircoSignal
from utils import map_dur, read_contents, extract_timings

def print_and_decode_signal(name, timings):
    s = [map_dur(a) for a in timings]

    pulse_dur = s[::2]
    gap_dur = s[1::2]

    if len(pulse_dur) < len(gap_dur):
        pulse_dur.append("")

    if len(gap_dur) < len(pulse_dur):
        gap_dur.append("")

    # Display pulse and gap underneath each other, resulting in a column for each pulse+gap pair
    line1 = ""
    line2 = ""
    for a, b in zip(pulse_dur, gap_dur, strict=True):
        # Make sure that every column has the same width
        val1 = str(a)
        val2 = str(b)
        length = max(len(val1), len(val2))

        line1 += val1.rjust(length)
        line2 += val2.rjust(length)

    print(f"\n{name}:")
    print(f"  Pulse: {line1}")
    print(f"  Gap:   {line2}")

    try:
        decoded_signal = AircoSignal(timings)
    except ValueError as e:
        print(f"  Could not decode signal: {e}\n")
        return

    prefix = len("  Pulse: ") + 8
    prefix = " " * prefix
    temp_str = f"{decoded_signal.temperature:>2} \N{DEGREE SIGN}C"

    temp_pos = 68
    temp_len = 5

    fan_pos = 80
    fan_len = 3

    vals = [
        (temp_str, temp_pos, temp_len, 0),
        (f"{decoded_signal.fan_mode_str}", fan_pos, fan_len, -1)
    ]


    line1 = ""
    line2 = ""
    for val, pos, length, offset in vals:
        line1 = line1.ljust(pos)
        line1 += "-" * length

        line2 = line2.ljust(pos + offset)
        line2 += val

    print(prefix + line1)
    print(prefix + line2)
    print()

def main():
    contents = read_contents("Remote_3.ir")
    timings = extract_timings(contents)

    for name, data in timings:
        print_and_decode_signal(name, data)

if __name__ == "__main__":
    main()



