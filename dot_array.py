import numpy as np
import pygame
import time

DOT_RADIUS = 14

class DotArray:
	def __init__(self, w, h, res=(1024,1024), upscale_factor = 1):
		self.upscale_factor = upscale_factor
		h *= self.upscale_factor
		w *= self.upscale_factor
		self.w = w
		self.h = h
		self.res = res
		self.array = np.zeros(res[0]*res[1])
		self.count = 0

		# find coordinates contained in each dot
		dots = np.zeros((h*w, DOT_RADIUS * DOT_RADIUS * 4), dtype=np.int32)
		spacing_x = (res[0] - DOT_RADIUS * 2 * h) / (h + 1)
		spacing_y = (res[1] - DOT_RADIUS * 2 * w) / (w + 1)
		if spacing_x < 0:
			raise ValueError("Not enough spacing on x-axis")
		if spacing_y < 0:
			raise ValueError("Not enough spacing on y-axis")
		for y in range(w):
			for x in range(h):
				left = int((x + 1) * spacing_x + 2 * x * DOT_RADIUS)
				top = int((y + 1) * spacing_y + 2 * y * DOT_RADIUS)
				for j in range(DOT_RADIUS * 2):
					for i in range(DOT_RADIUS * 2):
						dots[x + y * h][i + j * DOT_RADIUS * 2] = res[0] * (top + j) + left + i
		self.dots = dots

		# initialize pygame stuff
		pygame.init()
		self.screen = pygame.display.set_mode(res)
		self.surface = pygame.surfarray.make_surface(np.zeros(res))
	
	# takes array of shape (w*h, 3)
	def update(self, colors):
		# pygame.event.pump()
		self.game_events()

		# put into column-major order
		colors = colors.reshape((self.w // self.upscale_factor, self.h // self.upscale_factor, 3))
		# expand each entry into square of pixels
		colors = np.repeat(colors, self.upscale_factor, axis=1)
		colors = np.repeat(colors, self.upscale_factor, axis=0)
		# finish column-major-order
		colors = colors.reshape((self.w * self.h, 3), order='F')

		image = np.zeros((self.res[0]*self.res[1], 3), dtype=np.uint8)
		image[self.dots, :] = colors[:, np.newaxis, :]
		surface = pygame.surfarray.make_surface(image.reshape(self.res[0], self.res[1], 3))
		self.screen.blit(surface, (0,0))
		pygame.display.update()
		# print('updated', self.count)
		self.count += 1

	def game_events(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				raise RuntimeError("QUIT EVENT")


if __name__ == '__main__':
	d = DotArray(10, 10)

	activated = np.zeros((10 * 10,3), dtype=np.int8)
	activated.fill(255)
	print(activated.shape)
	for i in range(1):
		d.update(activated)

	time.sleep(10)