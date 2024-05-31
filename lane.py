import pygame.sprite

from note import Note, Hold


class Lane(pygame.sprite.Group):
    def __init__(self, lane: int, *sprites):
        super().__init__(*sprites)
        self.lane = lane

    def judge(self, timing: int, judge_type: int):
        # get closest note or earliest note?

        # hits = [timing - note.timing for note in self]
        # hits.sort(key=lambda a: abs(a))  # get closest note
        # print(hits[0])

        if len(self.sprites()) > 0:
            note = self.sprites()[0]

            should_judge_keydown = (isinstance(note, Note) or
                                    (isinstance(note, Hold) and not note.is_held) and
                                    judge_type == pygame.KEYDOWN)
            should_judge_keyup = (isinstance(note, Hold) and
                                  note.is_held and
                                  judge_type == pygame.KEYUP)

            if should_judge_keydown or should_judge_keyup:
                note.judge(timing)

