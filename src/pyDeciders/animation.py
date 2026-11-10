"""Small terminal animations for the decisions command.

Only the command line tool uses this module. The library functions never
print or animate, so they stay safe to call from other programs.

The result is always decided before the animation starts. The animation only
shows random "in progress" frames, so it never changes the answer, and the
same --seed gives the same answer with or without it.
"""

import random
import time

from rich.console import Console
from rich.live import Live
from rich.text import Text

FRAME_COUNT = 12

FIRST_DELAY = 0.04
DELAY_STEP = 0.012

COIN_SPIN = ("( H )", "( | )", "( T )", "( | )")
BALL_SHAKE = ("shaking the ball", "shaking the ball.", "shaking the ball..", "shaking the ball...")


def should_animate(no_animation, stream):
    """Decide whether to animate.

    Animations are off when the user passed --no-animation, or when the output
    is not a terminal (for example when it is piped into a file or another
    program), so scripts only ever see the final answer.
    """
    if no_animation:
        return False
    isatty = getattr(stream, "isatty", None)
    if isatty is None:
        return False
    return bool(isatty())


def build_frames(command, args, rng=None, count=FRAME_COUNT):
    """Return the list of in-progress frames to show for a command.

    The frames are just for show. They come from their own random generator,
    so they never use up the numbers that decide the real result.
    """
    if rng is None:
        rng = random.Random()

    if command == "dice":
        return [
            " ".join(f"[{rng.randint(1, args.sides)}]" for _ in range(args.n))
            for _ in range(count)
        ]
    if command == "coin":
        # each coin starts at a different point in the spin
        starts = [rng.randrange(len(COIN_SPIN)) for _ in range(args.times)]
        return [
            " ".join(COIN_SPIN[(start + i) % len(COIN_SPIN)] for start in starts)
            for i in range(count)
        ]
    if command in ("wheel", "pick"):
        # move through the options in order, like a pointer going round
        start = rng.randrange(len(args.options))
        return [
            f"> {args.options[(start + i) % len(args.options)]} <"
            for i in range(count)
        ]
    if command == "8ball":
        return [BALL_SHAKE[i % len(BALL_SHAKE)] for i in range(count)]
    raise ValueError(f"no animation for command {command!r}")


def frame_delays(count=FRAME_COUNT):
    """How long to show each frame, in seconds, getting slower towards the end."""
    return [FIRST_DELAY + DELAY_STEP * i for i in range(count)]


def animate(command, args, console=None, sleep=time.sleep):
    """Play the animation for a command, then clear it from the screen.

    The caller prints the final answer afterwards. console and sleep can be
    replaced in tests so nothing is drawn and nothing waits.
    """
    if console is None:
        console = Console()
    frames = build_frames(command, args)
    delays = frame_delays(len(frames))

    # transient=True removes the animation once it ends, leaving only the answer
    with Live(console=console, transient=True, auto_refresh=False) as live:
        for frame, delay in zip(frames, delays):
            live.update(Text(frame, style="bold cyan"), refresh=True)
            sleep(delay)
