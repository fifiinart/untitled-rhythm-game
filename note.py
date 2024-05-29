import pygame.sprite
from globals import *
from judge import Judge


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
        self.rect.x, self.rect.y = self.calculate_pos(timing, self.start_timing, self.rect, self.lane)

        if timing - self.start_timing > self._judge.timings[Judge.Judge.MISS]:
            self._judge.on_judge(Judge.Judge.MISS)
            self.kill()

    def calculate_pos(self, timing, note_timing, rect, lane):
        return lane * WIDTH // LANES, (timing - note_timing) * NOTE_SPEED + (JUDGEMENT_LINE_POS - rect.height)

    def judge(self, timing: int):
        if self._judge.judge(timing - self.start_timing):
            self.kill()


class Hold(Note):
    def __init__(self, timing: int, lane: int, end_timing: int, judge: Judge):
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
        self.hold_image.fill((*NOTE_COLOR, HOLD_TRANSPARENCY))
        self.hold_rect = self.hold_image.get_rect()

        self.is_held = False

    def update(self, timing: int) -> None:
        self.end_rect.x, self.end_rect.y = self.calculate_pos(timing, self.end_timing, self.end_rect, self.lane)
        self.start_rect.x, self.start_rect.y = self.calculate_pos(timing, timing if self.is_held else self.start_timing, self.start_rect,
                                                                  self.lane)
        height_difference = self.end_rect.y - self.start_rect.y
        if self.hold_rect.h != height_difference:
            self.hold_rect.h = height_difference
        self.hold_rect.midbottom = self.start_rect.centerx, self.start_rect.bottom + NOTE_HEIGHT // 2

        if not self.is_held:
            if timing - self.start_timing > self._judge.timings[Judge.Judge.MISS]:
                self._judge.on_judge(Judge.Judge.MISS)  # start
                self._judge.on_judge(Judge.Judge.MISS)  # end
                self.kill()
        else:
            if timing - self.end_timing > self._judge.timings[Judge.Judge.MISS]:
                self._judge.on_judge(Judge.Judge.MISS)
                self.kill()

        self.image = pygame.Surface((WIDTH // LANES, abs(self.end_rect.x - self.end_rect.y) + NOTE_HEIGHT))
        self.image.blits([
            (self.hold_image, self.hold_rect),
            (self.end_image, self.end_rect),
            (self.start_image, self.start_rect)
        ])
        self.rect.bottomleft = self.start_rect.bottomleft

    def judge(self, timing: int):
        if not self.is_held:
            if self._judge.judge(timing - self.start_timing):
                self.is_held = True
        else:
            if self._judge.judge(timing - self.end_timing):
                self.is_held = False
                self.kill()
