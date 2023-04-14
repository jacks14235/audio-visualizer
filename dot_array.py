import numpy as np
import pygame
import time

DOT_RADIUS = 2

class DotArray:
	def __init__(self, w, h, res=(512,512)):
		self.w = w
		self.h = h
		self.res = res
		self.array = np.zeros(res[0]*res[1])

		# find coordinates contained in each dot
		dots = np.zeros((w*h, DOT_RADIUS * DOT_RADIUS * 4), dtype=np.int32)
		spacing_x = (res[0] - DOT_RADIUS * 2 * w) / (w + 1)
		spacing_y = (res[1] - DOT_RADIUS * 2 * h) / (h + 1)
		if spacing_x < 0:
			raise ValueError("Not enough spacing on x-axis")
		if spacing_y < 0:
			raise ValueError("Not enough spacing on y-axis")
		for y in range(h):
			for x in range(w):
				left = int((x + 1) * spacing_x + 2 * x * DOT_RADIUS)
				top = int((y + 1) * spacing_y + 2 * y * DOT_RADIUS)
				for j in range(DOT_RADIUS * 2):
					for i in range(DOT_RADIUS * 2):
						dots[x + y * w][i + j * DOT_RADIUS * 2] = res[0] * (top + j) + left + i
		self.dots = dots

		# initialize pygame stuff
		pygame.init()
		self.screen = pygame.display.set_mode(res)
		self.surface = pygame.surfarray.make_surface(np.zeros(res))
	
	# takes array of shape (w*h, 3)
	def update(self, colors):
		self.game_events()
		image = np.zeros((self.res[0]*self.res[1], 3), dtype=np.uint8)
		# image.fill(255)
		image[self.dots, :] = colors[:, np.newaxis, :]
		surface = pygame.surfarray.make_surface(image.reshape(self.res[0], self.res[1], 3))
		self.screen.blit(surface, (0,0))
		pygame.display.update()
		time.sleep(1/60)

	def game_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_running = False

d = DotArray(48, 48)


activated = np.zeros((48 * 48,3), dtype=np.int8)
activated.fill(255)
print(activated.shape)
for i in range(1):
	d.update(activated)

time.sleep(10)