# PyIgnition test

import pygame, sys

from pyIgnitionAlpha.PyIgnition import ParticleEffect, DRAWTYPE_CIRCLE

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PyIgnition demo: fire")
clock = pygame.time.Clock()

fire = ParticleEffect(screen, (0, 0), (800, 600))
gravity = fire.CreateDirectedGravity(strength=0.07, direction=[0, -1])
wind = fire.CreateDirectedGravity(strength=0.05, direction=[1, 0])
source = fire.CreateSource((300, 500), 2.0, 0.0, 1.0, 0.5, 10, 100, DRAWTYPE_CIRCLE, (255, 200, 100), 3.0)
source.CreateParticleKeyframe(10, colour=(200, 50, 20), radius=4.0)
source.CreateParticleKeyframe(30, colour=(150, 0, 0), radius=6.0)
source.CreateParticleKeyframe(60, colour=(50, 20, 20), radius=20.0)
source.CreateParticleKeyframe(80, colour=(0, 0, 0), radius=50.0)
# source.CreateKeyframe(100, (500, 500), 2.0, 0.0, 1.0, 0.5, 10)
# source.CreateKeyframe(200, (400, 500), 2.0, 0.0, 1.0, 0.5, 10)

if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))
        source.pos = pygame.mouse.get_pos()
        fire.Update()
        fire.Redraw()
        pygame.display.update()
        clock.tick(30)
