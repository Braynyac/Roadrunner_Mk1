import RPi.GPIO as GPIO
import time


servo_signal = 3
throttle_signal = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_signal, GPIO.OUT)
GPIO.setup(throttle_signal, GPIO.OUT)
servo_pwm = GPIO.PWM(servo_signal, 100)
servo_pwm.start(0)
throttle_pwm = GPIO.PWM(throttle_signal, 100)
throttle_pwm.start(0)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def limit(num,minn,maxx):
    if num<minn:
        num=minn
    elif num>maxx:
        num=maxx
    return num

def throttle_control(speed):
    speed = limit(speed,-100,100)
    if speed == 0:
        return 13.5
    elif speed<0:
        return translate(speed,-100,0,4.25,12)
    elif speed>0:
        return translate(speed,0,100,14,24)

def update(angle,speed=0):
    duty = translate(float(angle), 0,180,20,10.7)
    servo_pwm.ChangeDutyCycle(duty)
    throttle_pwm.ChangeDutyCycle(float(speed))


def shutdown():
    GPIO.cleanup()

if __name__ == '__main__':    
    while True:
        i = float(input("Speed:"))
        update(90,throttle_control(i))
