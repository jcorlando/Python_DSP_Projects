import wave
import numpy as np
import sys
import matplotlib.pyplot as plt

signal = wave.open('imperial_march_noisy.wav', 'rb')

raw = signal.readframes(-1)
raw = np.frombuffer(raw, "int16")

fs = signal.getframerate()

dt = np.linspace(0, len(raw) / fs, num=len(raw))
plt.figure(1)
plt.title("Time Domain Plot")
plt.plot(dt, raw, color="blue")
plt.xlabel("Time")
plt.show()



plt.figure(2)






sampleRate = signal.getframerate()
ampWidth = signal.getsampwidth()
nChannels = signal.getnchannels()
nFrames = signal.getnframes()
filtered = wave.open("filtered.wav", "w")
filtered.setparams((1, ampWidth, sampleRate, nFrames, signal.getcomptype(), signal.getcompname()))
filtered.writeframes(raw.tobytes('C'))
filtered.close()