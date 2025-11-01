#!/usr/bin/env python3

import sys

from pipetools import (
    X,
    as_args,
    foreach,
    foreach_do,
    pipe,
    take_first,
    where,
)


def expand(s: str) -> str:
    result = []
    i = 0

    while i < len(s):
        if i + 2 < len(s) and s[i + 1] == "-":
            start, end = s[i], s[i + 2]
            for code in range(ord(start), ord(end) + 1):
                result.append(chr(code))
            i += 3
        else:
            result.append(s[i])
            i += 1

    return "".join(result)


def purrify(prefix: str, length: int) -> str:
    charsets = []
    mask = ""
    mask_len = 0
    in_bracket = False
    current_set = ""

    for char in prefix:
        if char == "[":
            in_bracket = True
            current_set = ""
        elif char == "]":
            in_bracket = False
            expanded = expand(current_set)
            charsets.append(expanded)
            mask += f"?{len(charsets)}"
            mask_len += 1
        elif in_bracket:
            current_set += char
        else:
            mask += char
            mask_len += 1

    mask += "?d" * (length - mask_len)

    if charsets:
        return ",".join(charsets) + "," + mask
    else:
        return mask


def parse_csv_line(line: str) -> list[str]:
    return [field.strip().strip('"') for field in line.rstrip("\n").split(";")]


def in_cities(row: list[str], cities: list[str], geo_indices: tuple[int]) -> bool:
    return any(
        city.lower() in row[idx].lower() for idx in geo_indices for city in cities
    )


def main():
    cities = sys.argv[1:]

    header = sys.stdin > pipe | take_first(1) | next | parse_csv_line
    prefix_idx = header.index("Prefix")
    length_idx = header.index("Length")
    type_idx = header.index("Type")
    geo_indices = header > (
        pipe | enumerate | where(X[1].startswith("Geocode:")) | foreach(X[0]) | tuple
    )
    min_length = max(prefix_idx, length_idx, type_idx, *geo_indices)

    _ = sys.stdin > (
        pipe
        | foreach(parse_csv_line)
        | where(X.__len__() > min_length)
        | where(X[type_idx] == "MOBILE")
        | where(in_cities, geo_indices=geo_indices, cities=cities)
        | foreach(lambda x: (x[prefix_idx], int(x[length_idx])))
        | foreach(as_args(purrify))
        | foreach_do(print)
    )


if __name__ == "__main__":
    main()
