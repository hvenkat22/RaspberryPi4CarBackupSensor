import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
TRIG_PIN = 11  # GPIO pin for the trigger
ECHO_PIN = 13  # GPIO pin for the echo
BUZZER_PIN = 15  # GPIO pin for the buzzer
GREEN_LED_PIN = 16  # GPIO pin for the green LED
RED_LED_PIN = 18    # GPIO pin for the red LED
BLUE_LED_PIN = 22   # GPIO pin for the blue LED


GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(BLUE_LED_PIN, GPIO.OUT)

def measure_distance():
    pulse_end_time=0
    pulse_start_time=0
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)  

    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start_time = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end_time = time.time()

   
    pulse_duration = pulse_end_time - pulse_start_time
    distance = (pulse_duration * 34300) / 2  

    return distance

def beep_buzzer(frequency, duration):
    buzzer = GPIO.PWM(BUZZER_PIN, frequency)
    buzzer.start(50) 
    time.sleep(duration)
    buzzer.stop()

def set_leds(distance):
    if distance < 10: 
        GPIO.output(GREEN_LED_PIN, GPIO.LOW)
        GPIO.output(RED_LED_PIN, GPIO.HIGH)
        GPIO.output(BLUE_LED_PIN, GPIO.LOW)
    elif distance >= 10 and distance < 20: 
        GPIO.output(GREEN_LED_PIN, GPIO.LOW)
        GPIO.output(RED_LED_PIN, GPIO.LOW)
        GPIO.output(BLUE_LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
        GPIO.output(RED_LED_PIN, GPIO.LOW)
        GPIO.output(BLUE_LED_PIN, GPIO.LOW)

try:
    while True:
        distance = measure_distance()
        print("Distance: {:.2f} cm".format(distance))

        if distance < 10: 
            beep_buzzer(3000, 0.1)  
        elif distance >=10 and distance < 20: 
            beep_buzzer(1000, 0.1) 

        set_leds(distance)

except KeyboardInterrupt:
    GPIO.cleanup() 

finally:
    GPIO.cleanup() 
