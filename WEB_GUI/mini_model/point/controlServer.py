import RPi.GPIO as gpio

#Motor 1 GPIO Pins
DRIVE_GO = 17 #IC3A
DRIVE_DIR = 4 #IC3, 4EN
#Motor 2 GPIO Pins
FRONT_DIR = 25 #IC1A
FRONT_GO = 10 #IC1, 2EN

gpio.setmode(gpio.BCM)

#GPIO.setup(en_pin, GPIO.OUT)
gpio.setup(DRIVE_GO, gpio.OUT)
gpio.setup(DRIVE_DIR, gpio.OUT)
gpio.setup(FRONT_GO, gpio.OUT)
gpio.setup(FRONT_DIR, gpio.OUT)

#pwm = GPIO.PWM(en_pin, 500)
#pwm.start(0)
MOTOR_A_A1_PWM=gpio.PWM(DRIVE_GO, 100)
MOTOR_A_A2_PWM=gpio.PWM(DRIVE_DIR, 100)
MOTOR_B_A1_PWM=gpio.PWM(FRONT_GO, 100)
MOTOR_B_A2_PWM=gpio.PWM(FRONT_DIR, 100)

MOTOR_A_A1_PWM.start(0)
MOTOR_A_A2_PWM.start(0)
MOTOR_B_A1_PWM.start(0)
MOTOR_B_A2_PWM.start(0)

gpio.output(DRIVE_DIR, gpio.LOW)
gpio.output(FRONT_DIR, gpio.LOW)

def forward():
    gpio.setmode(gpio.BCM)
    gpio.output(DRIVE_GO, True)
    gpio.output(DRIVE_DIR, False)
    gpio.output(FRONT_GO, True)
    gpio.output(FRONT_DIR, False)
    MOTOR_A_A1_PWM.ChangeDutyCycle(30)
    MOTOR_B_A1_PWM.ChangeDutyCycle(30)
    
def backward():
    gpio.setmode(gpio.BCM)
    gpio.output(DRIVE_GO, False)
    gpio.output(DRIVE_DIR, True)
    gpio.output(FRONT_GO, False)
    gpio.output(FRONT_DIR, True)
    MOTOR_A_A2_PWM.ChangeDutyCycle(30)
    MOTOR_B_A2_PWM.ChangeDutyCycle(30)
    
def left():
    gpio.setmode(gpio.BCM)
    gpio.output(DRIVE_GO, True)
    gpio.output(DRIVE_DIR, False)
    gpio.output(FRONT_GO, False)
    gpio.output(FRONT_DIR, True)

    MOTOR_A_A1_PWM.ChangeDutyCycle(20)
    MOTOR_B_A1_PWM.ChangeDutyCycle(20)
    
def right():
    gpio.setmode(gpio.BCM)
    gpio.output(DRIVE_GO, False)
    gpio.output(DRIVE_DIR, True)
    gpio.output(FRONT_GO, True)
    gpio.output(FRONT_DIR, False)
    MOTOR_A_A1_PWM.ChangeDutyCycle(20)
    MOTOR_B_A1_PWM.ChangeDutyCycle(20)    

def stop():
    gpio.setmode(gpio.BCM)
    gpio.output(FRONT_GO, gpio.LOW)
    gpio.output(FRONT_DIR, gpio.LOW)
    gpio.output(DRIVE_GO, gpio.LOW)
    gpio.output(DRIVE_DIR, gpio.LOW)
    #MOTOR_A_A1_PWM.ChangeDutyCycle(0)
    #MOTOR_B_A1_PWM.ChangeDutyCycle(0) 
    MOTOR_A_A1_PWM.stop(0)
    MOTOR_A_A2_PWM.stop(0)
    MOTOR_B_A1_PWM.stop(0)
    MOTOR_B_A2_PWM.stop(0)

def initMotors():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)

    #Pin Output Setup
    gpio.setup(FRONT_GO, gpio.OUT)
    gpio.setup(FRONT_DIR, gpio.OUT)
    gpio.setup(DRIVE_GO, gpio.OUT)
    gpio.setup(DRIVE_DIR, gpio.OUT)

    #Pin Initialization
    gpio.output(FRONT_GO, gpio.LOW)
    gpio.output(FRONT_DIR, gpio.LOW)
    gpio.output(DRIVE_GO, gpio.LOW)
    gpio.output(DRIVE_DIR, gpio.LOW)
