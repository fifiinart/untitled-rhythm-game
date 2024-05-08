import pygame.sprite
from globals import *


class Note(pygame.sprite.Sprite):
    WIDTH = 300 / 4
    HEIGHT = 15
    COLOR = (15, 50, 255)

    def __init__(self, timing: int):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((Note.WIDTH, Note.HEIGHT))
        self.image.fill(Note.COLOR)

        self.rect = self.image.get_rect()
        self.timing = timing

    def update(self, timing: int) -> None:
        self.rect.y = (timing - self.timing) * NOTE_SPEED + (JUDGEMENT_LINE_POS - self.rect.height)
