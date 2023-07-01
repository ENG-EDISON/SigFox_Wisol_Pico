from machine import Pin,UART,Timer
import time

SFMSend     = "AT$SF="
SFMSetTXFRQ = "AT$IF="
SFMSetRXFRQ = "AT$DR="
GetID       = "AT$I=10\n"
GetPAC      = "AT$I=11\n"
SFMATtest   = "AT\r\n"
SFMGetTXFRQ = "AT$IF?\n"
SFMGetRXFRQ = "AT$DR?\n"
SFMGetTemp  = "AT$T?\n"
SFMSendBit  = "AT$SB="

class sigfox:
    def __init__ (self,UartPort,tx_Pin,rx_Pin):
        self.rx_Pin=rx_Pin
        self.tx_Pin=tx_Pin
        self.UartPort=UartPort
        self.Sigfox_Uart=UART(self.UartPort,baudrate=9600,tx=Pin(self.tx_Pin),rx=Pin(self.rx_Pin));
    def Sigfox_Send_cmd(self,Command):
        Wait_time=time.ticks_ms()
        self.Sigfox_Uart.write(Command);
        while True:
            if self.Sigfox_Uart.any()>0:
                rxdata=self.Sigfox_Uart.read()
                if rxdata !=None:
                    return rxdata.decode('utf-8')
                else:
                    return None
            if time.ticks_ms()-Wait_time >7000:
                return "Error! Can't communicate with device"
    def Sigfox_Test(self):
        Sigfox_Res=self.Sigfox_Send_cmd(SFMATtest)
        return(Sigfox_Res)
    def Sigfox_Get_ID(self):
        Sigfox_ID=self.Sigfox_Send_cmd(GetID)
        return (Sigfox_ID)
    def Sigfox_Get_GetPAC(self):
        Sigfox_PAC=self.Sigfox_Send_cmd(GetPAC)
        return (Sigfox_PAC)
    def Sigfox_Get_Freq(self):
        Sigfox_Tx_Freq=self.Sigfox_Send_cmd(SFMGetTXFRQ)
        Sigfox_Rx_Freq=self.Sigfox_Send_cmd(SFMGetRXFRQ)
        return (Sigfox_Tx_Freq,Sigfox_Rx_Freq)
    def SigFox_Send_Data(self,data):
        self.data=data
        self.data=SFMSend+str(self.data)+"\n"
        Sigfox_Res=self.Sigfox_Send_cmd(self.data)
        return Sigfox_Res
    def SigFox_Send_Bit(self,Bit):
        self.Bit=Bit
        self.data=SFMSendBit+str(self.Bit)+"\n"
        Sigfox_Res=self.Sigfox_Send_cmd(self.data)
        return Sigfox_Res
    def SigFox_Get_Temp(self):
        Sigfox_Temp=self.Sigfox_Send_cmd(SFMGetTemp)
        return(Sigfox_Temp)
    def Sigfox_Set_Freq(self,Sigfox_Tx,Sigfox_Rx):
        self.Sigfox_Tx=Sigfox_Tx
        self.Sigfox_Rx=Sigfox_Rx
        Tx_freq=SFMSetTXFRQ+str(Sigfox_Tx)+"\r\n"
        Rx_freq=SFMSetRXFRQ+str(Sigfox_Rx)+"\r\n"
        Res=self.Sigfox_Send_cmd(Tx_freq)
        Res1=self.Sigfox_Send_cmd(Rx_freq)
        return (Res,Res1)
