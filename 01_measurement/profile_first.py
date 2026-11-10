"""Find the bottleneck before optimizing.

Run: python3 profile_first.py

Everyone's instinct says "parsing the lines must be the slow part".
The profiler disagrees: the accidental O(n^2) de-duplication dominates.
Speeding up parse() by 10x would change almost nothing.
"""
import cProfile
import pstats


def parse(line):
    user, _, action = line.partition(",")
    return user, action


def dedupe(items):
    out = []
    for item in items:
        if item not in out:  # list membership: O(n) each -> O(n^2) overall
            out.append(item)
    return out


def pipeline(lines):
    return dedupe([parse(line) for line in lines])


lines = [f"user{i % 3000},login" for i in range(30_000)]

profiler = cProfile.Profile()
profiler.runcall(pipeline, lines)
# Look at 'tottime': dedupe dwarfs parse. Fix the bottleneck (use a set / dict),
# not the part that merely looks suspicious.
pstats.Stats(profiler).sort_stats("tottime").print_stats(4)
