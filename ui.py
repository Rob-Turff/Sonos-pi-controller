
import time
import sys
import atexit

from PIL import ImageFont, Image, ImageDraw
from gfxhat import touch, lcd, backlight, fonts

class MenuOption:
    def __init__(self, name, action, font, options=()):
        self.name = name
        self.action = action
        self.options = options
        self.size = font.getsize(self.name)
        self.width, self.height = self.size

    def trigger(self):
        self.action(*self.options)

class UI:
    def __init__(self, controller, options_dict):
        print("""menu-options.py
        This example shows how you might store a list of menu options associated
        with functions and navigate them on GFX HAT.
        Press Ctrl+C or select "Exit" to exit.
        """)

        self.width, self.height = lcd.dimensions()
        self.font = ImageFont.truetype(fonts.BitbuntuFull, 10)
        self.image = Image.new('P', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

        for x in range(6):
            touch.set_led(x, 0)
            backlight.set_pixel(x, 255, 255, 255)
            touch.on(x, self.handler)

        backlight.show()

        atexit.register(self.cleanup)

        self.menu_options = []

        for key in options_dict:
            self.menu_options.append(MenuOption(key, controller.change_station, self.font, (options_dict[key], True)))

        self.current_menu_option = 1

        self.trigger_action = False

    def set_backlight(self, r, g, b):
        backlight.set_all(r, g, b)
        backlight.show()

    def handler(self, ch, event):
        if event != 'press':
            return
        print("Button pressed: " + str(ch))
        if ch == 1:
            self.current_menu_option += 1
        if ch == 0:
            self.current_menu_option -= 1
        if ch == 4:
            self.trigger_action = True
        self.current_menu_option %= len(self.menu_options)

    def cleanup(self):
        backlight.set_all(0, 0, 0)
        backlight.show()
        lcd.clear()
        lcd.show()

    def start(self):
        try:
            while True:
                self.image.paste(0, (0, 0, self.width, self.height))
                offset_top = 0

                if self.trigger_action:
                    self.menu_options[self.current_menu_option].trigger()
                    self.trigger_action = False

                for index in range(len(self.menu_options)):
                    if index == self.current_menu_option:
                        break
                    offset_top += 12

                for index in range(len(self.menu_options)):
                    x = 10
                    y = (index * 12) + (self.height / 2) - 4 - offset_top
                    option = self.menu_options[index]
                    if index == self.current_menu_option:
                        self.draw.rectangle(((x-2, y-1), (self.width, y+10)), 1)
                    self.draw.text((x, y), option.name, 0 if index == self.current_menu_option else 1, self.font)

                w, h = self.font.getsize('>')
                self.draw.text((0, (self.height - h) / 2), '>', 1, self.font)

                for x in range(self.width):
                    for y in range(self.height):
                        pixel = self.image.getpixel((x, y))
                        lcd.set_pixel(x, y, pixel)

                lcd.show()
                time.sleep(1.0 / 30)

        except KeyboardInterrupt:
            self.cleanup()