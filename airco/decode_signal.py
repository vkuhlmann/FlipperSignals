from pathlib import Path
import numpy as np
import re

matcher_name = re.compile(r"\nname: (?P<name>[^\n]+)\n")
matcher = re.compile(r"\ndata: (?P<data>[^\n]+)\n")

with Path("airco/Remote_3.ir").open("r") as f:
    contents = f.read()

signals = []

def map_dur(dur):
    if dur >= 360 and dur < 465:
        return "."
    
    if dur >= 1100 and dur < 1290:
        return "x"
    
    return f" ({dur}) "

class AircoSignal:
    signal: list[int]

    temperature : int
    fan_mode : int
    fan_mode_str : str

    def __init__(self, signal: list[int] | None):
        if signal is not None:
            self.set_signal(signal)

    def set_signal(self, val):
        self.signal = val
        self.populate_decoded()

    def populate_decoded(self):
        pulse_dur = self.signal[::2]
        gap_dur = self.signal[1::2]

        init_pulse = pulse_dur.pop(0)
        init_gap = gap_dur.pop(0)

        pulse_dur = [map_dur(a) for a in pulse_dur]
        gap_dur = [map_dur(a) for a in gap_dur]


        try:
            assert init_pulse >= 3230 and init_pulse < 3400
            assert init_gap >= 1550 and init_gap < 1700 

            assert all(a in ["."] for a in pulse_dur)
            assert all(a in [".", "x"] for a in gap_dur)
        except AssertionError:
            raise ValueError("Wrong pulse or gap durations")
        
        self.temperature = gap_dur[68:73]
        self.temperature = reversed(self.temperature)
        self.temperature = "".join(("1" if a == "x" else "0") for a in self.temperature)

        # Read integer in binary representation
        self.temperature = int(self.temperature, 2)

        fan_mode = "".join(gap_dur[80:83])
        fan_mode = {
            "x..": 4,
            ".x.": 3,
            "xx.": 2,
            "..x": 1,
            "...": 0 # Auto
        }[fan_mode]

        self.fan_mode = fan_mode

        self.fan_mode_str = {
            0: "Auto",
            1: "Fan 1",
            2: "Fan 2",
            3: "Fan 3",
            4: "Fan 4"
        }[self.fan_mode]





names = (a.group("name") for a in matcher_name.finditer(contents))
data = (a.group("data") for a in matcher.finditer(contents))

for name, data in zip(names, data, strict=True):
    data = data.split(" ")
    data = [int(a) for a in data]
    s = [map_dur(a) for a in data]

    signals.append(data)

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
        decoded_signal = AircoSignal(data)
    except ValueError as e:
        print(f"  Could not decode signal: {e}\n")
        continue

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

        # v += val.rjust(length)
        # v = v[:pos] + v[pos+length:]


    # print(prefix + (" " * 68) + "\\" + "-" * 3 + "/")
    # print(prefix + (" " * 68) + "-" * 5)
    # print(prefix + (" " * 68) + temp_str)
    print(prefix + line1)
    print(prefix + line2)
    print()



