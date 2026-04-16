import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

SERVO_PIN = 13  # change if needed

GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz for servo
pwm.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)

def sweep(speed_delay):
    # left to right
    for angle in range(0, 181, 2):
        set_angle(angle)
        time.sleep(speed_delay)

    # right to left
    for angle in range(180, -1, -2):
        set_angle(angle)
        time.sleep(speed_delay)

try:
    while True:
        sweep(0)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()

sweep(.01)
set_angle(200)
set_angle(100)
