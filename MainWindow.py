import kivy
from kivy.uix.gridlayout import GridLayout

kivy.require('1.11.1')  # replace with your current kivy version !

from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image

from filechosser import *
from kivy.resources import resource_find
from kivy.core.image import Image as CoreImage, Texture
from kivy.uix.textinput import TextInput

import os

import PIL

from EditImg import *
from Operations import *

from kivy.uix.screenmanager import ScreenManager, Screen

class MyApp(App):

    def build(self):
        ### Screens ###
        sm = ScreenManager()
        screen_mainWork = Screen(name='mainWork')
        screen_fileChooser = Screen(name='filechosser')
        sm.add_widget(screen_mainWork)
        sm.add_widget(screen_fileChooser)
        ### layouts ###
        box = GridLayout(rows=3)
        lay_buttons = BoxLayout(size_hint=(1,0.11), pos_hint={'top': 1})  # for buttons, max height 10%
        lay_inputs = GridLayout(cols=2, size_hint=(1,0.3))  # for inputs, max height 20%
        lay_inputs_left = GridLayout(rows=2)  # for lay_inputs layer (left)
        lay_inputs_right = BoxLayout()  # for lay_inputs layer (right)
        lay_images = GridLayout(cols=2, pos_hint={'top': 1})  # for images, max height 70%
        fc_layout = BoxLayout(orientation='vertical')

        ### Widgets and Objects ###
        ## image source ##
        img_source = Image(source='w3bw.bmp', size_hint=(2,2), pos_hint={'top': 1})
        ## image result1 ##
        texture = Texture.create(size=(640, 480), colorfmt='rgb')
        img_result1 = Image(texture=texture, size_hint=(2, 2))
        #img_result1 = Image(source='w3bw.bmp', size_hint=(2,2), pos_hint={'top': 1})
        ## Buttons ##
        button_readf = Button(text='READ FILE', size_hint=(1, 1))
        button_show = Button(text='SHOW HIDDEN', size_hint=(1, 1))
        button_make = Button(text='MAKE', size_hint=(1, 1))
        button_save = Button(text='SAVE', size_hint=(1, 1))
        button_back = Button(text='BACK', size_hint=(1, 0.2))
        ## file services ##
        fc = FileChooser()
        ## textbox input ##
        textinput_key = TextInput(hint_text='key', pos_hint={'top': 1})
        textinput_sten = TextInput(hint_text='sten', pos_hint={'top': 1})
        textinput_text = TextInput(hint_text='text', pos_hint={'top': 1})

        ### variables ###
        path_curr = os.path.dirname(os.path.abspath(__file__))
        d_buttons = {'button_readf': button_readf,
                     'button_show': button_show,
                     'button_make': button_make,
                     'button_save': button_save}
        d_inputs_left = {'textinput_key': textinput_key,
                         'textinput_sten': textinput_sten}
        d_inputs_right = {'textinput_text': textinput_text}
        d_images = {'img_source': img_source,
                    'img_result1': img_result1}
        all_obj = [d_buttons, d_inputs_left, d_inputs_right, d_images]
        lay_inputs.add_widget(lay_inputs_left)
        lay_inputs.add_widget(lay_inputs_right)
        layouts = [lay_buttons, lay_inputs, lay_images]

        ### properties ###
        fc.rootpath = path_curr #fc.add_widget(FileChooserIconLayout())

        ### Features ###
        ## set selection path ##
        def set_another_image(one, two):
            filename = resource_find(str(two[0]))
            try:
                cor_tmp = CoreImage(filename)
            except:
                #print(img_source.source)
                return
            img_source.source = str(two[0])
            #print(img_source.source)
        fc.bind(selection=set_another_image)

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

            # decode
            rawMessageToShow = ShowText(encryptedImg) # 16B/16B/xB
            (tag_b, nonce_b, cripertext_b) = convert_string_to_encode(rawMessageToShow)
            encoded_data = (tag_b, nonce_b, cripertext_b)
            assert type(tag_b) == bytes
            messageFromImg = AES_decode(sha_key, encoded_data)
            textinput_sten.text = messageFromImg

            # close all #
            new_img.close()
            encryptedImg.close()
        button_make.on_press = calculate_image

        ## change screen to filechooser ##
        def switch_screen():
            sm.switch_to(screen_fileChooser, direction='right')
        button_readf.on_press = switch_screen

        ## change screen do main ##
        def switch_screen():
            sm.switch_to(screen_mainWork, direction='left')
        button_back.on_press = switch_screen

        ### collect widgets of widgets ###
        fc.add_widget(FileChooserListLayout())

        ### push widgets to layouts ###
        for b in d_buttons.values():
            lay_buttons.add_widget(b)
        for ipsl in d_inputs_left.values():
            lay_inputs_left.add_widget(ipsl)
        for ipsr in d_inputs_right.values():
            lay_inputs_right.add_widget(ipsr)
        for img in d_images.values():
            lay_images.add_widget(img)

        ### push layouts to layout[s] ###
        ## main ##
        for l in layouts:
            box.add_widget(l)
        ## fc ##
        fc_layout.add_widget(fc)
        fc_layout.add_widget(button_back)


        ### set screens ###
        screen_mainWork.add_widget(box)
        screen_fileChooser.add_widget(fc_layout)


        ### Return main screen ###
        return sm


if __name__ == '__main__':
    MyApp().run()
