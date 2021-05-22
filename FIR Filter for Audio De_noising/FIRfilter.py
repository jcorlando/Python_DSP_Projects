import wave
import numpy as np
import sys
import math
import struct
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import lfilter, butter, kaiserord, firwin, freqz
from scipy.io import wavfile

# Use website below for documentaion of creating FIR Filters
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.remez.html

#------Open Noisy Signal file and set Parameters equal to variables------
x = wave.open('imperial_march_noisy.wav', 'rb')
sampleRate = x.getframerate()
sampWidth = x.getsampwidth()
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

#---------------Plot Time Domain of Original Signal---------------
# plt.figure()
# plt.title("Time Domain Plot (Original Signal)")
# plt.plot(dt, raw, color="blue")
# plt.xlabel("Time")
#---------------Plot Time Domain of Original Signal---------------

#------------------Compute the fft------------------
y = np.fft.fft(raw)
freq = np.fft.fftfreq(dt.shape[-1], 1/sampleRate)
#------------------Compute the fft------------------

#--------------Plot FFT Frequency Response of Original Signal---------------
# plt.figure()
# plt.title("Frequency Response of Orignal Signal")
# plt.plot(freq, abs(y))
# plt.xlim(-270, 5700)
# plt.ylim(-4.1E7, 1.949E9)
# plt.xlabel("Frequency")
# plt.ylabel('Magnitude')
#--------------Plot FFT Frequency Response of Original Signal---------------



#---------------------------Create 1st Band Stop Filter------------------------------
band = [1106, 1150]  # Desired stop band, Hz
trans_width = 30     # Width of transition from pass band to stop band, Hz
numtaps = 3301       # Size of the FIR filter.
edges = [0, band[0] - trans_width, band[0], band[1], band[1] + trans_width, 0.5*sampleRate]
taps_1 = signal.remez(numtaps, edges, [1, 0, 1], Hz=sampleRate)
w, h1 = signal.freqz(taps_1, [1], worN=2000)
#---------------------------Create 1st Band Stop Filter------------------------------


#----------------Plot Frequency Response of 1st filter----------------
# plt.figure()
# plt.plot(0.5*sampleRate*w/np.pi, 20*np.log10(np.abs(h1)))
# plt.ylim(-70, 8)
# plt.xlim(530, 1800)
# plt.grid(True)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Gain (dB)')
# plt.title("1st Band-stop Filter")
#----------------Plot Frequency Response of 1st filter----------------


#---------------------------Create 2nd Band Stop Filter------------------------------
band = [3500, 5322] # Desired stop band, Hz
trans_width = 100   # Width of transition from pass band to stop band, Hz
numtaps = 501       # Size of the FIR filter.
edges = [0, band[0] - trans_width, band[0], band[1], band[1] + trans_width, 0.5*sampleRate]
taps_2 = signal.remez(numtaps, edges, [1, 0, 1], Hz=sampleRate)
w, h2 = signal.freqz(taps_2, [1], worN=2000)
#---------------------------Create 2nd Band Stop Filter------------------------------


#----------------Plot Frequency Response of 2nd filter----------------
# plt.figure()
# plt.plot(0.5*sampleRate*w/np.pi, 20*np.log10(np.abs(h2)))
# plt.ylim(-71, 11)
# plt.xlim(1200, 8600)
# plt.grid(True)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Gain (dB)')
# plt.title("2nd Band-stop Filter")
#----------------Plot Frequency Response of 2nd filter----------------


#---------------------------Create 3rd Band Stop Filter------------------------------
band = [70, 76]     # Desired stop band, Hz
trans_width = 7    # Width of transition from pass band to stop band, Hz
numtaps = 10001     # Size of the FIR filter.
edges = [0, band[0] - trans_width, band[0], band[1], band[1] + trans_width, 0.5*sampleRate]
taps_3 = signal.remez(numtaps, edges, [1, 0, 1], Hz=sampleRate)
w, h3 = signal.freqz(taps_3, [1], worN=2000)
#---------------------------Create 3rd Band Stop Filter------------------------------


#----------------Plot Frequency Response of 3rd filter----------------
# plt.figure()
# plt.plot(0.5*sampleRate*w/np.pi, 20*np.log10(np.abs(h3)))
# plt.ylim(-22, 4)
# plt.xlim(-24, 575)
# plt.grid(True)
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Gain (dB)')
# plt.title("3rd Band-stop Filter")
#----------------Plot Frequency Response of 3rd filter----------------


#--------------Apply Filters to Signal------------------
raw_filtered = np.convolve(taps_1, raw, 'same')
raw_filtered = np.convolve(taps_2, raw_filtered, 'same')
raw_filtered = np.convolve(taps_3, raw_filtered, 'same')
# Or use below (lfilter), both work equally the same
# raw_filtered = lfilter(taps_1, [1], raw)
#--------------Apply Filters to Signal------------------


#------------------Compute the fft of Filtered Signal------------------
y = np.fft.fft(raw_filtered)
freq = np.fft.fftfreq(dt.shape[-1], 1/sampleRate)
#------------------Compute the fft of Filtered Signal------------------

#--------------Plot FFT Frequency Response of Filtered Signal---------------
# plt.figure()
# plt.title("Frequency Response of Filtered Signal")
# plt.plot(freq, abs(y))
# plt.xlim(-270, 5700)
# plt.ylim(-4.1E7, 1.949E9)
# plt.xlabel("Frequency")
# plt.ylabel('Magnitude')
#--------------Plot FFT Frequency Response of Filtered Signal---------------


#---------------Plot Time Domain of Filtered Signal---------------
# plt.figure()
# plt.title("Time Domain Plot (Filtered Signal)")
# plt.plot(dt, raw_filtered, color="blue")
# plt.xlabel("Time")
#---------------Plot Time Domain of Filtered Signal---------------

#-------Show all Plots and Figures-------
plt.show()
#-------Show all Plots and Figures-------

#-----------------Write Filtered file to new file-----------------
raw_filtered = raw_filtered.astype('int16')
filtered = wave.open("filtered.wav", "wb")
filtered.setparams( (nChannels, sampWidth, sampleRate, nFrames, x.getcomptype(), x.getcompname()) )
filtered.writeframes(raw_filtered.tobytes('C'))
filtered.close()
#-----------------Write Filtered file to new file-----------------