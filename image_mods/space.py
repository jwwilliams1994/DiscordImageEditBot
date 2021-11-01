from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random

def processSpaceImage(emoPng):
    images = []
    frames = 960-1
    img2 = Image.open('canvas.png').copy()
    # img2 = Image.new(mode="RGBA", size=(400, 400), color=(0, 0, 0, 0))
    frequency = 3
    frequency2 = 6
    xStart = []
    yStart = []
    dist = 100
    emoPng = emoPng.copy().convert('RGBA')
    for i in range(0, 4, 1):
        rotations = random.randint(0,360)*(math.pi/180)
        xStart.append(round(math.sin(rotations)*dist))
        yStart.append(round(math.cos(rotations)*dist))
    print(xStart)
    print(yStart)
    X = 0
    Y = 0
    stage = 0
    rotMul = 1
    interval = 240
    for i in range(0, frames, 1):
        if i == (interval):
            print('stage1')
            stage = 1
            X = 0
            Y = 0
        if i == (interval*2):
            print('stage2')
            stage = 2
            X = 0
            Y = 0
        if i == (interval*3):
            print('stage3')
            stage = 3
            X = 0
            Y = 0
            rotMul = 3
        canvas = Image.new(mode="RGBA", size=(400, 400), color=(0, 0, 0, 0))
        ratio = emoPng.height/emoPng.width
        if emoPng.width > 60:
            image = emoPng.copy().resize((60,round(60*ratio)), Image.BICUBIC)
        else:
            image = emoPng.copy().resize((60,round(60*ratio)), Image.NEAREST)
        image = image.rotate(i*1*rotMul, Image.BICUBIC, expand=1)
        xOff = round((60-image.width)/2)
        yOff = round(((60*ratio)-image.height)/2)
        if i == 50:
            print(image.width)
        ##the below static number is 400 minus width then divided by 2
        canvas.alpha_composite(image,(170+xStart[stage]+xOff,170+yStart[stage]+yOff))
##        X -= xStart[stage]*0.02
##        Y -= yStart[stage]*0.02
        X -= xStart[stage]*0.01
        Y -= yStart[stage]*0.01
        ##canvas.alpha_composite(image,(160,160))
        offsetX = round(X)
        offsetY = round(Y)
        image2 = ImageChops.offset(canvas,offsetX,offsetY)
        croppedImage = image2.crop((160,160,240,240))
        ##croppedImage = image2.crop((0,0,400,400))
        images.append(croppedImage)
    images.append(20)
    return images


def processSpaceGif(emoGif):
    images = []
    frames = 960-1
    img2 = Image.open('canvas.png')
    frequency = 3
    frequency2 = 6
    xStart = []
    yStart = []
    dist = 100
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    if type(gifDuration) is list:
        gifDuration = gifDuration[0]
    if gifDuration < 20:
        gifDuration = 100
    frame_ratio = 20/gifDuration
    for i in range(0, 4, 1):
        rotations = random.randint(0,360)*(math.pi/180)
        xStart.append(round(math.sin(rotations)*dist))
        yStart.append(round(math.cos(rotations)*dist))
    X = 0
    Y = 0
    stage = 0
    rotMul = 1
    interval = 240
    for i in range(0, frames, 1):
        #print(i)
        #print(frame_ratio)
        framePick = int(math.floor((i*frame_ratio)%totalFrames))
        emoPng = emoGif[framePick].copy().convert('RGBA')
        if i == (interval):
            #print('stage1')
            stage = 1
            X = 0
            Y = 0
        if i == (interval*2):
            #print('stage2')
            stage = 2
            X = 0
            Y = 0
        if i == (interval*3):
            #print('stage3')
            stage = 3
            X = 0
            Y = 0
            rotMul = 3
        canvas = Image.new(mode="RGBA", size=(400, 400), color=(0, 0, 0, 0))
        ratio = emoPng.height/emoPng.width
        if emoPng.width > 60:
            image = emoPng.copy().resize((60,round(60*ratio)), Image.BICUBIC)
        else:
            image = emoPng.copy().resize((60,round(60*ratio)), Image.NEAREST)
        image = image.rotate(i*1*rotMul, Image.BICUBIC, expand=1)
        xOff = round((60-image.width)/2)
        yOff = round(((60*ratio)-image.height)/2)
        if i == 50:
            print(image.width)
        ##the below static number is 400 minus width then divided by 2
        # canvas.alpha_composite(image,(170+xStart[stage]+xOff,170+yStart[stage]+yOff))
##        X -= xStart[stage]*0.02
##        Y -= yStart[stage]*0.02
        X -= xStart[stage]*0.01
        Y -= yStart[stage]*0.01
        ##canvas.alpha_composite(image,(160,160))
        offsetX = round(X)
        offsetY = round(Y)
        # image2 = ImageChops.offset(canvas,offsetX,offsetY)
        testX = 170 + xStart[stage] + xOff + offsetX
        testY = 170 + yStart[stage] + yOff + offsetY
        # print(testX,testY)
        if testX > 400:
            testX = 400
        if testX < 0:
            testX = 0
        if testY > 400:
            testY = 400
        if testY < 0:
            testY = 0
        canvas.alpha_composite(image, (testX, testY))
        image2 = canvas
        croppedImage = image2.crop((160,160,240,240))
        ##croppedImage = image2.crop((0,0,400,400))
        images.append(croppedImage)
    images.append(20)
    return images

