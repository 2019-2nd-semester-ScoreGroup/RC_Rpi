import RPi.GPIO as GPIO
from time import sleep

leftMotar = [19,26]
rightMotar = [20,21]
enableButton = [6, 12]

HIGH = True
LOW = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(leftMotar[0], GPIO.OUT)
GPIO.setup(leftMotar[1], GPIO.OUT)
GPIO.setup(rightMotar[0], GPIO.OUT) 
GPIO.setup(rightMotar[1], GPIO.OUT)

GPIO.setup(enableButton[0], GPIO.OUT)
GPIO.setup(enableButton[1], GPIO.OUT)


cnt1 = 50 
cnt2 = 50

pwm1 = GPIO.PWM(enableButton[0], cnt1)
pwm2 = GPIO.PWM(enableButton[1], cnt2)

pwm1.start(cnt1)
pwm2.start(cnt2)

GPIO.output(leftMotar[0], HIGH)
GPIO.output(leftMotar[1], LOW)
GPIO.output(rightMotar[0], HIGH)
GPIO.output(rightMotar[1], LOW)

sleep(2)

GPIO.cleanup()