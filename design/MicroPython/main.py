# Copyright (c) 2025 MTHS All rights reserved
#
# Created by: Isaac Ip
# Created on: Oct 2025
# This program reads in the amount of light.

from microbit import *


class HCSR04:

    def __init__(self, tpin=pin1, epin=pin2, spin=pin13):
        spi.init(
            baudrate=125000,
            sclk=self.sclk_pin,
            mosi=self.trigger_pin,
            miso=self.echo_pin,
        )

    def distance_mm(self):
        spi.init(
            baudrate=125000,
            sclk=self.sclk_pin,
            mosi=self.trigger_pin,
            miso=self.echo_pin,
        )
        pre = 0
        post = 0
        k = -1
        length = 500
        resp = bytearray(length)
        resp[0] = 0xFF
        spi.write_readinto(resp, resp)
        # find first non zero value
        try:
            i, value = next((ind, v) for ind, v in enumerate(resp) if v)
        except StopIteration:
            i = -1
        if i > 0:
            pre = bin(value).count("1")
            # find first non full high value afterwards
            try:
                k, value = next(
                    (ind, v)
                    for ind, v in enumerate(resp[i : length - 2])
                    if resp[i + ind + 1] == 0
                )
                post = bin(value).count("1") if k else 0
                k = k + i
            except StopIteration:
                i = -1
                dist = (
                    -1
                    if i < 0
                    else round(((pre + (k - i) * 8.0 + post) * 8 * 0.172) / 2)
                )
                return dist


sonar = HCSR04()

# get distance
while True:
    if button_a.is_pressed():
        display.show(sonar.distance_mm() / 10)
        sleep(5000)
        display.show(Image.HAPPY)
