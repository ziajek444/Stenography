import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from filechosser import *


class MyApp(App):

    def build(self):
        box = BoxLayout()
        lay1 = BoxLayout()
        lay2 = BoxLayout()
        lay1.add_widget(Label(text='Hello world'))
        lay1.add_widget(Button(text='Hello there'))
        fc = FileChooser()
        fc.id = 'fc'
        fc.add_widget(FileChooserIconLayout())
        #fc.add_widget(FileChooserListLayout())
        #print(fc.get_view_list())
        lay2.add_widget(fc)
        lay2.add_widget(Button(text='Kenobi?'))

        box.add_widget(lay2)
        box.add_widget(lay1)
        
        return box


if __name__ == '__main__':
    MyApp().run()
