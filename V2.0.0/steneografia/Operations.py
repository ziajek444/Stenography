# Operations
# author: MArcin Zijakowski

__author__ = 'Marcin Ziajkowski'

from kivy.core.image import Texture
from array import array

def get_template_texture_buffer(size_x, size_y, case=0):
    # config
    template_texture = Texture.create(size=(size_x, size_y), colorfmt='rgb')
    bufer_array = None
    if case == 0:
        size = size_x * size_y * 3
        buf = [int(x * 255 / size) for x in range(size)]
        bufer_array = array('B', buf)
        template_texture.blit_buffer(bufer_array, colorfmt='rgb', bufferfmt='ubyte')
    elif case == 1:
        size = size_x * size_y * 3
        buf = [int(x%255) for x in range(size)]
        bufer_array = array('B', buf)
        template_texture.blit_buffer(bufer_array, colorfmt='rgb', bufferfmt='ubyte')
    elif case == 2:
        size = size_x * size_y * 3
        buf = [255 for x in range(size)]
        bufer_array = array('B', buf)
        template_texture.blit_buffer(bufer_array, colorfmt='rgb', bufferfmt='ubyte')
    else:
        raise 'Not implemented!'

    assert bufer_array != None
    return template_texture


def horizontal_mirror_array(array, size_x = None, size_y = None):
    # [0, 0][0, 1][0, 2][0, 3]        [3, 0][3, 1][3, 2][3, 3]
    # [1, 0][1, 1][1, 2][1, 3]  =>    [2, 0][2, 1][2, 2][2, 3]
    # [2, 0][2, 1][2, 2][2, 3]  =>    [1, 0][1, 1][1, 2][1, 3]
    # [3, 0][3, 1][3, 2][3, 3]        [0, 0][0, 1][0, 2][0, 3]
    # first of all convert array to matrix
    # check inputs
    if size_x == None and size_y == None:
        # than it must be square matrix NxN
        IsSquare = int(len(array)**(1/2))
        assert IsSquare**2 == len(array)
    elif size_x == None or size_y == None:
        raise 'set both parameters'
    else:
        arrayLen = len(array)
        assert (size_x * size_y)*3 == arrayLen
    # conversion
    mirroredBytes = []
    pxls_size_x = size_x*3
    pxls_size_y = size_y * 3
    for j in range(pxls_size_y):
        mirroredBytes.append(array[j*pxls_size_x:(j+1)*pxls_size_x])
    # mirrroring
    mirroredBytes = mirroredBytes[::-1]
    # set mirroring bytes from list to byte variable
    returnBytes = None
    for e in mirroredBytes:
        if returnBytes == None:
            returnBytes = e
        else:
            returnBytes += e
    assert type(returnBytes) == bytes
    return returnBytes


def PIL_image_to_kivy_texture(pilImage):
    kivy_texture = Texture.create(size=pilImage.size, colorfmt='rgb')
    horiz_revers_bytes = horizontal_mirror_array(pilImage.tobytes(), pilImage.size[0], pilImage.size[1])
    kivy_texture.blit_buffer(horiz_revers_bytes, colorfmt='rgb', bufferfmt='ubyte')
    return kivy_texture

