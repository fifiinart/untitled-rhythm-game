import pygame

WIDTH = 400
HEIGHT = 400
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hello World")
clock = pygame.time.Clock()

# group all the sprites together for ease of update
all_sprites = pygame.sprite.Group()

# Game loop
running = True
while running:

    # 1 Process input/events
    clock.tick(FPS)  # will make the loop run at the same speed all the time
    for event in pygame.event.get():  # gets all the events which have occurred till now and keeps tab of them.
        # listening for the X button at the top
        if event.type == pygame.QUIT:
            running = False

    # 2 Update
    all_sprites.update()

    # 3 Draw/render
    screen.fill((0, 0, 0))

    all_sprites.draw(screen)
    ########################

    # Your code comes here

    ########################

    # Done after drawing everything to the screen
    pygame.display.flip()

pygame.quit()
