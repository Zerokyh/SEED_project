import RPi.GPIO as GPIO
import time

#en_pin = 18
m1a_pin = 19
m1b_pin = 18
GPIO.setmode(GPIO.BCM)
#GPIO.setup(en_pin, GPIO.OUT)
GPIO.setup(m1a_pin, GPIO.OUT)
GPIO.setup(m1b_pin, GPIO.OUT)
#pwm = GPIO.PWM(en_pin, 500)
#pwm.start(0)
MOTOR_A_A1_PWM=GPIO.PWM(m1a_pin, 20)
MOTOR_A_A1_PWM.start(0)
GPIO.output(m1b_pin, GPIO.LOW)

speed=0
try:
    while True:
        cmd = input("Command, f/r :")
        direction = cmd[0]
        if direction == "f":
            if speed < 100: speed+=10
            else: speed=100
        else:
            if speed > -100: speed-=10
        if speed > 0:
            GPIO.output(m1a_pin, True)
            GPIO.output(m1b_pin, False)
        elif speed < 0:
            GPIO.output(m1a_pin, False)
            GPIO.output(m1b_pin, True)
        else:
            GPIO.output(m1a_pin, False)
            GPIO.output(m1b_pin, False)
        print("speed=", speed)
        MOTOR_A_A1_PWM.ChangeDutyCycle(abs(speed))
        #pwm.ChangeDutyCycle(abs(speed))
finally:
    MOTOR_A_A1_PWM.stop(0)
    GPIO.cleanup()
