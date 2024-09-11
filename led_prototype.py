import itertools
import math

from PIL import Image
from ast import literal_eval

led_map = Image.open("led_map.png")
leds_array = [led_map.width, led_map.height]

max_pins = 6

best_pins = [999, 0, 0]

for m in range(max_pins):
    pins_encoding = m
    for n in range(max_pins + 1):
        c = 1
        for x in range(pins_encoding):
            c *= n - x
        p = int(c / math.factorial(pins_encoding))
        if p >= leds_array[0] * leds_array[1]:
            if n < best_pins[0]:
                best_pins[0] = n
                best_pins[1] = m
            elif n == best_pins[0] and best_pins[2] < p:
                best_pins[0] = n
                best_pins[1] = m
                best_pins[2] = p
            break

pins_encoding = best_pins[1]
for n in range(max_pins + 1):
    c = 1
    for x in range(pins_encoding):
        c *= n - x
    p = int(c / math.factorial(pins_encoding))
    if p >= leds_array[0] * leds_array[1]:
        pins = [i for i in range(n)]
        print(str(n) + "+2 pins is use, max " + str(p) + " pixels.")
        break
    elif n == max_pins:
        print(str(max_pins) + " pins would not be enough to display your image!!!")
        quit()

led_switch_pin = best_pins[0]+1
write_pin = best_pins[0]+2

comb = []


class Voltage:
    ON = "HIGH"
    OFF = "LOW"

    def SWITCH(self, initial):
        if initial == Voltage.ON:
            return Voltage.OFF
        else:
            return Voltage.ON


def switch_led_at(coord, volt):
    global pins
    global comb
    global leds_array
    global write_pin
    global pins_encoding

    print("(Pixel "+str(coord)+")")

    print("- Pin "+str(write_pin)+" set "+Voltage.ON, "(Writing start)")
    if coord[0] <= leds_array[0] - 1 and coord[1] <= leds_array[1] - 1:
        k = 0
        for i in itertools.combinations(pins, pins_encoding):
            if k < leds_array[0] * leds_array[1]:
                comb.append([i[j] for j in range(len(i) - 1, -1, -1)])
                k += 1
            else:
                break
        led = coord
        active_pins = comb[led[0] + led[1] * leds_array[0]]
        inactive_pins = [i for i in pins if i not in active_pins]
        print("- Pins "+str(active_pins)+" set", Voltage.ON)
        print("- Pins "+str(inactive_pins)+" set", Voltage.OFF)
        print("- Pin "+str(led_switch_pin) + " set "+volt, "(Written data)")
    else:
        print("Coordinate not on the LED map!!!")
        quit()
    print("- Pin "+str(write_pin) + " set "+Voltage.OFF, "(Writing end)")
    print("- Pin "+str(led_switch_pin)+" set "+Voltage.OFF, "(Reset data)")


def clear_led_map():
    global led_map
    global leds_array

    print("Clearing LED map.")

    for y in range(leds_array[1]):
        for x in range(leds_array[0]):
            switch_led_at([x, y], Voltage.OFF)


def draw_led_map():
    global led_map
    global leds_array

    print("Drawing LED map.")

    for y in range(leds_array[1]):
        for x in range(leds_array[0]):
            if led_map.getpixel([x, y]) == (255, 255, 255, 255):
                switch_led_at([x,y], Voltage.ON)
            else:
                switch_led_at([x,y], Voltage.OFF)


clear_led_map()
draw_led_map()