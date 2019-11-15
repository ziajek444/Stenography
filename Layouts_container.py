### layouts ###
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

box = GridLayout(rows=3)
lay_buttons = BoxLayout(size_hint=(1,0.11), pos_hint={'top': 1})  # for buttons, max height 10%
lay_inputs = GridLayout(cols=2, size_hint=(1,0.3))  # for inputs, max height 20%
lay_inputs_left = GridLayout(rows=2)  # for lay_inputs layer (left)
lay_inputs_right = BoxLayout()  # for lay_inputs layer (right)
lay_images = GridLayout(cols=2, pos_hint={'top': 1})  # for images, max height 70%
fc_layout = BoxLayout(orientation='vertical')
settings_layout = GridLayout(rows=10, cols=2)
