import RPi.GPIO as GPIO
import time


servo_signal = 3 # BCM GPIO number
throttle_signal = 2 # BCM GPIO number
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_signal, GPIO.OUT)
GPIO.setup(throttle_signal, GPIO.OUT)
servo_pwm = GPIO.PWM(servo_signal, 100)
throttle_pwm = GPIO.PWM(throttle_signal, 100)
servo_pwm.start(0)
throttle_pwm.start(0)

# A clone function of the arduino's map()
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

# updates angle and speed in a single function, default speed is zero for safety precaution
def update(angle,speed=0):
    # 10.7 and 20 is what I experimetally found to be the correct modulations between 0 and 180 degrees of the servo
    duty = translate(float(angle), 0,180,20,10.7)
    servo_pwm.ChangeDutyCycle(duty)
    throttle_pwm.ChangeDutyCycle(float(speed))


def shutdown():
    GPIO.cleanup() # cleans up the pins, but is not currently implemented
