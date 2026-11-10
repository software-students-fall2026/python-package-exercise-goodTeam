import math
import random


def spin_wheel(options, weights=None, seed=None):
    if not isinstance(options, (list, tuple)):
        raise TypeError("options must be a list or tuple")
    if not options:
        raise ValueError("options must not be empty")

    if weights is not None:
        if not isinstance(weights, (list, tuple)):
            raise TypeError("weights must be a list or tuple")
        if len(weights) != len(options):
            raise ValueError("weights must have one value per option")
        for weight in weights:
            if isinstance(weight, bool) or not isinstance(weight, (int, float)):
                raise TypeError("each weight must be a number")
            if not math.isfinite(weight) or weight < 0:
                raise ValueError("each weight must be a real number and least 0")
        if sum(weights) == 0:
            raise ValueError("at least one weight must be above 0")

    rng = random.Random(seed)
    return rng.choices(options, weights=weights, k=1)[0]
