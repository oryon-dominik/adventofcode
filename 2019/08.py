#!/usr/bin/env python3
# coding: utf-8

"""
AdventOfCode 2019 Day 8

decode an unknow image-format from the space elves

requirements: "Pillow"
"""


from PIL import Image


WIDTH, HEIGHT = 25 , 6


def read_image_data_from_file(file="08.data") -> str:
    """ read the image_layers from file """
    with open(file, "r") as image_file:
        image_str = image_file.read()
    return image_str


def build_layers_from_raw_data(image: str, image_format: tuple) -> list:
    """ - an image consists of an int per pixel
        - the format describes width & heigth
        - in every layer there is a defintion for every pixel in the image
        - the image is split into its sinlge layers and returned
    """
    width, height = image_format
    layer_lenght = width * height
    image_lenght = len(image)
    assert image_lenght % layer_lenght == 0
    layers = [image[px:px+layer_lenght] for px in range(0, image_lenght, layer_lenght)]
    layer_count = int(image_lenght / layer_lenght)
    assert len(layers) == layer_count
    return layers


def select_layer(layers: list) -> str:
    """ selects the layer with most zeros """
    zero_counts = [layer.count('0') for layer in layers]
    layer_index = zero_counts.index(min(zero_counts))
    layer = layers[layer_index]
    return layer


def calculate_result(layer):
    return layer.count('1') * layer.count('2')


def build_image_str(layers: list, image_format: tuple) -> str:
    """ paints layer per layer from layers on the final image
        0 = black
        1 = white
        2 = transparent
    """
    width, height = image_format
    image = ['2' for px in range(width * height)]  # full-transparent image
    for layer in reversed(layers):  # the top layer draws last
        for index, px in enumerate(layer):
            if int(px) < 2:  # transparent pixels do not paint
                image[index] = px
    return "".join(image)


def build_pixels_from_str(image: str, image_format: tuple) -> list:
    image = image.replace('0', ' ')  # for better readability
    width, _ = image_format
    image_rows = [image[px:px+width] for px in range(0, len(image), width)]
    return image_rows


def build_PIL(image_str: str, image_format: tuple):
    """ builds a black and white (mode='1') png from string and scales it up a bit """
    image = Image.new("1", image_format)
    image.putdata([int(c) for c in image_str])
    # scale the image up
    factor = 10
    image = image.resize((int(image.width * factor), int(image.height * factor)))
    image.save('08.png')
    return image


# TESTS
image_data = "123456789012"
layers = build_layers_from_raw_data(image_data, (3, 2))
assert layers == ["123456", "789012"]
image_data = "0222112222120000"
layers = build_layers_from_raw_data(image_data, (2, 2))
image_str = build_image_str(layers, (2, 2))
assert image_str == "0110"

# start the program
image_str = read_image_data_from_file()
image_format = (WIDTH, HEIGHT)
layers = build_layers_from_raw_data(image_str, image_format)
layer = select_layer(layers)
r = calculate_result(layer)

image_str = build_image_str(layers, image_format)
image_rows = build_pixels_from_str(image_str, image_format)

# create an image too
build_PIL(image_str, image_format)

print(f'>>> DEBUG: {image_rows}')

print(f"Day 8, Task 1 - The calculated result is: {r}")
print("Day 8, Task 2 - decoded image_pass is:")
for row in image_rows:
    print(f"    {row}")
