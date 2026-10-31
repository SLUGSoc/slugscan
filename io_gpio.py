#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time


class GPIOAccess:

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BOARD)

        # GPIO Pin definitions
        self.p_led = [13, 19]
        self.p_led[0] = 13  # Green
        self.p_led[1] = 19  # Red
        self.p_buzzer = 22

        GPIO.setup(self.p_led[0], GPIO.OUT)
        GPIO.setup(self.p_led[1], GPIO.OUT)
        GPIO.setup(self.p_buzzer, GPIO.OUT)

        # Set all on
        GPIO.output(self.p_led[0], True)
        GPIO.output(self.p_led[1], True)
        GPIO.output(self.p_buzzer, True)

        time.sleep(1)

        # Set all off
        GPIO.output(self.p_led[0], False)
        GPIO.output(self.p_led[1], False)
        GPIO.output(self.p_buzzer, False)

    def update(self) -> None:
        pass

    def buzz(self, duration: float, wait_time: float, color: int = 0) -> None:
        GPIO.output(self.p_led[color], True)
        GPIO.output(self.p_buzzer, True)

        time.sleep(duration)

        GPIO.output(self.p_led[color], False)
        GPIO.output(self.p_buzzer, False)

        time.sleep(wait_time)

    def successful_scan(self) -> None:
        self.buzz(0.25, 0.01)

    def failed_scan(self) -> None:
        self.buzz(0.8, 0.01, 1)

    def not_registered(self) -> None:
        for _ in range(5):
            self.buzz(0.1, 0.1)
