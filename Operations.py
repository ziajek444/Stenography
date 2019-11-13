# Operations
# author: MArcin Zijakowski

__author__ = 'Marcin Ziajkowski'

from kivy.core.image import Texture

def PIL_image_to_kivy_texture(pilImage):
    kivy_texture = Texture.create(size=pilImage.size, colorfmt='rgb')
    kivy_texture.blit_buffer(pilImage.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
    return kivy_texture

def convert_format_string_to_encodeddata(strData:str):
    # convert strData to encodedData
    pass