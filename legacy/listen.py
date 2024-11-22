import pyaudiowpatch as pyaudio
from scipy.fftpack import fft, fftfreq
import numpy as np
import wave
import pygame
from gradient import Gradient

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
DEPTH = 16
buckets = [40,80,160,320,640,1280,2560,5120,10240,20480]

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                input_device_index = 3,
                frames_per_buffer = CHUNK)

# for i in range(p.get_device_count()):
#     device = p.get_device_info_by_index(i)
#     if 'Stereo Mix' in device['name']:
#        print(device)

#setup screen
WIDTH = 400
HEIGHT = 400
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.surfarray.make_surface(np.zeros((WIDTH, HEIGHT)))
grad = Gradient.heat()

running_len = 10
running = np.zeros((running_len, len(buckets)))
curr = 0
weights = 2**np.array([i for i in range(len(buckets))])

frames = []
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
def callback(raw_data, frame_count, time_info, status):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_running = False
	# raw_data = stream.read(CHUNK)
	frames.append(raw_data)
	data = np.frombuffer(raw_data, dtype=np.int16) / (2**(DEPTH - 1))

	
	yf = fft(data)
	xf = fftfreq(CHUNK, 1 / RATE)
	avgs = np.zeros(len(buckets))
	bucket = 0
	start = 0
	while xf[start] < buckets[0]:
		start+=1
	for i in range(start, len(xf)):
		if (bucket+ 1 == len(buckets)):
			break
		if (xf[i] > buckets[bucket + 1]):
			if (i - start < 1):
				avgs[bucket] = avgs[bucket - 1]
				bucket += 1
			else:
				avgs[bucket] = np.abs(np.average(yf[start:i]))
				start = i
				bucket += 1
	
	image = np.zeros((WIDTH, HEIGHT, 3))
	current_vals = (.25 * avgs) * weights
	running[curr % running_len] = current_vals
	curr+=1
	
	running_avg = np.average(running, axis=0)
	bucket_width = WIDTH / len(buckets)
	for i, val in enumerate(running_avg):
		height = int(HEIGHT * (1-val))
		start = int(i * bucket_width)
		end = int((i+1) * bucket_width)
		# print(start, end, height)
		image[start:end, height:, :] = np.array(grad.eval(val))

	surface = pygame.surfarray.make_surface(image)

    # Blit the surface onto the screen and update the display
	screen.blit(surface, (0, 0))
	pygame.display.update()
	

print('* done recording')
stream.stop_stream()
stream.close()
p.terminate()


wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
