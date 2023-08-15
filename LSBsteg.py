from PIL import Image


def convert_image_RGBA(image_object):
    try:
        img = image_object.convert("RGBA")
        return img
    except IOError:
        return image_object

def get_image_size(image_Object):
    width, height = image_Object.size
    return width * height * 4


def hide_bin_image_lsb(image_path, msg):
    ###Load image and get check factors
    img = Image.open(image_path)
    img = convert_image_RGBA(img)
    width, height = img.size
    max_msg_length = width * height * 4
    

    ###Pad end of message so fits within the Image
    if len(msg) > max_msg_length:
        return None
    else:
        msg += '0' * (max_msg_length - len(msg))

    pixels = img.load()
    bit_index = 0
    for y in range(height):
        for x in range(width):
            r,g,b,a = pixels[x,y]
            if bit_index < len(msg):
                ## Modify each LSB of each colour channel
                r = (r & 254) | int(msg[bit_index])
                g = (g & 254) | int(msg[bit_index + 1])
                b = (b & 254) | int(msg[bit_index + 2])
                a = (a & 254) | int(msg[bit_index + 3])
                bit_index += 4
                pixels[x,y] = (r,g,b,a)

    ## Save image
    output_image_path = image_path.replace(".png", "_steg.png")
    img.save(output_image_path)


def retireve_bin_image_lsb(image_path):
    img = Image.open(image_path)
    width, heigth = img.size

    ##Extract Bits
    msg = ''
    pixels = img.load()
    for y in range(heigth):
        for x in range(width):
            r,g,b,a = pixels[x,y]
            msg += str(r & 1) + str(g & 1) + str(b & 1) + str(a & 1)

    return msg



print("Hello")
#msg = retireve_bin_image_lsb('EmeraldLake_steg.png')

#rint(msg)


##hide_bin_image_lsb('flower_original.png', "010010101010111101")
##print(retireve_bin_image_lsb('flower_original_steg.png'))