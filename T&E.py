# A code primarily made to test smaller sections of the main code independedntly for syntax errors and working logic before adding them to the main code.
import soundcard as sc
import numpy as np

samplerate = 48000
blocksize = 1024

loopback = sc.all_microphones(include_loopback=True)[0]

with loopback.recorder(samplerate=samplerate, blocksize=blocksize) as recorder:
   while True:         
        data = recorder.record(numframes=blocksize)
        mono = data.mean(axis=1)

        spectrum = np.fft.rfft(mono)
        magnitude = np.abs(spectrum)
        frequencies = np.fft.rfftfreq(blocksize, 1 / samplerate)
        Bass = (frequencies >= 20) & (frequencies <= 250)
        strongest = np.argmax(magnitude)

        print(f"Bass frequency is {frequencies[Bass]}")
        print(f"RMS of Bass is {np.sqrt(np.mean(magnitude[Bass]**2))}")