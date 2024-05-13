import pygame.sprite

from note import Note


class Lane(pygame.sprite.Group):
    def __init__(self, lane: int, *sprites):
        super().__init__(*sprites)
        self.lane = lane

    def judge(self, timing: int):
        # get closest note or earliest note?

        # hits = [timing - note.timing for note in self]
        # hits.sort(key=lambda a: abs(a))  # get closest note
        # print(hits[0])

        if len(self.sprites()) > 0:
            note: Note = self.sprites()[0]
            note.judge(timing)

