import RPi.GPIO as GPIO
import time

#en_pin = 18

#motorA
mA_m1a_pin = 17
mA_m1b_pin = 4

#motorB
mB_m1a_pin = 10
mB_m1b_pin = 25

GPIO.setmode(GPIO.BCM)
#GPIO.setup(en_pin, GPIO.OUT)
GPIO.setup(mA_m1a_pin, GPIO.OUT)
GPIO.setup(mA_m1b_pin, GPIO.OUT)
GPIO.setup(mB_m1a_pin, GPIO.OUT)
GPIO.setup(mB_m1b_pin, GPIO.OUT)
#pwm = GPIO.PWM(en_pin, 500)
#pwm.start(0)
MOTOR_A_A1_PWM=GPIO.PWM(mA_m1a_pin, 20)
MOTOR_A_A2_PWM=GPIO.PWM(mA_m1b_pin, 20)
MOTOR_B_A1_PWM=GPIO.PWM(mB_m1a_pin, 20)
MOTOR_B_A2_PWM=GPIO.PWM(mB_m1b_pin, 20)

MOTOR_A_A1_PWM.start(0)
MOTOR_A_A2_PWM.start(0)
MOTOR_B_A1_PWM.start(0)
MOTOR_B_A2_PWM.start(0)

GPIO.output(mA_m1b_pin, GPIO.LOW)
GPIO.output(mB_m1b_pin, GPIO.LOW)

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
            GPIO.output(mA_m1a_pin, True)
            GPIO.output(mA_m1b_pin, False)
            GPIO.output(mB_m1a_pin, True)
            GPIO.output(mB_m1b_pin, False)
            MOTOR_A_A1_PWM.ChangeDutyCycle(abs(speed))
            MOTOR_B_A1_PWM.ChangeDutyCycle(abs(speed))
        elif speed < 0:
            GPIO.output(mA_m1a_pin, False)
            GPIO.output(mA_m1b_pin, True)
            GPIO.output(mB_m1a_pin, False)
            GPIO.output(mB_m1b_pin, True)
            MOTOR_A_A2_PWM.ChangeDutyCycle(abs(speed))
            MOTOR_B_A2_PWM.ChangeDutyCycle(abs(speed))
        else:
            GPIO.output(mA_m1a_pin, False)
            GPIO.output(mA_m1b_pin, False)
            GPIO.output(mB_m1a_pin, False)
            GPIO.output(mB_m1b_pin, False)
            MOTOR_A_A1_PWM.ChangeDutyCycle(abs(speed))
            MOTOR_A_A2_PWM.ChangeDutyCycle(abs(speed))
            MOTOR_B_A1_PWM.ChangeDutyCycle(abs(speed))
            MOTOR_B_A2_PWM.ChangeDutyCycle(abs(speed))
        print("speed=", speed)
        #pwm.ChangeDutyCycle(abs(speed))
finally:
    MOTOR_A_A1_PWM.stop(0)
    MOTOR_A_A2_PWM.stop(0)
    MOTOR_B_A1_PWM.stop(0)
    MOTOR_B_A2_PWM.stop(0)
    GPIO.cleanup()
