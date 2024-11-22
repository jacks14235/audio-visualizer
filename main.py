import time
import threading
import numpy as np
import sys
import pickle
from gradient import Gradient
from music import music
from image import image
from text import text, text_mask

class LightDisplay:
    def __init__(self, resolution, minUpdateTime):
        # self.layers = []
        self.last_update = 0
        self.minUpdateTime = minUpdateTime
        self.resolution = resolution
        self.layers = []
        self.layer_modes = []
  
    # func is a function which takes a numpy array of data as argument
    # addLayer begins func in a new thread and expects it to edit the array
    def addLayer(self, func, mode, *args):
        array = np.zeros((*self.resolution, 3), np.uint8)
        self.layers.append(array)
        self.layer_modes.append(mode)
        t = threading.Thread(target=func, args=(array, self.resolution, *args))
        t.daemon = True
        print("starting", func, file=sys.stderr)
        t.start()
        return array
    
    def removeLayer(self, index):
        if index < 0 or index >= len(self.layers):
            print(f"layer {index} out of range for {len(self.layers)} layers.", file=sys.stderr)
            return
        del self.layers[index]
  
    def update_data(self):
        pixels = np.zeros((*self.resolution, 3), dtype=np.uint8)
        for i in range(len(self.layers)):
            if self.layer_modes[i] == 'add':
                pixels += self.layers[i]
            else:
                mask = np.invert(np.all(self.layers[i] == 0, axis=-1))
                pixels[mask] = self.layers[i][mask]
        return pixels.reshape((self.resolution[0] * self.resolution[1], 3), order='F')


def grad(data, _):
    grad = Gradient.rainbow()
    t = 0
    while True:
        t += .002
        color = grad.eval(t - t // 1)
        data[:,:] = color
        time.sleep(.016)

def christmas(data, _):
    t = 0
    while True:
        t += .4
        new_data = np.array([i for i in range(data.shape[0] * data.shape[1])]).reshape((data.shape[0], data.shape[1]))
        new_data += int(t // 1)
        new_data = new_data % (new_data.shape[0] + 3)
        new_data = new_data // (new_data.shape[0] // 2 + 1)

        # Create a new array with an additional dimension for color
        new_array = np.zeros((*new_data.shape, 3), dtype=np.uint8)

        # Replace 0s with [255, 0, 0] and 1s with [0, 255, 0]
        new_array.fill(255)
        new_array[new_data == 0] = [255, 0, 0]
        new_array[new_data == 1] = [0, 255, 0]
        data[:] = new_array
        # print('new_array', file=sys.stderr)
        # print(new_array, file=sys.stderr)
        time.sleep(.016)

ld = LightDisplay((29, 29), .1)
print("BEFORE", file=sys.stderr)
# ld.addLayer(grad, 'add')
# print("AFTER", file=sys.stderr)
ld.addLayer(image, 'add', 'jets.jpg')
ld.addLayer(music, 'pizza')
# ld.addLayer(christmas, 'add')
# ld.addLayer(text_mask, 'fill')
# ld.addLayer(text, 'fill', 'merry christmas')

while True:
    pixels = ld.update_data()
    try:
        pickle.dump(pixels, sys.stdout.buffer)
        sys.stdout.buffer.flush()
    except Exception as e:
        print(e)
    time.sleep(.033)