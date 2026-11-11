"""A fortune-telling ball for the indecisive."""

import random

POSITIVE = (
    "Absolutely, go for it.",
    "The stars say yes.",
    "Without a shadow of a doubt.",
    "Yes, and you knew that already.",
    "Signs point to a cheerful yes.",
)
UNSURE = (
    "Hmm, the ball is buffering. Ask again.",
    "Too foggy to tell right now.",
    "Ask me after a snack.",
    "The answer is hiding. Try later.",
    "Maybe. Maybe not. Maybe so.",
)
NEGATIVE = (
    "Not a chance.",
    "The stars say no.",
    "I would not bet on it.",
    "Nope, not today.",
    "All signs point to no.",
)

ANSWERS = POSITIVE + UNSURE + NEGATIVE


def magic_8_ball(question, seed=None):
    """Ask the ball a yes-or-no question and get its answer.

    Args:
        question: the question to ask, e.g. "Should I order pizza?". Must be a
            string with at least one non-space character.
        seed: optional number that makes the result repeatable. The same seed
            always gives the same answer.

    Returns:
        One answer string from ANSWERS.

    Raises:
        TypeError: if question is not a string.
        ValueError: if question is empty or only whitespace.
    """
    if not isinstance(question, str):
        raise TypeError("question must be a string")
    if not question.strip():
        raise ValueError("question must not be empty")

    # a private random generator, so seeding here never affects other code
    rng = random.Random(seed)

    return rng.choice(ANSWERS)
