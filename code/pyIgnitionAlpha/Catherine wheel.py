# Catherine wheel

import PyIgnition, pygame, sys


screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("PyIgnition demo: catherine wheel")
clock = pygame.time.Clock()

wheel = PyIgnition.ParticleEffect(screen, (0, 0), (600, 600))
image = pygame.image.load("Spark.png").convert_alpha()
flame = wheel.CreateSource((300, 300), 20.0, 0.0, 0.0, 0.5, 3, 50, PyIgnition.DRAWTYPE_SCALELINE, colour = (255, 200, 200), length = 20.0)
sparks = wheel.CreateSource((300, 300), 1.0, 0.0, 0.9, 3.141592653, 1, 300, PyIgnition.DRAWTYPE_IMAGE, image = image)
wheel.CreateDirectedGravity(strength = 0.05, direction = [0, 1])

velocity = 0.1
maxvelocity = 0.5
acceleration = 0.001


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	
	flame.initdirection += velocity
	
	if velocity <= maxvelocity:
		velocity += acceleration
	
	screen.fill((10, 0, 50))
	wheel.Update()
	wheel.Redraw()
	pygame.display.update()
	clock.tick(30)
