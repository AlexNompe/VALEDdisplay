import itertools
import math
import timeit

from PIL import Image

# !!! Before everything!!!
# !!! LEDS turn ON and OFF.
# !!! PINS set HIGH and LOW.

# The image to display on the LED panel. Only pixels that are pure white (#FFFFFF) will turn ON the corresponding LEDs.
led_map = Image.open("led_map.png").convert("RGB")

# GPIO PINS on a microcontroller may be arranged and labeled inconsistently.
# This dictionary remaps the PIN indexes to the actual physical GPIO PINS.
# (In this case, PIN index +2 is used, but feel free to customize the mapping for your setup).
pin_map = {
    0: 2,
    1: 3,
    2: 4,
    3: 5,
    4: 6,
    5: 7,
    6: 8,
    7: 9,
    8: 10,
    9: 11,
    10: 12,
    11: 13,
    12: 14,
    13: 15,
    14: 16,
    15: 17,
    16: 18,
    17: 19,
    18: 20,
    19: 21,
    20: 22,
    21: 23,
    22: 24,
    23: 25,
    24: 26,
    25: 27,
    26: 28
}

# Maximum number of GPIO PINS to use as encoded ADDRESSES for controlling LEDS.
# Note: Two additional PINS are required for writing data to the LED panel.
# The configuration is calculated based on factorial combinations of these PINS.
max_pins = 24

# After this bit of code the best_pin_options dictionary contains 3 values:
# ["min_pins"] is a minimum number of PINS to properly display your image.
# ["amo_enc_pins"] is a number of encoding PINS which make your ADDRESS at the time. (ADDRESS looks like: (0, 1, 2) ).
# ["max_pixels"] is a maximum number of pixels you can get from ["min_pins"] PINS.
best_pin_options = {
    "min_pins": 999,
    "amo_enc_pins": 0,
    "max_pixels": 0
}
for enc_pins in range(max_pins):
    fac = math.factorial(enc_pins)
    for min_pins in range(max_pins + 1):
        combinations = 1
        for x in range(enc_pins):
            combinations *= min_pins - x
        pixels = int(combinations / fac)
        # We check if the max amount of [pixels] for [min_pins] PINS is enough to store our image,
        # and if the result is better that the previous best, write it down to the [best_pin_options].
        if pixels >= led_map.width * led_map.height:
            if min_pins < best_pin_options["min_pins"]:
                best_pin_options["min_pins"] = min_pins
                best_pin_options["amo_enc_pins"] = enc_pins
                best_pin_options["max_pixels"] = pixels
            elif min_pins == best_pin_options["min_pins"] and best_pin_options["max_pixels"] < pixels:
                best_pin_options["min_pins"] = min_pins
                best_pin_options["amo_enc_pins"] = enc_pins
                best_pin_options["max_pixels"] = pixels
            break

# Info about how many PINS are used, pixels needed.
# (Saved up for later to be printed out the second time in case python console overflows with instructions).
starting_message = ""

# Check if the number of available [max_pixels] can support the image and print the result.
if best_pin_options["max_pixels"] >= led_map.width * led_map.height:
    pins = [pin_map[i] for i in range(best_pin_options["min_pins"])]
    starting_message = f"{best_pin_options["min_pins"]}+2 PINS is use, {led_map.width * led_map.height}/{best_pin_options["max_pixels"]} pixels."
    print(starting_message)
else:
    raise ValueError(f"ERROR!!! {max_pins} PINS would not be enough to display your image!!!")

# The PIN to be used as a WRITING PIN.
# (When it is HIGH, our microcontroller writes data on the board).
write_pin = pin_map[best_pin_options["min_pins"]]

# And the PIN to be used as a DATA PIN.
# (When it is writing time, data is copied to the board).
data_pin = pin_map[best_pin_options["min_pins"] + 1]


class Voltage:
    # Voltage class, ON is HIGH, OFF is LOW, SWITCH inverts the given signal (ON becomes OFF and vies versa).
    ON = "HIGH"
    OFF = "LOW"

    @staticmethod
    def SWITCH(initial):
        if initial == Voltage.ON:
            return Voltage.OFF
        else:
            return Voltage.ON


