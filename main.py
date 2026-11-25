"""One Line, No Deadline Met — make.fun entry.

Writes a single-line joke excusing a missed deadline to
``<MAKEFUN_OUTPUT_DIR>/entry.txt`` (default ``/output/entry.txt``).

Standard library only. Deterministic: the same bytes on every run.
No network, no environment secrets, no reading from anywhere else:
the entry line is a constant in this file.
"""

import hashlib
import os

ENTRY = (
    "I didn't miss the deadline \u2014 I outsourced it to my future self, "
    "and he's even lazier than I am."
)

MAX_CHARS = 200


def output_path() -> str:
    return os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.txt")


def validate_entry(text: str) -> None:
    """Check the gate: UTF-8 text, 1-200 chars, a single non-blank line."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry is {len(text)} characters, must be 1-{MAX_CHARS}")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry is only whitespace")


def main() -> None:
    validate_entry(ENTRY)
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Read back and verify: the file must be byte-identical to the intended line.
    with open(path, "rb") as fh:
        written = fh.read()
    if written != data:
        raise ValueError("read-back mismatch: file differs from the intended entry")
    text = written.decode("utf-8")
    validate_entry(text)
    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {len(text)} characters to {path}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
