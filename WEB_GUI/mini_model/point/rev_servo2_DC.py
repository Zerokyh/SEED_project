import pigpio
import time

pwm_pin_f = 19
pwm_pin_r = 18
pi = pigpio.pi()
pi.set_mode(pwm_pin_f, pigpio.OUTPUT)
pi.set_mode(pwm_pin_r, pigpio.OUTPUT)
speed = 0

pi.hardware_PWM(pwm_pin_f, 20, 0)#500000)
pi.hardware_PWM(pwm_pin_r, 50, 0)#100000)
time.sleep(1)

try:
    while True:
        cmd = input("Command, f/r: ")
        direction = cmd[0]
        if direction == "f":
            if speed < 100: speed += 10
            else: speed = 100
        else:
            if speed > -100: speed -= 10
            else: speed = -100
        if speed > 0:
            pi.hardware_PWM(pwm_pin_r, 50, 0)
            pi.hardware_PWM(pwm_pin_f, 20, speed*10000)
        elif speed < 0:
            pi.hardware_PWM(pwm_pin_f, 50, 0)
            pi.hardware_PWM(pwm_pin_r, 20, abs(speed)*10000)
        else:
            pi.hardware_PWM(pwm_pin_f, 20, 0)
            pi.hardware_PWM(pwm_pin_r, 50, 0)
        print("speed=", speed)
finally:
    pi.hardware_PWM(pwm_pin_f, 20, 0)
    pi.hardware_PWM(pwm_pin_r, 50, 0)
    pi.stop()

