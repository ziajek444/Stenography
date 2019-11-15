### Screens ###
from kivy.uix.screenmanager import ScreenManager, Screen

sm = ScreenManager()
screen_mainWork = Screen(name='mainWork')
screen_fileChooser = Screen(name='filechosser')
screen_settings = Screen(name='settings')
sm.add_widget(screen_mainWork)
sm.add_widget(screen_fileChooser)
sm.add_widget(screen_settings)
