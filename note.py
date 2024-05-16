import pygame.sprite
from globals import *
from judge import Judge


class Note(pygame.sprite.Sprite):
    HEIGHT = 15
    COLOR = (15, 50, 255)

    def __init__(self, timing: int, lane: int, judge: Judge):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((WIDTH // LANES, Note.HEIGHT))
        self.image.fill(Note.COLOR)

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
