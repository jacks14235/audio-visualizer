from scipy.fftpack import fft, fftfreq
from scipy.io import wavfile # get the api
import numpy as np
import matplotlib.pyplot as plt

freq_range = (80, 4000)
# if __name__ == '__main__':
	# BIT_DEPTH=16.
	# CHUNK=1024

	# fs, data = wavfile.read('loopback_record.wav') # load the data
	# a = data.T[0][CHUNK*100:CHUNK*101] # this is a two channel soundtrack, I get the first track
	# print(len(a))
	# print(a[:10])
	# b=[(ele/2**BIT_DEPTH)*2-1 for ele in a] # normalize to [-1,1]
	# c = fft(b) # calculate fourier transform (complex numbers list)
	# d = len(c)/2  # you only need half of the fft list (real signal symmetry)

	# print(c)


	# N = 128
	# # # sample spacing
	# T = 1.0 / 800.0
	# # x = np.linspace(0.0, len(a), N, endpoint=False)
	# # y = c
	# yf = c
	# xf = fftfreq(N, 44100)[:N//2]

	# plt.plot(xf[2:], 2.0/N * np.abs(yf[0:N//2])[2:])
	# plt.grid()
	# plt.show()

class TestReader:
	def __init__(self):
		self.CHUNK = 1024
		self.BUCKETS = 64
		self.DEPTH = 16
		self.SAMPLE = 44100

		fs, data = wavfile.read('loopback_record.wav') # load the data
		data = data[:, 0] / (2**(self.DEPTH - 1))
		self.data = data # you only need half of the fft list (real signal symmetry)
		print(data[4932:4940])
		self.pointer = 0
		print("Data max", max(data))

	def _seek(self, n):
		self.pointer = n
    
	def getNext(self):
		if self.pointer + self.CHUNK > len(self.data):
			return None
		curr = self.data[self.pointer:self.pointer+self.CHUNK]
		self.pointer += self.CHUNK
		return curr
	
	def getNextVals(self, n_buckets=12):
		curr = self.getNext()
		curr = np.array(curr) / 2**self.DEPTH
		N = self.CHUNK

		yf = fft(curr)
		xf = fftfreq(N, 1 / self.SAMPLE)

		buckets = np.logspace(freq_range[0], freq_range[1], num=12, base=2)
		

		return xf, yf


if __name__ == '__main__':
	reader = TestReader()
	reader._seek(((2*44100)//1024)*1024)

	xf, yf = reader.getNextVals()
	print(len(xf), len(yf))
	plt.plot(xf[:500], np.abs(yf)[:500])
	plt.show()
