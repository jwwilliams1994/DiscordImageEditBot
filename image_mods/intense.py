from PIL import Image, ImageFilter, GifImagePlugin, ImageFont, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random


def intensifytext(inputText, red, green, blue, intensity, emojiId):
    print(inputText, red, green, blue, intensity, emojiId)
    myFont = ImageFont.truetype('font/whitney-semibold.otf', 30)
    marker = 0
    if inputText == "BeeMovie ":
        myFont = ImageFont.truetype('font/whitney-semibold.otf', 7)
        print("opening file")
        text_file = open("movieScript.txt", "r")
        text_info = text_file.read()
        print(len(text_info))
        text_file.close()
        inputText = text_info
    # loopT = round(len(inputText)/100)+8
    while True:
        print('loop...')
        if (marker + 100) > len(inputText):
            print("broke at ", marker)
            break
        beginning = marker + 100
        marker = inputText.rfind(" ", 0, beginning)
        if marker == -1:
            marker = 100
        print(marker)
        inputText = inputText[:marker] + ' \n' + inputText[marker:]
        # print(inputText)
    inputText = inputText + '\n'
    canv = Image.open('canvas.png').resize((1400, 7000))
    d1 = ImageDraw.Draw(canv)
    d1.multiline_text((0, 0), inputText, font=myFont, fill=(red, green, blue), align='center', spacing=1)
    xd, yd = d1.multiline_textsize(inputText, font=myFont, spacing=1)
    if yd > 7000:
        yd = 7000
    ##xd, yd = myFont.getsize(inputText)
    canv = canv.crop((0, 0, xd, yd))
    images = []
    frames = 12 - 1
    frequency = 4
    frequency2 = 3
    canvas = Image.open('canvas.png').resize((xd + 50, yd + 50))
    for i in range(0, frames, 1):
        image = canv
        canvas.paste(image)
        image = canvas
        offsetX = round(math.sin(((2 * math.pi) / frequency2) * (i - frequency2))) * intensity
        offsetY = round(math.sin(((2 * math.pi) / frequency) * (i - frequency))) * intensity
        image2 = ImageChops.offset(image, offsetX, offsetY)
        croppedImage = image2.crop((0, 0, xd, (yd + -20)))
        alpha = croppedImage.split()[3]
        croppedImage = croppedImage.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        croppedImage.paste(255, mask)
        images.append(croppedImage)
    images[0].save(emojiId + 'intense.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2)
    return (emojiId + 'intense.gif')
