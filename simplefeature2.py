import PIL
from kivy.resources import resource_find
from kivy.core.image import Image as CoreImage

from AES_feature import from_string_to_SHA512, AES_encode, convert_encode_to_string
from EditImg import HideTextMASK, HideText
from Operations import PIL_image_to_kivy_texture
from Screens_container import *
from Layouts_container import *
from Images_container import *
from Buttons_container import *
from TextInputs_container import *
from Switchers_container import *
from Labels_container import *
from FileChooser_container import *

def init_sf2():
    ## save encoded img ##
    def save_encoded_img():
        current_path = str(img_source.source)
        dot_pos = current_path.find('.')
        # save mask img
        if switch_saveMask.active:
            mask_path = current_path[0:dot_pos] + '_mask' + '.png'
            img_mask1.texture.save(mask_path)
            print(mask_path)
        # save encoded img
        new_path = current_path[0:dot_pos] + '_encoded' + '.png'
        print(new_path)
        img_result1.texture.save(new_path)
        print('saved!')
    button_save.on_press = save_encoded_img

    ## set selection path ##
    def set_another_image(object, path, mouseEvent):
        Path = path[0]
        filename = resource_find(str(Path))
        try:
            cor_tmp = CoreImage(filename)
        except:
            #print(img_source.source)
            return
        img_source.source = str(Path)
        #print(img_source.source)
        sm.switch_to(screen_mainWork, direction='left')
    fc.bind(on_submit=set_another_image)

    ## calculate steography ##
    def calculate_image():
        ### download image to calculate ###
        new_img = PIL.Image.open(img_source.source, mode='r')
        #new_img = new_img.transpose(method=PIL.Image.FLIP_TOP_BOTTOM)
        # crypto #
        messageToHide = textinput_text.text
        assert len(messageToHide) > 0
        key_string = textinput_key.text
        assert len(key_string) > 0
        sha_key = from_string_to_SHA512(key_string)
        tag, nonce, messageToHide = AES_encode(sha_key, messageToHide)
        encoded_data = (tag, nonce, messageToHide)
        string_encoded_data = convert_encode_to_string(encoded_data)
        # calculate #
        encryptedImg = HideText(new_img.copy(), string_encoded_data)
        # show #
        img_result1.texture = PIL_image_to_kivy_texture(encryptedImg)
        # mask
        img_mask1_tmp = HideTextMASK(new_img.copy(), string_encoded_data)
        img_mask1.texture = PIL_image_to_kivy_texture(img_mask1_tmp)

        # decode
        # rawMessageToShow = ShowText(encryptedImg) # 16B/16B/xB
        # (tag_b, nonce_b, cripertext_b) = convert_string_to_encode(rawMessageToShow)
        # encoded_data = (tag_b, nonce_b, cripertext_b)
        # assert type(tag_b) == bytes
        # messageFromImg = AES_decode(sha_key, encoded_data)
        # textinput_sten.text = messageFromImg

        # close all #
        new_img.close()
        encryptedImg.close()
    button_make.on_press = calculate_image


