import PIL
from PIL import Image


print("hello there")



img = Image.open('w3bw.bmp')
#img = Image.open('falkowicz.jpg')
pixels = img.load()


RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

wspR = 1
wspG = 1
wspB = 1

pxAmount = img.size[0] * img.size[1]

for i in range(img.size[0]):
    for j in range(img.size[1]):
        (r,g,b) = pixels[i,j]

        if(g+b < r*1.5):
            wspR+=1
        elif(b+r < g*1.5):
            wspG+=1
        elif(r+g < b*1.5):
            wspB+=1
        else:
            pass

wspR = 64 - ((wspR / pxAmount) * 255)
wspG = 64 - ((wspG / pxAmount) * 255)
wspB = 64 - ((wspB / pxAmount) * 255)
print(wspR,wspG,wspB)


for i in range(img.size[0]):
    for j in range(img.size[1]):
        (r,g,b) = pixels[i,j]


        if(g+b < r+wspR):
            pixels[i,j] = RED
        elif(b+r < g+wspG):
            pixels[i,j] = GREEN
        elif(r+g < b+wspB):
            pixels[i,j] = BLUE
        else:
            pixels[i,j] = (r,g,b)            


print("hello there")
img.show()
img.close()
print("hello there")
