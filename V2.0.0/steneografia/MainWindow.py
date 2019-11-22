import sys

import kivy

kivy.require('1.11.1')  # replace with your current kivy version !

from kivy.app import App

import os

import popups

from Screens_container import *
from Layouts_container import *
from Images_container import *
from Buttons_container import *
from TextInputs_container import *
from Switchers_container import *
from Labels_container import *
from FileChooser_container import *

import simplefeature1
from simplefeature2 import *
import simplefeature2


class MyApp(App):

    def build(self):
        # init #
        self.title = 'version: 2.0.0'
        simplefeature1.init_sf1()
        #simplefeature2.init_sf2()

        ### variables ###
        path_curr = os.path.dirname(os.path.abspath(__file__))
        d_buttons = {'button_readf': button_readf,
                     'button_show': button_show,
                     'button_make': button_make,
                     'button_save': button_save,
                     'button_settings': button_settings}
        d_inputs_left = {'textinput_key': textinput_key,
                         'textinput_sten': textinput_sten}
        d_inputs_right = {'textinput_text': textinput_text}
        d_images = {'img_source': img_source,
                    'img_result1': img_result1}
        d_switchers = {'switch_saveMask': switch_saveMask,
                       'switch_wholeFile': switch_wholeFile,
                       'switch_checkSize': switch_checkSize,
                       'switch_onlyBesPixels': switch_onlyBesPixels,
                       'switch_prieview': switch_prieview,
                       'switch_filePresenter': switch_filePresenter}
        d_labels = {'label_saveMask': label_saveMask,
                    'label_wholeFile': label_wholeFile,
                    'label_checkSize': label_checkSize,
                    'label_onlyBesPixels': label_onlyBesPixels,
                    'label_prieview': label_prieview,
                    'label_filePresenter': label_filePresenter}
        #all_obj = [d_buttons, d_inputs_left, d_inputs_right, d_images, d_switchers, d_labels]
        lay_inputs.add_widget(lay_inputs_left)
        lay_inputs.add_widget(lay_inputs_right)
        layouts = [lay_buttons, lay_inputs, lay_images]

        ### properties ###
        fc.rootpath = path_curr

        ### collect widgets of widgets ###
        fc.add_widget(FileChooserListLayout())
        # fc.add_widget(FileChooserIconLayout())

        ### push widgets to layouts ###
        for b in d_buttons.values():
            lay_buttons.add_widget(b)
        for ipsl in d_inputs_left.values():
            lay_inputs_left.add_widget(ipsl)
        for ipsr in d_inputs_right.values():
            lay_inputs_right.add_widget(ipsr)
        for img in d_images.values():
            lay_images.add_widget(img)
        for (sw, lab) in zip(d_switchers.values(),d_labels.values()):
            settings_layout.add_widget(lab)
            settings_layout.add_widget(sw)
        settings_layout.add_widget(label_backFromSett)
        settings_layout.add_widget(button_backFromSett)
        fc_layout.add_widget(button_back)

        ### push layouts to layout[s] ###
        ## main ##
        for l in layouts:
            box.add_widget(l)
        ## fc ##
        fc_layout.add_widget(fc)



        ### set screens ###
        screen_mainWork.add_widget(box)
        screen_fileChooser.add_widget(fc_layout)
        screen_settings.add_widget(settings_layout)


        ### Return main screen ###
        return sm


if __name__ == '__main__':
    MyApp().run()
    sys.stdout.flush()
    sys.stdout.close()
