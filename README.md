# pyDeciders

[![CI](https://github.com/software-students-fall2026/python-package-exercise-goodTeam/actions/workflows/ci.yml/badge.svg)](https://github.com/software-students-fall2026/python-package-exercise-goodTeam/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/pyDeciders)](https://pypi.org/project/pyDeciders/)

Can't decide? Let the dice, the coin, or a very opinionated 8 ball do it for you.

**pyDeciders** is a small, lighthearted Python package for making decisions. Use it as a **library** (five functions you can import into your own code) or as a **command-line tool** called `decisions` with little terminal animations.

- Roll dice, flip (even loaded) coins, pick from a list, spin a weighted wheel, and consult a magic 8 ball.
- Every function accepts a `seed`, so results are repeatable.
- The library never prints or animates; only the command-line tool does.

**PyPI page:** https://pypi.org/project/pyDeciders/

## Install

```bash
pip install pyDeciders
```

Requires Python 3.11 or newer.

## Quick start

### Command line

```bash
decisions dice -n 2 --sides 20       # roll two 20-sided dice
decisions coin --times 3 --bias 0.7  # flip a coin that lands heads 70% of the time
decisions pick pizza tacos sushi     # pick one option
decisions wheel pizza tacos sushi --weights 5 1 1   # weighted wheel
decisions 8ball "Should I order pizza?"
```

### Python

```python
from pyDeciders import roll_dice, flip_coin, pick_one, spin_wheel, magic_8_ball

roll_dice(n=2, sides=6, seed=42)                 # [6, 1]
flip_coin(times=3, seed=42)                      # ['tails', 'heads', 'heads']
pick_one(["pizza", "tacos", "sushi"], seed=42)   # 'sushi'
```

## Library reference

All functions take an optional `seed`. The same seed always gives the same result. Bad input raises `TypeError` (wrong type) or `ValueError` (wrong value) with a clear message.

### `roll_dice(n=1, sides=6, seed=None)`

Roll `n` dice with `sides` sides each. Returns a list of ints between 1 and `sides`.

```python
from pyDeciders import roll_dice

roll_dice(n=2, sides=6, seed=42)   # [6, 1]
roll_dice(sides=20, seed=42)       # [4]
roll_dice(n=0)                     # ValueError: n must be at least 1
```

### `flip_coin(times=1, bias=0.5, seed=None)`

Flip a coin `times` times. `bias` is the chance of heads, from `0.0` (always tails) to `1.0` (always heads). Returns a list of `"heads"` / `"tails"`.

```python
from pyDeciders import flip_coin

flip_coin(times=3, seed=42)             # ['tails', 'heads', 'heads']
flip_coin(times=3, bias=1.0)            # ['heads', 'heads', 'heads']
flip_coin(bias=2)                       # ValueError: bias must be between 0 and 1
```

### `pick_one(options, seed=None)`

Pick one item from a list or tuple, each equally likely.

```python
from pyDeciders import pick_one

pick_one(["pizza", "tacos", "sushi"], seed=42)   # 'sushi'
pick_one([])                                     # ValueError: options must contain at least one choice
pick_one("pizza")                                # TypeError: options must be a list or tuple of choices
```

### `spin_wheel(options, weights=None, seed=None)`

Like `pick_one`, but each option can have a weight. A weight of 5 is five times as likely as a weight of 1. Weights must be non-negative numbers with the same length as `options`, and at least one must be above 0.

```python
from pyDeciders import spin_wheel

spin_wheel(["pizza", "tacos", "sushi"], weights=[5, 1, 1], seed=42)   # 'pizza'
spin_wheel([])                                                        # ValueError: options must not be empty
```

### `magic_8_ball(question, seed=None)`

Ask a yes-or-no question and get a fortune (positive, unsure, or negative).

```python
from pyDeciders import magic_8_ball

magic_8_ball("Should I order pizza?", seed=42)   # 'Not a chance.'
magic_8_ball("   ")                              # ValueError: question must not be empty
```

## Command-line reference

```
decisions <command> [options] [--seed N] [--no-animation]
```

| Command | Arguments | Example |
|---|---|---|
| `dice` | `-n COUNT` (default 1), `--sides SIDES` (default 6) | `decisions dice -n 2 --sides 20` |
| `coin` | `--times COUNT` (default 1), `--bias CHANCE_OF_HEADS` (default 0.5) | `decisions coin --times 3 --bias 0.7` |
| `pick` | one or more options | `decisions pick pizza tacos sushi` |
| `wheel` | one or more options, `--weights W1 W2 ...` | `decisions wheel pizza tacos sushi --weights 5 1 1` |
| `8ball` | a question | `decisions 8ball "Should I order pizza?"` |

Options for every command:

- `--seed N` makes the result repeatable.
- `--no-animation` prints the answer immediately.

The animation also turns itself off when the output isn't a terminal (for example, when piped into a file). Errors are printed as `decisions: <message>` and the command exits with a non-zero code.

```console
$ decisions dice -n 2 --sides 20 --seed 42 --no-animation
4 1
$ decisions pick pizza tacos sushi --seed 42 --no-animation
sushi
$ decisions wheel pizza tacos sushi --weights 5 1 1 --seed 42 --no-animation
pizza
$ decisions 8ball "Should I order pizza?" --seed 42 --no-animation
Not a chance.
```

## Example programs

Two runnable examples are in the [`example/`](./example) folder:

- [`example/dinner_decider.py`](./example/dinner_decider.py) uses **every function** and shows seeds, error handling, and a small combined scenario. It prints the same output every run.
- [`example/animated_demo.py`](./example/animated_demo.py) runs each command so the **terminal animations** play. Run it in a real terminal.

```bash
python example/dinner_decider.py
python example/animated_demo.py
```

End of `dinner_decider.py` output:

```text
=== Putting it together ===
Every function, one dinner.
  Step 1, roll two dice for the guest count: 4 guests
  Step 2, flip a coin (heads = stay home): eating at home
  Step 3, spin the pizza-heavy wheel: pizza
  Step 4, ask the 8 ball if that's a good idea: The stars say yes.

Tonight: 4 guests, at home, pizza.
```

## Contributing

You need Python 3.11+, [git](https://git-scm.com/), and [pipenv](https://pipenv.pypa.io/) (`pip install pipenv`).

```bash
git clone https://github.com/software-students-fall2026/python-package-exercise-goodTeam.git
cd python-package-exercise-goodTeam

pipenv install --dev            # create the virtual environment and install dependencies
pipenv run pytest               # run the tests
pipenv run python -m build      # build the package into dist/
pipenv run decisions coin       # run the command-line tool
pipenv run python example/dinner_decider.py   # run an example
```

If `decisions` isn't found after you change `pyproject.toml`, run `pipenv install -e .` to refresh it.

Workflow: create a feature branch (never commit to `main`), push it, open a pull request against this repository's `main`, ask a teammate to review and run the tests, then merge and delete the branch. GitHub Actions builds the package and runs the tests on Python 3.11 and 3.12 for every pull request.

### Platform notes

- **macOS / Linux:** use `python3` and `pip3` if `python` isn't available.
- **Windows (PowerShell):** use `py` or `python`, and put the 8 ball question in double quotes: `decisions 8ball "Should I order pizza?"`.
- Animations need a real terminal. In IDE output panels, pipes, or CI, only the answers print.

### Environment variables and data

None. The package needs no environment variables, configuration files, or starter data.

## Team

- [Sanay Daptardar](https://github.com/sanay-d-nyu)
- [Jialiang Cao](https://github.com/jialiangcao)
- [Ryan Jiang](https://github.com/UIYrj)
- [Yi Fei](https://github.com/yeefeizhao)

## License

GNU General Public License v3.0. See [LICENSE](./LICENSE).
