import pygame

WIDTH = 400
HEIGHT = 400
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Untitled Rhythm Game")
clock = pygame.time.Clock()

# group all the sprites together for ease of update
all_sprites = pygame.sprite.Group()

BPM = 120
last_beat = 56 # ms offset
next_beat = last_beat + 60000 // 120
hits = []

pygame.mixer_music.load("beat.mp3")
pygame.mixer_music.play()

# Game loop
running = True
while running and pygame.mixer_music.get_busy():
    # 1 Process input/events
    clock.tick(FPS)  # will make the loop run at the same speed all the time
    for event in pygame.event.get():  # gets all the events which have occurred till now and keeps tab of them.
        # listening for the X button at the top
        if event.type == pygame.QUIT:
            print(sum(hits) / len(hits))
            running = False

        if event.type == pygame.KEYDOWN:
            print(pygame.mixer_music.get_pos() - last_beat)
            hits.append(pygame.mixer_music.get_pos() - last_beat)

    # 2 Update
    all_sprites.update()

    if next_beat <= pygame.mixer_music.get_pos():
        last_beat += (60000 // BPM)
        next_beat += (60000 // BPM)
        screen.fill((255, 255, 255))
    else:
        # 3 Draw/render
        screen.fill((0, 0, 0))

    all_sprites.draw(screen)
    ########################

    # Your code comes here

    ########################

    # Done after drawing everything to the screen
    pygame.display.flip()

pygame.quit()
