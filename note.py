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

        self.image = pygame.Surface((WIDTH // LANES, HEIGHT), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()

        self.start_image = pygame.Surface((WIDTH // LANES, NOTE_HEIGHT))
        self.start_image.fill(NOTE_COLOR)
        self.start_rect = self.start_image.get_rect()

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
        self.rect.x, self.end_rect.y = calculate_pos(timing, self.end_timing, self.end_rect, self.lane)
        _, self.start_rect.y = calculate_pos(timing, timing if self.is_held else self.start_timing,
                                                             self.start_rect,
                                                             self.lane)

        height_difference = min(self.start_rect.y, HEIGHT) - max(self.end_rect.y, 0)
        if self.hold_rect.h != abs(height_difference):
            self.hold_rect.h = abs(height_difference)

            self.hold_image = pygame.Surface(self.hold_rect.size)
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

        self.image.fill((255, 255, 255, 0))
        self.hold_rect.topleft = (WIDTH // LANES // 2 - self.hold_rect.w // 2,
                                  self.end_rect.centery if height_difference > 0
                                  else self.start_rect.centery)

        # if self.end_rect.bottom >= 0 and self.end_rect.top <= 600:
        #     self.image.blit(self.end_image, (0, self.end_rect.y))
        # if self.start_rect.bottom >= 0 and self.start_rect.top <= 600:
        #     self.image.blit(self.start_image, (0, self.start_rect.y))
        # if height_difference > 0:
        #     self.image.blit(self.hold_image, (WIDTH // LANES // 2 - self.hold_rect.w // 2,
        #                                       self.end_rect.centery if height_difference > 0
        #                                       else self.start_rect.centery))

        # self.image.blit(self.start_image, (0, self.start_rect.y))
        # self.image.blit(self.end_image, (0, self.end_rect.y))
        pygame.draw.rect(self.image, NOTE_COLOR, self.start_rect)
        pygame.draw.rect(self.image, NOTE_COLOR, self.end_rect)
        pygame.draw.rect(self.image, NOTE_COLOR, self.hold_rect)

    def judge(self, timing: int):
        if not self.is_held:
            if self._judge.judge(timing - self.start_timing):
                self.is_held = True
        else:
            print("keyup")
            if self._judge.judge(timing - self.end_timing):
                self.is_held = False
                self.kill()
