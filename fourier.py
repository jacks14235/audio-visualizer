from scipy.fftpack import fft, fftfreq
from scipy.io import wavfile # get the api
import numpy as np
import matplotlib.pyplot as plt

BIT_DEPTH=16.
CHUNK=1024

fs, data = wavfile.read('stadium-rave.wav') # load the data
a = data.T[0][CHUNK*100:CHUNK*101] # this is a two channel soundtrack, I get the first track
print(len(a))
print(a[:10])
b=[(ele/2**BIT_DEPTH)*2-1 for ele in a] # normalize to [-1,1]
c = fft(b) # calculate fourier transform (complex numbers list)
d = len(c)/2  # you only need half of the fft list (real signal symmetry)



N = 12
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, len(a), N, endpoint=False)
y = c
yf = fft(y)
xf = fftfreq(N, T)[:N//2]
import matplotlib.pyplot as plt
plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
plt.grid()
plt.show()