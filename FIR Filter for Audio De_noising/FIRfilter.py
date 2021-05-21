import wave
import numpy as np
import sys
import math
import matplotlib.pyplot as plt
from scipy import signal as sig
from scipy.signal import lfilter, butter, kaiserord, firwin, freqz

# Use website below for documentaion of creating FIR Filters
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.remez.html

#------Open Noisy Signal file and set Parameters equal to variables------
signal = wave.open('imperial_march_noisy.wav', 'rb')
sampleRate = signal.getframerate()
ampWidth = signal.getsampwidth()
nChannels = signal.getnchannels()
nFrames = signal.getnframes()
#------Open Noisy Signal file and set Parameters equal to variables------

#-----------Extract Raw Data from wav file--------------
raw = signal.readframes(-1)
raw = np.frombuffer(raw, "int16")
#-----------Extract Raw Data from wav file--------------

#------------------Define and set x-axis------------------------
dt = np.linspace(0, len(raw) / sampleRate, num=len(raw))
#------------------Define and set x-axis------------------------

#---------------Plot Time Domain Signal of Original Signal---------------
plt.figure(1)
plt.title("Time Domain Plot")
plt.plot(dt, raw, color="blue")
plt.xlabel("Time")
#---------------Plot Time Domain Signal of Original Signal---------------

#------------------Compute the fft------------------
y = np.fft.fft(raw)
freq = np.fft.fftfreq(dt.shape[-1], 1/sampleRate)
#------------------Compute the fft------------------

#--------------Plot FFT Frequency Domain of Original Signal---------------
plt.figure(2)
plt.title("Frequency Response of Signal")
plt.plot(freq, abs(y))
plt.xlabel("Frequency")
plt.ylabel('Magnitude')
#--------------Plot FFT Frequency Domain of Original Signal---------------




#---------------------------Create Band Stop Filter------------------------------
band = [6000, 8000]  # Desired stop band, Hz
trans_width = 200    # Width of transition from pass band to stop band, Hz
numtaps = 175        # Size of the FIR filter.
edges = [0, band[0] - trans_width, band[0], band[1], band[1] + trans_width, 0.5*sampleRate]
taps = sig.remez(numtaps, edges, [1, 0, 1], Hz=sampleRate)
w, h = sig.freqz(taps, [1], worN=2000)
#---------------------------Create Band Stop Filter------------------------------


#----------------Plot Frequency Response of filter----------------
plt.figure(3)
plt.plot(0.5*sampleRate*w/np.pi, 20*np.log10(np.abs(h)))
plt.ylim(-40, 5)
plt.xlim(0, 0.5*sampleRate)
plt.grid(True)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain (dB)')
plt.title("Band-stop Filter")
#----------------Plot Frequency Response of filter----------------




#--------------Filter the Original Signal------------------

#--------------Filter the Original Signal------------------





#-------Show all Plots and Figures-------
plt.show()
#-------Show all Plots and Figures-------

#-----------------Write Filtered file to new file-----------------
filtered = wave.open("filtered.wav", "w")
filtered.setparams( (1, ampWidth, sampleRate, nFrames, signal.getcomptype(), signal.getcompname()) )
filtered.writeframes(raw.tobytes('C'))
filtered.close()
#-----------------Write Filtered file to new file-----------------