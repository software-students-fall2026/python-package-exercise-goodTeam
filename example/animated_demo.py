"""Animated demo: runs each decisions command so the animations play.

Run this in a real terminal. When output is piped or captured, the animations
are skipped and only the answers are printed.
"""

import sys
import time

from pyDeciders.cli import main

SEED = 2026
PAUSE = 1.0

DEMOS = [
    ("Rolling two d20s", ["dice", "-n", "2", "--sides", "20"]),
    ("Flipping three coins", ["coin", "--times", "3"]),
    ("Picking a snack", ["pick", "pizza", "tacos", "sushi"]),
    (
        "Spinning the wheel",
        ["wheel", "pizza", "tacos", "sushi", "--weights", "5", "1", "1"],
    ),
    ("Asking the 8 ball", ["8ball", "Will the demo work?"]),
]


def run_demo(label, argv):
    print(f"\n{label}...")
    code = main(argv + ["--seed", str(SEED)])
    if code != 0:
        print(f"(that command failed with exit code {code})")
    time.sleep(PAUSE)


def run_all():
    if not sys.stdout.isatty():
        print("No terminal detected, so the animations will be skipped.")
    for label, argv in DEMOS:
        run_demo(label, argv)

    print("\nThe same coin flips with --no-animation:")
    main(["coin", "--times", "3", "--seed", str(SEED), "--no-animation"])


if __name__ == "__main__":
    run_all()
