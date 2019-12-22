from PIL import Image
import os
import json

class Emoji:
    """
    attributes: filename
                r - Average red value of the image
                g - Average green value of the image
                b - Average blue value of the image
                alpha_count - Count of pixels where alpha (opacity) = 0
                h - Average hue of the image
                s - Average saturation of the image
                l - Average lightness of the image

    methods:    _get_average_color(img) returns the average color of a PIL Image object
                _rgb_to_hsl(r,g,b)      returns the (hue, saturation, lightness) as a tuple
                                        given the red (r), green(g), and blue (b) values
    """

    def __init__(self, filename):
        self.filename = filename

        # Open the image
        img_file = Image.open('128/' + filename)
        img = img_file.convert('RGBA')

        self.r, self.g, self.b, self.zero_alpha_count = self._get_average_color(img)
        self.h, self.s, self.l = self._rgb_to_hsl(self.r, self.g, self.b)



    @staticmethod
    def _get_average_color(img):
        """
        :param img: A python Image object
        :return: An tuple with the r, g, b value at position 0, 1, and 2 respectively and the alpha pixel count at position 4
        """
        width, height = img.size

        r = 0
        g = 0
        b = 0
        a = 0
        count = 0
        for w in range(width):
            for h in range(height):
                color = img.getpixel((w, h))
                alpha = color[3]
                if alpha != 0:

                    r += color[0]
                    g += color[1]
                    b += color[2]

                else:
                    #
                    a += 1

        finalRed = int(r / ((width * height) - a))
        finalGreen = int(g / ((width * height) - a))
        finalBlue = int(b / ((width * height) - a))

        return (finalRed, finalGreen, finalBlue, a)

    @staticmethod
    def _rgb_to_hsl(r, g, b):
        """
        :param r: the r vealue of a pixel (0-255)
        :param g: the g vealue of a pixel (0-255)
        :param b: the b vealue of a pixel (0-255)
        :return:
        """
        r1 = r / 255
        g1 = g / 255
        b1 = b / 255
        cmax = max(r1, g1, b1)
        cmin = min(r1, g1, b1)
        d = cmax - cmin

        # lightness
        l = (cmax + cmin) / 2

        # saturation
        if d == 0:
            s = 0
        else:
            s = d / (1 - abs(2 * l - 1))

        # hue
        if d == 0:
            h = 0
        elif cmax == r1:
            h = 60 * (((g1 - b1) / d) % 6)
        elif cmax == g1:
            h = 60 * (((b1 - r1) / d) + 2)
        else:
            h = 60 * (((r1 - g1) / d) + 4)

        return int(h), int(s * 100), int(l*100)


# Go through all the image files in the 128 folder
# Create a dictionary of all the Emoji objects, with the filename as their keys
emoji_dict = {}
for filename in os.listdir('128'):
    emoji = Emoji(filename)
    emoji_dict[filename] = emoji.__dict__


# Write Emoji dict to file
with open('emoji_dict.json', 'w') as filehandle:
    json.dump(emoji_dict, filehandle)
