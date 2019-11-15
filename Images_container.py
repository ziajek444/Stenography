### Image containers ###
## image source ##
from kivy.uix.image import Image

from Operations import get_template_texture_buffer

img_source = Image(source='w3bw.bmp', size_hint=(2,2), pos_hint={'top': 1})
## image result1 ##
result_texture1 = get_template_texture_buffer(640, 480, case=1)
img_result1 = Image(texture=result_texture1, size_hint=(2, 2))
## image mask1 ##
mask_texture1 = get_template_texture_buffer(640, 480, case=2)
img_mask1 = Image(texture=mask_texture1, size_hint=(2, 2))