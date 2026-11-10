"""Dice rolling for the indecisive."""

import random


def roll_dice(n=1, sides=6, seed=None):
    """Roll one or more dice.

    Args:
        n: how many dice to roll. Must be a whole number of at least 1.
        sides: how many sides each die has. Must be a whole number of at least 2.
            The default of 6 is a regular die; use 20 for a D&D d20.
        seed: optional number that makes the result repeatable. The same seed
            always gives the same rolls.

    Returns:
        A list of ints, one per die, each between 1 and sides.

    Raises:
        TypeError: if n or sides is not a whole number.
        ValueError: if n is less than 1, or sides is less than 2.
    """
    # bool is a subclass of int, so True would sneak through as 1
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be a whole number")
    if n < 1:
        raise ValueError("n must be at least 1")

    if isinstance(sides, bool) or not isinstance(sides, int):
        raise TypeError("sides must be a whole number")
    if sides < 2:
        raise ValueError("a die needs at least 2 sides")

    # a private random generator, so seeding here never affects other code
    rng = random.Random(seed)

    results = []
    for _ in range(n):
        results.append(rng.randint(1, sides))
    return results
