# Wind - randomised gravity

import PyIgnition, pygame, sys


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PyIgnition demo: wind")
clock = pygame.time.Clock()

effect = PyIgnition.ParticleEffect(screen, (0, 0), (800, 600))
source = effect.CreateSource((400, 600), 5.0, 0.0, 2.0, 0.2, 10, 200, PyIgnition.DRAWTYPE_POINT, colour = (255, 255, 200))
grav = effect.CreateDirectedGravity(0.0, 0.2, [1, 0])


if __name__ =="__main__":
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		screen.fill((100, 125, 200))
		effect.Update()
		effect.Redraw()
		pygame.display.update()
		clock.tick(30)