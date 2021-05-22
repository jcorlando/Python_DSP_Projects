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
plt.figure()
plt.title("Time Domain Plot")
plt.plot(dt, raw, color="blue")
plt.xlabel("Time")
#---------------Plot Time Domain Signal of Original Signal---------------

#------------------Compute the fft------------------
y = np.fft.fft(raw)
freq = np.fft.fftfreq(dt.shape[-1], 1/sampleRate)
#------------------Compute the fft------------------

#--------------Plot FFT Frequency Domain of Original Signal---------------
plt.figure()
plt.title("Frequency Response of Signal")
plt.plot(freq, abs(y))
plt.xlabel("Frequency")
plt.ylabel('Magnitude')
#--------------Plot FFT Frequency Domain of Original Signal---------------




#---------------------------Create Band Stop Filter------------------------------

#---------------------------Create Band Stop Filter------------------------------


#----------------Plot Frequency Response of filter----------------

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