from PIL import Image, ImageFilter, GifImagePlugin, ImageFont, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random


def speedtext(inputText, red, green, blue, intensity, emojiId):
    intensity = round(intensity) * 10
    if intensity < 20:
        intensity = 20
    if intensity > 500:
        intensity = 500
    myFont = ImageFont.truetype('font/whitney-semibold.otf', 30)
    listy = inputText.split(" ")
    largestWord = max(listy, key=len)
    xd, yd = myFont.getsize(largestWord)
    print(xd, yd, largestWord)
    # canv = Image.open('canvas.png').resize((1400,1400))
    # canv = canv.crop((0,0,xd,yd))
    canvas = Image.open('canvas.png').resize((xd, yd))
    images = []
    for i in range(len(listy)):
        canvas2 = canvas.copy()
        canv = Image.open('canvas.png').resize((xd, yd))
        d1 = ImageDraw.Draw(canv)
        d1.multiline_text((0, 0), listy[i], font=myFont, fill=(red, green, blue), align='center', spacing=1)
        xd2, yd2 = myFont.getsize(listy[i])
        offset = round((xd - xd2) / 2)
        canvas2.paste(canv, (offset, 0))
        croppedImage = canvas2
        alpha = croppedImage.split()[3]
        croppedImage = croppedImage.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        croppedImage.paste(255, mask)
        images.append(croppedImage)
    images[0].save(emojiId + 'speed.gif', save_all=True, append_images=images[1:], duration=intensity, loop=0, optimize=False, transparency=255, disposal=2)
    return (emojiId + 'speed.gif')
