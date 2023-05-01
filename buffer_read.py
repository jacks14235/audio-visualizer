"""
Works with finaler.py to make a pygame window that doesn't crash
"""


from dot_array import DotArray
import numpy as np
import sys
import pickle
import time

array = DotArray(11,11)
while True:
  try:
    arr = pickle.load(sys.stdin.buffer)
  except pickle.UnpicklingError as p:
    print("ERROR:", p)
  array.update(arr)
