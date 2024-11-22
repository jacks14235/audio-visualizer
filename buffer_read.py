"""
Works with finaler.py to make a pygame window that doesn't crash
"""


from dot_array import DotArray
import numpy as np
import sys
import pickle
import time

array = DotArray(29,29, upscale_factor=1)
while True:
  try:
    arr = pickle.load(sys.stdin.buffer)
    array.update(arr)
  except pickle.UnpicklingError as p:
    print("ERROR:", p)
  except OSError as e:
    print("OSError", e)
