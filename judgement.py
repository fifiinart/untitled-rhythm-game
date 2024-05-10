from collections import OrderedDict
from enum import Enum


class Judgement:
    class Judgement(Enum):
        PERF = 4
        GREAT = 3
        GOOD = 2
        BAD = 1
        MISS = 0

    timings = OrderedDict([
        (Judgement.PERF, 43),
        (Judgement.GREAT, 76),
        (Judgement.GOOD, 106),
        (Judgement.BAD, 127),
        (Judgement.MISS, 164)
    ])

    def __init__(self):
        self.hits = {e: 0 for e in Judgement.Judgement}

        self.combo = 0
        self.accuracy = 1.00

    def miss(self):
        self.hits[Judgement.Judgement.MISS] += 1

        self.combo = 0

    def judge(self):
        pass
        # todo: set up judgement and updating of accuracy
