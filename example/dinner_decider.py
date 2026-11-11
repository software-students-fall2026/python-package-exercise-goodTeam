"""A guided tour of every pyDeciders function.

Each section shows the call, what its arguments mean, and what came back.
Every call uses a seed, so the output is the same on every run.
"""

from pyDeciders import flip_coin, magic_8_ball, pick_one, roll_dice, spin_wheel

SEED = 2026
MENU = ["pizza", "tacos", "sushi"]
WEIGHTS = [5, 1, 1]

# Storing as lambda functions to be called later
BAD_CALLS = [
    ("roll_dice(n=0)", lambda: roll_dice(n=0)),
    ("roll_dice(sides=1)", lambda: roll_dice(sides=1)),
    ("flip_coin(bias=2)", lambda: flip_coin(bias=2)),
    ("pick_one('pizza')", lambda: pick_one("pizza")),
    ("spin_wheel([])", lambda: spin_wheel([])),
    ("magic_8_ball('   ')", lambda: magic_8_ball("   ")),
]


def heading(title, description):
    print(f"\n=== {title} ===")
    print(description)


# Print abstraction to format results
def show(call, result):
    print(f"  {call:<44} -> {result!r}  ({type(result).__name__})")


def tour():
    heading("roll_dice", "One number per die, each between 1 and `sides`.")
    show(f"roll_dice(n=2, sides=6, seed={SEED})", roll_dice(n=2, sides=6, seed=SEED))
    show(f"roll_dice(n=1, sides=20, seed={SEED})", roll_dice(n=1, sides=20, seed=SEED))

    heading(
        "flip_coin",
        "`bias` is the chance of heads: 1.0 is always heads, 0.0 always tails.",
    )
    show(f"flip_coin(times=3, seed={SEED})", flip_coin(times=3, seed=SEED))
    show("flip_coin(times=3, bias=1.0)", flip_coin(times=3, bias=1.0))
    show("flip_coin(times=3, bias=0.0)", flip_coin(times=3, bias=0.0))

    heading("pick_one", "Every option is equally likely.")
    show(f"pick_one(MENU, seed={SEED})", pick_one(MENU, seed=SEED))

    heading(
        "spin_wheel",
        "Like pick_one, but each option has a weight: 5 is five times as likely as 1.",
    )
    show(
        f"spin_wheel(MENU, weights={WEIGHTS}, seed={SEED})",
        spin_wheel(MENU, weights=WEIGHTS, seed=SEED),
    )

    heading("magic_8_ball", "Ask a yes-or-no question and get a fortune.")
    show(
        f"magic_8_ball('Should we order in?', seed={SEED})",
        magic_8_ball("Should we order in?", seed=SEED),
    )


def seeds():
    heading(
        "Seeds",
        "The same seed always gives the same result. A different seed can give a different one.",
    )
    first = roll_dice(n=3, seed=42)
    second = roll_dice(n=3, seed=42)
    other = roll_dice(n=3, seed=7)
    show("roll_dice(n=3, seed=42)", first)
    show("roll_dice(n=3, seed=42) again", second)
    show("roll_dice(n=3, seed=7)", other)
    print(f"  seed 42 twice identical: {first == second}")


def errors():
    heading(
        "Bad input",
        "Invalid arguments raise TypeError or ValueError with a clear message.",
    )
    for call, attempt in BAD_CALLS:
        try:
            attempt()
        except (TypeError, ValueError) as error:
            print(f"  {call:<22} -> {type(error).__name__}: {error}")


def dinner_decider():
    heading("Putting it together", "Every function, one dinner.")
    guests = sum(roll_dice(n=2, seed=SEED))
    print(f"  Step 1, roll two dice for the guest count: {guests} guests")

    heads = flip_coin(seed=SEED)[0] == "heads"
    where = "at home" if heads else "out"
    print(f"  Step 2, flip a coin (heads = stay home): eating {where}")

    cuisine = spin_wheel(MENU, weights=WEIGHTS, seed=SEED)
    print(f"  Step 3, spin the pizza-heavy wheel: {cuisine}")

    verdict = magic_8_ball(f"Is {cuisine} a good idea?", seed=SEED)
    print(f"  Step 4, ask the 8 ball if that's a good idea: {verdict}")

    print(f"\nTonight: {guests} guests, {where}, {cuisine}.")


def main():
    tour()
    seeds()
    errors()
    dinner_decider()


if __name__ == "__main__":
    main()
