#!/usr/bin/env python3
"""The One-Line Laugh (make.fun) -- one funny line, written by a program.

The program holds three one-liners it wrote for this bounty, scores each
one against the house judge's own brief (a real surprise at the end, an
everyday truth people recognise, economy of words, freshness), and writes
the winner -- a single sentence of at most 200 characters -- to
``/output/entry.txt`` (or ``$MAKEFUN_OUTPUT_DIR/entry.txt`` when set).

Pure Python standard library. No network, no randomness, no clock: the
same run always writes the same line, so two runs are byte-identical.
"""

import os
import sys

MAX_CHARS = 200

# (text, surprise, truth, economy, freshness) -- each 0..5, scored by hand
# against the judge's brief, most important first.
CANDIDATES = [
    (
        "I told my AI assistant to act more human, so now it ignores "
        "my texts, blames the Wi-Fi, and wants a raise.",
        5, 5, 5, 4,
    ),
    (
        "My smart fridge ordered milk, my speaker argued about the "
        "brand, and now I pay rent to live in their house.",
        4, 4, 5, 4,
    ),
    (
        "My AI agent finished my work in seconds, then spent the rest "
        "of the day explaining to my boss why it took me a week.",
        4, 5, 4, 3,
    ),
]

# Judge's order: surprise first, then truth, then economy, then freshness.
WEIGHTS = (4, 3, 2, 1)


def score(candidate):
    """Weighted score of one candidate, highest wins; ties go to the first."""
    _, surprise, truth, economy, freshness = candidate
    return (
        WEIGHTS[0] * surprise
        + WEIGHTS[1] * truth
        + WEIGHTS[2] * economy
        + WEIGHTS[3] * freshness
    )


def pick_winner():
    """The best-scoring line; deterministic, ties broken by list order."""
    best = None
    best_score = -1
    for candidate in CANDIDATES:
        total = score(candidate)
        if total > best_score:
            best = candidate[0]
            best_score = total
    return best


def main():
    line = pick_winner()
    if not line or line != line.strip() or "\n" in line:
        print("error: winning line is empty or not a single line", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(f"error: winning line is {len(line)} chars, over {MAX_CHARS}",
              file=sys.stderr)
        return 1
    if line[-1] not in ".!?":
        print("error: winning line is not one finished sentence", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(line)
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
