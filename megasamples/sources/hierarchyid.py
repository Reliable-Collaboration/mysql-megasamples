#!/usr/bin/env python3
"""Decode SQL Server's `hierarchyid` binary to its path string, and encode it back.

AdventureWorks ships `HumanResources.Employee.OrganizationNode` and `Production.Document.DocumentNode`
as bare hex of the internal binary form. MySQL has no hierarchyid, so the path (`/1/1/`) is
materialised alongside the raw bytes.

The format is a concatenation of variable-length codes, one per level, zero-padded to a byte
boundary. Each code is a prefix that selects a range, then a payload; every code ends in a 1 bit,
which is what makes the trailing zero padding unambiguous. The ranges below were derived from
AdventureWorks itself -- one manager there has 22 consecutive children, which pins values 1 to 22 --
and confirmed against the two values Microsoft's own documentation gives: `0x58` is `/1/` and
`0x5AC0` is `/1/1/`.

Ranges outside the table raise rather than guess: a wrong path would be silently wrong, and this
decoder has only been checked over the values these datasets actually contain. `encode` exists so the
build can round-trip every row back to its original bytes instead of trusting the decode.
"""

# (prefix bits, payload bit count, first value)
RANGES = [
    ("01", 3, 0),
    ("100", 3, 4),
    ("101", 4, 8),
    ("11000001", 4, 16),
]


class HierarchyIdError(ValueError):
    pass


def _bits(data):
    return "".join(f"{b:08b}" for b in data)


def decode(data):
    """bytes -> path string, e.g. b'\\x5a\\xc0' -> '/1/1/'."""
    bits, i, parts = _bits(data), 0, []
    while i < len(bits):
        if "1" not in bits[i:]:                     # only padding left
            break
        for prefix, width, base in RANGES:
            if bits.startswith(prefix, i):
                payload = bits[i + len(prefix):i + len(prefix) + width]
                if len(payload) < width:
                    raise HierarchyIdError(f"truncated code at bit {i} in {data.hex()}")
                value = int(payload, 2)
                if value % 2 == 0:
                    raise HierarchyIdError(f"even payload {payload} at bit {i} in {data.hex()}")
                parts.append(base + (value - 1) // 2)
                i += len(prefix) + width
                break
        else:
            raise HierarchyIdError(f"unknown code at bit {i} in {data.hex()}: {bits[i:i + 12]}")
    return "/" + "".join(f"{p}/" for p in parts)


def encode(path):
    """path string -> bytes, the inverse of decode."""
    parts = [int(p) for p in path.strip("/").split("/") if p != ""]
    bits = ""
    for value in parts:
        for prefix, width, base in RANGES:
            if base <= value < base + (1 << width) // 2:
                bits += prefix + format((value - base) * 2 + 1, f"0{width}b")
                break
        else:
            raise HierarchyIdError(f"value {value} is outside the verified ranges")
    if not bits:
        return b""
    bits += "0" * (-len(bits) % 8)
    return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))


def level(path):
    return len([p for p in path.strip("/").split("/") if p != ""])
