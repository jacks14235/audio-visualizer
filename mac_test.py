import pygame
from gradient import Gradient
import numpy as np
from scipy.io import wavfile



CHUNK = 1024
dCHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10000
WAVE_OUTPUT_FILENAME = "output.wav"
DEPTH = 16
buckets = [40,80,160,320,640,1280,2560,5120,10240,20480]

#setup screen
WIDTH = 400
HEIGHT = 400
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.surfarray.make_surface(np.zeros((WIDTH, HEIGHT)))
grad = Gradient.rainbow()

running_len = 10
running = np.zeros((running_len, len(buckets)))
curr = 0
weights = 2**np.array([i for i in range(len(buckets))])

fs, data = wavfile.read('loopback_record.wav')


