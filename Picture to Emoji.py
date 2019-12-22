from PIL import Image
import os
import json


def averageColor(image, width, height, square_size):
    """
    :param image: A PIL Image object
    :param width: the x coordinate of where to start sampling colors
    :param height: the y coordinate of where to start sampling colors
    :param square_size: The offset from the x and y coordinate.
    :return: the red, green, and blue value in a tuple (r, g, b)

    The image
    [````````````|```````````````````````````]
    [          height                        ]
    [            |                           ]
    [--- width --.-- square size ------>     ]
    [            |\\\\\\\\\\\\\\\\\\\\\\     ]
    [          square \\\\\ Area to \\\\     ]
    [           size \\\\\ be sampled \\     ]
    [            |\\\\\\\\\\\\\\\\\\\\\\     ]
    [            |\\\\\\\\\\\\\\\\\\\\\\     ]
    [            |\\\\\\\\\\\\\\\\\\\\\\     ]
    [                                        ]
    [                                        ]
    [________________________________________]

    """
    r = 0
    g = 0
    b = 0
    for w in range(width, width+square_size):
        for h in range(height, height+square_size):
            color = image.getpixel((w, h))
            r += color[0]
            g += color[1]
            b += color[2]
    finalRed = int(r/(square_size ** 2))
    finalGreen = int(g/(square_size ** 2))
    finalBlue = int(b/(square_size ** 2))
    return (finalRed, finalGreen, finalBlue)

def rgb_to_hsl(r, g, b):
    """
    :param r: the r value of a pixel (0-255)
    :param g: the g value of a pixel (0-255)
    :param b: the b value of a pixel (0-255)
    :return: the hue, saturation, and lighting of the rgb value
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

    return int(h), int(s * 100), int(l * 100)


# Open emoji dict
with open('emoji_dict.json', 'r') as f:
    emoji_dict = json.loads(f.read())

emoji_list = []
for k in emoji_dict.keys():
    emoji_list.append(emoji_dict[k])

# Sort the emojis (r,g,b,h,s,l,zero_alpha) based on user-input
emoji_filter = input("Filter (r, g, b, h, s, or l):")
emoji_list.sort(key=lambda i: i[emoji_filter])

# Get square size from user
SquareSize = int(input("Square size:"))

source_image = str(4)
saved_image = Image.open('sourceImages/'+ source_image +'.jpg')
primary_image = saved_image.convert('RGBA')


width, height = primary_image.size
if width < 500:
    width *= 2
    height *= 2
    primary_image = primary_image.resize((width, height))
usable_width = width - (width % SquareSize)
usable_height = height - (height % SquareSize)

endImage = Image.new('RGBA', (usable_width, usable_height))

for w in range(0, usable_width, SquareSize):
    for h in range(0, usable_height, SquareSize):
        # Make a dictionary for the color in a square
        r, g, b = averageColor(primary_image, w, h, SquareSize)
        hue, s, l = rgb_to_hsl(r, g, b)
        color_square_dict = {'r': r, 'g': g, 'b': b, 'h': hue, 's': s, 'l': l}

        # Add the color_square dictionary to the list
        emoji_list.append(color_square_dict)
        emoji_list.sort(key=lambda i: i[emoji_filter])
        index = emoji_list.index(color_square_dict)

        final_index = index

        # Delete the color_square dictionary from the list
        del emoji_list[index]

        while final_index in range(1, len(emoji_list) - 3) and abs(emoji_list[final_index]['l'] - l) > 15:
            if index >= len(emoji_list)/2:
                final_index -= 1
            else:
                final_index += 1

        # The edge case where the emoji index was the length of emoji_list before the color_square_dict was deleted
        if final_index == len(emoji_list):
            final_index -= 1

        emoji_file = emoji_list[final_index]['filename']
        emoji_image = Image.open('128/' + emoji_file)
        emoji_image = emoji_image.resize((SquareSize, SquareSize))
        color_square_image = Image.new('RGBA', (SquareSize, SquareSize), (r, g, b, 255))
        blend_emoji_image = Image.alpha_composite(color_square_image, emoji_image)

        endImage.paste(blend_emoji_image, (w, h))

endImage.save(str(SquareSize) + str(emoji_filter) + '.png')
endImage.show()
print(str(SquareSize) + str(emoji_filter) + '.png created!')