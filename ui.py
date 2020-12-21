
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
        self.controller = controller

        for x in range(6):
            touch.set_led(x, 0)
            self.set_backlight()
            touch.on(x, self.handler)

        backlight.show()

        atexit.register(self.cleanup)

        self.menu_options = []

        for key in options_dict:
            self.menu_options.append(MenuOption(key, controller.change_station, self.font, (options_dict[key], True)))

        self.current_menu_option = 1

        self.trigger_action = False

    def set_backlight(self):
        if self.controller.get_playing_state():
            colour = [255, 255, 255]
        else:
            colour = [255, 0, 0]
        backlight.set_all(colour[0], colour[1], colour[2])
        backlight.show()

    def change_menu_option(self, diff):
        if self.current_menu_option == len(self.menu_options) and diff > 0:
            pass
        elif self.current_menu_option == 1 and diff < 0:
            pass
        else:
            self.current_menu_option += diff

    def handler(self, ch, event):
        if event != 'press':
            return
        print("Button pressed: " + str(ch))
        if ch == 1:
            self.change_menu_option(diff=1)
        if ch == 0:
            self.change_menu_option(diff=-1)
        if ch == 4:
            self.trigger_action = True
        if ch == 3:
            self.controller.change_volume(-5)
        if ch == 5:
            self.controller.change_volume(5)

    def cleanup(self):
        backlight.set_all(0, 0, 0)
        backlight.show()
        lcd.clear()
        lcd.show()

    def set_now_playing(self):
        option = MenuOption("Now Playing: ", self.controller.get_playing_state(), self.font, None)
        return option

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

                for index in range(len(self.menu_options) + 1):
                    x = 10
                    y = (index * 12) + (self.height / 2) - 4 - offset_top

                    if index == 0:
                        option = self.set_now_playing()
                        w, h = self.font.getsize('♫')
                        self.draw.rectangle(((x, 13), (self.width, 14)), 1)
                        self.draw.text((x, 1), option.name, 1, self.font)
                        self.draw.text((0, (self.height - h) / 2), '♫', 1, self.font)
                    else:
                        option = self.menu_options[index - 1]
                        if index == self.current_menu_option:
                            self.draw.rectangle(((x-2, y-1), (self.width, y+10)), 1)
                        self.draw.text((x, y), option.name, 0 if index == self.current_menu_option else 1, self.font)

                w, h = self.font.getsize('>')
                self.draw.text((0, (self.height - h) / 2), '>', 1, self.font)

                for x in range(self.width):
                    for y in range(self.height):
                        pixel = self.image.getpixel((x, y))
                        lcd.set_pixel(x, y, pixel)

                self.set_backlight()

                lcd.show()
                time.sleep(1.0 / 30)

        except KeyboardInterrupt:
            self.cleanup()