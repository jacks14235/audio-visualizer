"""
Works with finaler.py to make a pygame window that doesn't crash
"""


from dot_array import DotArray
import numpy as np
import sys
array = DotArray(10,10)
while True:
  arr = np.load(sys.stdin.buffer)
  array.update(arr)