from machine import Pin, Timer
from machine import UART
import time

print("inicio")

#s = "%08x%04x" % (5,4)
#print(s)

import struct
import binascii
def float_to_hex(f):
    return str( binascii.hexlify(struct.pack('<f', f)) ,"ascii")
#print( float_to_hex(17.5) )


tfox = UART(1, 9600) #usar el uart0 a 9600 baudios
tfox_rst = Pin(3, Pin.OUT) #usar el pin 3 como reset para despertar el tinyfox
tfox_rst.value(0)

led = Pin(25, Pin.OUT)
timer = Timer()

def id_pac():
    tfox_rst.value(0)
    time.sleep(0.05)
    tfox_rst.value(1)
    time.sleep(1)
    tfox.write('AT$I=10\n')
    print(tfox.readline())
    tfox.write('AT$I=11\n')
    print(tfox.readline())

def send(payload):
    tfox_rst.value(0)
    time.sleep(0.05)
    tfox_rst.value(1) #resetear el tinyfox
    time.sleep(1) #dejar que encienda
    tfox.write('AT$RC\n') #leer configuracion
    time.sleep(1) #dejar que procese
    tfox.write('AT$SF=')
    #tfox.write('abcdef00')
    tfox.write(payload)
    print(payload)
    tfox.write('\n')
    #time.sleep(4) #dejar transmita
    print(tfox.readline())
    #tfox.write('AT$P=2\n') #mandar a dormir. descomentar para ahorrar energia

def latido(timer):
    #led.toggle()
    led.value(1)
    time.sleep(0.05)
    led.value(0)
    time.sleep(0.1)
    led.value(1)
    time.sleep(0.05)
    led.value(0)

timer.init(freq=1, mode=Timer.PERIODIC, callback=latido) #juego de leds para ver que el raspberry esta andando
#id_pac()
#send("123abc")
#send( "%08x%04x" % (5,4) )
#PL = "%08x%04x" % (5,4)
PL = "%08x%04x" % (5244678,63000)
PL = PL + float_to_hex(17.52457)
#print( PL )
send( PL )
print("hecho")

