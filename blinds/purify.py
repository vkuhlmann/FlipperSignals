import numpy as np

from utils import read_contents, write_timings, extract_timings_per_line

short_signal = 418
long_signal = 836

def decode_length(val):
    absv = np.abs(val)

    if np.abs(np.abs(absv) - short_signal) < 100:
        return "0"
    
    if np.abs(np.abs(absv) - long_signal) < 100:
        return "1"
    
    return f" ({val}) "

def cast_lengths(val):
    absv = np.abs(val)

    if np.abs(np.abs(absv) - short_signal) < 100:
        return short_signal * np.sign(val)
    
    if np.abs(np.abs(absv) - long_signal) < 100:
        return long_signal * np.sign(val)
    
    if np.abs(np.abs(absv) - 5300) < 400:
        return 5300 * np.sign(val)
    
    if np.abs(np.abs(absv) - 10e3) < 100:
        return int(10e3) * np.sign(val)
    
    assert val < -50e3
    return val


def main():
    contents = read_contents("Blinds.sub")

    new_vals_all = []

    for vals in extract_timings_per_line(contents):
        new_vals = [cast_lengths(a) for a in vals]
        new_vals_all.append(new_vals)

    dst_file = "blinds_sig3_again.sub"
    write_timings(dst_file, new_vals_all)

if __name__ == "__main__":
    main()

