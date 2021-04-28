import pygame

pygame.init()

w, h = 840, 650
win = pygame.display.set_mode((w, h))
pygame.display.set_caption("Car Race")

clock = pygame.time.Clock()
Font_ = pygame.font.SysFont('system', 35)


def text(txt, x, y, clr):
    text = Font_.render(txt, 1, clr)
    win.blit(text, (x, y))


def small_text():
    pass