import pygame.sprite


class Lane(pygame.sprite.Group):
    def __init__(self, lane: int, *sprites):
        super().__init__(*sprites)
        self.lane = lane

    def judge(self, timing: int):
        hits = [timing - note.timing for note in self]
        hits.sort(key=lambda a: abs(a))  # get closest note
        print(hits[0])

