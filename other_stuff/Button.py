import pygame

pygame.init()
font = pygame.font.SysFont("Arial", 20)


class Button:
    def __init__(self, text, x, y, bg="black"):
        self.x = x
        self.y = y
        self.change_text(text, bg)

    def change_text(self, text, bg="black"):
        self.text = font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