# PIN combinations must be saved only once and outside a function, that's why they're stored here.
comb = []


def generate_combinations(pins, best_pin_options):
    # Generate all possible PIN combinations for addressing any single LED,
    # and stop once the number of required pixels is reached.
    global comb
    if not comb:
        needed_pixels = 0
        for i in itertools.combinations(pins, best_pin_options["amo_enc_pins"]):
            if needed_pixels < led_map.width * led_map.height:
                comb.append(i)
                needed_pixels += 1
            else:
                break


def set_led_at(xy, signal, no_comments=False):
    # Toggle the appropriate PIN to address the LED at position [xy],
    # Set the WRITING PIN to HIGH to start writing, adjust the DATA PIN according to the signal (ON/OFF),
    # then set the WRITING PIN to LOW to complete writing.
    global pins, comb, write_pin, best_pin_options

    if xy[0] <= led_map.width - 1 and xy[1] <= led_map.height - 1:
        generate_combinations(pins, best_pin_options)

        active_pins = comb[xy[0] + xy[1] * led_map.width]
        inactive_pins = [i for i in pins if i not in active_pins]

        if not no_comments:
            print(f"(Pixel {xy}) should be {signal}")

            print(f"- PINS {active_pins} set", Voltage.ON)
            print(f"- PINS {inactive_pins} set", Voltage.OFF)
            print(f"- PIN {write_pin} set", Voltage.ON, "(Writing start)")
            print(f"- PIN {data_pin} set", signal, "(Written data)")
    else:
        raise IndexError("ERROR!!! Coordinate not on the LED map!!!")
    if not no_comments:
        print(f"- PIN {write_pin} set", Voltage.OFF, "(Writing end)")


def clear_led_map(no_comments=False):
    # Clear the LED map by turning off all LEDs. Set all ADDRESS PINS to HIGH, set the WRITING PIN to HIGH,
    # set the DATA PIN to LOW, and then set the WRITING PIN to LOW.
    global pins

    if not no_comments:
        print("Clearing our LED map:")

        print(f"- PINS {pins} set", Voltage.ON)
        print(f"- PIN {write_pin} set", Voltage.ON, "(Writing start)")
        print(f"- PIN {data_pin} set", Voltage.OFF, "(Written data)")
        print(f"- PIN {write_pin} set", Voltage.OFF, "(Writing end)")


def draw_led_map(no_comments=False):
    # Turn ON the LED at [xy] if the corresponding pixel in the image is white.
    global led_map

    if not no_comments:
        print("Drawing our LED map:")

    for y in range(led_map.height):
        for x in range(led_map.width):
            if led_map.getpixel([x, y]) == (255, 255, 255, 255):
                set_led_at([x, y], Voltage.ON, no_comments)


def redraw_led_map(no_comments=False):
    # Check every pixel of the image and set an LED at those coordinates accordingly.
    global led_map

    if not no_comments:
        print("Redrawing our LED map:")

    for y in range(led_map.height):
        for x in range(led_map.width):
            if led_map.getpixel([x, y]) == (255, 255, 255):
                set_led_at([x, y], Voltage.ON, no_comments)
            else:
                set_led_at([x, y], Voltage.OFF, no_comments)


# AS FOR OUR ACTUAL ALGORITHM.
# First, we draw the map.
redraw_led_map()

# After, measure how many times the LED map can be drawn in one second to calculate the refresh rate.
timing_start = timeit.default_timer()
timing_end = timing_start
fps = 0
while (timing_end := timeit.default_timer()) - timing_start < 1:
    redraw_led_map(True)
    fps += 1

# Calculate the refresh rate in Hz, rounding to two decimal places if needed for more precision.
if (timing_end - timing_start) > 1.05:
    refresh_rate = round(fps / (timing_end - timing_start), 2)
else:
    refresh_rate = fps

print("Debug stats:")
print(f"+- {math.floor((timing_end - timing_start) * 1000)}ms spent of drawing the LED map {fps} times.",
      f"(~{round(timing_end - timing_start, 2)} second{"s" * round(max(min(round(timing_end - timing_start + 0.45), 2) - 1, 0))})")
print(f"~{refresh_rate}Hz absolute refresh rate.")
print("Repeating!", starting_message)
