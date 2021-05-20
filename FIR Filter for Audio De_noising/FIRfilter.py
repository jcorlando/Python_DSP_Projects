import wave
import numpy as np
import sys
import matplotlib.pyplot as plt

# Open Noisy Signal file and set Parameters equal to variables
signal = wave.open('imperial_march_noisy.wav', 'rb')
sampleRate = signal.getframerate()
ampWidth = signal.getsampwidth()
nChannels = signal.getnchannels()
nFrames = signal.getnframes()

# Extract Raw Data from wav file
raw = signal.readframes(-1)
raw = np.frombuffer(raw, "int16")

# Define and set x-axis
dt = np.linspace(0, len(raw) / sampleRate, num=len(raw))

#  Plot Time Domain Signal
plt.figure(1)
plt.title("Time Domain Plot")
plt.plot(dt, raw, color="blue")
plt.xlabel("Time")

# Compute the fft
y = np.fft.fft(raw)
freq = np.fft.fftfreq(dt.shape[-1], 1/sampleRate)

# Plot FFT Frequency Domain 
plt.figure(2)
plt.title("Frequency Response of Signal")
plt.plot(freq, abs(y))
plt.xlabel("Frequency")
plt.ylabel('Magnitude')
plt.show()












filtered = wave.open("filtered.wav", "w")
filtered.setparams( (1, ampWidth, sampleRate, nFrames, signal.getcomptype(), signal.getcompname()) )
filtered.writeframes(raw.tobytes('C'))
filtered.close()