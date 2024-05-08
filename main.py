import pygame
from globals import *
from note import Note

judgement_line = pygame.Rect(0, JUDGEMENT_LINE_POS, WIDTH, 2)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Untitled Rhythm Game")
clock = pygame.time.Clock()

# group all the sprites together for ease of update
notes = pygame.sprite.Group()

BPM = 120
OFFSET = 56
# last_beat = 56  # ms offset
# next_beat = last_beat + 60000 // 120

notes.add(*[Note(OFFSET + i * (60000 // BPM)) for i in range(8)])  # pool 8 notes for use currently

print([note.timing for note in notes])

hits = []

pygame.mixer_music.load("beat.mp3")
pygame.mixer_music.play()

# Game loop
running = True
while running and pygame.mixer_music.get_busy():
    # 1 Process input/events
    clock.tick(FPS)  # will make the loop run at the same speed all the time

    timing = pygame.mixer_music.get_pos()

    for event in pygame.event.get():  # gets all the events which have occurred till now and keeps tab of them.
        # listening for the X button at the top
        if event.type == pygame.QUIT:
            # print(sum(hits) / len(hits))
            running = False

        # if event.type == pygame.KEYDOWN:
            # print(timing - last_beat)
            # hits.append(timing - last_beat)

    # 2 Update
    notes.update(timing)

    # if next_beat <= pygame.mixer_music.get_pos():
    #     last_beat += (60000 // BPM)
    #     next_beat += (60000 // BPM)
    #     screen.fill((255, 255, 255))
    # else:
    #     # 3 Draw/render
    #     screen.fill((0, 0, 0))

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, JUDGEMENT_LINE_COL, judgement_line)
    notes.draw(screen)

    # Done after drawing everything to the screen
    pygame.display.flip()

pygame.quit()
