import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

pwm=GPIO.PWM(11, 50)
pwm.start(0)

print("left")
pwm.ChangeDutyCycle(5) # left -90 deg position
sleep(1)
print("netrual")
pwm.ChangeDutyCycle(7.5) # neutral position
sleep(1)
print("right")
pwm.ChangeDutyCycle(10) # right +90 deg position
sleep(1)

pwm.stop()
GPIO.cleanup()
