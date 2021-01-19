import math

from PIL import Image, ImageChops, ImageOps

wMod = 1.5
def wobble(emoPng, fIn, emojiId):
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
        alpha = canv.split()[3]
        canv = canv.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canv.paste(255, mask)
        images.append(canv)
    images[0].save(str(emojiId) + 'wobble.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'wobble.gif'

def wobbleGif(emoGif, fIn, emojiId):
    width, height = emoGif.size
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    # emoPng = emoPng.convert('RGBA')
    canvas = Image.new('RGBA', (round(width * 2), round(height * 2)), (0, 0, 0, 0))
    # canv = Image.open('canvas.png').resize((round(width*2), round(height*2)))
    images = []
    wRangeMod = 0.1
    wRange = round(width * wRangeMod)
    fMax = totalFrames
    fMult = (360 / fMax) * fIn
    for f in range(fMax):
        emoGif.seek(f)
        emoPng = emoGif.convert('RGBA')
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
        alpha = canv.split()[3]
        canv = canv.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canv.paste(255, mask)
        images.append(canv)
    images[0].save(str(emojiId) + 'wobble.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'wobble.gif'


def shrink(emoPng, dur, emojiId):
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
        alpha = img.split()[3]
        img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        img.paste(255, mask)
        images.append(img)
    images[0].save(str(emojiId) + 'shrink.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'shrink.gif'

# img = Image.open('testem.png')
# shrink(img, 500, "88")