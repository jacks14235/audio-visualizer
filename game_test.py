import pygame
import numpy as np
import math

pygame.init()
screen = pygame.display.set_mode((400, 400))

color = lambda x: 255 * ((math.sin(.005 * x) + 1) / 2)

x = 0
image = np.zeros((400, 400, 3), dtype=np.uint8)

left = image[:200]
right = image[200:]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the image
    x += 1
    
    left[:,:] = np.array([255, 0, color(x)])

    # Create a new surface from the updated array
    surface = pygame.surfarray.make_surface(image)

    # Blit the surface onto the screen and update the display
    screen.blit(surface, (0, 0))
    pygame.display.update()
