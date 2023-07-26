from pathlib import Path
import re
import numpy as np
from typing import Iterable

header = """Filetype: Flipper SubGhz RAW File
Version: 1
Frequency: 868950000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
"""

def get_data_dir():
    data_dir = Path.cwd() / "data"
    if not data_dir.exists():
        data_dir = Path.cwd() / "blinds" / "data"

    assert data_dir.exists()
    return data_dir


def read_contents(file) -> str:
    data_dir = get_data_dir()    
    with (data_dir / file).open("r") as f:
        contents = f.read()

    return contents

def extract_timings_per_line(contents : str) -> Iterable[list[int]]:
    assert contents.startswith(header)
    contents = contents[len(header):]

    all_vals = []

    for l in contents.strip().split("\n"):
        m = re.fullmatch(r"RAW_Data:(?P<timings>( -?\d+)+)", l)

        vals = [int(a) for a in m.group("timings").strip().split(" ")]

        assert np.all(np.sign(vals[::2]) == 1)
        assert np.all(np.sign(vals[1::2]) == -1)

        yield vals


def extract_timings(contents : str) -> list[int]:
    all_vals = np.concatenate(
        [np.array(a) for a in extract_timings_per_line(contents)]
    )

    assert np.all(np.sign(all_vals[::2]) == 1)
    assert np.all(np.sign(all_vals[1::2]) == -1)
    return all_vals

def write_timings(name, vals : list[list[int]]):
    data_dir = get_data_dir()

    dst_file : Path = data_dir / name

    with dst_file.open("w", encoding="ascii") as f:
        f.write(header)

        for a in vals:
            data_line = " ".join(str(a) for a in a)
            f.write(f"RAW_Data: {data_line}\n")
