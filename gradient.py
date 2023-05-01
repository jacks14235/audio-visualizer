class Gradient:
    def __init__(self, colors, stops=[]):
        if (len(stops) == 0):
            stops = [(i + 1) / (len(colors)-1) for i in range(len(colors)-2)]
        elif len(stops) != len(colors) - 2:
            print('legnth of stops must be two less than length of colors, 0 and 1 are assumed as endpoints')
            return None
        self.colors = colors
        stops.insert(0, 0)
        stops.append(1)
        self.stops = stops

    def eval(self, n):
        try:
          if (n <= 0):
              return self.colors[0]
          if (n >= 1):
              return self.colors[-1]
          i = 0
          while self.stops[i] <= n:
              i += 1
          start = self.stops[i-1]
          end = self.stops[i]
          rat = (n - start) / (end - start)
          color = [0,0,0]
          for j in range(3):
            color[j] = (self.colors[i][j] - self.colors[i-1][j]) * rat + self.colors[i-1][j]
        except IndexError:
            print('Error', start, end, rat)
        return color
    
    def reverse(self):
        self.colors = [self.colors[-i] for i in range(1, len(self.colors) + 1)]
        self.stops = [(1 - self.stops[-i]) for i in range(1, len(self.stops) + 1)]
        return self
    
    def heat():
        return Gradient([
            [255,0,0],
            [255,255,0]
        ])

    def heat2():
        return Gradient([
            [255,0,0],
            [255,127,0],
            [255,255,0]
        ], [
            .66
        ])
    
    def cool():
        return Gradient([
            [0,0,255],
            [0,255,255],
            [0,255,0]
        ])
    
    def temp():
        return Gradient([
            [0,255,255],
            [0,255,0],
            [255,255,0],
            [255,0,0]
        ])
    
    def rainbow():
        return Gradient([
            [255,0,0],
            [255,255,0],
            [0,255,0],
            [0,255,255],
            [0,0,255],
            [255,0,255],
            [255,0,0]
        ])
    




if __name__ == '__main__':
    g = Gradient([[255,0,0], [0,255,0]], [])

    print(g.eval(.235))