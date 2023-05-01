import socket
import pickle
import numpy as np
# import neopixel
# import board
from dot_array import DotArray

PORT = 7777
HOST='127.0.0.1'

# pixels1 = neopixel.NeoPixel(board.D18, 150, brightness=.03)
count = 0
array = DotArray(11, 11)

def get_wall_indices(size, gap):
    indices = []
    gaps = []
    count = 0
    for i in range(size):
        if i % 2 == 0:
            # up
            curr = size - i - 1
            inc = size
        else:
            # down
            curr = size * size - (i + 1)
            inc = -size
        for _ in range(size):
            indices.append(curr)
            curr += inc
            count += 1
        if i != size -1:
            for _ in range(gap):
                indices.append(0)
                gaps.append(count)
                count += 1
    return indices, gaps

def main():
   wall_indices, wall_gaps = get_wall_indices(11, 2)

   with socket.socket() as sock:
        sock.bind(('', PORT))
        sock.listen()
        print("Listening...")
        accepted = sock.accept()
        conn = accepted[0]
        with conn:
            while True:
                try:
                    in_flo = conn.makefile(mode='rb')
                    data = pickle.load(in_flo)
                    reshaped = data[wall_indices]
                    #print(len(pixels1))
                    #print("2")
                    reshaped[wall_gaps] = [0,0,0]
                    # pixels1[:len(wall_indices)-1]=reshaped
                    array.update()
                except pickle.UnpicklingError as e:
                    print('Error')

if __name__ == '__main__':
    main()
