import PIL
from kivy.resources import resource_find
from kivy.core.image import Image as CoreImage

import popups

from AES_feature import from_string_to_SHA512, AES_encode, convert_encode_to_string, convert_string_to_encode, \
    AES_decode
from EditImg import HideTextMASK, HideText, ShowText, HideDisperse, HideDisperseMASK, ShowDisperse
from Operations import PIL_image_to_kivy_texture
from Screens_container import *
from Layouts_container import *
from Images_container import *
from Buttons_container import *
from TextInputs_container import *
from Switchers_container import *
from Labels_container import *
from FileChooser_container import *


## calculate steography ##
def calculate_image():
    global czemuMnieNieWidzi
    ### download image to calculate ###
    new_img = PIL.Image.open(img_source.source, mode='r')
    # crypto #
    messageToHide = textinput_text.text
    assert len(messageToHide) > 0
    key_string = textinput_key.text
    assert len(key_string) > 0
    sha_key = from_string_to_SHA512(key_string)
    tag, nonce, messageToHideCriper = AES_encode(sha_key, messageToHide)
    encoded_data = (tag, nonce, messageToHideCriper)
    string_encoded_data = convert_encode_to_string(encoded_data)
    # calculate #
    if switch_wholeFile.active:
        czemuMnieNieWidzi = HideDisperse(new_img.copy(), string_encoded_data)
        # mask
        img_mask1_tmp = HideDisperseMASK(new_img.copy(), string_encoded_data)
        img_mask1.texture = PIL_image_to_kivy_texture(img_mask1_tmp)
    else:
        # real hide
        czemuMnieNieWidzi = HideText(new_img.copy(), string_encoded_data)
        # mask
        img_mask1_tmp = HideTextMASK(new_img.copy(), string_encoded_data)
        img_mask1.texture = PIL_image_to_kivy_texture(img_mask1_tmp)
    assert czemuMnieNieWidzi != None

    # show #
    if not switch_prieview.active:
        img_result1.texture = PIL_image_to_kivy_texture(czemuMnieNieWidzi.copy())
    else:
        img_result1.texture = img_mask1.texture

    # verify
    needVerify = True
    if needVerify:
        rawMessageToShow = None
        if switch_wholeFile.active:
            rawMessageToShow = ShowDisperse(czemuMnieNieWidzi.copy())  # 16B/16B/xB per DISPERSE (default 5)
        else:
            rawMessageToShow = ShowText(czemuMnieNieWidzi.copy())  # 16B/16B/xB
        assert rawMessageToShow != None
        (tag_b, nonce_b, cripertext_b) = convert_string_to_encode(rawMessageToShow)
        encoded_data = (tag_b, nonce_b, cripertext_b)
        assert type(tag_b) == bytes
        messageFromImg = AES_decode(sha_key, encoded_data)
        assert messageFromImg == messageToHide
        print('VERIFIED OK!')
    else:
        print('Not verified!')

    popups.popup_hided_data.open()
button_make.on_press = calculate_image


## save encoded img ##
def save_encoded_img():
    global czemuMnieNieWidzi
    current_path = str(img_source.source)
    last_dot = current_path.rfind('.')
    # save mask img
    if switch_saveMask.active:
        mask_path = current_path[0:last_dot] + '_mask' + '.bmp'  # update to png
        img_mask1.texture.save(mask_path)
    # save encoded img
    new_path = current_path[0:last_dot] + '_encoded' + '.bmp'  # update to png
    czemuMnieNieWidzi.save(new_path, format='BMP')
    print('saved!')
    if switch_saveMask.active:
        popups.popup_image_saved_m.open()
    else:
        popups.popup_image_saved.open()
button_save.on_press = save_encoded_img


## set selection path ##
def set_another_image(object, path, mouseEvent):
    Path = path[0]
    filename = resource_find(str(Path))
    try:
        cor_tmp = CoreImage(filename)
    except:
        popups.popup_wrong_format.open()
        return
    img_source.source = str(Path)
    print(img_source.source)
    sm.switch_to(screen_mainWork, direction='left')
fc.bind(on_submit=set_another_image)


def draft_hidden_message():
    ### download image to calculate ###
    encryptedImg = PIL.Image.open(img_source.source, mode='r')
    # prepare parameters #
    key_string = textinput_key.text
    assert len(key_string) > 0
    sha_key = from_string_to_SHA512(key_string)

    # decode
    #rawMessageToShow = ShowText(encryptedImg)  # 16B/16B/xB
    if switch_wholeFile.active:
        rawMessageToShow = ShowDisperse(encryptedImg.copy())  # 16B/16B/xB per DISPERSE (default 5)
    else:
        rawMessageToShow = ShowText(encryptedImg.copy())  # 16B/16B/xB
    (tag_b, nonce_b, cripertext_b) = convert_string_to_encode(rawMessageToShow)
    encoded_data = (tag_b, nonce_b, cripertext_b)
    assert type(tag_b) == bytes
    messageFromImg = AES_decode(sha_key, encoded_data)
    textinput_text.text = messageFromImg
    popups.popup_drafted_data.open()
button_show.on_press = draft_hidden_message




