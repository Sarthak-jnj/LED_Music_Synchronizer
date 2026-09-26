import random as rdm
import serial as srl
import time
arduino = srl.Serial('COM13', 115200)
time.sleep(2)
while True:
    time.sleep(0.05)
    Bass = rdm.randint(0, 255)
    Treble = rdm.randint(0, 255)
    Highs = rdm.randint(0, 255)
    Lows = rdm.randint(0, 255)
    RDM_NMR = [Bass, Treble, Highs, Lows]
    ID = ["A", "B", "C", "D"]
    for i in range (0, 4):
        arduino.write(ID[i].encode())
        arduino.write(bytes([RDM_NMR[i]]))
        print(f"{ID[i]} : {RDM_NMR[i]}")