import RPi.GPIO as GPIO
import time

SERVO_PIN = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set PWM frequency to 50Hz (standard for servos)
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def set_speed(duty_cycle):
    pwm.ChangeDutyCycle(duty_cycle)

try:
    while True:
        # Rotate one direction
        set_speed(7)   # adjust between ~6.5–7.5 depending on your servo

except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()
