from PIL import Image
import numpy as np

def image(data, resolution, filename):
  img = Image.open(filename)
  width, height = img.size
  if width > height:
    cropL = (width - height) // 2
    cropR = (1 + width - height) // 2
    img = img.crop((cropL, 0, width - cropR, height))
  else:
    cropT = (height - width) // 2
    cropB = (1 + height - width) // 2
    img = img.crop((0, cropT, width, height - cropB))
  img = img.resize(resolution)
  if img.mode == 'RGBA':
    background = Image.new("RGB", img.size, (0, 0, 0))
    background.paste(img, mask=img.split()[3])
    img = background
  # img.show()
  arr = np.array(img)
  # arr = np.rot90(arr)
  arr = np.transpose(arr, (1,0,2))
  # print(arr[0][:30])
  # print(arr.dtype)
  # print(arr.shape)
  # print(data.shape)
  data[:] = arr

if __name__ == '__main__':
  image(np.zeros((29,29,3)), [29,29], 'jets.jpg')