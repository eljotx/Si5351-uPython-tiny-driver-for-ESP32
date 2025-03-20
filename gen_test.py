import machine 
from machine import Pin, SoftI2C
from SI5351 import Tiny_SI5351

#start I2C connection
i2c = SoftI2C(scl=Pin(25), sda=Pin(26),freq=400000)
#print(i2c.scan()) #uncomment for I2C bus scanning but usually si5351 is 96 (dec) or 0x60 (hex)
i2c_addr = 96

gen1 = Tiny_SI5351() #creating si5351 instance generator
gen1.ster(10500000,2,0) #setting frequency 10.5MHz on channel 2 -> output f0
gen1.ctrl(6) #enable output for f0 and disable for f1 and f2


