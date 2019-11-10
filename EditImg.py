# EditImg
# Edit images
# author: MArcin Ziajkowski

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
        pixels[e1[0], e1[1]] = (r+1, g, b)
    for e1 in ExtraPixels[1]:
        (r, g, b) = pixels[e1[0], e1[1]]
        pixels[e1[0], e1[1]] = (r, g+1, b)
    for e1 in ExtraPixels[2]:
        (r, g, b) = pixels[e1[0], e1[1]]
        pixels[e1[0], e1[1]] = (r, g, b+1)
    print(len(ExtraPixels[0]), len(ExtraPixels[1]), len(ExtraPixels[2]))
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
    #print(len(ExtraPixels[0]), len(ExtraPixels[1]), len(ExtraPixels[2]))
    return img
##############################################

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

def add_len_to_begin(MessageLength:int, imgLoadObj):
    # imgLoadObj is access to pixels
    pass

def HideText(img, text):
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
            r -= 1
        elif x1 == a1 ^ a3 and x2 != a2 ^ a3:
            # change a2
            g -= 1
        elif x1 != a1 ^ a3 and x2 != a2 ^ a3:
            # change a3
            b -= 1
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
        bits =  bits + str(a1 ^ a3)
        bits =  bits + str(a2 ^ a3)
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
        e = str(bin(ord(c)))[2:]
        while len(e) < 8:
            e = '0' + e
        Text += e
    # amount of bits
    doWrite = len(Text)
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
                    r -= 1
                elif x1 == a1 ^ a3 and x2 != a2 ^ a3:
                    # change a2
                    g -= 1
                elif x1 != a1 ^ a3 and x2 != a2 ^ a3:
                    # change a3
                    b -= 1
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
            if letsBegin:
                letsBegin-=1
            else:
                (r, g, b) = pixels[i, j]
                l_bittext += str(r & 1 ^ b & 1)
                l_bittext += str(g & 1 ^ b & 1)
                doneBits += 2
                if lengthOfBits == doneBits:
                    break
        if DEBUG: print("wiadomosc odczyt: ", l_bittext)
    text = ''
    znak = ''
    for e1 in l_bittext:
        znak += e1
        if len(znak) == 8:
            text += chr(int(znak, 2))
            znak = ''

    if DEBUG: print(text)
    return text


## TODO
## zrobic bardziej modulowo

if __name__ == "__main__":
    text = 'abcdefgh'
    digitsBinary = convert_text_to_bits(text)
    for e in range(len(text)):
        print(digitsBinary[e*8:e*8+8])