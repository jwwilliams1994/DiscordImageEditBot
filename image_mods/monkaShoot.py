from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random

frameOffset = 5
framesTotal = 38
tTime = 5
rx, ry = (105/168),(58/112)

def processShootImage(emoPng,emojiId):
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
        alpha = img2.split()[3]
        img2 = img2.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
        img2.paste(255, mask)
        images.append(img2.crop((0,0,300,112)))
    images[0].save(emojiId+'Shoot.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2)
    return (str(emojiId)+'Shoot.gif')
