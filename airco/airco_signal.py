# Auxiilary file for decode_signal.py

from utils import map_dur

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
