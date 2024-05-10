import pygame
from globals import *
from judgement import Judgement
from lane import Lane
from note import Note

judgement_line = pygame.Rect(0, JUDGEMENT_LINE_POS, WIDTH, LINE_WIDTH)
lane_separators = [pygame.Rect(WIDTH // LANES * i - (LINE_WIDTH / 2), 0, LINE_WIDTH, HEIGHT) for i in range(1, LANES)]

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Untitled Rhythm Game")
clock = pygame.time.Clock()

# group all the sprites together for ease of update
notes: pygame.sprite.Group = pygame.sprite.Group()
lanes: list[Lane] = [Lane(i) for i in range(LANES)]

BPM = 120
OFFSET = 56

judgement = Judgement()

# pool 8 notes for testing
notes.add(*[Note(OFFSET + i * (60000 // BPM), i % LANES, judgement) for i in range(8)])

# sort notes into lanes
for note in notes:
    lanes[note.lane].add(note)


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
            running = False

        if event.type == pygame.KEYDOWN:
            try:
                index = LANE_KEYS.index(event.key)
                lanes[index].judge(timing)
            except ValueError:
                print("invalid key " + str(event.key))

    # 2 Update
    notes.update(timing)

    screen.fill((0, 0, 0))

    [pygame.draw.rect(screen, LANE_SEP_COL, sep) for sep in lane_separators]
    pygame.draw.rect(screen, JUDGEMENT_LINE_COL, judgement_line)
    notes.draw(screen)

    pygame.display.flip()

pygame.quit()
