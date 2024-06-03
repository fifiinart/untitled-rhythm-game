import re

import pygame
from globals import *
from judge import Judge
from lane import Lane
from note import Note, Hold
from graphics import Graphics

judgement_line = pygame.Rect(0, JUDGEMENT_LINE_POS, WIDTH, LINE_WIDTH)
lane_separators = [pygame.Rect(WIDTH // LANES * i - (LINE_WIDTH / 2), 0, LINE_WIDTH, HEIGHT) for i in range(1, LANES)]

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()



beatmap = {
    "general": {},
    "metadata": {},
    "hit-objects": []
}
with open("beat.osu", "r") as f:
    state = None
    for line in f:
        if not re.match(r"^\s*$", line):  # just whitespace
            if m := re.match(r"\[(.+)]", line):  # new [Header]
                state = m.group(1)
            elif state == "General":
                k, v = re.match(r"(.+):\s*(.+)", line).groups()  # $key: $value format
                beatmap["general"][k] = v
            elif state == "Metadata":
                k, v = re.match(r"(.+):\s*(.+)", line).groups()  # $key: $value format
                beatmap["metadata"][k] = v
            elif state == "HitObjects":
                x, time, type, end_time = re.match(r"^(\d+),\d+,(\d+),(\d+),\d+,(\d+)", line).groups()
                beatmap["hit-objects"].append((int(x), int(time), int(type), int(end_time)))


pygame.display.set_caption(beatmap["metadata"]["Title"] + " - " + beatmap["metadata"]["Artist"])

# group all the sprites together for ease of update
notes: pygame.sprite.Group = pygame.sprite.Group()
lanes: list[Lane] = [Lane(i) for i in range(LANES)]

graphics = Graphics(notes)

BPM = 120
OFFSET = 56

judge = Judge()

judge.on_judge_event += [graphics.render_accuracy, graphics.render_combo]
#
# for x, time, type, end_time in beatmap["hit-objects"]:
#     if type == 3:
#         note = Hold(time, x * 4 // 512, end_time, judge)
#     else:
#         note = Note(time, x * 4 // 512, judge)
#     notes.add(note)
#     lanes[x * 4 // 512].add(note)

for i in range(8):
    note = Hold(i * 1000, i % 4, i * 1000 + 500, judge)
    note2 = Note(i * 1000, (i+1) % 4, judge)
    note3 = Note(i * 1000 + 500, (i + 1) % 4, judge)
    # notes.add(note)
    # lanes[i % 4].add(note)
    for n in [note, note2, note3]:
        notes.add(n)
        lanes[n.lane].add(n)


# # sort notes into lanes
# for note in notes:
#     lanes[note.lane].add(note)

hits = []
wait_timer = 2000
pygame.mixer_music.load("beat.mp3")

# Game loop
running = True

while running and (wait_timer > 0 or pygame.mixer_music.get_busy()):
    # 1 Process input/events
    clock.tick(FPS)  # will make the loop run at the same speed all the time

    if wait_timer > 0:
        wait_timer -= clock.get_time()
        timing = -wait_timer
        if wait_timer <= 0:
            pygame.mixer_music.play()

    if wait_timer <= 0:
        timing = pygame.mixer_music.get_pos()

    for event in pygame.event.get():  # gets all the events which have occurred till now and keeps tab of them.
        # listening for the X button at the top
        if event.type == pygame.QUIT:
            running = False

        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            try:
                index = LANE_KEYS.index(event.key)
                lanes[index].judge(timing, event.type)
            except ValueError:
                pass

    # 2 Update
    notes.update(timing)

    graphics.draw(screen)

pygame.quit()
