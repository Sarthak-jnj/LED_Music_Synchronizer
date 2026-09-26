import soundcard as sc
import numpy as np
import serial as srl
import time

samplerate = 48000
blocksize = 1024
arduino = srl.Serial('COM13', 115200)
IDs = ["A", "B","C","D"]
Max_RMS_Bass = 1e-8
Max_RMS_Low_mid = 1e-8
Max_RMS_High_mid = 1e-8
Max_RMS_Treble = 1e-8

Smooth_Bass = 0.0
Smooth_Low_mid = 0.0
Smooth_High_mid = 0.0
Smooth_Treble = 0.0

Music_input = sc.all_microphones(include_loopback=True)[0]

time.sleep(1)
with Music_input.recorder(samplerate=samplerate, blocksize=blocksize) as recorder:
    while True:
        Data = recorder.record(numframes=blocksize)
        Mono = Data.mean(axis=1)
        frequencies_raw = np.fft.rfft(Mono)
        magnitude = np.abs(frequencies_raw)
        frequencies = np.fft.rfftfreq(blocksize, 1 / samplerate)

        Bass = (frequencies >= 20 ) & (frequencies < 250)
        Low_mid = (frequencies >= 250 ) & (frequencies < 2000)
        High_mid = (frequencies >= 2000 ) & (frequencies < 4000)
        Treble = (frequencies >= 4000 ) & (frequencies < 20000)

        RMS_Bass = np.sqrt(np.mean(magnitude[Bass]**2))
        RMS_Low_mid = np.sqrt(np.mean(magnitude[Low_mid]**2))
        RMS_High_mid = np.sqrt(np.mean(magnitude[High_mid]**2))
        RMS_Treble = np.sqrt(np.mean(magnitude[Treble]**2))

        if (RMS_Bass >= Smooth_Bass):
            Smooth_Bass = Smooth_Bass * 0.85 + RMS_Bass * 0.15
        else:
            Smooth_Bass = Smooth_Bass * 0.75 + RMS_Bass * 0.25
        if (RMS_Low_mid >= Smooth_Low_mid):
            Smooth_Low_mid = Smooth_Low_mid * 0.85 + RMS_Low_mid * 0.15
        else:
            Smooth_Low_mid = Smooth_Low_mid * 0.75 + RMS_Low_mid * 0.25
        if (RMS_High_mid >= Smooth_High_mid):
            Smooth_High_mid = Smooth_High_mid * 0.85 + RMS_High_mid * 0.15
        else:
            Smooth_High_mid = Smooth_High_mid * 0.75 + RMS_High_mid * 0.25
        if (RMS_Treble >= Smooth_Treble):
            Smooth_Treble = Smooth_Treble * 0.85 + RMS_Treble * 0.15
        else:
            Smooth_Treble = Smooth_Treble * 0.75 + RMS_Treble * 0.25

        if (RMS_Bass > Max_RMS_Bass):
            Max_RMS_Bass = RMS_Bass

        if (RMS_Low_mid > Max_RMS_Low_mid):
            Max_RMS_Low_mid = RMS_Low_mid

        if (RMS_High_mid > Max_RMS_High_mid):
            Max_RMS_High_mid = RMS_High_mid

        if (RMS_Treble > Max_RMS_Treble):
            Max_RMS_Treble = RMS_Treble

        LED_Bass = (Smooth_Bass/Max_RMS_Bass)**3*255
        LED_Low_mid = (Smooth_Low_mid/Max_RMS_Low_mid)**3*255
        LED_High_mid = (Smooth_High_mid/Max_RMS_High_mid)**3*255
        LED_Treble = (Smooth_Treble/Max_RMS_Treble)**3*255

        PWM_values = [int(LED_Bass), int(LED_Low_mid), int(LED_High_mid), int(LED_Treble)]
        Max_RMS_values = [Max_RMS_Bass, Max_RMS_Low_mid, Max_RMS_High_mid, Max_RMS_Treble]
        for i in range(0, 4):
            arduino.write(IDs[i].encode())
            arduino.write(bytes([PWM_values[i]]))
            print(PWM_values[i])

        Max_RMS_Bass *= 0.95
        Max_RMS_Low_mid *= 0.95
        Max_RMS_High_mid *= 0.95
        Max_RMS_Treble *= 0.95