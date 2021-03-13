from machine import Pin, Timer
from machine import UART
import time

print("boot")
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

def send():
    tfox_rst.value(0)
    time.sleep(0.05)
    tfox_rst.value(1) #resetear el tinyfox
    time.sleep(1) #dejar que encienda
    tfox.write('AT$RC\n') #leer configuracion
    time.sleep(1) #dejar que procese
    tfox.write('AT$SF=01234567\n')
    time.sleep(4) #dejar transmita
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
id_pac()
send()
print("hecho")

#timer.init(freq=1, mode=Timer.PERIODIC, callback=latido) #juego de leds para ver que el raspberry esta andando
