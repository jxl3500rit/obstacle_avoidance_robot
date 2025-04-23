import RPi.GPIO as GPIO
import time

# ------------------------ Define GPIO Pin ------------------------
# Ultrasonic Sensor HC-SR04
TRIG = 5
ECHO = 6

# L298N Motor Driver
IN1 = 17
IN2 = 18
IN3 = 22
IN4 = 23
ENA = 13
ENB = 12

# ------------------------ Initialize GPIO ------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Ultrasonic sensor
# GPIO5 needs to output a signal to TRIG pin on ultrasonic sensor, triggering the sensor's measurement process
# GPIO6 is set to IN since the Pi receives the signal back from the sensor after it sends a pulse
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Motor control
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

# PWM Setting
pwm_left = GPIO.PWM(ENA, 1000) #1kHz
pwm_right = GPIO.PWM(ENB, 1000)

pwm_left.start(0)
pwm_right.start(0)


# ------------------------ Functions ------------------------
def set_speed(left_speed, right_speed):
    pwm_left.ChangeDutyCycle(left_speed)
    pwm_right.ChangeDutyCycle(right_speed)

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)    
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    set_speed(0, 0)

def forward(speed = 60):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    set_speed(speed, speed)

def backward(speed = 50):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    set_speed(speed, speed)

def turn_left(speed = 50):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    set_speed(speed, speed)


def turn_right(speed = 50):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    set_speed(speed, speed)

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.01)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    
    duration = pulse_end - pulse_start
    distance = duration * 17150 #cm
    distance = round(distance, 2)
    return distance


# ------------------------ Main Loop ------------------------

try:
    print("Press Ctrl+C to stop the program")
    while True:
        dist = get_distance()
        print("Distance: ", dist, " cm")
        
        if dist > 25:
                forward(60)
        else:
            stop()
            time.sleep(0.2)
            backward(50)
            time.sleep(0.5)
            turn_left(50)
            time.sleep(0.6)

except KeyboardInterrupt:
    print("The program is terminated")
    stop()
    pwm_left.stop()
    pwm_right.stop()
    GPIO.cleanup()