from collections import OrderedDict
from enum import Enum


class Judge:
    class Judge(Enum):
        PERF = 4
        GREAT = 3
        GOOD = 2
        BAD = 1
        MISS = 0

    timings = OrderedDict([
        (Judge.PERF, 43),
        (Judge.GREAT, 76),
        (Judge.GOOD, 106),
        (Judge.BAD, 127),
        (Judge.MISS, 164)
    ])

    judge_accuracy = {
        Judge.PERF: 100,
        Judge.GREAT: 75,
        Judge.GOOD: 50,
        Judge.BAD: 25,
        Judge.MISS: 0
    }

    def __init__(self):
        self.hits = {e: 0 for e in Judge.Judge}
        self.judgements = 0

        self.combo = 0
        self.accuracy = 100.0

    def miss(self):
        self.hits[Judge.Judge.MISS] += 1
        self.judgements += 1
        self.combo = 0

    def judge(self, diff_timing: int):
        if diff_timing > self.timings[Judge.Judge.MISS]:
            return False
        for judgement, window in self.timings.items():
            if abs(diff_timing) < window:
                self.hits[judgement] += 1
                if judgement == Judge.Judge.MISS:
                    self.combo = 0
                else:
                    self.combo += 1
                self.judgements += 1

                self.accuracy = (self.accuracy * self.judgements - 1 + self.judge_accuracy[judgement]) / self.judgements
                print(self.accuracy)  # todo: fix accuracy
                return True  # don't judge for worse judgements
