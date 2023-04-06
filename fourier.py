from scipy.fftpack import fft, fftfreq
from scipy.io import wavfile # get the api
import numpy as np
import matplotlib.pyplot as plt
import time

LO = 40
HI = 21000
NUM_BUCKETS = 12
buckets = [LO * (HI / LO) ** (i / NUM_BUCKETS) for i in range(NUM_BUCKETS)]
print(buckets)

class TestReader:
	def __init__(self):
		self.CHUNK = 1024
		self.BUCKETS = NUM_BUCKETS
		self.DEPTH = 16
		self.SAMPLE = 44100

		fs, data = wavfile.read('stadium-rave.wav') # load the data
		data = data[:, 0] / (2**(self.DEPTH - 1))
		self.data = data # you only need half of the fft list (real signal symmetry)
		self.pointer = 0

	def _seek(self, n):
		self.pointer = n
    
	def getNext(self):
		if self.pointer + self.CHUNK > len(self.data):
			return None
		curr = self.data[self.pointer:self.pointer+self.CHUNK]
		self.pointer += self.CHUNK
		return curr
	
	def getNextVals(self, n_buckets=12):
		start_time = time.time()
		time_per_chunk = self.CHUNK / self.SAMPLE

		curr = self.getNext()
		if curr is None:
			return None
		curr = np.array(curr) / 2**self.DEPTH
		N = self.CHUNK

		yf = fft(curr)
		xf = fftfreq(N, 1 / self.SAMPLE)

		avgs = np.zeros((self.BUCKETS))
		bucket = 0
		start = 0
		while xf[start] < buckets[0]:
			start+=1
		for i in range(start, len(xf)):
			if (bucket+ 1 == len(buckets)):
				break
			if (xf[i] > buckets[bucket + 1]):
				if (i - start < 2):
					# print("no data for bucket", bucket)
					avgs[bucket] = avgs[bucket - 1]
					bucket += 1
				else:
					avgs[bucket] = np.abs(np.average(yf[start:i-1]))
					start = i
					bucket += 1

		time.sleep(start_time + time_per_chunk - time.time())
		return avgs


class Transformer:
	def __init__(self):
		self.reader = TestReader()
		self.curr = self.reader.getNextVals()
	
	def start(self):
		while (curr := self.reader.getNextVals()) != None:
			self.curr = curr
			time.sleep(time_per_chunk)


if __name__ == '__main__':
	reader = TestReader()
	# reader._seek(((2*44100)//1024)*1024)
	time_per_chunk = 1024 / 44100


	xf, yf = reader.getNextVals()
	power_spectrum = np.abs(xf)**2 / (1024)
	normalized_spectrum = power_spectrum / np.sum(power_spectrum)

	plt.bar(yf[:1024//2], normalized_spectrum[:(1024)//2])
	plt.xlabel('Frequency (Hz)')
	plt.ylabel('Normalized Amplitude')
	plt.show()
