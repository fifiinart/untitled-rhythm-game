import pygame.sprite
from globals import *
from judgement import Judgement


class Note(pygame.sprite.Sprite):
    HEIGHT = 15
    COLOR = (15, 50, 255)

    MISS_WINDOW = 250

    def __init__(self, timing: int, lane: int, judgement: Judgement):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((WIDTH // LANES, Note.HEIGHT))
        self.image.fill(Note.COLOR)

        self.rect = self.image.get_rect()
        self.timing = timing
        self.lane = lane

        self.judgement = judgement

    def update(self, timing: int) -> None:
        self.rect.x = self.lane * WIDTH // LANES
        self.rect.y = (timing - self.timing) * NOTE_SPEED + (JUDGEMENT_LINE_POS - self.rect.height)

        if timing - self.timing > self.MISS_WINDOW:
            self.judgement.miss()
            self.kill()

    def judge(self, timing: int):
        pass
