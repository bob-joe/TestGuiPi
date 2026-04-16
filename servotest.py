import RPi.GPIO as GPIO
import time

# Use BCM numbering
GPIO.setmode(GPIO.BCM)

# Set GPIO 16 as output
servo_pin = 16
GPIO.setup(servo_pin, GPIO.OUT)

# Set PWM frequency to 50Hz (standard for servos)
pwm = GPIO.PWM(servo_pin, 50)

# Start PWM with duty cycle 0
pwm.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)  # Convert angle to duty cycle
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        # Move servo to different positions
        set_angle(0)
        time.sleep(1)

        set_angle(90)
        time.sleep(1)

        set_angle(180)
        time.sleep(1)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
