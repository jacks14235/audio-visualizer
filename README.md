# Audio Visualizer Instructions


### To Run with Fake Dot Array Using Pygame
```bash
python main.py | python buffer_read.py
```

### To Run on Raspberry Pi
1. Start the server on the Raspberry Pi:
   ```bash
   sudo python 2server.py
   ```
2. Run the following command in the Anaconda Prompt:
   ```bash
   python main.py | python sock.py
   ```

---

## LEGACY CODE

### To Run with Fake Dot Array Using Pygame
```bash
python finaler.py | python buffer_read.py
```

### To Run on Windows with Raspberry Pi
1. Start the server (`server.py`, not included in this repository) on the Raspberry Pi.
   ```bash
   sudo python server.py
   ```
2. Start client on the windows computer.
   ```bash
   python client.py
   ```
