import pygame
import numpy as np
import math
import fourier


WIDTH = 400
HEIGHT = 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

color = lambda x: 255 * ((math.sin(.005 * x) + 1) / 2)

x = 0
image = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)


current_vals = [.16, .33, .5, .67, .83, 1, .83, .66,.5,.33,.17,0]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the image
    x += 1

    image = np.zeros((WIDTH, HEIGHT, 3))

    bucket_width = WIDTH / len(current_vals)
    for i, val in enumerate(current_vals):
        height = int(HEIGHT * val)
        start = int(i * bucket_width)
        end = int((i+1) * bucket_width)
        print(start, end, height)
        image[start:end, :height, :] = np.array([255, 0, 0])


    # Create a new surface from the updated array
    surface = pygame.surfarray.make_surface(image)

    # Blit the surface onto the screen and update the display
    screen.blit(surface, (0, 0))
    pygame.display.update()
