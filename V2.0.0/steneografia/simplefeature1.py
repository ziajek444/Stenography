from Screens_container import *
from Layouts_container import *
from Images_container import *
from Buttons_container import *
from TextInputs_container import *
from Switchers_container import *
from Labels_container import *
from FileChooser_container import *


def init_sf1():
    ### Features ###
    ## change screen to filechooser ##
    def switch_screen_to_choose():
        sm.switch_to(screen_fileChooser, direction='right')
        fc._update_files()
    button_readf.on_press = switch_screen_to_choose


    ## change screen to main ##
    def switch_screen_to_main():
        sm.switch_to(screen_mainWork, direction='left')
    button_back.on_press = switch_screen_to_main


    ## change screen to settings ##
    def switch_screen_to_settings():
        sm.switch_to(screen_settings, direction='left')
    button_settings.on_press = switch_screen_to_settings


    ## change screen from settings ##
    def switch_screen_from_settings():
        sm.switch_to(screen_mainWork, direction='right')
    button_backFromSett.on_press = switch_screen_from_settings


    ## settings ##
    def saveMask_callback(instance, value):
        print('the saveMask', instance, 'is', value)
    switch_saveMask.bind(active=saveMask_callback)


    def wholeFile_callback(instance, value):
        print('the wholeFile', instance, 'is', value)
    switch_wholeFile.bind(active=wholeFile_callback)


    def checkSize_callback(instance, value):
        print('the wholeFile', instance, 'is', value)
    switch_checkSize.bind(active=checkSize_callback)


    def onlyBesPixels_callback(instance, value):
        print('the onlyBesPixels', instance, 'is', value)
    switch_onlyBesPixels.bind(active=onlyBesPixels_callback)


    def prieview_callback(instance, value):
        print('the onlyBesPixels', instance, 'is', value)
    switch_prieview.bind(active=prieview_callback)


    def filePresenter_callback(instance, value):
        #fc.add_widget(FileChooserIconLayout())
        print('the filePresenter', instance, 'is', value)
    switch_filePresenter.bind(active=filePresenter_callback)


