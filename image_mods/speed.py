from PIL import Image, ImageFilter, GifImagePlugin, ImageFont, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random


pause_for = [',', ';', ':', '.', '-', '~', '?', '!']


def speedtext(inputText="pock is ho", red=255, green=255, blue=255, intensity=100, pauses=True, mult=2):
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
    dur_arr = []
    images = []
    for i in range(len(listy)):
        if pauses:
            if listy[i][-1] in pause_for or listy[i] == listy[-1]:
                dur_arr.append(round(intensity * mult))
            else:
                dur_arr.append(intensity)
        else:
            dur_arr.append(intensity)
        canvas2 = canvas.copy()
        canv = Image.open('canvas.png').resize((xd, yd))
        d1 = ImageDraw.Draw(canv)
        d1.multiline_text((0, 0), listy[i], font=myFont, fill=(red, green, blue), align='center', spacing=1)
        xd2, yd2 = myFont.getsize(listy[i])
        offset = round((xd - xd2) / 2)
        canvas2.paste(canv, (offset, 0))
        croppedImage = canvas2
        images.append(croppedImage)
    images.append(dur_arr)
    return images
