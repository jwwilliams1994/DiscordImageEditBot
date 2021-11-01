from PIL import Image, ImageFilter, GifImagePlugin, ImageFont, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random


def intensifytext(inputText="pock is ho", red=255, green=255, blue=255, intensity=4):
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
    if intensity > 0:
        for i in range(0, frames, 1):
            image = canv
            canvas.paste(image)
            image = canvas
            offsetX = round(math.sin(((2 * math.pi) / frequency2) * (i - frequency2))) * intensity
            offsetY = round(math.sin(((2 * math.pi) / frequency) * (i - frequency))) * intensity
            image2 = ImageChops.offset(image, offsetX, offsetY)
            croppedImage = image2.crop((0, 0, xd, (yd + -20)))
            images.append(croppedImage)
        images.append(20)
        return images
    else:
        image = canv
        canvas.paste(image)
        image = canvas
        croppedImage = image.crop((0, 0, xd, (yd + -20)))
        return croppedImage


import datetime
def gettime():
    d = datetime.datetime.now(datetime.timezone.utc)
    print(d.hour, d.minute, d.second)
    hours = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]
    minutesten = ["O\'", "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    minutesone = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    minutesteen = ["", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    if d.hour > 12 + 5:
        first = hours[d.hour - 12 - 6]
    else:
        first = hours[d.hour - 6]
    if d.minute < 11 or d.minute > 19:
        if d.minute >= 10:
            if str(d.minute)[1] != "0":
                second = minutesten[int(str(d.minute)[0])] + "-" + minutesone[int(str(d.minute)[1])]
            else:
                second = minutesten[int(str(d.minute)[0])]
        else:
            second = "O\'" + minutesone[d.minute]
    else:
        second = minutesteen[d.minute - 10]
    if d.second < 11 or d.second > 19:
        if d.second >= 10:
            if str(d.second)[1] != "0":
                third = minutesten[int(str(d.second)[0])] + "-" + minutesone[int(str(d.second)[1])]
            else:
                third = minutesten[int(str(d.second)[0])]
        else:
            third = minutesone[d.second]
    else:
        third = minutesteen[d.second - 10]
    string = "The time is: " + first + " " + second + " and " + third + " seconds."
    # string = "The time is: Four Twenty and " + third + " seconds."
    return string


from math import floor
def marqueetext(input="time", red=255, green=255, blue=255, speed=2):
    weed = False
    if input == "time":
        input = gettime()
        if input[:24] == "The time is: Four Twenty":
            weed = True
    myFont = ImageFont.truetype('font/visitor2.ttf', 13)
    xd, yd = myFont.getsize(input)
    print(xd, yd)
    canv = Image.new('RGBA', (xd+140, yd+3), (0, 0, 0, 255))
    if weed:
        hcjGrip = Image.open("hcjGrip.png")
        canv.alpha_composite(hcjGrip, (xd + 60 + 1, 0))
    d1 = ImageDraw.Draw(canv)
    d1.multiline_text((60, 0), input, font=myFont, fill=(red, green, blue), align='center', spacing=1)
    totalFrames = (xd + 80) / speed
    images = []
    print(totalFrames, speed)
    for f in range(round(totalFrames)):
        image = ImageChops.offset(canv, floor(speed * -f), 0)
        croppedImage = image.crop((0, 0, 60, 11))
        # alpha = croppedImage.split()[3]
        # croppedImage = croppedImage.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        # mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        # croppedImage.paste(255, mask)
        images.append(croppedImage)
    images.append(20)
    return images
