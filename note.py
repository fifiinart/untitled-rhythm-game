import pygame.sprite
from globals import *
from judge import Judge


class Note(pygame.sprite.Sprite):

    def __init__(self, timing: int, lane: int, judge: Judge):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((WIDTH // LANES, NOTE_HEIGHT))
        self.image.fill(NOTE_COLOR)

        self.rect = self.image.get_rect()
        self.timing = timing
        self.lane = lane

        self._judge = judge

    def update(self, timing: int) -> None:
        self.rect.x = self.lane * WIDTH // LANES
        self.rect.y = (timing - self.timing) * NOTE_SPEED + (JUDGEMENT_LINE_POS - self.rect.height)

        if timing - self.timing > self._judge.timings[Judge.Judge.MISS]:
            self._judge.on_judge(Judge.Judge.MISS)
            self.kill()

    def judge(self, timing: int):
        if self._judge.judge(timing - self.timing):
            self.kill()
