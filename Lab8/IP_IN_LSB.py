#!/usr/bin/env python
#not sure is shebang is needed
from PIL import Image
image_to_obf = "company_logo.png"
message_to_hide = "TARGET:192.168.1.50"

def set_LSB(value, bit):
    if bit == '0':
        value = value & 254
    else:
        value = value | 1
    return value


def hide_message(image, message, outfile):

    message += chr(0)
    c_image = Image.open(image)
    c_image = c_image.convert('RGBA')
    out = Image.new(c_image.mode, c_image.size)
    width, height = c_image.size
    pixList = list(c_image.getdata())
    newArray = []
    
    for i in range(len(message)):
        charInt = ord(message[i])
        cb = str(bin(charInt))[2:].zfill(8)
        pix1 = pixList[i*2]
        pix2 = pixList[(i*2)+1]
        newpix1 = []
        newpix2 = []

        for j in range(0,4):
            newpix1.append(set_LSB(pix1[j], cb[j]))
            newpix2.append(set_LSB(pix2[j], cb[j+4]))

        newArray.append(tuple(newpix1))
        newArray.append(tuple(newpix2))

    newArray.extend(pixList[len(message)*2:])
    
    out.putdata(newArray)
    out.save(outfile)
    return outfile   


if __name__ == "__main__":

    print(hide_message(image_to_obf, "TARGET:192.168.1.50", 'company_logo_stego.png'))
