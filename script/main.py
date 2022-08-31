import pygame, sys
from settings import *
from level import Level

# pygame setup
pygame.init()
pygame.display.set_mode(REAL_RES, pygame.DOUBLEBUF|pygame.OPENGL)
screen = pygame.Surface(VIRTUAL_RES).convert((255, 65280, 16711680, 0))
crt_shader = Graphic_engine(screen=screen, style=2, VIRTUAL_RES=VIRTUAL_RES)

clock = pygame.time.Clock()
level = Level(level_data=level_map, surface=screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                crt_shader.change_shader()

    level.run()
    
    crt_shader()
    clock.tick(60)