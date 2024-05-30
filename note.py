import pygame.sprite
from globals import *
from judge import Judge


def calculate_pos(timing, note_timing, rect, lane):
    return lane * WIDTH // LANES, (timing - note_timing) * NOTE_SPEED + (JUDGEMENT_LINE_POS - rect.height)


class Note(pygame.sprite.Sprite):

    def __init__(self, timing: int, lane: int, judge: Judge):
        super().__init__()

        self.image = pygame.Surface((WIDTH // LANES, NOTE_HEIGHT))
        self.image.fill(NOTE_COLOR)

        self.rect = self.image.get_rect()
        self.start_timing = timing
        self.lane = lane

        self._judge = judge

    def update(self, timing: int) -> None:
        self.rect.x, self.rect.y = calculate_pos(timing, self.start_timing, self.rect, self.lane)

        if timing - self.start_timing > self._judge.timings[Judge.Judge.MISS]:
            self._judge.on_judge(Judge.Judge.MISS)
            self.kill()

    def judge(self, timing: int):
        if self._judge.judge(timing - self.start_timing):
            self.kill()


class Hold(pygame.sprite.Sprite):

    def __init__(self, timing: int, lane: int, end_timing: int, judge: Judge):
        super().__init__()

        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()

        self.start_image = pygame.Surface((WIDTH // LANES, NOTE_HEIGHT))
        self.start_image.fill(NOTE_COLOR)

        self.start_rect = self.image.get_rect()
        self.start_timing = timing
        self.lane = lane

        self._judge = judge

        self.end_image = pygame.Surface((WIDTH // LANES, NOTE_HEIGHT))
        self.end_image.fill(NOTE_COLOR)
        self.end_rect = self.end_image.get_rect()

        self.end_timing = end_timing

        self.hold_image = pygame.Surface((WIDTH / LANES * 0.9, 0))
        self.hold_image.fill(NOTE_COLOR)
        self.hold_rect = self.hold_image.get_rect()

        self.is_held = False

    def update(self, timing: int) -> None:
        self.end_rect.x, self.end_rect.y = calculate_pos(timing, self.end_timing, self.end_rect, self.lane)
        self.start_rect.x, self.start_rect.y = calculate_pos(timing, timing if self.is_held else self.start_timing,
                                                             self.start_rect,
                                                             self.lane)
        height_difference = pygame.math.clamp(self.start_rect.y - self.end_rect.y, 0, float('inf'))
        if self.hold_rect.h != height_difference:
            self.hold_rect.h = height_difference
            self.hold_image.fill((255, 255, 255))

        if not self.is_held:
            if timing - self.start_timing > self._judge.timings[Judge.Judge.MISS]:
                self._judge.on_judge(Judge.Judge.MISS)  # start
                self._judge.on_judge(Judge.Judge.MISS)  # end
                self.kill()
        else:
            if timing - self.end_timing > self._judge.timings[Judge.Judge.MISS]:
                self._judge.on_judge(Judge.Judge.MISS)
                self.kill()

        self.image = pygame.Surface((WIDTH // LANES, abs(self.end_rect.y - self.start_rect.y) + NOTE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, self.start_rect.bottom)
        self.hold_rect.midbottom = self.rect.centerx, self.rect.bottom
        pygame.draw.rect(self.image, NOTE_COLOR, self.hold_rect)
        self.image.blits([
            (self.end_image, self.rect.topleft),
            (self.start_image, (self.rect.left, self.rect.bottom + NOTE_HEIGHT))
        ])
        self.rect.left = self.start_rect.left


    def judge(self, timing: int):
        if not self.is_held:
            if self._judge.judge(timing - self.start_timing):
                self.is_held = True
        else:
            if self._judge.judge(timing - self.end_timing):
                self.is_held = False
                self.kill()
