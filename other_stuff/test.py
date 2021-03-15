import pygame
from other_stuff.Button import Button


pygame.init()
WIN = pygame.display.set_mode((500, 500))
WIN.fill((155,155,155))
FPS = 60


def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    pygame.quit()


main()
