from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random

frameOffset = 5
framesTotal = 38
tTime = 5
rx, ry = (105/168),(58/112)


def processShootImage(emoPng):
    images = []
    bullArr = []
    gun = Image.open('monkaShoot5.gif')
    ratio = emoPng.height/emoPng.width
    emg = emoPng.convert('RGBA').resize((30,round(30*ratio)),Image.LANCZOS)
    img = Image.open('canvas.png').resize((700,112))
    for i in range(0,framesTotal):
        img2 = img.copy()
        foff = ((i+frameOffset)%9) #starts at offset
        gun.seek(foff)
        for x in bullArr:
            x[0] += 20
            x[1] -= 1.6
            img2.alpha_composite(emg,(round(x[0]),round(x[1])))
            if x[0] > 350:
                bullArr.remove(x)
        if foff == tTime:
            bullArr.append([round(rx*168)-20,round(ry*112)-18])
        img2.alpha_composite(gun.convert('RGBA').resize((168,112),Image.LANCZOS))
        images.append(img2.crop((0,0,300,112)))
    images.append(20)
    return images
