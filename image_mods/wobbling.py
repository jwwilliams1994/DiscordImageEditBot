import math

from PIL import Image, ImageChops, ImageOps

wMod = 1.5
def wobble(emoPng, fIn=60):
    width, height = emoPng.size
    emoPng = emoPng.convert('RGBA')
    canvas = Image.new('RGBA', (round(width*2), round(height*2)), (0, 0, 0, 0))
    # canv = Image.open('canvas.png').resize((round(width*2), round(height*2)))
    images = []
    wRangeMod = 0.1
    wRange = round(width * wRangeMod)
    fMax = fIn
    fMult = 360 / fMax
    for f in range(fMax):
        emoImg = emoPng.copy()
        canv = canvas.copy()
        xOff = (round(width*2)-width)/2
        yOff = (round(height*2)-height)/2
        xPos = round(math.sin(math.radians(f * fMult)) * wRange)
        Rot = (math.sin(math.radians(f * fMult + 90)) * 10)
        emoImg = emoImg.rotate(Rot, Image.BICUBIC, expand=1)
        wid, hig = emoImg.size
        xDif = (wid - width) / 2
        yDif = (hig - height) / 2
        canv.alpha_composite(emoImg, (round(xOff - xDif) + xPos, round(yOff - yDif)))
        nWid, nHit = canv.size
        # xOff2 = ((width * 1.2) - nWid)
        # yOff2 = ((height * 1.2) - nHit)
        xOff2 = (round(width*2)-width) / 2 * (1 / wMod)
        yOff2 = (round(height*2)-height) / 2 * (1 / wMod)
        canv = canv.crop((xOff2, yOff2, (nWid - xOff2), (nHit - yOff2)))
        images.append(canv)
    images.append(20)
    return images


def wobbleGif(emoGif, fIn, emojiId):
    width, height = emoGif[0].size
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    if type(gifDuration) is list:
        gifDuration = gifDuration[0]
    # emoPng = emoPng.convert('RGBA')
    canvas = Image.new('RGBA', (round(width * 2), round(height * 2)), (0, 0, 0, 0))
    # canv = Image.open('canvas.png').resize((round(width*2), round(height*2)))
    images = []
    wRangeMod = 0.1
    wRange = round(width * wRangeMod)
    fMax = totalFrames
    fMult = (360 / fMax) * fIn
    for f in range(fMax):
        emoPng = emoGif[f].convert('RGBA')
        emoImg = emoPng.copy()
        canv = canvas.copy()
        xOff = (round(width * 2) - width) / 2
        yOff = (round(height * 2) - height) / 2
        xPos = round(math.sin(math.radians(f * fMult)) * wRange)
        Rot = (math.sin(math.radians(f * fMult + 90)) * 10)
        emoImg = emoImg.rotate(Rot, Image.BICUBIC, expand=1)
        wid, hig = emoImg.size
        xDif = (wid - width) / 2
        yDif = (hig - height) / 2
        canv.alpha_composite(emoImg, (round(xOff - xDif) + xPos, round(yOff - yDif)))
        nWid, nHit = canv.size
        # xOff2 = ((width * 1.2) - nWid)
        # yOff2 = ((height * 1.2) - nHit)
        xOff2 = (round(width * 2) - width) / 2 * (1 / wMod)
        yOff2 = (round(height * 2) - height) / 2 * (1 / wMod)
        canv = canv.crop((xOff2, yOff2, (nWid - xOff2), (nHit - yOff2)))
        images.append(canv)
    images.append(gifDuration)
    return images


def shrink(emoPng, dur):
    images = []
    width, height = emoPng.size
    emoPng = emoPng.convert('RGBA')
    canvas = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    for f in range(dur):
        canv = canvas.copy()
        scale = (1/((f/40)+1))
        img = emoPng.copy()
        img = img.resize((round(width * scale), round(height * scale)))
        iwidth, iheight = img.size
        canv.alpha_composite(img, (round((width - iwidth) / 2), round((height - iheight) / 2)))
        img = canv
        images.append(img)
    images.append(20)
    return images

# img = Image.open('testem.png')
# shrink(img, 500, "88")