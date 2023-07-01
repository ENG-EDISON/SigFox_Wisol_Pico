from SigfoxModule import sigfox
import struct
import time
Module1=sigfox(0,0,1)
while True:
    print("Reading temperature........")
    temp=Module1.SigFox_Get_Temp()
    print("Temp=",temp)
    time.sleep(1)
    print("Sending data........")
    data=Module1.SigFox_Send_Data('ABCD')
    print(data)
    print("Sending bit.........")
    bit=Module1.SigFox_Send_Bit(1)
    print(bit)
    time.sleep(10)

