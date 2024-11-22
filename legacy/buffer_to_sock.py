import numpy as np
import sys
import pickle
import time

array = DotArray(29,29, upscale_factor=1)
while True:
  try:
    arr = pickle.load(sys.stdin.buffer)
  except pickle.UnpicklingError as p:
    print("ERROR:", p)
  array.update(arr)
