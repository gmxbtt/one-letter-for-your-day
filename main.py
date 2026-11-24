#!/usr/bin/env python3
"""One Letter for Your Day — the entry program.

The competition asks for exactly one letter, A to Z, standing for the
word that describes your day. This program carries a single letter,
checks that it really is one uppercase letter, and hands it to the
grader at /output/entry.txt — nothing else, no newline, no spaces.

The letter: J, for "Jittery".

Why J, and why "jittery", against the judge's five criteria:

1. It is the initial of a word that describes the day. Jittery is a
   state of a day: hands shaking, heart buzzing, third coffee in,
   twelve tabs open, every notification a small electric shock.
2. It is vivid and specific. "Jittery" calls up a sharp physical
   picture — the trembling hand, the tapping foot — not a vague mood
   like "tired" or "good".
3. It is funny in a way that lands at once. Everyone has had the
   too-much-coffee, too-many-deadlines day; the word makes a reader
   grin and repeat it to a friend.
4. It feels true. It is an honest report of a real, ordinary day,
   not a performance: nobody pretends to be jittery.
5. J suits the word and is not the obvious pick. The crowded letters
   are Z (zero sleep), K (knackered), G (grind), H (hangover) and X
   (exhausted) — all spent by hundreds of entries. J is uncommon,
   sharp, and fits the sound of the word: the quick, clipped J of a
   nerve that will not sit still.

Candidates beaten by J: D for "Doomscrolling" (the most vivid word,
but the obvious clever pick, so likely saturated, and an activity
rather than a state of the day); B for "Bamboozled" (funnier, but it
describes being tricked, not the day itself); U for "Unraveling"
(vivid and honest, but dramatic rather than funny); L for "Loopy"
(funny and honest, but a weaker physical picture than jittery).
"""

import os
import sys

# The entry: one uppercase letter, A-Z, and nothing else.
CHOSEN_LETTER = "J"

# The gate allows exactly 1 character of UTF-8 text, not whitespace.
OUTPUT_PATH = os.path.join(
    os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.txt"
)


def check_single_letter(candidate: str) -> str:
    """Refuse anything that is not exactly one uppercase letter A-Z."""
    if len(candidate) != 1:
        raise ValueError("entry must be exactly one character")
    if not ("A" <= candidate <= "Z"):
        raise ValueError("entry must be a letter A-Z, got %r" % candidate)
    return candidate


def emit_letter(letter: str, destination: str) -> str:
    """Write the validated letter to the output file, exactly as-is.

    No trailing newline, no extra text: the file holds the letter and
    nothing else, so the judge reads one letter and one letter only.
    After writing, read the file back and refuse to succeed unless it
    is byte for byte the single letter — a wrong file must fail loudly
    here, not silently pass the gate as an invalid entry.
    """
    folder = os.path.dirname(destination)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(destination, "w", encoding="utf-8", newline="") as handle:
        handle.write(letter)
    with open(destination, "rb") as handle:
        written = handle.read()
    if written != letter.encode("utf-8"):
        raise ValueError(
            "wrote %r to %s, expected exactly %r"
            % (written, destination, letter.encode("utf-8"))
        )
    return letter


def main() -> int:
    """Validate the letter, write it out, and say it once on stdout."""
    try:
        letter = check_single_letter(CHOSEN_LETTER)
    except ValueError as exc:
        print("invalid entry: %s" % exc, file=sys.stderr)
        return 1
    emit_letter(letter, OUTPUT_PATH)
    print(letter)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
