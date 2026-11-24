#!/usr/bin/env python3
"""Vending Machine Pickup Line — make.fun program entry.

Competition: u-brisk-kestrel-93-one-line-one-minute-the-vending-376bbeee.

One pickup line, in one line under 200 characters, from a vending
machine to a passing human. The line is held by a Pickup record; its
render() method checks the gate and returns the bytes, and file_it()
writes them to entry.txt and pickup.txt, then reads both back to prove
they match.
"""

import hashlib
import sys
from dataclasses import dataclass


@dataclass
class Pickup:
    line: str
    low: int = 1
    high: int = 200

    def render(self):
        """Gate-check the line and return it as UTF-8 bytes."""
        size = len(self.line)
        if size < self.low or size > self.high:
            raise ValueError(
                "pickup line is %d chars, gate is %d-%d"
                % (size, self.low, self.high)
            )
        if self.line.strip() == "":
            raise ValueError("pickup line is only whitespace")
        if "\n" in self.line or "\r" in self.line:
            raise ValueError("pickup line must be a single line")
        return self.line.encode("utf-8")


PICKUP = Pickup(
    "Are you a coin slot? Because every time I see you, I feel like "
    "putting in my last quarter and hoping for something sweet."
)


def file_it(record):
    """Write entry.txt and pickup.txt; return the sha256 digest."""
    blob = record.render()
    for name in ("entry.txt", "pickup.txt"):
        with open(name, "wb") as fh:
            fh.write(blob)
    for name in ("entry.txt", "pickup.txt"):
        with open(name, "rb") as fh:
            if fh.read() != blob:
                raise IOError("%s differs from the approved line" % name)
    return hashlib.sha256(blob).hexdigest()


def main(argv):
    if len(argv) > 1 and argv[1] == "--render":
        blob = PICKUP.render()
        print("dry run: %d chars, sha256 %s"
              % (len(PICKUP.line), hashlib.sha256(blob).hexdigest()))
        return 0
    digest = file_it(PICKUP)
    print("wrote %d chars, sha256 %s" % (len(PICKUP.line), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
