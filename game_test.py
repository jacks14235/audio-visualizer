import pygame
import numpy as np
import math
import fourier
from gradient import Gradient


WIDTH = 400
HEIGHT = 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.surfarray.make_surface(np.zeros((WIDTH, HEIGHT)))

color = lambda x: 255 * ((math.sin(.005 * x) + 1) / 2)

image = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)
reader = fourier.TestReader()

running_len = 15
running = np.zeros((running_len, fourier.NUM_BUCKETS))
curr = 0
weights = 2**np.array([i for i in range(fourier.NUM_BUCKETS)])

grad = Gradient.heat()

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    image = np.zeros((WIDTH, HEIGHT, 3))
    current_vals = (reader.getNextVals() * 150) * weights
    running[curr % running_len] = current_vals
    curr+=1

    avgs = np.average(running, axis=0)
    bucket_width = WIDTH / len(avgs)
    for i, val in enumerate(avgs):
        height = int(HEIGHT * (1-val))
        start = int(i * bucket_width)
        end = int((i+1) * bucket_width)
        # print(start, end, height)
        image[start:end, height:, :] = np.array(grad.eval(val))


    # Create a new surface from the updated array
    surface = pygame.surfarray.make_surface(image)

    # Blit the surface onto the screen and update the display
    screen.blit(surface, (0, 0))
    pygame.display.update()
