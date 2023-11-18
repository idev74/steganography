from PIL import Image, ImageDraw,ImageFont


def decode_image(path_to_png):
    """
    Decodes an image hidden in an image using binary.
    """
    # Open the image using PIL:
    encoded_image = Image.open(path_to_png)

    # Separate the red channel from the rest of the image:
    red_channel = encoded_image.split()[0]

    # Create a new PIL image with the same size as the encoded image:
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    x_size, y_size = encoded_image.size

    for x in range(x_size):
        for y in range(y_size):
            pixel = red_channel.getpixel((x, y))
            lsb = pixel % 2
            if lsb == 1:
                pixels[x, y] = (255, 255, 255)
            else:
                pixels[x, y] = (0, 0, 0)

    print(red_channel)

    # DO NOT MODIFY. Save the decoded image to disk:
    decoded_image.save("decoded_image.png")


def encode_image(path_to_png, hidden_text):
    """
    Encodes an image hidden in an image using binary.
    """
    # Open the image using PIL:
    original_image = Image.open(path_to_png)
    encoded_image = original_image.copy()
    pixels = encoded_image.load()
    x_size, y_size = original_image.size

    # Create a new PIL image with the same size as the encoded image:
    image_text = write_text(hidden_text, x_size, y_size)
    text_pixels = image_text.load()

    # Iterate over the pixels of both images and modify the LSB of the original image
    for x in range(x_size):
        for y in range(y_size):
            original_pixel = original_image.getpixel((x, y))
            text_pixel = text_pixels[x, y]
            
            # Modify the LSB of the red channel of the original image
            new_red_channel = (original_pixel[0] & 0xFE) | (text_pixel[0] >> 7)
            new_pixel = (new_red_channel, original_pixel[1], original_pixel[2])
            
            pixels[x, y] = new_pixel
    
    # Save the encoded image to disk:
    encoded_image.save("encoded_image.png")

def write_text(text_to_write, width, height):
    """
    Writes text to an image and returns the image.
    """
    # Create a blank black image
    img = Image.new('RGB', (width, height), color='black')
    create = ImageDraw.Draw(img)

    # Adjust the font size as needed
    font_size = 100
    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', font_size)
    
    create.text((10, 10), text_to_write, font=font, fill='white')

    # Save the image to disk
    img.save('text.png')
    return img
    
encode_image('reef.png', 'Credit to Francesco Ungaro on Unsplash!')

# Will be the same as 'text.png
decode_image('encoded_image.png')