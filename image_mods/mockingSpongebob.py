from PIL import Image, ImageFilter, GifImagePlugin, ImageFont, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random
#54,259


def mockingSpongebob(inputText):
    marker = 0
    for i in range(len(inputText)):
        if random.randint(1,100) > 40:
            if inputText[i-3:i].upper() != inputText[i-3:i]:
                inputText = inputText[:i] + inputText[i].upper() + inputText[i+1:]
            else:
                inputText = inputText[:i] + inputText[i].lower() + inputText[i+1:]
        else:
            if inputText[i-3:i].lower() != inputText[i-3:i]:
                inputText = inputText[:i] + inputText[i].lower() + inputText[i+1:]
            else:
                inputText = inputText[:i] + inputText[i].upper() + inputText[i+1:]
    while True:
        if (marker+40) > len(inputText):
            break
        beginning = marker+40
        marker = inputText.rfind(" ", 0, beginning)
        if marker == -1:
            marker = 40
        inputText = inputText[:marker]+' \n'+inputText[marker:]
    myFont = ImageFont.truetype('font/whitney-semibold.otf',34)
    canvas = Image.open('canvas.png').resize((800,300))
    text_color = (255,255,255)
    shadow_color = (20,20,20)
    background = Image.open('spongebobTemplate.png').convert('RGBA')
    draw = ImageDraw.Draw(canvas)
    draw.multiline_text((0,0),inputText, font=myFont, fill=text_color, align='center', stroke_width=2, stroke_fill=shadow_color)
    xd, yd = draw.multiline_textsize(inputText, font=myFont, spacing=1)
    xoffset = round(350-(xd/2))
    if xoffset < 0:
        xoffset = 0
    if yd > 56:
        yoffset = -30
    else:
        yoffset = 0
    background.alpha_composite(canvas,(xoffset,yoffset+300))
    #background.alpha_composite(canvas,(54,259))
    return background

#mockingSpongebob("this is a test this is a test this is a test this is a test this is a test",1235)
