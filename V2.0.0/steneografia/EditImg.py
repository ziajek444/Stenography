# EditImg
# Edit images
# author: MArcin Ziajkowski
#
from TextInputs_container import textinput_sten

__author__ = 'Marcin Ziajkowski'

from AES_feature import *

EI_RED = (255, 0, 0)
EI_GREEN = (0, 255, 0)
EI_BLUE = (0, 0, 255)
EI_BLACK = (0, 0, 0)
EI_WHITE = (255, 255, 255)
DEBUG = True

def findExtraPixels(in_pixels, imgX, imgY):
    ExtraPixelsR = []
    ExtraPixelsG = []
    ExtraPixelsB = []

    for j in range(imgY):
        for i in range(imgX):
            (r, g, b) = in_pixels[i, j]

            if ((g + b)//2 < r-32):
                ExtraPixelsR.append((i, j))
            elif ((b + r)//2 < g-32):
                ExtraPixelsG.append((i, j))
            elif ((r + g)//2 < b-32):
                ExtraPixelsB.append((i, j))
            else:
                pass
    ExtraPixels = (ExtraPixelsR, ExtraPixelsG, ExtraPixelsB)
    return ExtraPixels


def add_one_to_best(img):
    pixels = img.load()

    ExtraPixels = findExtraPixels(pixels, img.size[0], img.size[1])

    for e1 in ExtraPixels[0]:
        (r, g, b) = pixels[e1[0], e1[1]]
        pixels[e1[0], e1[1]] = (r, 0, 0)
    for e1 in ExtraPixels[1]:
        (r, g, b) = pixels[e1[0], e1[1]]
        pixels[e1[0], e1[1]] = (0, g, 0)
    for e1 in ExtraPixels[2]:
        (r, g, b) = pixels[e1[0], e1[1]]
        pixels[e1[0], e1[1]] = (0, 0, b)
    return img


def best_is_black(img):
    pixels = img.load()

    ExtraPixels = findExtraPixels(pixels, img.size[0], img.size[1])

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i, j] = EI_WHITE

    for e1 in ExtraPixels[0]:
        (r, g, b) = pixels[e1[0], e1[1]]
        pixels[e1[0], e1[1]] = EI_BLACK
    for e1 in ExtraPixels[1]:
        (r, g, b) = pixels[e1[0], e1[1]]
        pixels[e1[0], e1[1]] = EI_BLACK
    for e1 in ExtraPixels[2]:
        (r, g, b) = pixels[e1[0], e1[1]]
        pixels[e1[0], e1[1]] = EI_BLACK
    return img


def generate_text_to_hide(input_key_value, textToEncode):
    sha512Key = from_string_to_SHA512(input_key_value)
    encodedData = AES_encode(sha512Key, textToEncode)
    return encodedData


def convert_text_to_bits(text):
    BinText = ''
    for c in text:
        # convert character to binary
        e = str(bin(ord(c)))[2:]
        # make 8 digit binary number (101 -> 00000101)
        while len(e) != 8:
            e = '0' + e
        # add next character in binary
        BinText += e
    # check if len of BinText is correct
    assert len(BinText) == len(text) * 8
    return BinText


def convert_number_to_32bits(number):
    binaryTextString = str(bin(number))[2:]
    while len(binaryTextString) != 32:
        binaryTextString = '0' + binaryTextString
    return binaryTextString


def add_len_to_begin(pixels, binaryTextString):
    for i in range(16):
        (r, g, b) = pixels[i, 0]
        a1 = r & 1
        a2 = g & 1
        a3 = b & 1
        x1 = int(binaryTextString[i * 2])
        x2 = int(binaryTextString[(i * 2) + 1])

        if x1 == a1 ^ a3 and x2 == a2 ^ a3:
            # no change
            pass
        elif x1 != a1 ^ a3 and x2 == a2 ^ a3:
            # change a1
            if r > 0:
                r -= 1
            else:
                r += 1
        elif x1 == a1 ^ a3 and x2 != a2 ^ a3:
            # change a2
            if g > 0:
                g -= 1
            else:
                g += 1
        elif x1 != a1 ^ a3 and x2 != a2 ^ a3:
            # change a3
            if b > 0:
                b -= 1
            else:
                b += 1
        else:
            print("!!!!!!!\n\nHARD ERROR !!!!!!!!! FATAL, ...\n\n!!!!!!!!")
        pixels[i, 0] = (r, g, b)


def convert_text_to_digital_bits(text):
    digital_bits = ''
    for c in text:
        if type(c) == str:
            e = str(bin(ord(c)))[2:]
        else:
            e = str(bin(c))[2:]

        while len(e) < 8:
            e = '0' + e
        digital_bits += e
    return digital_bits


def HideText(img, text):
    # convert text to bits and set length of text
    lengthOfText = len(text)
    binaryTextString = convert_number_to_32bits(lengthOfText)
    assert len(binaryTextString) == 32
    # from (0,0) to (32,0) save size
    # I can save 2bits per pixel
    # to save 8B I need 64bits. 64/2 = 32pixels
    # set on first 32 bit len of following text
    pixels = img.load()
    add_len_to_begin(pixels,binaryTextString)
    # test whether bit are correct saved
    #region verify bits
    bits = ""
    for i in range(16):
        (r, g, b) = pixels[i, 0]
        a1 = r & 1
        a2 = g & 1
        a3 = b & 1
        bits =  bits + str(a1 ^ a3)
        bits =  bits + str(a2 ^ a3)
    if (int(bits, 2) == lengthOfText):
        if DEBUG: print("liczba zapisanych bitow zapis: ", bits)
        pass
    else:
        raise 1
    #endregion

    # main text hider
    # go per pixels (per 3 Byte), save 2 bits per pixel
    # start from 31th pixel
    # convert text to digital bits
    Text = ''
    for c in text:
        if type(c) == str:
            e = str(bin(ord(c)))[2:]
        else:
            e = str(bin(c))[2:]

        while len(e) < 8:
            e = '0' + e
        Text += e
    # amount of bits
    doWrite = len(Text)
    assert doWrite == len(text) * 8
    indexText = 0
    # save main text to img
    bityWych = ''  # for debug
    for j in range(img.size[1]):
        if doWrite == indexText:
            break
        for i in range(img.size[0]):
            if not (i < 32 and j == 0):
                (r, g, b) = pixels[i, j]
                a1 = r & 1
                a2 = g & 1
                a3 = b & 1
                x1 = int(Text[indexText])
                indexText += 1
                x2 = int(Text[indexText])
                indexText += 1
                if x1 == a1 ^ a3 and x2 == a2 ^ a3:
                    # no change
                    pass
                elif x1 != a1 ^ a3 and x2 == a2 ^ a3:
                    # change a1
                    if r > 0:
                        r -= 1
                    else:
                        r += 1
                elif x1 == a1 ^ a3 and x2 != a2 ^ a3:
                    # change a2
                    if g > 0:
                        g -= 1
                    else:
                        g += 1
                elif x1 != a1 ^ a3 and x2 != a2 ^ a3:
                    # change a3
                    if b > 0:
                        b -= 1
                    else:
                        b += 1
                else:
                    print("!!!!!!!\n\nHARD ERROR !!!!!!!!! FATAL, ...\n\n!!!!!!!!")
                pixels[i, j] = (r, g, b)
                if DEBUG:
                    bityWych += str(r&1 ^ b&1)
                    bityWych += str(g&1 ^ b&1)

                if doWrite == indexText:
                    break
    if DEBUG: print("wiadomosc zapis: ", bityWych)
    return img


class RounedCounter:
    def __init__(self, max, min=0):
        if max > min:
            self.max = max
            self.min = min
        else:
            self.min = max
            self.max = min
        assert self.min != self.max
        self.current_value = min
    def update(self):
        if self.current_value < self.max:
            self.current_value += 1
        else:
            self.current_value = self.min
    def reset(self):
        self.current_value = self.min
    def get(self):
        return self.current_value

def get_random_pixels(width, height, knum):
    # get random pixels from 32b begin
    seed_text = textinput_sten.text
    seed_number = None
    if len(seed_text) > 0:
        seed_str_number = ''
        for e in seed_text:
            seed_str_number += str(ord(e) % 10)
        seed_number = int(seed_str_number)
    else:
        seed_number = 10
    import random
    random.seed(seed_number)
    return_pixels_list = set()
    j = RounedCounter(height - 1)

    while(len(return_pixels_list) < knum):
        i = random.randint(0, width-1)
        if not (i < 32 and j.get() == 0):
            return_pixels_list.add((i, j.get()))
        j.update()
    return return_pixels_list


def HideDisperse(img, text):
    # convert text to bits and set length of text
    lengthOfText = len(text)
    binaryTextString = convert_number_to_32bits(lengthOfText)
    assert len(binaryTextString) == 32
    # from (0,0) to (32,0) save size
    # I can save 2bits per pixel
    # to save 8B I need 64bits. 64/2 = 32pixels
    # set on first 32 bit len of following text
    pixels = img.load()
    add_len_to_begin(pixels,binaryTextString)
    # test whether bit are correct saved
    #region verify bits
    bits = ""
    for i in range(16):
        (r, g, b) = pixels[i, 0]
        a1 = r & 1
        a2 = g & 1
        a3 = b & 1
        bits =  bits + str(a1 ^ a3)
        bits =  bits + str(a2 ^ a3)
    if (int(bits, 2) == lengthOfText):
        if DEBUG: print("liczba zapisanych bitow zapis: ", bits)
        pass
    else:
        raise 1
    #endregion

    # main text hider
    # go per pixels (per 3 Byte), save 2 bits per pixel
    # start from 31th pixel
    # convert text to digital bits
    Text = ''
    for c in text:
        if type(c) == str:
            e = str(bin(ord(c)))[2:]
        else:
            e = str(bin(c))[2:]

        while len(e) < 8:
            e = '0' + e
        Text += e
    # amount of bits
    doWrite = len(Text)
    assert doWrite == len(text) * 8
    indexText = 0
    # save main text to img
    bityWych = ''  # for debug
    r = get_random_pixels(img.size[0], img.size[1], doWrite/2)
    for e in r:
        i = e[0]
        j = e[1]
        (r, g, b) = pixels[i, j]
        a1 = r & 1
        a2 = g & 1
        a3 = b & 1
        x1 = int(Text[indexText])
        indexText += 1
        x2 = int(Text[indexText])
        indexText += 1
        if x1 == a1 ^ a3 and x2 == a2 ^ a3:
            # no change
            pass
        elif x1 != a1 ^ a3 and x2 == a2 ^ a3:
            # change a1
            if r > 0:
                r -= 1
            else:
                r += 1
        elif x1 == a1 ^ a3 and x2 != a2 ^ a3:
            # change a2
            if g > 0:
                g -= 1
            else:
                g += 1
        elif x1 != a1 ^ a3 and x2 != a2 ^ a3:
            # change a3
            if b > 0:
                b -= 1
            else:
                b += 1
        else:
            print("!!!!!!!\n\nHARD ERROR !!!!!!!!! FATAL, ...\n\n!!!!!!!!")
        pixels[i, j] = (r, g, b)
        if DEBUG:
            bityWych += str(r&1 ^ b&1)
            bityWych += str(g&1 ^ b&1)

        if doWrite == indexText:
            break
    if DEBUG: print("wiadomosc zapis: ", bityWych)

    return img


def HideTextMASK(img, text):
    # convert text to bits and set length od text
    lengthOfText = len(text)
    binaryTextString = str(bin(lengthOfText))[2:]
    while len(binaryTextString) != 32:
        binaryTextString = '0' + binaryTextString

    # from (0,0) to (32,0) save size
    # I can save 2bits per pixel
    # to save 8B I need 64bits. 64/2 = 32pixels
    # set on first 32 bit len of following text
    pixels = img.load()
    for i in range(16):
        (r, g, b) = pixels[i, 0]
        a1 = r & 1
        a2 = g & 1
        a3 = b & 1
        x1 = int(binaryTextString[i*2])
        x2 = int(binaryTextString[(i * 2) + 1])

        if x1 == a1 ^ a3 and x2 == a2 ^ a3:
            # no change
            pass
        elif x1 != a1 ^ a3 and x2 == a2 ^ a3:
            # change a1
            if r > 0:
                r -= 1
            else:
                r += 1
        elif x1 == a1 ^ a3 and x2 != a2 ^ a3:
            # change a2
            if g > 0:
                g -= 1
            else:
                g += 1
        elif x1 != a1 ^ a3 and x2 != a2 ^ a3:
            # change a3
            if b > 0:
                b -= 1
            else:
                b += 1
        else:
            print("!!!!!!!\n\nHARD ERROR !!!!!!!!! FATAL, ...\n\n!!!!!!!!")
        pixels[i, 0] = (r, g, b)

    # test whether bit are correct saved
    bits = ""
    for i in range(16):
        (r, g, b) = pixels[i, 0]
        a1 = r & 1
        a2 = g & 1
        a3 = b & 1
        bits = bits + str(a1 ^ a3)
        bits = bits + str(a2 ^ a3)
    if (int(bits, 2) == lengthOfText):
        if DEBUG: print("liczba zapisanych bitow zapis: ", bits)
        pass
    else:
        raise 1

    # main text hider
    # go per pixels (per 3 Byte), save 2 bits per pixel
    # start from 31th pixel
    # convert text to digital bits
    Text = ''
    for c in text:
        if type(c) == str:
            e = str(bin(ord(c)))[2:]
        else:
            e = str(bin(c))[2:]

        while len(e) < 8:
            e = '0' + e
        Text += e
    # amount of bits
    doWrite = len(Text)
    assert doWrite == len(text) * 8
    indexText = 0
    # save main text to img
    bityWych = ''  # for debug
    for j in range(img.size[1]):
        if doWrite == indexText:
            break
        for i in range(img.size[0]):
            if not (i < 32 and j == 0):
                indexText += 2
                pixels[i, j] = (0, 0, 0)

                if doWrite == indexText:
                    break
    return img


def HideDisperseMASK(img, text):
    # convert text to bits and set length od text
    lengthOfText = len(text)
    binaryTextString = str(bin(lengthOfText))[2:]
    while len(binaryTextString) != 32:
        binaryTextString = '0' + binaryTextString

    # from (0,0) to (32,0) save size
    # I can save 2bits per pixel
    # to save 8B I need 64bits. 64/2 = 32pixels
    # set on first 32 bit len of following text
    pixels = img.load()
    for i in range(16):
        (r, g, b) = pixels[i, 0]
        a1 = r & 1
        a2 = g & 1
        a3 = b & 1
        x1 = int(binaryTextString[i*2])
        x2 = int(binaryTextString[(i * 2) + 1])

        if x1 == a1 ^ a3 and x2 == a2 ^ a3:
            # no change
            pass
        elif x1 != a1 ^ a3 and x2 == a2 ^ a3:
            # change a1
            if r > 0:
                r -= 1
            else:
                r += 1
        elif x1 == a1 ^ a3 and x2 != a2 ^ a3:
            # change a2
            if g > 0:
                g -= 1
            else:
                g += 1
        elif x1 != a1 ^ a3 and x2 != a2 ^ a3:
            # change a3
            if b > 0:
                b -= 1
            else:
                b += 1
        else:
            print("!!!!!!!\n\nHARD ERROR !!!!!!!!! FATAL, ...\n\n!!!!!!!!")
        pixels[i, 0] = (r, g, b)

    # test whether bit are correct saved
    bits = ""
    for i in range(16):
        (r, g, b) = pixels[i, 0]
        a1 = r & 1
        a2 = g & 1
        a3 = b & 1
        bits = bits + str(a1 ^ a3)
        bits = bits + str(a2 ^ a3)
    if (int(bits, 2) == lengthOfText):
        if DEBUG: print("liczba zapisanych bitow zapis: ", bits)
        pass
    else:
        raise 1

    # main text hider
    # go per pixels (per 3 Byte), save 2 bits per pixel
    # start from 31th pixel
    # convert text to digital bits
    Text = ''
    for c in text:
        if type(c) == str:
            e = str(bin(ord(c)))[2:]
        else:
            e = str(bin(c))[2:]

        while len(e) < 8:
            e = '0' + e
        Text += e
    # amount of bits
    doWrite = len(Text)
    assert doWrite == len(text) * 8
    indexText = 0
    # save main text to img
    bityWych = ''  # for debug
    r = get_random_pixels(img.size[0], img.size[1], doWrite / 2)
    for e in r:
        i = e[0]
        j = e[1]
        indexText += 2
        pixels[i, j] = (0, 0, 0)

        if doWrite == indexText:
            break
    return img


def ShowDisperse(img):
    pixels = img.load()
    bits = ""
    for i in range(16):
        (r, g, b) = pixels[i, 0]
        a1 = r & 1
        a2 = g & 1
        a3 = b & 1
        bits = bits + str(a1 ^ a3)
        bits = bits + str(a2 ^ a3)
    if DEBUG: print("liczba zapisanych bajtow odczyt: ", bits)

    lengthOfText = int(bits, 2)
    lengthOfBits = lengthOfText * 8
    doneBits = 0
    letsBegin = 32
    l_bittext = ""
    r = get_random_pixels(img.size[0], img.size[1], lengthOfBits / 2)
    for e in r:
        i = e[0]
        j = e[1]
        (r, g, b) = pixels[i, j]
        l_bittext += str(r & 1 ^ b & 1)
        l_bittext += str(g & 1 ^ b & 1)
        doneBits += 2
        if lengthOfBits == doneBits:
            break
    if DEBUG: print("wiadomosc odczyt bit: ", l_bittext)
    text = ''
    znak = ''
    for e1 in l_bittext:
        znak += e1
        if len(znak) == 8:
            text += chr(int(znak, 2))
            znak = ''

    if DEBUG: print(text)
    assert type(text) == str
    return text


# read raw string from img
def ShowText(img):
    pixels = img.load()
    bits = ""
    for i in range(16):
        (r, g, b) = pixels[i, 0]
        a1 = r & 1
        a2 = g & 1
        a3 = b & 1
        bits = bits + str(a1 ^ a3)
        bits = bits + str(a2 ^ a3)
    if DEBUG: print("liczba zapisanych bajtow odczyt: ", bits)

    lengthOfText = int(bits, 2)
    lengthOfBits = lengthOfText * 8
    doneBits = 0
    letsBegin = 32
    l_bittext = ""
    for j in range(img.size[1]):
        if lengthOfBits == doneBits:
            break
        for i in range(img.size[0]):
            if not (i < 32 and j == 0):
                (r, g, b) = pixels[i, j]
                l_bittext += str(r & 1 ^ b & 1)
                l_bittext += str(g & 1 ^ b & 1)
                doneBits += 2
                if lengthOfBits == doneBits:
                    break
    if DEBUG: print("wiadomosc odczyt bit: ", l_bittext)
    text = ''
    znak = ''
    for e1 in l_bittext:
        znak += e1
        if len(znak) == 8:
            text += chr(int(znak, 2))
            znak = ''

    if DEBUG: print(text)
    assert type(text) == str
    return text


if __name__ == "__main__":
    # import PIL
    # from PIL import Image
    #
    # # text = 'abcdefgh'
    # # digitsBinary = convert_text_to_bits(text)
    # # for e in range(len(text)):
    # #     print(digitsBinary[e*8:e*8+8])
    #
    # # test image set all pixels
    # print("test 1")
    # message = '1234567890' * 1000
    # #test_img1 = PIL.Image.open('w3bw.bmp', mode='r')
    # #test_img1 = PIL.Image.open('Jellyfish.jpg', mode='r')
    # test_img1 = PIL.Image.open('Hydrangeas.jpg', mode='r')
    # test_img1.show()
    # test_img2 = HideText(test_img1.copy(), message)
    # test_img2.show()
    #
    # # where pixels are saved
    # test_img3 = HideTextMASK(test_img1.copy(), message)
    # test_img3.show()
    #
    # returnmessage = ShowText(test_img2.copy())
    # print(returnmessage == message)
    # assert returnmessage == message

    print("test 2")
    tmp = get_random_pixels(40000, 40000, 10000)
    print(list(tmp)[0:20])
    assert len(tmp) == 10000
    print('done')
