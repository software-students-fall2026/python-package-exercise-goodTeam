"""Dinner Decider: a tour of every pyDeciders function."""

from pyDeciders import flip_coin, magic_8_ball, pick_one, roll_dice, spin_wheel

SEED = 2026
MENU = ["pizza", "tacos", "sushi"]


def heading(title):
    print(f"\n=== {title} ===")


def tour():
    heading("roll_dice")
    print("Two six-sided dice:", roll_dice(n=2, sides=6, seed=SEED))
    print("One twenty-sided die:", roll_dice(sides=20, seed=SEED))

    heading("flip_coin")
    print("Three fair flips:", flip_coin(times=3, seed=SEED))
    print("A loaded coin (bias=1.0):", flip_coin(times=3, bias=1.0))

    heading("pick_one")
    print("Tonight's pick:", pick_one(MENU, seed=SEED))

    heading("spin_wheel")
    print("Pizza-heavy wheel:", spin_wheel(MENU, weights=[5, 1, 1], seed=SEED))

    heading("magic_8_ball")
    print("Should we order in?", magic_8_ball("Should we order in?", seed=SEED))


def seeds_and_errors():
    heading("Seeds make results repeatable")
    first = roll_dice(n=3, seed=42)
    second = roll_dice(n=3, seed=42)
    print(first, second, "-> identical:", first == second)

    heading("Bad input is rejected")
    try:
        roll_dice(n=0)
    except ValueError as error:
        print("roll_dice(n=0) ->", error)
    try:
        spin_wheel([])
    except ValueError as error:
        print("spin_wheel([]) ->", error)


def dinner_decider():
    heading("Putting it together: tonight's dinner")
    guests = sum(roll_dice(n=2, seed=SEED))
    where = "at home" if flip_coin(seed=SEED)[0] == "heads" else "out"
    cuisine = spin_wheel(MENU, weights=[5, 1, 1], seed=SEED)
    verdict = magic_8_ball(f"Is {cuisine} a good idea?", seed=SEED)
    print(f"{guests} guests are eating {where}.")
    print(f"The wheel chose {cuisine}.")
    print(f"The 8 ball says: {verdict}")


def main():
    tour()
    seeds_and_errors()
    dinner_decider()


if __name__ == "__main__":
    main()
