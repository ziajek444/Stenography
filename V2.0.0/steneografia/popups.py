from kivy.uix.button import Button
from kivy.uix.popup import Popup

# content_ = Button(text='ok')
content_image_saved = Button(text='ok')
content_image_saved_m = Button(text='ok')
content_hided_data = Button(text='ok')
content_wrong_format = Button(text='ok')
content_drafted_data = Button(text='ok')


# popup_ = Popup(title='xxx', content=content_, size_hint=(0.5, 0.2), auto_dismiss=False)
popup_image_saved = Popup(title='Image saved', content=content_image_saved, size_hint=(0.5, 0.2), auto_dismiss=False)
popup_image_saved_m = Popup(title='Image & mask saved', content=content_image_saved_m, size_hint=(0.5, 0.2), auto_dismiss=False)
popup_hided_data = Popup(title='Hided data', content=content_hided_data, size_hint=(0.5, 0.2), auto_dismiss=False)
popup_wrong_format = Popup(title='Wrong format', content=content_wrong_format, size_hint=(0.5, 0.2), auto_dismiss=False)
popup_drafted_data = Popup(title='Drafted data', content=content_drafted_data, size_hint=(0.5, 0.2), auto_dismiss=False)


# content_.bind(on_press=popup_.dismiss)
content_image_saved.bind(on_press=popup_image_saved.dismiss)
content_image_saved_m.bind(on_press=popup_image_saved_m.dismiss)
content_hided_data.bind(on_press=popup_hided_data.dismiss)
content_wrong_format.bind(on_press=popup_wrong_format.dismiss)
content_drafted_data.bind(on_press=popup_drafted_data.dismiss)






