import wave
import numpy as np
import sys
import math
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import lfilter, butter, kaiserord, firwin, freqz

# Use website below for documentaion of creating FIR Filters
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.remez.html

#------Open Noisy Signal file and set Parameters equal to variables------
x = wave.open('imperial_march_noisy.wav', 'rb')
sampleRate = x.getframerate()
ampWidth = x.getsampwidth()
nChannels = x.getnchannels()
nFrames = x.getnframes()
#------Open Noisy Signal file and set Parameters equal to variables------

#-----------Extract Raw Data from wav file--------------
raw = x.readframes(-1)
raw = np.frombuffer(raw, "int16")
#-----------Extract Raw Data from wav file--------------

#------------------Define and set x-axis------------------------
dt = np.linspace(0, len(raw) / sampleRate, num=len(raw))
#------------------Define and set x-axis------------------------

#---------------Plot Time Domain Signal of Original Signal---------------
# plt.figure()
# plt.title("Time Domain Plot")
# plt.plot(dt, raw, color="blue")
# plt.xlabel("Time")
#---------------Plot Time Domain Signal of Original Signal---------------

#------------------Compute the fft------------------
y = np.fft.fft(raw)
freq = np.fft.fftfreq(dt.shape[-1], 1/sampleRate)
#------------------Compute the fft------------------

#--------------Plot FFT Frequency Domain of Original Signal---------------
# plt.figure()
# plt.title("Frequency Response of Signal")
# plt.plot(freq, abs(y))
# plt.xlabel("Frequency")
# plt.ylabel('Magnitude')
#--------------Plot FFT Frequency Domain of Original Signal---------------




#---------------------------Create Band Stop Filter------------------------------
band = [1106, 1150]  # Desired stop band, Hz
trans_width = 600    # Width of transition from pass band to stop band, Hz
numtaps = 175        # Size of the FIR filter.
edges = [0, band[0] - trans_width, band[0], band[1], band[1] + trans_width, 0.5*sampleRate]
taps = signal.remez(numtaps, edges, [1, 0, 1], Hz=sampleRate)
w, h = signal.freqz(taps, [1], worN=2000)
#---------------------------Create Band Stop Filter------------------------------


#----------------Plot Frequency Response of filter----------------
plt.figure()
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
filtered.setparams( (1, ampWidth, sampleRate, nFrames, x.getcomptype(), x.getcompname()) )
filtered.writeframes(raw.tobytes('C'))
filtered.close()
#-----------------Write Filtered file to new file-----------------