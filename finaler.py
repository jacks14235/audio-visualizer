from scipy.fftpack import fft, fftfreq
import numpy as np
from gradient import Gradient
import pyaudiowpatch as pyaudio
import time
from dot_array import DotArray
import sys

CHUNK = 1024
dCHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10000
WAVE_OUTPUT_FILENAME = "output.wav"
DEPTH = 16
buckets = [40,80,160,320,640,1280,2560,5120,10240,20480]
N_BUCKETS = 10
BUCKET_HEIGHT = 10

running_len = 10
running = np.zeros((running_len, len(buckets)))
curr = 0
weights = 2**np.array([i for i in range(len(buckets))])

frames = []

# dots = DotArray(N_BUCKETS, BUCKET_HEIGHT)
grad = Gradient.rainbow()
in_progress = False
def callback(raw_data, frame_count, time_info, status):
	global in_progress
	if in_progress:
		print("Already in progress")
		return (raw_data, pyaudio.paContinue)
	in_progress = True
	global curr
	frames.append(raw_data)
	data = np.frombuffer(raw_data, dtype=np.int16) / (2**(DEPTH - 1))

	# get fourier data
	yf = fft(data)
	xf = fftfreq(CHUNK, 1 / RATE)
	avgs = np.zeros(len(buckets))
	bucket = 0
	start = 0
	# organize fourier data into larger buckets
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

	# scale fourier data and add to running average
	current_vals = (.007 * avgs) * weights
	running[curr % running_len] = current_vals
	curr += 1
  
	running_avg = np.average(running, axis=0)
	# convert values to colors
	colors = np.array([grad.eval(val) for val in running_avg], dtype=np.uint8)
	# stretch to height of pixels and reshape
	pixels = np.repeat([colors], [BUCKET_HEIGHT], axis=0)
	for i in range(N_BUCKETS):
		maxH = int(BUCKET_HEIGHT * running_avg[i])
		for j in range(maxH, BUCKET_HEIGHT):
			pixels[j][i].fill(0)
	pixels = pixels.reshape((N_BUCKETS*BUCKET_HEIGHT, 3))
	# dots.update(pixels)
	np.save(sys.stdout.buffer, pixels)
	in_progress = False
	return (raw_data, pyaudio.paContinue)
	

with pyaudio.PyAudio() as p:
		"""
		Create PyAudio instance via context manager.
		Spinner is a helper class, for `pretty` output
		"""
		try:
			# Get default WASAPI info
			wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
		except OSError:
			print("Looks like WASAPI is not available on the system. Exiting...")
			#spinner.stop()
			exit()
		
		# Get default WASAPI speakers
		default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
		
		if not default_speakers["isLoopbackDevice"]:
			for loopback in p.get_loopback_device_info_generator():
				"""
				Try to find loopback device with same name(and [Loopback suffix]).
				Unfortunately, this is the most adequate way at the moment.
				"""
				if default_speakers["name"] in loopback["name"]:
					default_speakers = loopback
					break
			else:
				print("Default loopback output device not found.\n\nRun `python -m pyaudiowpatch` to check available devices.\nExiting...\n")
				# spinner.stop()
				exit()
				
		print(f"Recording from: ({default_speakers['index']}){default_speakers['name']}")
        
        # wave_file = wave.open(filename, 'wb')
        # wave_file.setnchannels(default_speakers["maxInputChannels"])
        # wave_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        # wave_file.setframerate(int(default_speakers["defaultSampleRate"]))
        
        # def callback(in_data, frame_count, time_info, status):
        #     """Write frames and return PA flag"""
        #     wave_file.writeframes(in_data)
        #     return (in_data, pyaudio.paContinue)
        
		with p.open(format=pyaudio.paInt16,
				channels=default_speakers["maxInputChannels"],
				rate=int(default_speakers["defaultSampleRate"]),
				frames_per_buffer=CHUNK,
				input=True,
				input_device_index=default_speakers["index"],
				stream_callback=callback
		) as stream:
			"""
			Opena PA stream via context manager.
			After leaving the context, everything will
			be correctly closed(Stream, PyAudio manager)            
			"""
			time.sleep(RECORD_SECONDS) # Blocking execution while playing
		
		# wave_file.close()