"""Picking one option for the indecisive."""

import random


def pick_one(options, seed=None):
    """Pick one option at random, each with an equal chance.

    Args:
        options: a list or tuple of choices, e.g. ["pizza", "tacos", "sushi"].
            Must contain at least one item.
        seed: optional number that makes the result repeatable. The same seed
            always gives the same pick.

    Returns:
        One item from options.

    Raises:
        TypeError: if options is not a list or tuple (a single string counts as
            wrong, since it would pick one letter).
        ValueError: if options is empty.
    """
    if not isinstance(options, (list, tuple)):
        raise TypeError("options must be a list or tuple of choices")
    if len(options) == 0:
        raise ValueError("options must contain at least one choice")

    # a private random generator, so seeding here never affects other code
    rng = random.Random(seed)

    return rng.choice(options)
