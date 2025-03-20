# algorithm based on https://dk7ih.de/a-simple-software-to-control-the-si5351a-generator-chip/
#tested with 3 output ports Si5351 module
import machine 
from machine import Pin, SoftI2C

#i2c definition for si5351 -> scl Pin 25, sda pin 25, change it according to your environment
i2c = SoftI2C(scl=Pin(25), sda=Pin(26),freq=400000)
#print(i2c.scan()) #uncomment for I2C bus scanning but usually si5351 is 96 (dec) or 0x60 (hex)
i2c_addr = 96

class Tiny_SI5351:
    
    #write byte to si5351 register
    def w_to_si5351(self,i2c_addr,addr,val): 
        i2c.writeto_mem(i2c_addr,addr,bytearray([val]))
    
    #read byte from si5351 register addr, diagnostic function only
    def r_fm_si5351(self,i2c_addr,addr): 
        r = i2c.readfrom_mem(i2c_addr,addr,1)
        #print("reg = ", addr,int.from_bytes(r,"big")) #uncomment to print value
    
    #setting up frequency on PLL and output, 
    def ster(self,freq,channel,corr):
        #method for frequency setting on channel 0-4, don't use channels 0 and 1 during normal work
        #freq as integer, eg. 10300080 means 10.30008 MHz, not important for PLL channels A and B
        #channel: 0 -> PLLA, 1 -> PLLB, 2 -> F0, 3 -> F1, 4 -> F2
        #corr in Hz eg. 3 when 3Hz higher than set or -4 when 4Hz below set frequency
        corr = 1000 * corr
        fvco = 900000000 - corr
        reg = [0,0,0,0,0,0,0,0]
        p3 = 1048575 #setting max resolution of Si5351
        if channel < 2: #settings for PLLA/B frequency 
            p1 = 4096
            p2 = 0
        else: #calculation for f0 to f3 frequency (channels 2-4)
            fdiv = fvco/freq
            a = int(fdiv)
            rm = (fvco - a * freq)/freq
            b = rm * p3
            tmp =  int(128 * b / p3)
            p1 = 128 * a + tmp - 512
            p2 = int(128 * b - p3 * tmp)
        reg[0] = 255 #filling register reg with data to send to si5351
        reg[1] = 255
        reg[2] = (p1 & 196608) >> 16
        reg[3] = (p1 & 65280) >> 8
        reg[4] = p1 & 255
        tmp = (p2 & 983040) >> 16
        reg[5] =  tmp + 240
        reg[6] = (p2 & 65280) >> 8
        reg[7] = p2 & 255
        #detailed register description on https://cdn-shop.adafruit.com/datasheets/Si5351.pdf
        if channel == 0: #setting address of frequency register for channels 0-4
            addr = 26
        elif channel == 1:
            addr = 34
        elif channel == 2:
            addr = 42
        elif channel == 3:
            addr = 50
        elif channel == 4:
            addr = 58
        for i in range (8):
            self.w_to_si5351(i2c_addr,addr+i,reg[i])
      
    def __init__(self):
        #detailed register description on https://cdn-shop.adafruit.com/datasheets/Si5351.pdf
        self.w_to_si5351(i2c_addr,183,210) #210 -> oxd2 -> setting capacity 10pF
        self.w_to_si5351(i2c_addr,2,83) #no interrupts
        self.w_to_si5351(i2c_addr,15,0) #PLL source PLLA and PLLB as xtal
        self.w_to_si5351(i2c_addr,16,15) #15 -> 0x0f -> PLLA -> CLK0, 8mA
        self.w_to_si5351(i2c_addr,17,47) #15 -> 0x0f -> PLLB -> CLK0, 8mA
        self.w_to_si5351(i2c_addr,18,47) #15 -> 0x0f -> PLLB -> CLK0, 8mA
        self.w_to_si5351(i2c_addr,177,160) #160 -> 0xa0 -> reset PLLA and B
        self.ster(0,0,0) #start PLLA at 900MHz
        self.ster(0,1,0) #start PLLB at 900MHz

    def ctrl(self,ctrl):
        #method for output control
        #eg. 6 -> f0 enable, 5 -> f1 enable, 3 -> f2 enable, 0 -> all fx enable, 7 -> all fx disable etc.
        self.w_to_si5351(i2c_addr,3,ctrl)


#usage example to generate 10MHz on f0 output with no PLL frequency correction
#gen = Tiny_SI5351() #class instance creating
#gen.ster(10000000, 2, 0) #setting 10MHz on f0 (2) port with no PLL frequency correction (0)
#gen.control(6) #unlock port f0 for operation