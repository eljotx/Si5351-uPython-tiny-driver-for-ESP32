# Si5351-uPython-tiny-driver
A simple program to create and control the SI5351 generator

The program was written for the needs of a direct conversion transceiver generator or a single or double conversion transceiver.
When writing the program, I was inspired by the information from the website https://dk7ih.de/a-simple-software-to-control-the-si5351a-generator-chip/ and the factory catalog data of the SI5351 chip, in particular the division calculation algorithm and the method and possibilities of controlling individual registers.

When writing the program I tried to achieve the goal with minimal effort and code complexity so contain onlu constructor and only two methods for generator using. From this point of view the program does not pretend to be the best achievements in the field of programming but I hope it will be useful to someone in the initial steps with upython and the SI5351 chip.

# How to use the program:
1. Copy the SI5351.py file to ESP32
2. Import the machine, I2C and SI5351 libraries<br/>
  ***import machine***<br/>
  ***from machine import Pin, SoftI2C***
3. Declare the I2c channel<br/>
  ***i2c = SoftI2C(scl=Pin(25), sda=Pin(26),freq=400000)*** #change scl pin and sda pin according to your environment<br/>
  ***i2c_addr = 96***
4. Create an instance of the generator, e.g. named gen1 by running constructor<br/>
  ***gen1 = Tiny_SI5351()***
  
# Methods available:<br/>
1. Setting the frequency on channel 2-4<br/>
  ***gen1.ster(frequency,channel,corr)***<br/>
2. Unblocking the output of channel 2-4<br/>
  ***gen1.ctrl(ctrl)***

## The ***frequency*** parameter.
Must be specified in ***Hz as an integer***. The control accuracy is approximately 1Hz for a frequency of 10MHz (approx. 10Hz at 100MHz)
## The ***channel*** parameter.
In the range ***2-4*** corresponds to the ***f0-f2*** frequencies of the SI5351 system. Channels 0 and 1 should not be used during normal control, as they are only used during system initialization and when the reference frequencies of 900MHz are set for PLL A and B loops.
## The ***corr*** parameter.
Allows for the ***correction of the SI5351 system reference frequency***. I suggest performing the correction at a frequency of 10MHz by setting this frequency, for example, at the f0 output. After thermal stabilization for approximately 10 minutes, the ***corr*** parameter should be selected so that the reference meter also shows 10MHz. The ***corr*** value selected in this way should then be used in your own program when calling the ***ster*** method. My SI5351 system required correction of about 18 Hz.
## the ***ctrl*** parameter.
Is responsible for ***blocking or unblocking the f0-f2 frequency outputs***. The three lowest bits of register 3 SI5351 are responsible for the state of these outputs in such a way that bit 0 is responsible for the f0 state, bit 1 for the f1 state and bit 2 for the f2 state. The value 0 of a given bit opens the port and the value 1 closes the corresponding port. So ctrl = 0 will unblock all outputs, ctrl = 7 will block all outputs and ctrl = 2 will block only the f1 output etc.

# Some useful information:
## Tested ESP32 module
I tested the program with the ***ESP32 WROOM* processor with 30 pins shown in the picture.

## I2C address of the SI5351
I tested the program with two SI5351 modules (showed on pictures) which already containing the I2C environment. Both modules had a decimal address ***96*** or ***0x60*** hexadecimal.
If you need to detect the I2C address, I suggest using an I2C address detector by uncommenting the line:<br/>
***#print(i2c.scan())***
   
## Control accuracy.
Theoretically, the program should operate on double precision numbers, but uPython for ESP32 does not provide such accuracy. Measurements show that for a frequency of about 10MHz, it is possible to obtain a resolution of about 1Hz, which of course will deteriorate with increasing frequency to about 10Hz for 100MHz.

## Lower control limit.
The SI5351 system operates from about 8KHz with additional help of Rx registers for each channel, but the presented program does not have such a possibility, omitting Rx registers, which means that the lowest achievable frequency is about 400kHz, which in the case of a receiver with direct conversion (Tayloe mixer) ensures operation of devices from about 125kHz with a x4 multiplier.

I hope that the reader will find useful information despite the incompetence and shortcomings of the program code and the amateur programmer himself, and will simply find a use for the solutions shown.  Just have a fun ;-)! 
