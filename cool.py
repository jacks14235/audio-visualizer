import time
import pickle
import numpy as np
import sys
from noise import pnoise3
from PIL import Image

pixels = pnoise3(32, 32, 3, octaves=1)
print(pixels)

# while True:
#     try:
#         pickle.dump(pixels, sys.stdout.buffer)
#         sys.stdout.buffer.flush()
#     except Exception as e:
#         print(e)
#     time.sleep(.033)