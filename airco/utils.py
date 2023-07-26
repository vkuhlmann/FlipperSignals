from pathlib import Path
from typing import Iterable, Tuple, Sequence
import re

def map_dur(dur):
    if dur >= 360 and dur < 465:
        return "."
    
    if dur >= 1100 and dur < 1290:
        return "x"
    
    return f" ({dur}) "


def read_contents(file) -> str:
    data_dir = Path.cwd() / "data"
    if not data_dir.exists():
        data_dir = Path.cwd() / "airco" / "data"

    with (data_dir / file).open("r") as f:
        contents = f.read()

    return contents


def extract_timings_iter(contents : str) -> Iterable[Tuple[str, Sequence[int]]]:
    matcher_name = re.compile(r"\nname: (?P<name>[^\n]+)\n")
    matcher = re.compile(r"\ndata: (?P<data>[^\n]+)\n")

    names = (a.group("name") for a in matcher_name.finditer(contents))
    data = (a.group("data") for a in matcher.finditer(contents))

    for name, data in zip(names, data, strict=True):
        data = data.split(" ")
        data = [int(a) for a in data]

        yield name, data

# Returns a list of tuples (name, data)
# For example: [("25", [300, 500, 800, ...]), ("auto", [900, 100, 300, ...]), ...]
def extract_timings(contents: str) -> list[Tuple[str, Sequence[int]]]:
    return list(extract_timings_iter(contents))

