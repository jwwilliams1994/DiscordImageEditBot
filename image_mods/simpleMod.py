import math, datetime
import colorsys
from PIL import Image, ImageOps
import requests, io


def rotateImg(emoImg, rot, emojiId):
    emoImg = emoImg.convert("RGBA").rotate(-rot, Image.BICUBIC, expand=1)
    emoImg.save("{0}rotated.png".format(str(emojiId)))
    return "{0}rotated.png".format(str(emojiId))


def rotateGif(emoGif, rot, emojiId):
    images = []
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    for f in range(0, totalFrames):
        emoGif.seek(f)
        emoImg = emoGif.copy()
        emoImg = emoImg.convert("RGBA").rotate(-rot, Image.BICUBIC, expand=1)
        alpha = emoImg.split()[3]
        emoImg = emoImg.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        emoImg.paste(255, mask)
        images.append(emoImg)
    images[0].save(str(emojiId) + 'rotated.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'rotated.gif'


def flipImg(emoImg, emojiId):
    emoImg = emoImg.convert("RGBA").transpose(method=Image.FLIP_LEFT_RIGHT)
    emoImg.save("{0}flip.png".format(str(emojiId)))
    return "{0}flip.png".format(str(emojiId))


def flipGif(emoGif, emojiId):
    images = []
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    for f in range(0, totalFrames):
        emoGif.seek(f)
        emoImg = emoGif.copy()
        emoImg = emoImg.convert("RGBA").transpose(method=Image.FLIP_LEFT_RIGHT)
        alpha = emoImg.split()[3]
        emoImg = emoImg.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        emoImg.paste(255, mask)
        images.append(emoImg)
    images[0].save(str(emojiId) + 'flip.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'flip.gif'


def hyperImg(emoImg, input, emojiId):
    images = []
    side = False
    gifDuration = (input + 1) * 10
    for f in range(0, 2):
        img = emoImg.copy().convert("RGBA")
        if f % 2 == 1:
            img = img.transpose(method=Image.FLIP_LEFT_RIGHT)
        alpha = img.split()[3]
        img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        img.paste(255, mask)
        images.append(img)
    images[0].save(str(emojiId) + 'hyper.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return (str(emojiId) + 'hyper.gif')


def hyperGif(emoGif, input, emojiId):
    images = []
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    if gifDuration < 20:
        gifDuration = 20
    frame_ratio = 20 / gifDuration
    realFrames = round(totalFrames * (1 / frame_ratio))
    side = False
    mod = input + 1
    for f in range(0, realFrames):
        framePick = int(math.floor((f * frame_ratio) % totalFrames))
        emoGif.seek(framePick)
        img = emoGif.copy().convert("RGBA")
        if f % mod == 0:
            print(f, side)
            if side:
                side = False
            else:
                side = True
        if side:
            img = img.transpose(method=Image.FLIP_LEFT_RIGHT)
        alpha = img.split()[3]
        img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        img.paste(255, mask)
        images.append(img)
    images[0].save(str(emojiId) + 'hyper.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255, disposal=2,
                   interlace=False)
    return (str(emojiId) + 'hyper.gif')


def widen(emoPng, emojiId):
    width, height = emoPng.size
    emoPng = emoPng.resize((width * 4, height), Image.NEAREST)
    emoPng.save(str(emojiId) + "wide.png")
    return str(emojiId) + "wide.png"


def widenGif(emoGif, emojiId):
    width, height = emoGif.size
    images = []
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    for f in range(totalFrames):
        emoGif.seek(f)
        emoPng = emoGif.copy().convert('RGBA').resize((width * 4, height), Image.NEAREST)
        # emoPng.resize((width*4, height), Image.NEAREST)
        alpha = emoPng.split()[3]
        emoPng = emoPng.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        emoPng.paste(255, mask)
        images.append(emoPng)
    images[0].save(str(emojiId) + 'wide.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'wide.gif'


def resize(emoPng, sm, emojiId):
    width, height = emoPng.size
    wratio = width / height
    hratio = height / width
    if height < width:
        emoPng = emoPng.resize((round(sm * wratio), sm), Image.LANCZOS)
    if width < height:
        emoPng = emoPng.resize((sm, round(sm * hratio)), Image.LANCZOS)
    if height == width:
        emoPng = emoPng.resize((sm, sm), Image.LANCZOS)
    emoPng.save(str(emojiId) + "resize.png")
    return str(emojiId) + "resize.png"


def resizeGif(emoGif, sm, emojiId):
    width, height = emoGif.size
    wratio = width / height
    hratio = height / width
    images = []
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    for f in range(totalFrames):
        emoGif.seek(f)
        emoPng = emoGif.copy().convert('RGBA')
        if height < width:
            emoPng = emoPng.resize((round(sm * wratio), sm), Image.LANCZOS)
        if width < height:
            emoPng = emoPng.resize((sm, round(sm * hratio)), Image.LANCZOS)
        if height == width:
            emoPng = emoPng.resize((sm, sm), Image.LANCZOS)
        alpha = emoPng.split()[3]
        emoPng = emoPng.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        emoPng.paste(255, mask)
        images.append(emoPng)
    images[0].save(str(emojiId) + 'resize.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'resize.gif'


def crop(emoPng, off, emojiId):
    if off >= 1 or off <= 0:
        return "for crop, input float between 0 and 1"
    width, height = emoPng.size
    xOff = round((width * off) / 2)
    yOff = round((height * off) / 2)
    emoPng = emoPng.crop((xOff, yOff, (width - xOff), (height - yOff)))
    emoPng.save(str(emojiId) + "crop.png")
    return str(emojiId) + "crop.png"


def cropGif(emoGif, off, emojiId):
    if off >= 1 or off <= 0:
        return "for crop, input float between 0 and 1"
    width, height = emoGif.size
    xOff = round((width * off) / 2)
    yOff = round((height * off) / 2)
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    images = []
    for f in range(totalFrames):
        emoGif.seek(f)
        emoPng = emoGif.copy().convert('RGBA')
        emoPng = emoPng.crop((xOff, yOff, (width - xOff), (height - yOff)))
        alpha = emoPng.split()[3]
        emoPng = emoPng.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        emoPng.paste(255, mask)
        images.append(emoPng)
    images[0].save(str(emojiId) + 'crop.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'crop.gif'


def grabImage(urll):  # if you direct link to a png/gif/etc, it will directly return it as a bytestream of the image
    r = requests.get(urll, allow_redirects=True)
    r.close()
    return io.BytesIO(r.content)


def exists(path):  # checks if url exists
    r = requests.head(path)
    return r.status_code == requests.codes.ok


def getUrl(text, emojiId):
    image = Image.open(grabImage(text))
    append = text[-4:]
    print(append)
    if append != ".gif":
        image.convert('RGBA').save(str(emojiId) + "url" + '.png')
        return str(emojiId) + "url" + '.png'
    else:
        totalFrames = image.n_frames
        gifDuration = image.info['duration']
        images = []
        for f in range(totalFrames):
            image.seek(f)
            emoPng = image.copy().convert('RGBA')
            alpha = emoPng.split()[3]
            emoPng = emoPng.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
            mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            emoPng.paste(255, mask)
            images.append(emoPng)
        images[0].save(str(emojiId) + 'grab.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                       disposal=2)
        return str(emojiId) + 'grab.gif'


def transparency(emoPng, arg, emojiId):
    emoPng = emoPng.convert("RGBA")
    width, height = emoPng.size
    lod = emoPng.load()
    for x in range(width):
        for y in range(height):
            r, g, b, a = lod[x, y]
            a = round(a * arg)
            lod[x, y] = (r, g, b, a)
            # lod[x, y][3] = round(lod[x, y][3] * arg)
    emoPng.save(str(emojiId) + "trans.png")
    return str(emojiId) + "trans.png"


def transparencyGif(emoGif, arg, emojiId):
    return "gifs don't support transparency, dummy"


def thinking(emoPng, xIn, yIn, scale, emojiId):
    width, height = emoPng.size
    emoPng = emoPng.convert('RGBA')
    fing = Image.open("thinkingfinger.png").convert("RGBA")
    fwidth, fheight = fing.size
    if width > height:
        fing = fing.resize((round(height * scale), round(height * scale)), Image.LANCZOS)
        xOff = round((width - height) / 2)
        yOff = 0
    if width < height:
        fing = fing.resize((round(width * scale), round(width * scale)), Image.LANCZOS)
        yOff = round((height - width) / 2)
        xOff = 0
    if width == height:
        fing = fing.resize((round(width * scale), round(height * scale)), Image.LANCZOS)
        xOff = 0
        yOff = 0
    print(xOff, yOff, fing.size)
    fwidth, fheight = fing.size
    xDif = width - fwidth
    yDif = height - fheight
    emoPng.alpha_composite(fing, (0 + xIn, 0 + yDif - yIn))
    emoPng.save(str(emojiId) + "thinking.png")
    return str(emojiId) + "thinking.png"


def thinkingGif(emoGif, xIn, yIn, scale, emojiId):
    width, height = emoGif.size
    emoPng = emoGif.convert('RGBA')
    fing = Image.open("thinkingfinger.png")
    if width > height:
        fing = fing.resize((round(height * scale), round(height * scale)), Image.LANCZOS)
        xOff = round((width - height) / 2)
        yOff = 0
    if width < height:
        fing = fing.resize((round(width * scale), round(width * scale)), Image.LANCZOS)
        yOff = round((height - width) / 2)
        xOff = 0
    if width == height:
        fing = fing.resize((round(width * scale), round(height * scale)), Image.LANCZOS)
        xOff = 0
        yOff = 0
    fwidth, fheight = fing.size
    xDif = width - fwidth
    yDif = height - fheight
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    images = []
    for f in range(totalFrames):
        emoGif.seek(f)
        emoPng = emoGif.copy().convert("RGBA")
        finger = fing.copy()
        emoPng.alpha_composite(fing, (0 + xIn, 0 + yDif - yIn))
        alpha = emoPng.split()[3]
        emoPng = emoPng.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        emoPng.paste(255, mask)
        images.append(emoPng)
    images[0].save(str(emojiId) + 'thinking.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + "thinking.gif"


def information(emoImg, emojiId):
    x, y = emoImg.size
    stringy = "Image dimensions are: " + str(x) + " " + str(y)
    return stringy


def information2(emoGif, emojiId):
    x, y = emoGif.size
    info = emoGif.info
    totalFrames = emoGif.n_frames
    stringy = "Image dimensions are: " + str(x) + " " + str(y) + "\n" + "Number of frames: " + str(totalFrames) + "\n" + "Other info: " + str(info)
    return stringy


def save(emoPng, emojiId):
    emoPng.save(str(emojiId) + "save.png")
    return "Image saved as " + str(emojiId) + "save.png\nInsert filename.png instead of emoji to use, file will be deleted afterwards."


def saveGif(emoGif, emojiId):
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    images = []
    for f in range(totalFrames):
        emoGif.seek(f)
        emoPng = emoGif.copy().convert('RGBA')
        alpha = emoPng.split()[3]
        emoPng = emoPng.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        emoPng.paste(255, mask)
        images.append(emoPng)
    images[0].save(str(emojiId) + 'save.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    # emoPng.save(str(emojiId) + "save.gif")
    return "Image saved as " + str(emojiId) + "save.gif\nInsert filename.gif instead of emoji to use, file will be deleted afterwards."


def append(emoGif, endGif, emojiId):
    return "idk what you're trying to accomplish here"


def appendGif(emoGif, endGif, emojiId):
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    images = []
    for f in range(totalFrames):
        emoGif.seek(f)
        emoPng = emoGif.copy().convert('RGBA')
        alpha = emoPng.split()[3]
        emoPng = emoPng.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        emoPng.paste(255, mask)
        images.append(emoPng)
    totalFrames2 = endGif.n_frames
    width, height = emoGif.size
    wratio = width / height
    width2, height2 = endGif.size
    width3 = round(height2 * wratio)
    xOff = round((width2 - width3) / 2)
    print(width, height, width2, height2, xOff, width3)
    for f in range(totalFrames2):
        endGif.seek(f)
        emoPng = endGif.copy().convert('RGBA')
        emoPng = emoPng.crop((xOff, 0, xOff + width3, height2)).resize((width, height), Image.LANCZOS)
        alpha = emoPng.split()[3]
        emoPng = emoPng.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        emoPng.paste(255, mask)
        images.append(emoPng)
    images[0].save(str(emojiId) + 'append.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'append.gif'


def areyousure(emoPng, emojiId):
    gif = Image.open("johncena.gif")
    totalFrames = gif.n_frames
    gifDuration = gif.info['duration']
    images = []
    width, height = emoPng.size
    width2, height2 = gif.size
    wratio2 = width2 / height2
    hratio2 = height2 / width2
    if height2 > height:
        width2 = round(height * wratio2)
        height2 = height
    if width2 > width:
        height2 = round(width * hratio2)
        width2 = width
    xoff = round((width - width2) / 2)
    yoff = round((height - height2) / 2)
    for f in range(totalFrames):
        gif.seek(f)
        top = gif.copy().convert('RGBA').resize((width2, height2), Image.LANCZOS)
        tl = top.load()
        for x in range(width2):
            for y in range(height2):
                r, g, b, a = tl[x, y]
                if r < (g - 60) and b < (g - 60):
                    tl[x, y] = (0, 0, 0, 0)
        bottom = emoPng.copy().convert('RGBA')
        bottom.alpha_composite(top, (xoff, yoff))
        alpha = bottom.split()[3]
        bottom = bottom.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        bottom.paste(255, mask)
        images.append(bottom)
    images[0].save(str(emojiId) + 'areyousure.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'areyousure.gif'


def justdoit(emoPng, emojiId):
    gif = Image.open("justdoit.gif")
    totalFrames = gif.n_frames
    gifDuration = gif.info['duration']
    images = []
    width, height = emoPng.size
    width2, height2 = gif.size
    wratio2 = width2 / height2
    hratio2 = height2 / width2
    if height2 > height:
        width2 = round(height * wratio2)
        height2 = height
    if width2 > width:
        height2 = round(width * hratio2)
        width2 = width
    xoff = round((width - width2) / 2)
    yoff = round((height - height2))
    for f in range(totalFrames):
        gif.seek(f)
        top = gif.copy().convert('RGBA').resize((width2, height2), Image.LANCZOS)
        tl = top.load()
        for x in range(width2):
            for y in range(height2):
                r, g, b, a = tl[x, y]
                if r < (g - 30) and b < (g - 30):
                    tl[x, y] = (0, 0, 0, 0)
        bottom = emoPng.copy().convert('RGBA')
        bottom.alpha_composite(top, (xoff, yoff))
        alpha = bottom.split()[3]
        bottom = bottom.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        bottom.paste(255, mask)
        images.append(bottom)
    images[0].save(str(emojiId) + 'areyousure.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'areyousure.gif'


def couch(emoPng, emojiId):
    gif = Image.open("escapecouch.gif")
    totalFrames = gif.n_frames
    gifDuration = gif.info['duration']
    images = []
    width, height = emoPng.size
    width2, height2 = gif.size
    wratio2 = width2 / height2
    hratio2 = height2 / width2
    if height2 > height:
        width2 = round(height * wratio2)
        height2 = height
    if width2 > width:
        height2 = round(width * hratio2)
        width2 = width
    xoff = round((width - width2) / 2)
    yoff = round((height - height2) / 2)
    for f in range(-60, totalFrames, 1):
        bottom = emoPng.copy().convert('RGBA')
        if f >= 0:
            gif.seek(f)
            top = gif.copy().convert('RGBA').resize((width2, height2), Image.LANCZOS)
            tl = top.load()
            for x in range(width2):
                for y in range(height2):
                    r, g, b, a = tl[x, y]
                    if r < (g - 30) and b < (g - 30):
                        tl[x, y] = (0, 0, 0, 0)
            bottom.alpha_composite(top, (xoff, yoff))
        alpha = bottom.split()[3]
        bottom = bottom.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        bottom.paste(255, mask)
        images.append(bottom)
    images[0].save(str(emojiId) + 'areyousure.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'areyousure.gif'


def manydoors(emoPng, emojiId):
    gif = Image.open("manydoors.gif")
    totalFrames = gif.n_frames
    gifDuration = gif.info['duration']
    images = []
    width, height = emoPng.size
    width2, height2 = gif.size
    wratio2 = width2 / height2
    hratio2 = height2 / width2
    if height2 > height:
        width2 = round(height * wratio2)
        height2 = height
    if width2 > width:
        height2 = round(width * hratio2)
        width2 = width
    xoff = round((width - width2) / 2)
    yoff = round((height - height2) / 2)
    for f in range(-30, totalFrames, 1):
        bottom = emoPng.copy().convert('RGBA')
        if f >= 0:
            gif.seek(f)
            top = gif.copy().convert('RGBA').resize((width2, height2), Image.LANCZOS)
            tl = top.load()
            for x in range(width2):
                for y in range(height2):
                    r, g, b, a = tl[x, y]
                    if r < (g - 30) and b < (g - 30):
                        tl[x, y] = (0, 0, 0, 0)
            bottom.alpha_composite(top, (xoff, yoff))
        alpha = bottom.split()[3]
        bottom = bottom.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        bottom.paste(255, mask)
        images.append(bottom)
    images[0].save(str(emojiId) + 'areyousure.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'areyousure.gif'


import random


def masked(imag2, r1, g1, b1, h2, a2, p1, p2, p3):
    imag = imag2.copy().convert('RGBA')
    width, height = imag.size
    data = imag.load()
    for x in range(width):
        for y in range(height):
            r, g, b, a = data[x, y]
            if a == 0:
                continue
            h, s, v = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            h3, s3, v3 = colorsys.rgb_to_hls(r1 / 255, g1 / 255, b1 / 255)
            if (abs(h3 - h) < (p1 / 100) or abs(h3 - h) > ((100 - p1) / 100)) and abs(s3 - s) < (p2 / 100) and abs(v3 - v) < (p3 / 100):
                rr, gg, bb = colorsys.hls_to_rgb((h2 / 360), s, v)
                if a2 == 255:
                    data[x, y] = round(rr * 255), round(gg * 255), round(bb * 255), a
                else:
                    data[x, y] = round(rr * 255), round(gg * 255), round(bb * 255), a2
    return imag


def maskingPng(emoPng, r1, g1, b1, h2, p1, p2, p3, emojiId):
    img = emoPng.convert("RGBA")
    img = masked(img, r1, g1, b1, h2, 255, p1, p2, p3)
    img.save(str(emojiId) + 'masked.png')
    return str(emojiId) + 'masked.png'


def maskingGif(emoGif, r1, g1, b1, h2, p1, p2, p3, emojiId):
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    images = []
    for f in range(totalFrames):
        emoGif.seek(f)
        img2 = emoGif.copy().convert('RGBA')
        img = masked(img2, r1, g1, b1, h2, 255, p1, p2, p3)
        alpha = img.split()[3]
        img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        img.paste(255, mask)
        images.append(img)
    images[0].save(str(emojiId) + 'masking.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'masking.gif'


def maskingPng2(emoPng, r1, g1, b1, ft, p1, p2, p3, emojiId):
    images = []
    img2 = emoPng.convert("RGBA")
    for f in range(ft):
        h2 = (f / ft) * 360
        img = masked(img2, r1, g1, b1, h2, 255, p1, p2, p3)
        alpha = img.split()[3]
        img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        img.paste(255, mask)
        images.append(img)
    images[0].save(str(emojiId) + 'masking.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'masking.gif'


def maskingGif2(emoGif, r1, g1, b1, n, p1, p2, p3, emojiId):
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    images = []
    for f in range(totalFrames):
        emoGif.seek(f)
        img2 = emoGif.copy().convert('RGBA')
        h2 = ((f * n) / totalFrames) * 360
        img = masked(img2, r1, g1, b1, h2, 255, p1, p2, p3)
        alpha = img.split()[3]
        img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        img.paste(255, mask)
        images.append(img)
    images[0].save(str(emojiId) + 'masking.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'masking.gif'


def masked2(imag, imag2, r1, g1, b1, p1, p2, p3):
    width, height = imag.size
    data = imag.load()
    data2 = imag2.load()
    for x in range(width):
        for y in range(height):
            r, g, b, a = data[x, y]
            if a == 0:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            h3, s3, v3 = colorsys.rgb_to_hsv(r1 / 255, g1 / 255, b1 / 255)
            if (abs(h3 - h) < (p1 / 100) or abs(h3 - h) > ((100 - p1) / 100)) and abs(s3 - s) < (p2 / 100) and abs(v3 - v) < (p3 / 100):
                if data2[x, y][3] < 128:
                    # data[x, y] = data2[x, y]
                    pass
                else:
                    ar, ge, be, ay = data2[x, y]
                    data[x, y] = (ar, ge, be, 255)
    return imag


def maskingOne(emoImg1, emoImg2, r1, g1, b1, p1, p2, p3, emojiId):
    # img1 = emoPng1.convert('RGBA')
    # img2 = emoPng2.convert('RGBA')
    width, height = emoImg1.size
    width2, height2 = emoImg2.size
    gif1, gif2 = False, False
    totalFrames = 0
    try:
        gifDuration = emoImg1.info['duration']
        totalFrames = emoImg1.n_frames
        gif1 = True
    except:
        gif1 = False
    try:
        gifDuration = emoImg2.info['duration']
        totalFrames = emoImg2.n_frames
        gif2 = True
    except:
        gif2 = False
    # if emoImg1.info != {}:
    #     totalFrames = emoImg1.n_frames
    #     gifDuration = emoImg1.info['duration']
    #     gif1 = True
    # if emoImg2.info != {}:
    #     totalFrames = emoImg2.n_frames
    #     gifDuration = emoImg2.info['duration']
    #     gif2 = True
    if gif1 and gif2:
        return "wrong, idiot"
    # so if 1 and 2 are both pngs, this is simple; use modified mask and output the single mixed image
    # if 1 nand 2 are gifs, processing depends on order, but the first should be the frame and the second should be the inlaid
    # in this second instance, we know which is a gif already and can choose how to handle this easily provided we don't be stupid
    # the first input image should be used as the reference size, and the second should be sized up so the inner edges touch?
    print(gif1, gif2, totalFrames)
    if gif1 or gif2:  # if one input is a gif, this'll need a loop of frames
        images = []
        for f in range(totalFrames):
            if gif1:
                emoImg1.seek(f)
                img1 = emoImg1.copy().convert('RGBA')
                img2 = emoImg2.convert('RGBA')
            elif gif2:
                emoImg2.seek(f)
                img2 = emoImg2.copy().convert('RGBA')
                img1 = emoImg1.convert('RGBA')
            # so we have an image from both 1 and 2, regardless of if they're gifs... we need to match their sizes up to the 1st
            wratio1 = height / width
            wratio2 = height2 / width2
            if wratio1 > wratio2:  # so if 1 is skinnier tall than 2..., we'll be matching height and cutting sides off 2
                # print("wide")
                width3 = round((width2 / height2) * height)
                img2 = img2.resize((width3, height), Image.LANCZOS).crop((round((width3 - width) / 2), 0, width + round((width3 - width) / 2), height))
            elif wratio2 > wratio1:
                # print("tall")
                height3 = round((height2 / width2) * width)
                img2 = img2.resize((width, height3), Image.LANCZOS).crop((0, round((height3 - height) / 2), width, height + round((height3 - height) / 2)))
            elif wratio2 == wratio1:
                # print("square")
                img2 = img2.resize((width, height), Image.LANCZOS)
            out = masked2(img1, img2, r1, g1, b1, p1, p2, p3)
            alpha = out.split()[3]
            out = out.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
            mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            out.paste(255, mask)
            images.append(out)
        images[0].save(str(emojiId) + 'masking.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                       disposal=2)
        return str(emojiId) + 'masking.gif'
    else:  # combine just the two images
        img1 = emoImg1.convert('RGBA')
        img2 = emoImg2.convert('RGBA')
        wratio1 = height / width
        wratio2 = height2 / width2
        if wratio1 > wratio2:  # so if 1 is skinnier tall than 2..., we'll be matching height and cutting sides off 2
            print("wide")
            width3 = round((width2 / height2) * height)
            img2 = img2.resize((width3, height), Image.LANCZOS).crop((round((width3 - width) / 2), 0, width + round((width3 - width) / 2), height))
        elif wratio2 > wratio1:
            print("tall")
            height3 = round((height2 / width2) * width)
            img2 = img2.resize((width, height3), Image.LANCZOS).crop((0, round((height3 - height) / 2), width, height + round((height3 - height) / 2)))
        elif wratio2 == wratio1:
            print("square")
            img2 = img2.resize((width, height), Image.LANCZOS)
        out = masked2(img1, img2, r1, g1, b1, p1, p2, p3)
        out.save(str(emojiId) + 'masking.png')
        return str(emojiId) + 'masking.png'


def masked3(imag, imag2):
    width, height = imag.size
    data = imag.load()
    data2 = imag2.load()
    for x in range(width):
        for y in range(height):
            r, g, b, a = data[x, y]
            if a > 128:
                pass
            else:
                data[x, y] = data2[x, y]
    return imag


def maskingTwo(emoImg1, emoImg2, emojiId):
    # img1 = emoPng1.convert('RGBA')
    # img2 = emoPng2.convert('RGBA')
    width, height = emoImg1.size
    width2, height2 = emoImg2.size
    gif1, gif2 = False, False
    totalFrames = 0
    try:
        gifDuration = emoImg1.info['duration']
        totalFrames = emoImg1.n_frames
        gif1 = True
    except:
        gif1 = False
    try:
        gifDuration = emoImg2.info['duration']
        totalFrames = emoImg2.n_frames
        gif2 = True
    except:
        gif2 = False
    # if emoImg1.info != {}:
    #     totalFrames = emoImg1.n_frames
    #     gifDuration = emoImg1.info['duration']
    #     gif1 = True
    # if emoImg2.info != {}:
    #     totalFrames = emoImg2.n_frames
    #     gifDuration = emoImg2.info['duration']
    #     gif2 = True
    if gif1 and gif2:
        return "wrong, idiot"
    # so if 1 and 2 are both pngs, this is simple; use modified mask and output the single mixed image
    # if 1 nand 2 are gifs, processing depends on order, but the first should be the frame and the second should be the inlaid
    # in this second instance, we know which is a gif already and can choose how to handle this easily provided we don't be stupid
    # the first input image should be used as the reference size, and the second should be sized up so the inner edges touch?
    print(gif1, gif2, totalFrames)
    if gif1 or gif2:  # if one input is a gif, this'll need a loop of frames
        images = []
        for f in range(totalFrames):
            if gif1:
                emoImg1.seek(f)
                img1 = emoImg1.copy().convert('RGBA')
                img2 = emoImg2.convert('RGBA')
            elif gif2:
                emoImg2.seek(f)
                img2 = emoImg2.copy().convert('RGBA')
                img1 = emoImg1.convert('RGBA')
            # so we have an image from both 1 and 2, regardless of if they're gifs... we need to match their sizes up to the 1st
            wratio1 = height / width
            wratio2 = height2 / width2
            if wratio1 > wratio2:  # so if 1 is skinnier tall than 2..., we'll be matching height and cutting sides off 2
                width3 = round((width2 / height2) * height)
                img2 = img2.resize((width3, height), Image.LANCZOS).crop((round((width3 - width) / 2), 0, width + round((width3 - width) / 2), height))
            elif wratio2 > wratio1:
                height3 = round((height2 / width2) * width)
                img2 = img2.resize((width, height3), Image.LANCZOS).crop((0, round((height3 - height) / 2), width, height + round((height3 - height) / 2)))
            elif wratio2 == wratio1:
                img2 = img2.resize((width, height), Image.LANCZOS)
            out = masked3(img1, img2)
            alpha = out.split()[3]
            out = out.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
            mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            out.paste(255, mask)
            images.append(out)
        images[0].save(str(emojiId) + 'masking.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                       disposal=2)
        return str(emojiId) + 'masking.gif'
    else:  # combine just the two images
        img1 = emoImg1.convert('RGBA')
        img2 = emoImg2.convert('RGBA')
        wratio1 = height / width
        wratio2 = height2 / width2
        if wratio1 > wratio2:  # so if 1 is skinnier tall than 2..., we'll be matching height and cutting sides off 2
            print("wide")
            width3 = round((width2 / height2) * height)
            img2 = img2.resize((width3, height), Image.LANCZOS).crop((round((width3 - width) / 2), 0, width + round((width3 - width) / 2), height))
        elif wratio2 > wratio1:
            print("tall")
            height3 = round((height2 / width2) * width)
            img2 = img2.resize((width, height3), Image.LANCZOS).crop((0, round((height3 - height) / 2), width, height + round((height3 - height) / 2)))
        elif wratio2 == wratio1:
            print("square")
            img2 = img2.resize((width, height), Image.LANCZOS)
        print(img1.size, img2.size)
        out = masked3(img1, img2)
        out.save(str(emojiId) + 'masking.png')
        return str(emojiId) + 'masking.png'


def masked4(imag2, h2):
    imag = imag2.copy().convert('RGBA')
    width, height = imag.size
    data = imag.load()
    for x in range(width):
        for y in range(height):
            r, g, b, a = data[x, y]
            if a == 0:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            rr, gg, bb = colorsys.hsv_to_rgb(((h2 / 360) + h), s, v)
            data[x, y] = round(rr * 255), round(gg * 255), round(bb * 255), a
    return imag


def maskingPng4(emoPng, ft, emojiId):
    images = []
    img2 = emoPng.convert("RGBA")
    for f in range(ft):
        h2 = (f / ft) * 360
        img = masked4(img2, h2)
        alpha = img.split()[3]
        img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        img.paste(255, mask)
        images.append(img)
    images[0].save(str(emojiId) + 'masking.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'masking.gif'


def maskingGif4(emoGif, n, emojiId):
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    images = []
    for f in range(totalFrames):
        emoGif.seek(f)
        img2 = emoGif.copy().convert('RGBA')
        h2 = ((f * n) / totalFrames) * 360
        img = masked4(img2, h2)
        alpha = img.split()[3]
        img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        img.paste(255, mask)
        images.append(img)
    images[0].save(str(emojiId) + 'masking.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'masking.gif'

def lcdize(image, do, noise):
    image = image.convert('RGBA')
    pix = Image.open('pixels/6x6.png')
    width, height = pix.size
    bx, by = image.size
    result = Image.new('RGBA', (width * bx, height * by), (0, 0, 0, 0))

    pixl = pix.load()
    blockl = image.load()
    resultl = result.load()
    for x in range(bx):
        for y in range(by):
            r, g, b, a = blockl[x, y]
            if do:
                r = round((a / 255) * r)
                if r < 24:
                    r = 24
                g = round((a / 255) * g)
                if g < 24:
                    g = 24
                b = round((a / 255) * b)
                if b < 24:
                    b = 24
            if noise > 0:
                noiseadd = random.randint(-noise, noise)
                r = r + noiseadd
                g = g + noiseadd
                b = b + noiseadd
                if r > 255:
                    r = 255
                if r < 0:
                    r = 0
                if g > 255:
                    g = 255
                if g < 0:
                    g = 0
                if b > 255:
                    b = 255
                if b < 0:
                    b = 0
            for x2 in range(width):
                for y2 in range(height):
                    try:
                        r2, g2, b2, a2 = pixl[x2, y2]
                    except:
                        r2, g2, b2 = pixl[x2, y2]
                    if r2 == 255:
                        r3 = r

                    elif g2 == 255:
                        g3 = g

                    elif b2 == 255:
                        b3 = b

                    else:
                        r3, g3, b3 = (0, 0, 0)
                        # r3 = round(r / 16)
                        # g3 = round(g / 16)
                        # b3 = round(b / 16)
                    a3 = a
                    if do:
                        if a3 < 255:
                            a3 = 255
                    resultl[x*width + x2, y*height + y2] = r3, g3, b3, a3
    return result

def lcdPng(emoPng, emojiId):
    emoPng = lcdize(emoPng, False, 0)
    emoPng.save(str(emojiId) + 'lcd.png')
    return str(emojiId) + 'lcd.png'

def lcdGif(emoGif, emojiId):
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    images = []
    for f in range(totalFrames):
        emoGif.seek(f)
        img = lcdize(emoGif.copy().convert('RGBA'), False, 0)
        alpha = img.split()[3]
        img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        img.paste(255, mask)
        images.append(img)
    images[0].save(str(emojiId) + 'lcd.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'lcd.gif'

def lcdPng2(emoPng, emojiId):
    emoPng = lcdize(emoPng, True, 0)
    emoPng.save(str(emojiId) + 'lcd.png')
    return str(emojiId) + 'lcd.png'

def lcdGif2(emoGif, emojiId):
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    images = []
    for f in range(totalFrames):
        emoGif.seek(f)
        img = lcdize(emoGif.copy().convert('RGBA'), True, 0).convert('P', palette=Image.ADAPTIVE, colors=255)
        images.append(img)
    images[0].save(str(emojiId) + 'lcd.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'lcd.gif'

def lcdPng3(emoPng, noise, emojiId):
    images = []
    for i in range(10):
        emoImg = lcdize(emoPng, True, noise).convert('P', palette=Image.ADAPTIVE, colors=255)
        images.append(emoImg)
    images[0].save(str(emojiId) + 'lcd.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'lcd.gif'

def lcdGif3(emoGif, noise, emojiId):
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    images = []
    for f in range(totalFrames):
        emoGif.seek(f)
        img = lcdize(emoGif.copy().convert('RGBA'), True, noise).convert('P', palette=Image.ADAPTIVE, colors=255)
        images.append(img)
    images[0].save(str(emojiId) + 'lcd.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + 'lcd.gif'
