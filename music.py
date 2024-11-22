import pyaudiowpatch as pyaudio
import numpy as np
import sys
import time
from gradient import Gradient
from scipy.fftpack import fft, fftfreq
import time


curr = 0
def music(outer_data, resolution, bucket_width=3, get_background=None, get_foreground=None):
  print("starting music", file=sys.stderr)
  CHUNK = 1024
  RATE = 44100
  RECORD_SECONDS = 10000
  DEPTH = 16
  f_min = 40
  f_max = 20480
  # each bucket is this many pixels wide
  BUCKET_WIDTH = bucket_width
  N_BUCKETS = ((resolution[0] - 1) // BUCKET_WIDTH) + 1
  BUCKET_HEIGHT = resolution[1]
  log_scale = (f_max / f_min)**(1/(N_BUCKETS))
  buckets = [f_min * log_scale**i for i in range(N_BUCKETS + 1)]
  xf = fftfreq(CHUNK, 1 / RATE)

  running_len = 10
  running = np.zeros((running_len, len(buckets)))
  weights = .008 * log_scale**np.array([i for i in range(len(buckets))])
  def get_background(x, y, t, v, a):
    return np.array([0,0,0])
    if False:# a < .05 and z[y][x] == 1:
      return bg_grad.eval((((y/BUCKET_HEIGHT)/3) + (500 + t) / 1000) % 1.0)
    else:
      return (np.array(bg_grad.eval((((y/BUCKET_HEIGHT)/3) + t / 1000) % 1.0)) * 1).astype(np.int)
  
	
  # get_background = lambda x, y, t, v, a:  [0,255,0]
  fg_grad = Gradient.rainbow()
  get_foreground = lambda x, y, t, v: fg_grad.eval(((v / 8) + (500 + t) / 1000) % 1.0)
  # get_foreground = lambda x, y, t, v: [0,255,0]

  bg_grad = Gradient.rainbow()

  def callback(raw_data, frame_count, time_info, status):
    global curr
    data = np.frombuffer(raw_data, dtype=np.int16) / (2**(DEPTH - 1))
    # get fourier data
    yf = fft(data)
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
    current_vals = avgs * weights
    running[curr % running_len] = current_vals
    curr += 1
    
    pixels = np.zeros((N_BUCKETS, BUCKET_HEIGHT, 3), dtype=np.uint8)
    running_avg = np.average(running, axis=0)
    for x in range(N_BUCKETS):
      val = running_avg[x]
      for y in range(BUCKET_HEIGHT):
        if val > y / BUCKET_HEIGHT:
          pixels[x, y] = get_foreground(x, y, curr, val)
        else:
          pixels[x, y] = get_background(x, y, curr, val, np.average(running_avg))
          
    pixels = np.flip(pixels, axis=1)
    pixels = np.repeat(pixels, BUCKET_WIDTH, axis=0)    
    pixels = pixels[:resolution[0],:,:]
    outer_data[:] = pixels
    return (raw_data, pyaudio.paContinue)
  
  with pyaudio.PyAudio() as p:
      """
      Create PyAudio instance via context manager.
      Spinner is a helper class, for `pretty` output
      """
      print("Starting PyAudio", file=sys.stderr)
      try:
        # Get default WASAPI info
        wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
      except OSError:
        print("Looks like WASAPI is not available on the system. Exiting...", file=sys.stderr)
        #spinner.stop()
        exit()
      
      # Get default WASAPI speakers
      default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
      
      print(default_speakers, file=sys.stderr)
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
          
      print(f"Recording from: ({default_speakers['index']}){default_speakers['name']}", file=sys.stderr)
          
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