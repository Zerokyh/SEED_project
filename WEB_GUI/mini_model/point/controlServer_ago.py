import RPi.GPIO as gpio

#Motor 1 GPIO Pins
DRIVE_GO = 17 #IC3A
DRIVE_DIR = 4 #IC3, 4EN
#Motor 2 GPIO Pins
FRONT_DIR = 25 #IC1A
FRONT_GO = 10 #IC1, 2EN

def forward():
    gpio.setmode(gpio.BCM)
    gpio.output(DRIVE_GO, gpio.HIGH)
    gpio.output(DRIVE_DIR, gpio.HIGH)
def backward():
    gpio.setmode(gpio.BCM)
    gpio.output(DRIVE_GO, gpio.HIGH)
    gpio.output(DRIVE_DIR, gpio.LOW)
def left():
    gpio.setmode(gpio.BCM)
    gpio.output(FRONT_DIR, gpio.HIGH)
    gpio.output(FRONT_GO, gpio.HIGH)
def right():
    gpio.setmode(gpio.BCM)
    gpio.output(FRONT_DIR, gpio.LOW)
    gpio.output(FRONT_GO, gpio.HIGH)
def stop():
    gpio.setmode(gpio.BCM)
    gpio.output(FRONT_GO, gpio.LOW)
    gpio.output(FRONT_DIR, gpio.LOW)
    gpio.output(DRIVE_GO, gpio.LOW)
    gpio.output(DRIVE_DIR, gpio.LOW)

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