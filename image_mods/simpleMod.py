import math, datetime, os, PIL
import colorsys
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageChops
from math import sqrt, pi, e, pow, exp, ceil, sin, cos, atan2, pi
import requests, io
import moviepy.editor as mp
import random
from random import randint, random


def clamp(inp, low, high):
    out = 0
    if inp < low:
        out = low
    elif inp > high:
        out = high
    else:
        out = inp
    return out


def rotateImg(emoImg, rot=90):
    return emoImg.convert("RGBA").rotate(-rot, Image.BICUBIC, expand=1)


def rotateGif(emoGif, rot=90):
    print(emoGif)
    images = []
    totalFrames = len(emoGif) - 1
    gif_duration = emoGif[-1]
    for f in range(0, totalFrames):
        emoImg = emoGif[f].copy()
        emoImg = emoImg.convert("RGBA").rotate(-rot, Image.BICUBIC, expand=1)
        images.append(emoImg)
    images.append(gif_duration)
    return images


def flipImg(emoImg):
    return emoImg.convert("RGBA").transpose(method=Image.FLIP_LEFT_RIGHT)


def flipGif(emoGif):
    images = []
    total_frames = len(emoGif) - 1
    gif_duration = emoGif[-1]
    for f in range(0, total_frames):
        emoImg = emoGif[f].copy()
        emoImg = emoImg.convert("RGBA").transpose(method=Image.FLIP_LEFT_RIGHT)
        images.append(emoImg)
    images.append(gif_duration)
    return images


def hyperImg(emoImg, input=1):
    images = []
    side = False
    gifDuration = (input + 1) * 10
    for f in range(0, 2):
        img = emoImg.convert("RGBA")
        if f % 2 == 1:
            img = img.transpose(method=Image.FLIP_LEFT_RIGHT)
        images.append(img)
    images.append(gifDuration)
    return images


def hyperGif(emoGif, input=1):
    images = []
    total_frames = len(emoGif) - 1
    gif_duration = emoGif[-1]
    if gif_duration < 20:
        gif_duration = 20
    frame_ratio = 20 / gif_duration
    realFrames = round(total_frames * (1 / frame_ratio))
    side = False
    mod = input + 1
    for f in range(0, realFrames):
        framePick = int(math.floor((f * frame_ratio) % total_frames))
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
        images.append(img)
    images.append(20)
    return images


def widen(emoPng, mult=1):
    print("triedpng", emoPng)
    width, height = emoPng.size
    return emoPng.resize((round(width * 4 * mult), height), Image.NEAREST)


def widenGif(emoGif, mult=1):
    print("triedgif", emoGif)
    width, height = emoGif[0].size
    images = []
    total_frames = len(emoGif) - 1
    gif_duration = emoGif[-1]
    for f in range(0, total_frames):
        emoPng = emoGif[f].copy().convert('RGBA').resize((round(width * 4 * mult), height), Image.NEAREST)
        images.append(emoPng)
    images.append(gif_duration)
    return images


def resize(emoPng, sm=100):
    width, height = emoPng.size
    wratio = width / height
    hratio = height / width
    if height < width:
        emoPng = emoPng.resize((round(sm * wratio), sm), Image.LANCZOS)
    if width < height:
        emoPng = emoPng.resize((sm, round(sm * hratio)), Image.LANCZOS)
    if height == width:
        emoPng = emoPng.resize((sm, sm), Image.LANCZOS)
    return emoPng


def resizeGif(emoGif, sm=100):
    width, height = emoGif[0].size
    wratio = width / height
    hratio = height / width
    images = []
    total_frames = len(emoGif) - 1
    gif_duration = emoGif[-1]
    for f in range(total_frames):
        emoPng = emoGif[f].copy().convert('RGBA')
        if height < width:
            emoPng = emoPng.resize((round(sm * wratio), sm), Image.LANCZOS)
        if width < height:
            emoPng = emoPng.resize((sm, round(sm * hratio)), Image.LANCZOS)
        if height == width:
            emoPng = emoPng.resize((sm, sm), Image.LANCZOS)
        images.append(emoPng)
    images.append(gif_duration)
    return images


def crop(emoPng, off=0.1):
    width, height = emoPng.size
    xOff = round((width * off) / 2)
    yOff = round((height * off) / 2)
    emoPng = emoPng.crop((xOff, yOff, (width - xOff), (height - yOff)))
    return emoPng


def cropGif(emoGif, off=0.1):
    width, height = emoGif[0].size
    xOff = round((width * off) / 2)
    yOff = round((height * off) / 2)
    total_frames = len(emoGif) - 1
    gif_duration = emoGif[-1]
    images = []
    for f in range(total_frames):
        emoPng = emoGif[f].copy().convert('RGBA')
        emoPng = emoPng.crop((xOff, yOff, (width - xOff), (height - yOff)))
        images.append(emoPng)
    images.append(gif_duration)
    return images


def transparency(emoPng, arg=0.5):
    emoPng = emoPng.convert("RGBA")
    width, height = emoPng.size
    lod = emoPng.load()
    for x in range(width):
        for y in range(height):
            r, g, b, a = lod[x, y]
            a = round(a * arg)
            lod[x, y] = (r, g, b, a)
            # lod[x, y][3] = round(lod[x, y][3] * arg)
    return emoPng


def transparencyGif(emoGif, arg=0.5):
    return "gifs don't support transparency, dummy"


def thinking(emoPng, xIn=0, yIn=0, scale=0.5):
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
    return emoPng


def thinkingGif(emoGif, xIn=0.5, yIn=0.5, scale=0.5):
    width, height = emoGif[0].size
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
    total_frames = len(emoGif) - 1
    gif_duration = emoGif[-1]
    images = []
    for f in range(total_frames):
        emoPng = emoGif[f].copy().convert("RGBA")
        finger = fing.copy()
        emoPng.alpha_composite(fing, (0 + xIn, 0 + yDif - yIn))
        images.append(emoPng)
    images.append(gif_duration)
    return images


def information(emoImg):
    x, y = emoImg.size
    stringy = "Image dimensions are: " + str(x) + " " + str(y)
    return stringy


def information2(emoGif):
    x, y = emoGif[0].size
    total_frames = len(emoGif) - 1
    gif_duration = emoGif[-1]
    stringy = "Image dimensions are: " + str(x) + " " + str(y) + "\n" + "Number of frames: " + str(total_frames) + "\n" + "Durations: " + str(gif_duration)
    return stringy


def save(emoPng):
    emojiId = random.randint(11111, 9999999)
    emoPng.save(str(emojiId) + "save.png")
    return "Image saved as " + str(emojiId) + "save.png\nInsert filename.png instead of emoji to use, file will be deleted afterwards."


def saveGif(emoGif):
    emojiId = random.randint(11111, 9999999)
    total_frames = len(emoGif) - 1
    gif_duration = emoGif[-1]
    images = []
    for f in range(total_frames):
        emoPng = emoGif[f].copy().convert('RGBA')
        alpha = emoPng.split()[3]
        emoPng = emoPng.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        emoPng.paste(255, mask)
        images.append(emoPng)
    images[0].save(str(emojiId) + 'save.gif', save_all=True, append_images=images[1:], duration=gif_duration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return "Image saved as " + str(emojiId) + "save.gif\nInsert filename.gif instead of emoji to use, file will be deleted afterwards."


def grabImage(urll):  # if you direct link to a png/gif/etc, it will directly return it as a bytestream of the image
    r = requests.get(urll, allow_redirects=True)
    r.close()
    return io.BytesIO(r.content)


def get_emoji_url(emoji_string):
    id_string = emoji_string[emoji_string.rfind(':') + 1:-1]
    url = "https://cdn.discordapp.com/emojis/" + str(id_string)
    return url


def exists(path):  # checks if url exists
    r = requests.head(path)
    return r.status_code == requests.codes.ok


def getUrl(text):
    image = Image.open(grabImage(text))
    return image


def append(emoGif, endGif):
    return "idk what you're trying to accomplish here"


def appendGif(emoGif, endGif):
    total_frames = len(emoGif) - 1
    gif_duration = emoGif[-1]
    images = []
    for f in range(total_frames):
        emoPng = emoGif[f].copy().convert('RGBA')
        images.append(emoPng)
    total_frames2 = len(endGif) - 1
    width, height = emoGif[0].size
    wratio = width / height
    width2, height2 = endGif[0].size
    width3 = round(height2 * wratio)
    xOff = round((width2 - width3) / 2)
    print(width, height, width2, height2, xOff, width3)
    for f in range(total_frames2):
        emoPng = endGif[f].copy().convert('RGBA')
        emoPng = emoPng.crop((xOff, 0, xOff + width3, height2)).resize((width, height), Image.LANCZOS)
        images.append(emoPng)
    arr1 = emoGif[-1]
    arr2 = endGif[-1]
    total_durations = []
    if type(arr1) is list:
        for i in arr1:
            total_durations.append(i)
    else:
        arr1 = [arr1] * total_frames
        for i in arr1:
            total_durations.append(i)
    if type(arr2) is list:
        for i in arr2:
            total_durations.append(i)
    else:
        arr2 = [arr2] * total_frames
        for i in arr2:
            total_durations.append(i)
    images.append(total_durations)
    return images


def areyousure(emoPng):
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
    images.append(gifDuration)
    return images


def justdoit(emoPng):
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
    images.append(gifDuration)
    return images


def couch(emoPng):
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
    images.append(gifDuration)
    return images


def manydoors(emoPng):
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
    images.append(gifDuration)
    return images


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


def maskingPng(emoPng, r1=255, g1=255, b1=255, h2=0, p1=16, p2=10, p3=30):
    img = emoPng.convert("RGBA")
    img = masked(img, r1, g1, b1, h2, 255, p1, p2, p3)
    return img


def maskingGif(emoGif, r1=255, g1=255, b1=255, h2=0, p1=16, p2=10, p3=30):
    total_frames = len(emoGif) - 1
    gif_duration = emoGif[-1]
    images = []
    for f in range(total_frames):
        img2 = emoGif[f].copy().convert('RGBA')
        img = masked(img2, r1, g1, b1, h2, 255, p1, p2, p3)
        alpha = img.split()[3]
        img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        img.paste(255, mask)
        images.append(img)
    images.append(gif_duration)
    return images


def maskingPng2(emoPng, r1=255, g1=255, b1=255, ft=40, p1=16, p2=20, p3=30):
    images = []
    img2 = emoPng.convert("RGBA")
    for f in range(ft):
        h2 = (f / ft) * 360
        img = masked(img2, r1, g1, b1, h2, 255, p1, p2, p3)
        images.append(img)
    images.append(20)
    return images


def maskingGif2(emoGif, r1=255, g1=255, b1=255, n=1, p1=16, p2=20, p3=30):
    total_frames = len(emoGif) - 1
    gif_duration = emoGif[-1]
    images = []
    for f in range(total_frames):
        img2 = emoGif[f].copy().convert('RGBA')
        h2 = ((f * n) / total_frames) * 360
        img = masked(img2, r1, g1, b1, h2, 255, p1, p2, p3)
        images.append(img)
    images.append(gif_duration)
    return images


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


def maskingOne(emoImg1, emoImg2, r1=255, g1=255, b1=255, p1=16, p2=10, p3=20):
    gif1, gif2 = False, False
    totalFrames = 0
    if type(emoImg1) is list:
        gifDuration = emoImg1[-1]
        totalFrames = len(emoImg1) - 1
        gif1 = True
        width, height = emoImg1[0].size
    else:
        gif1 = False
        width, height = emoImg1.size
    if type(emoImg2) is list:
        gifDuration = emoImg2[-1]
        totalFrames = len(emoImg2) - 1
        gif2 = True
        width2, height2 = emoImg2[0].size
    else:
        gif2 = False
        width2, height2 = emoImg2.size
    if gif1 and gif2:
        return "wrong, idiot"
    # so if 1 and 2 are both pngs, this is simple; use modified mask and output the single mixed image
    # if 1 nand 2 are gifs, processing depends on order, but the first should be the frame and the second should be the inlaid
    # in this second instance, we know which is a gif already and can choose how to handle this easily provided we don't be stupid
    # the first input image should be used as the reference size, and the second should be sized up so the inner edges touch?
    if gif1 or gif2:  # if one input is a gif, this'll need a loop of frames
        images = []
        for f in range(totalFrames):
            if gif1:
                img1 = emoImg1[f].copy().convert('RGBA')
                img2 = emoImg2.convert('RGBA')
            elif gif2:
                img2 = emoImg2[f].copy().convert('RGBA')
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
            images.append(out)
        images.append(gifDuration)
        return images
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
        return out


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


def maskingTwo(emoImg1, emoImg2):
    gif1, gif2 = False, False
    totalFrames = 0
    if type(emoImg1) is list:
        gifDuration = emoImg1[-1]
        totalFrames = len(emoImg1) - 1
        gif1 = True
        width, height = emoImg1[0].size
    else:
        gif1 = False
        width, height = emoImg1.size
    if type(emoImg2) is list:
        gifDuration = emoImg2[-1]
        totalFrames = len(emoImg2) - 1
        gif2 = True
        width2, height2 = emoImg2[0].size
    else:
        gif2 = False
        width2, height2 = emoImg2.size
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
                img1 = emoImg1[f].copy().convert('RGBA')
                img2 = emoImg2.convert('RGBA')
            elif gif2:
                img2 = emoImg2[f].copy().convert('RGBA')
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
            images.append(out)
        images.append(gifDuration)
        return images
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
        return out


def masked4(imag2, h2=50):
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


def maskingPng4(emoPng, ft=60):
    images = []
    img2 = emoPng.convert("RGBA")
    for f in range(ft):
        h2 = (f / ft) * 360
        img = masked4(img2, h2)
        images.append(img)
    images.append(20)
    return images


def maskingGif4(emoGif, n=1):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img2 = emoGif[f].copy().convert('RGBA')
        h2 = ((f * n) / totalFrames) * 360
        img = masked4(img2, h2)
        images.append(img)
    images.append(gifDuration)
    return images


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


def lcdPng(emoPng):
    return lcdize(emoPng, False, 0)


def lcdGif(emoGif):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img = lcdize(emoGif[f].copy().convert('RGBA'), False, 0)
        images.append(img)
    images.append(gifDuration)
    return images


def lcdPng2(emoPng):
    return lcdize(emoPng, True, 0)


def lcdGif2(emoGif):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img = lcdize(emoGif[f].copy().convert('RGBA'), True, 0).convert('RGB').quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        images.append(img)
    images.append(gifDuration)
    return images


def lcdPng3(emoPng, noise=20):
    images = []
    for i in range(10):
        emoImg = lcdize(emoPng, True, noise).convert('RGB')
        emoImg = emoImg.quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        images.append(emoImg)
    images.append(20)
    return images


def lcdGif3(emoGif, noise=20):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img = lcdize(emoGif[f].copy().convert('RGBA'), True, noise).convert('RGB')
        img = img.quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        images.append(img)
    images.append(gifDuration)
    return images


def lcdPng4(emoPng, noise=20):
    images = []
    for i in range(10):
        emoImg = lcdize(emoPng, True, noise).convert('RGB').filter(ImageFilter.GaussianBlur(radius=1.2))
        emoImg = ImageEnhance.Brightness(emoImg).enhance(2.2)
        emoImg = ImageEnhance.Contrast(emoImg).enhance(1.4)
        emoImg = emoImg.quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        images.append(emoImg)
    images.append(20)
    return images


def lcdGif4(emoGif, noise=20):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img = lcdize(emoGif[f].copy().convert('RGBA'), True, noise).convert('RGB').filter(ImageFilter.GaussianBlur(radius=1.2))
        img = ImageEnhance.Brightness(img).enhance(2.2)
        img = ImageEnhance.Contrast(img).enhance(1.4)
        img = img.quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        images.append(img)
    images.append(gifDuration)
    return images


def intoGif(*args):
    emojiId = args[-1]
    duration = args[-2]
    imgs = args[:-2]
    images = [*imgs]
    images2 = []
    for f in range(len(images) * duration):
        frame = math.floor(f/duration)
        print(f, frame, len(images))
        img = images[frame]
        alpha = img.split()[3]
        img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        img.paste(255, mask)
        images2.append(img)
    gifDuration = 20 * duration
    images.append(gifDuration)
    return images
    # images[0].save(str(emojiId) + 'into.gif', save_all=True, append_images=images2[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
    #                disposal=2)
    # return str(emojiId) + 'into.gif'


def intoMp4(inp, emojiId=random.randint(11111, 999999)):
    inp.save("input.gif", save_all=True)
    clip = mp.VideoFileClip("input.gif")
    # clip = clip.fx(mp.vfx.loop)
    clip.write_videofile(str(emojiId) + "video.mp4")
    return str(emojiId) + "video.mp4"


def getMp4asGif(inp, emojiId=random.randint(11111, 999999)):
    r = requests.get(str(inp))
    with open(str(emojiId) + "input.mp4", 'wb') as f:
        f.write(r.content)
    clip = mp.VideoFileClip(str(emojiId) + 'input.mp4')
    clip.write_gif(str(emojiId) + "video.gif")
    os.remove(str(emojiId) + 'input.mp4')
    return str(emojiId) + "video.gif"


def emboss(emoPng):
    return emoPng.filter(ImageFilter.EMBOSS)


def embossGif(emoGif):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        try:
            emoPng = emoGif[f].copy().convert('RGBA')
        except:
            print("failed at", f)
            emoPng = emoGif[f].copy().convert('RGBA')
        emoPng = emoPng.filter(ImageFilter.EMBOSS).convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        # alpha = emoPng.split()[3]
        # emoPng = emoPng.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        # mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        # emoPng.paste(255, mask)
        images.append(emoPng)
    images.append(gifDuration)
    return images


def aggressivePng(emoPng):
    ft = (24*3)
    emoPng = emoPng.convert('RGBA')
    width, height = emoPng.size
    savg = (width + height) / 2
    buffw = round(savg*0.1)
    buffh = round(savg*0.1)
    images = []
    borderc = Image.new('RGBA', (width + (buffw * 2), height + (buffh * 2)), (0, 0, 0, 0))
    borderc.alpha_composite(emoPng.copy(), (buffw, buffh))
    borderc = borderc.filter(ImageFilter.GaussianBlur(radius=1.5)).convert('RGBA')
    # borderc.alpha_composite(bord.copy(), (buffw, buffh))
    bl = borderc.load()
    for x in range(borderc.size[0]):
        for y in range(borderc.size[1]):
            if bl[x, y][3] > 0:
                bl[x, y] = (0, 0, 0, 255)
    for f in range(ft-1):
        h2 = (f / ft) * 360
        canvas = Image.new('RGBA', (width+(buffw*2), height+(buffh*2)), (0, 0, 0, 0))
        # borderc = Image.new('RGBA', (width+(buffw*2), height+(buffh*2)), (0, 0, 0, 0))
        canvas.alpha_composite(emoPng.copy(), (buffw, buffh))
        # borderc.alpha_composite(bord.copy(), (buffw, buffh))
        offX = round((math.sin(((2 * math.pi) / 3) * (f - 3))) * 3 * (savg / 300))
        offY = round((math.sin(((2 * math.pi) / 4) * (f - 4))) * 3 * (savg / 300))
        img = ImageChops.offset(canvas, offX, offY).crop((0, 0, width+(buffw*2), height+(buffh*2)))
        # border = ImageChops.offset(borderc, offX, offY).crop((0, 0, width+(buffw*2), height+(buffh*2)))
        back = borderc.copy()
        back.alpha_composite(masked4(img, h2), (0, 0))
        images.append(back)
    images.append(20)
    return images


def bordering(inp, thicc, r=0, g=0, b=0, a=0):
    width, height = inp.size
    savg = (width + height) / 2
    buffw = round(savg * 0.1)
    buffh = round(savg * 0.1)
    canvas = Image.new('RGBA', (width + (buffw * 2), height + (buffh * 2)), (0, 0, 0, 0))
    canvas.alpha_composite(inp.copy(), (buffw, buffh))
    borderc = Image.new('RGBA', (width + (buffw * 2), height + (buffh * 2)), (0, 0, 0, 0))
    borderc.alpha_composite(inp.copy(), (buffw, buffh))
    if a != 0:
        bl = borderc.load()
        for x in range(borderc.size[0]):
            for y in range(borderc.size[1]):
                if bl[x, y][3] <= a and bl[x, y][3] != 0:
                    bl[x, y] = (0, 0, 0, 0)
    borderc = borderc.filter(ImageFilter.GaussianBlur(radius=thicc)).convert('RGBA')
    bl = borderc.load()
    for x in range(borderc.size[0]):
        for y in range(borderc.size[1]):
            if bl[x, y][3] > 0:
                bl[x, y] = (clamp(r, 0, 255), clamp(g, 0, 255), clamp(b, 0, 255), 255)
    borderc.alpha_composite(canvas, (0, 0))
    return borderc


def border(emoPng, thicc=1):
    return bordering(emoPng, thicc)


def borderGif(emoGif, thicc=1):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        emoPng = emoGif[f].copy().convert('RGBA')
        emoPng = bordering(emoPng, thicc)
        images.append(emoPng)
    images.append(gifDuration)
    return images


def border2(emoPng, thicc=1, r=255, g=0, b=0, a=255):
    return bordering(emoPng, thicc, r, g, b, a)


def borderGif2(emoGif, thicc=1, r=255, g=0, b=0, a=255):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        emoPng = emoGif[f].copy().convert('RGBA')
        emoPng = bordering(emoPng, thicc, r, g, b, a)
        images.append(emoPng)
    images.append(gifDuration)
    return images


def modC(inp):
    # if inp <= 128:
    #     inp = inp / 2
    # if 128 < inp <= 192:
    #     inp = (1.27 * inp) - 98
    # if 192 < inp <= 240:
    #     inp = (1.69 * inp) - 179
    # if 240 < inp <= 250:
    #     inp = (1.9 * inp) - 230
    inp = math.pow(inp, 2) * (1 / 255)
    return round(inp)


def enchant(emoPng):
    images = []
    overlay = Image.open('enchanted_item_glint.png').convert('RGBA')
    width, height = emoPng.size
    overlay = overlay.resize((width*6, width*6), Image.LANCZOS).rotate(90)
    for f in range(200):
        over = ImageChops.offset(overlay.copy(), round(((width*6)/200) * f), round(((-width*6)/200) * f))
        over = over.crop((0, 0, width, height))
        out = emoPng.copy().convert('RGBA')
        ol = out.load()
        ovl = over.load()
        for x in range(width):
            for y in range(height):
                r1, g1, b1, a1 = ol[x, y]
                r2, g2, b2, a2 = ovl[x, y]
                r1 = clamp(r1 + modC(r2), 0, 255)
                g1 = clamp(g1 + modC(g2), 0, 255)
                b1 = clamp(b1 + modC(b2), 0, 255)
                ol[x, y] = (r1, g1, b1, a1)
        images.append(out)
    images.append(40)
    return images


def halve(emoGif):
    width, height = emoGif[0].size
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    dur_arr = []
    for f in range(math.floor(totalFrames/2)):
        emoPng = emoGif[f*2].copy().convert('RGBA')
        images.append(emoPng)
        if type(gifDuration) is list:
            dur_arr.append(gifDuration[f*2])
    if type(gifDuration) is list:
        images.append(gifDuration)
    else:
        images.append(40)
    return images


def diff(inp, inp2):
    dif1 = abs(inp[0] - inp2[0])
    dif2 = abs(inp[1] - inp2[1])
    dif3 = abs(inp[2] - inp2[2])
    return ((dif1 * .299) + (dif2 * .587) + (dif3 * .114))


def colorcompare(inp, inp2):
    luma1 = (inp[0]*.299 + inp[1]*.587 + inp[2]*.114) / 255
    luma2 = (inp2[0]*.299 + inp2[1]*.587 + inp2[2]*.114) / 255
    lumadiff = luma1 - luma2
    dif1 = (inp[0] - inp2[0]) / 255
    dif2 = (inp[1] - inp2[1]) / 255
    dif3 = (inp[2] - inp2[2]) / 255
    return (dif1 * dif1 * 0.299 + dif2 * dif2 * 0.587 + dif3 * dif3 * 0.114) * 0.75 + lumadiff * lumadiff


def nes(inp, pal):
    img = Image.open(pal + '_palette.png').convert('RGB')
    c_arr = []
    iml = img.load()
    xd, yd = img.size
    for x in range(xd):
        for y in range(yd):
            r, g, b = iml[x, y]
            if [r, g, b] not in c_arr:
                c_arr.append([*iml[x, y]])
    inp = inp.convert('RGBA')
    width, height = inp.size
    canvas = Image.new('RGB', (width, height), (0, 0, 0))
    il = inp.load()
    cl = canvas.load()
    e_arr = [(0, 0, 0)] * ((width * 3) + 1)
    for y in range(height):
        # pr, pg, pb = 0, 0, 0
        for x in range(width):
            ar, ge, be, ay = il[x, y]
            ar = ar + e_arr[0][0]
            ge = ge + e_arr[0][1]
            be = be + e_arr[0][2]
            lowest = 0
            for i in range(len(c_arr)):
                dif1 = colorcompare([ar, ge, be], c_arr[i])
                dif2 = colorcompare([ar, ge, be], c_arr[lowest])
                # dif1 = diff([ar2, ge2, be2], c_arr[i])
                # dif2 = diff([ar2, ge2, be2], c_arr[lowest])
                if dif1 < dif2:
                    lowest = i
            r, g, b = c_arr[lowest]
            pr = il[x, y][0] - r
            pg = il[x, y][1] - g
            pb = il[x, y][2] - b
            e_arr[1] = (e_arr[1][0] + (pr * (5 / 32)), e_arr[1][1] + (pg * (5 / 32)), e_arr[1][2] + (pb * (5 / 32)))
            e_arr[2] = (e_arr[2][0] + (pr * (3 / 32)), e_arr[2][1] + (pg * (3 / 32)), e_arr[2][2] + (pb * (3 / 32)))
            e_arr[width-2] = (e_arr[width-2][0] + (pr * (2 / 32)), e_arr[width-2][1] + (pg * (2 / 32)), e_arr[width-2][2] + (pb * (2 / 32)))
            e_arr[width-1] = (e_arr[width-1][0] + (pr * (4 / 32)), e_arr[width-1][1] + (pg * (4 / 32)), e_arr[width-1][2] + (pb * (4 / 32)))
            e_arr[width] = (e_arr[width][0] + (pr * (5 / 32)), e_arr[width][1] + (pg * (5 / 32)), e_arr[width][2] + (pb * (5 / 32)))
            e_arr[width+1] = (e_arr[width+1][0] + (pr * (4 / 32)), e_arr[width+1][1] + (pg * (4 / 32)), e_arr[width+1][2] + (pb * (4 / 32)))
            e_arr[width+2] = (e_arr[width+2][0] + (pr * (2 / 32)), e_arr[width+2][1] + (pg * (2 / 32)), e_arr[width+2][2] + (pb * (2 / 32)))
            e_arr[-3] = (e_arr[-3][0] + (pr * (2 / 32)), e_arr[-3][1] + (pg * (2 / 32)), e_arr[-3][2] + (pb * (2 / 32)))
            e_arr[-2] = (e_arr[-2][0] + (pr * (3 / 32)), e_arr[-2][1] + (pg * (3 / 32)), e_arr[-2][2] + (pb * (3 / 32)))
            e_arr[-1] = (e_arr[-1][0] + (pr * (2 / 32)), e_arr[-1][1] + (pg * (2 / 32)), e_arr[-1][2] + (pb * (2 / 32)))
            e_arr.pop(0)
            e_arr.append((0, 0, 0))
            cl[x, y] = (r, g, b)
    canvas = canvas.convert('RGBA')
    cl = canvas.load()
    for y in range(height):
        for x in range(width):
            ar, ge, be, ay = il[x, y]
            r, g, b, a = cl[x, y]
            cl[x, y] = (r, g, b, ay)
    return canvas


def luma(inp):
    l = ((inp[0] * 299) + (inp[1] * 587) + (inp[2] * 114))
    return l


from operator import itemgetter
import numpy as np
# try:
#     import c_dithering
# except:
#     print("don't worry about it?")


def ordering(inp, plist):
    t_matrix = [
    [0, 12, 3, 15],
    [8, 4, 11, 7],
    [2, 14, 1, 13],
    [10, 6, 9, 5]
    ]
    c_arr = []
    xd = len(plist)
    yd = len(plist[0])
    for x in range(xd):
        for y in range(yd):
            r, g, b = plist[x][y]
            if [r, g, b] not in c_arr:
                c_arr.append([*plist[x][y]])
    width = len(inp)
    height = len(inp[0])
    canvas = []
    error = [0, 0, 0]
    threshold = 0.6
    for x in range(width):
        canv_layer2 = []
        for y in range(height):
            candidate_list = []
            while len(candidate_list) < 16:
                ar, ge, be, ay = inp[x][y]
                ar2 = ar + error[0] * threshold
                ge2 = ge + error[1] * threshold
                be2 = be + error[2] * threshold
                lowest = 0
                for i in range(len(c_arr)):
                    dif1 = colorcompare([ar2, ge2, be2], c_arr[i])
                    dif2 = colorcompare([ar2, ge2, be2], c_arr[lowest])
                    # dif1 = diff([ar2, ge2, be2], c_arr[i])
                    # dif2 = diff([ar2, ge2, be2], c_arr[lowest])
                    if dif1 < dif2:
                        lowest = i
                r, g, b = c_arr[lowest]
                candidate_list.append([[0],[r, g, b]])
                pr = ar - r
                pg = ge - g
                pb = be - b
                error = [pr, pg, pb]
            key_arr = []
            for i in candidate_list:
                i[0] = luma(i[1][0:3])
            candidate_list.sort()
            index = t_matrix[x % 4][y % 4]
            canv_layer2.append(candidate_list[index][1][0:3])
        canvas.append(canv_layer2)
    for y in range(height):
        for x in range(width):
            ar, ge, be, ay = inp[x][y]
            try:
                r, g, b = canvas[x][y]
            except:
                print(canvas[x][y])
                r, g, b = canvas[x][y]
            canvas[x][y] = (r, g, b, ay)
    return canvas


def ordered(inp, pal):
    t_matrix = [
    [0, 12, 3, 15],
    [8, 4, 11, 7],
    [2, 14, 1, 13],
    [10, 6, 9, 5]
    ]
    img = inp.convert("RGBA")
    iml = np.asarray(img).tolist()
    pal = np.asarray(Image.open(str(pal).upper() + '_palette.png').convert('RGB')).tolist()
    # oot = c_dithering.ordered(iml, pal)
    oot = ordering(iml, pal)
    canvas = Image.fromarray(np.uint8(oot), 'RGBA')
    # img = Image.open(pal + '_palette.png').convert('RGB')
    # c_arr = []
    # iml = img.load()
    # xd, yd = img.size
    # for x in range(xd):
    #     for y in range(yd):
    #         r, g, b = iml[x, y]
    #         if [r, g, b] not in c_arr:
    #             c_arr.append([*iml[x, y]])
    # inp = inp.convert('RGBA')
    # width, height = inp.size
    # canvas = Image.new('RGB', (width, height), (0, 0, 0))
    # il = inp.load()
    # cl = canvas.load()
    # error = [0, 0, 0]
    # threshold = 0.6
    # for y in range(height):
    #     for x in range(width):
    #         candidate_list = []
    #         while len(candidate_list) < 16:
    #             ar, ge, be, ay = il[x, y]
    #             ar2 = ar + error[0] * threshold
    #             ge2 = ge + error[1] * threshold
    #             be2 = be + error[2] * threshold
    #             lowest = 0
    #             for i in range(len(c_arr)):
    #                 dif1 = colorcompare([ar2, ge2, be2], c_arr[i])
    #                 dif2 = colorcompare([ar2, ge2, be2], c_arr[lowest])
    #                 # dif1 = diff([ar2, ge2, be2], c_arr[i])
    #                 # dif2 = diff([ar2, ge2, be2], c_arr[lowest])
    #                 if dif1 < dif2:
    #                     lowest = i
    #             r, g, b = c_arr[lowest]
    #             candidate_list.append([r, g, b, 0])
    #             pr = ar - r
    #             pg = ge - g
    #             pb = be - b
    #             error = [pr, pg, pb]
    #         key_arr = []
    #         for i in candidate_list:
    #             i[-1] = luma(i[0:3])
    #         candidate_list = sorted(candidate_list, key=itemgetter(-1))
    #         index = t_matrix[x % 4][y % 4]
    #         cl[x, y] = tuple(candidate_list[index][0:3])
    # canvas = canvas.convert('RGBA')
    # cl = canvas.load()
    # for y in range(height):
    #     for x in range(width):
    #         ar, ge, be, ay = il[x, y]
    #         r, g, b, a = cl[x, y]
    #         cl[x, y] = (r, g, b, ay)
    return canvas


def palettePng(emoPng, inp="sega"):
    img = emoPng.convert("RGBA")
    return nes(img, str(inp).upper())


def paletteGif(emoGif, inp="sega"):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img2 = emoGif[f].copy().convert('RGBA')
        img = nes(img2, str(inp).upper())
        images.append(img)
    images.append(gifDuration)
    return images


def palettePng2(emoPng, inp="sega"):
    img = emoPng.convert("RGBA")
    return ordered(img, str(inp).upper())


def paletteGif2(emoGif, inp="sega"):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img2 = emoGif[f].copy().convert('RGBA')
        img = ordered(img2, str(inp).upper())
        images.append(img)
    images.append(gifDuration)
    return images


def make_palette(pal):
    img = Image.open(pal.upper() + '_palette.png').convert('RGB')
    c_arr = []
    iml = img.load()
    xd, yd = img.size
    for x in range(xd):
        for y in range(yd):
            r, g, b = iml[x, y]
            if [r, g, b] not in c_arr:
                c_arr.append([*iml[x, y]])
    return c_arr


def nearest_palette_color(color, mod, c_arr, prnt=False):
    r = color[0] + mod
    g = color[1] + mod
    b = color[2] + mod
    lowest = 0
    for i in range(len(c_arr)):
        dif1 = colorcompare((r, g, b), c_arr[lowest])
        dif2 = colorcompare((r, g, b), c_arr[i])
        if dif2 < dif1:
            lowest = i
    if prnt:
        print(lowest)
    return c_arr[lowest]


def ordered2(img, pal):
    t_map = [
        [0, 12, 3, 15],
        [8, 4, 11, 7],
        [2, 14, 1, 13],
        [10, 6, 9, 5]
    ]
    img = img.convert('RGBA')
    width, height = img.size
    i_arr = np.asarray(img).tolist()
    c_arr = make_palette(pal)
    threshold = 0.3
    n = len(t_map)
    r = 255/n
    c_layer = []
    for y in range(height):
        c_layer2 = []
        for x in range(width):
            color = i_arr[y][x]
            mody = r * (t_map[x % n][y % n] / (n*n) - 0.5) * 0.5
            color2 = nearest_palette_color(color, mody, c_arr)
            c_layer2.append(tuple([*color2, color[-1]]))
        c_layer.append(c_layer2)
    return Image.fromarray(np.uint8(c_layer), 'RGBA')


def palettePng3(emoPng, inp="sega"):
    img = emoPng.convert("RGBA")
    return ordered2(img, str(inp).upper())


def paletteGif3(emoGif, inp="sega"):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img2 = emoGif[f].copy().convert('RGBA')
        img = ordered2(img2, str(inp).upper())
        images.append(img)
    images.append(gifDuration)
    return images


def upscale(inp):
    width, height = inp.size
    inp = inp.resize((width*2, height*2), Image.NEAREST)
    return inp


def downscale(inp):
    width, height = inp.size
    inp = inp.resize((round(width/2), round(height/2)), Image.LANCZOS)
    return inp


def upscalePng(emoPng):
    img = emoPng.convert("RGBA")
    return upscale(img)


def upscaleGif(emoGif):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img2 = emoGif[f].copy().convert('RGBA')
        img = upscale(img2)
        images.append(img)
    images.append(gifDuration)
    return images


def downscalePng(emoPng):
    img = emoPng.convert("RGBA")
    return downscale(img)


def downscaleGif(emoGif):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img2 = emoGif[f].copy().convert('RGBA')
        img = downscale(img2)
        images.append(img)
    images.append(gifDuration)
    return images


def stitchw(inp, inp2):
    inp = inp.convert('RGBA')
    inp2 = inp2.convert('RGBA')
    w1, h1 = inp.size
    w2, h2 = inp2.size
    if h1 > h2:
        h = h1
    else:
        h = h2
    canvas = Image.new('RGBA', (w1 + w2, h), (0, 0, 0, 0))
    canvas.alpha_composite(inp.convert('RGBA'), (0, 0))
    canvas.alpha_composite(inp2.convert('RGBA'), (w1, 0))
    return canvas


def stitchwPng(*args):
    image_arr = list(args)
    for i in image_arr:
        if type(i) is list:
            return stitchwGif(*args)
    for i in range(len(image_arr)-1):
        image_arr[i+1] = stitchw(image_arr[i], image_arr[i+1])
    img = image_arr[-1]
    return img


def stitchwGif(*args):
    image_arr = list(args)
    for i in image_arr:
        if type(i) is list:
            totalFrames = len(i) - 1
            gifDuration = i[-1]
            break
    images = []
    for f in range(totalFrames):
        image_arr = list(args)
        for i in range(len(image_arr) - 1):
            if type(image_arr[i]) is list:
                try:
                    img1 = image_arr[i][f]
                except:
                    img1 = image_arr[i][-2]
            if type(image_arr[i + 1]) is list:
                try:
                    img2 = image_arr[i + 1][f]
                except:
                    img2 = image_arr[i + 1][-2]
            image_arr[i + 1] = stitchw(img1.convert('RGBA'), img2.convert('RGBA'))
        img = image_arr[-1]
        images.append(img)
    images.append(gifDuration)
    return images


def stitchh(inp, inp2):
    inp = inp.convert('RGBA')
    inp2 = inp2.convert('RGBA')
    w1, h1 = inp.size
    w2, h2 = inp2.size
    if w1 > w2:
        w = w1
    else:
        w = w2
    canvas = Image.new('RGBA', (w, h1 + h2), (0, 0, 0, 0))
    canvas.alpha_composite(inp.convert('RGBA'), (0, 0))
    canvas.alpha_composite(inp2.convert('RGBA'), (0, h1))
    return canvas


def stitchhPng(*args):
    image_arr = list(args)
    for i in image_arr:
        if type(i) is list:
            return stitchhGif(*args)
    for i in range(len(image_arr) - 1):
        image_arr[i + 1] = stitchh(image_arr[i], image_arr[i + 1])
    img = image_arr[-1]
    return img


def stitchhGif(*args):
    image_arr = list(args)
    for i in image_arr:
        if type(i) is list:
            totalFrames = len(i) - 1
            gifDuration = i[-1]
            break
    images = []
    for f in range(totalFrames):
        image_arr = list(args)
        for i in range(len(image_arr) - 1):
            if type(image_arr[i]) is list:
                try:
                    img1 = image_arr[i][f]
                except:
                    img1 = image_arr[i][-2]
            if type(image_arr[i + 1]) is list:
                try:
                    img2 = image_arr[i + 1][f]
                except:
                    img2 = image_arr[i + 1][-2]
            image_arr[i + 1] = stitchh(img1.convert('RGBA'), img2.convert('RGBA'))
        img = image_arr[-1]
        images.append(img)
    images.append(gifDuration)
    return images


def fixGif(Gif):
    totalFrames = len(Gif) - 1
    images = []
    dur_array = []
    for i in range(totalFrames):
        img = Gif[i].copy().convert('RGBA')
        dur_array.append(Gif[-1][i])
        for f in range(0, dur_array[-1], 20):
            images.append(img)
    images.append(20)
    return images


def contrastImg(emoImg, cnt=1.2):
    return ImageEnhance.Contrast(emoImg.convert('RGBA')).enhance(cnt)


def contrastGif(emoGif, cnt=1.2):
    images = []
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    for f in range(0, totalFrames):
        emoImg = emoGif[f].copy()
        emoImg = ImageEnhance.Contrast(emoImg.convert('RGBA')).enhance(cnt)
        images.append(emoImg)
    images.append(gifDuration)
    return images


def brightnessImg(emoImg, cnt=1.2):
    return ImageEnhance.Brightness(emoImg.convert('RGBA')).enhance(cnt)


def brightnessGif(emoGif, cnt, emojiId):
    images = []
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    for f in range(0, totalFrames):
        emoImg = emoGif[f].copy()
        emoImg = ImageEnhance.Brightness(emoImg.convert('RGBA')).enhance(cnt)
        images.append(emoImg)
    images.append(gifDuration)
    return images


def gaussImg(emoImg, cnt=1.2):
    return emoImg.convert('RGBA').filter(ImageFilter.GaussianBlur(radius=cnt))


def gaussGif(emoGif, cnt, emojiId):
    images = []
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    for f in range(0, totalFrames):
        emoImg = emoGif[f].copy()
        emoImg = emoImg.convert('RGBA').filter(ImageFilter.GaussianBlur(radius=cnt))
        images.append(emoImg)
    images.append(gifDuration)
    return images


def saturationImg(emoImg, cnt=1.2):
    return ImageEnhance.Color(emoImg.convert('RGBA')).enhance(cnt)


def saturationGif(emoGif, cnt=1.2):
    images = []
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    for f in range(0, totalFrames):
        emoImg = emoGif[f].copy()
        emoImg = ImageEnhance.Color(emoImg.convert('RGBA')).enhance(cnt)
        images.append(emoImg)
    images.append(gifDuration)
    return images


def diffract(img, pixl=3):
    width, height = img.size
    img = img.convert("RGBA")
    canvas = Image.new("RGBA", (width+(pixl*2), height), (0, 0, 0, 0))
    width2 = width+(pixl*2)
    il = img.load()
    cl = canvas.load()
    for x in range(width):
        for y in range(height):
            r, g, b, a = cl[x, y]
            r = il[x, y][0]
            a1 = il[x, y][3]
            r = round(r * (a1 / 255))
            if a1 > a:
                a = a1
            cl[x, y] = (r, g, b, a)
    for x in range(width):
        for y in range(height):
            r, g, b, a = cl[x + pixl, y]
            g = il[x, y][1]
            a1 = il[x, y][3]
            g = round(g * (a1 / 255))
            if a1 > a:
                a = a1
            cl[x + pixl, y] = (r, g, b, a)
    for x in range(width):
        for y in range(height):
            r, g, b, a = cl[x + (pixl * 2), y]
            b = il[x, y][2]
            a1 = il[x, y][3]
            b = round(b * (a1 / 255))
            if a1 > a:
                a = a1
            cl[x + (pixl * 2), y] = (r, g, b, a)
    return canvas


def diffractPng(emoPng, pixl=3):
    img = emoPng.convert("RGBA")
    return diffract(img, pixl)


def diffractGif(emoGif, pixl=3):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img2 = emoGif[f].copy().convert('RGBA')
        img = diffract(img2, pixl)
        images.append(img)
    images.append(gifDuration)
    return images


def diffract2(img, pixl=3, wid=20, t=5):
    width, height = img.size
    img = img.convert("RGBA")
    width2 = width+(pixl*2)
    il = img.load()
    images = []
    height2 = height + wid*4
    tim = 20 * t
    for f in range(tim):
        # mod = (width3 * (f / tim)) * 1.4 - (.2 * width3)
        mod = (height2 * (f / tim)) * 2 - (.6 * height2)
        canvas = Image.new("RGBA", (width2, height), (0, 0, 0, 0))
        cl = canvas.load()
        for y in range(height):
            xmod = round(pixl * math.exp(-((y - mod) ** 2) / (2 * (wid ** 2))))
            for x in range(width2):
                ex = x - pixl + xmod
                r, g, b, a = (0, 0, 0, 0)
                a1, a2, a3 = [0, 0, 0]
                if 0 < ex < width:
                    r = il[ex, y][0]
                    a1 = il[ex, y][3]
                    r = round(r * (a1 / 255))
                ex = x - pixl
                if 0 < ex < width:
                    g = il[ex, y][1]
                    a2 = il[ex, y][3]
                    g = round(g * (a2 / 255))
                ex = x - pixl - xmod
                if 0 < ex < width:
                    b = il[ex, y][2]
                    a3 = il[ex, y][3]
                    b = round(b * (a3 / 255))
                list = [a1, a2, a3]
                list.sort()
                a = list[-1]
                cl[x, y] = (r, g, b, a)
        images.append(canvas)
    images.append(20)
    return images


def diffractAni(emoPng, pixl=6, wid=20, t=5):
    img = emoPng.convert("RGBA")
    return diffract2(img, pixl, wid, t)


def glitch(img, amt=1):
    img = img.convert("RGB")
    while True:
        b = io.BytesIO()
        img.save(b, "jpeg")
        modify = b.getbuffer()
        try:
            for i in range(amt):
                index = random.randint(0, modify.nbytes-1)
                modify[index] = random.randint(1, 255)
            img2 = Image.open(b).convert("RGBA")
            break
        except:
            pass
    return img2


def glitchPng(emoPng, pixl=3):
    img = emoPng.convert("RGBA")
    return glitch(img, pixl)


def glitchGif(emoGif, pixl=3, chance=0.7):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    img = emoGif[0].copy().convert('RGB')
    size = img.size
    b = io.BytesIO()
    img.save(b, "jpeg")
    modify = b.getbuffer()
    nbytes = modify.nbytes
    indexes = []
    for i in range(pixl):
        indexes.append(random.randint(0, nbytes - 1))
    for f in range(totalFrames):
        img = emoGif[f].copy().convert('RGB')
        size = img.size
        while True:
            b = io.BytesIO()
            img.save(b, "jpeg")
            modify = b.getbuffer()
            if random.random() > chance:
                indexes = []
                for i in range(pixl):
                    indexes.append(random.randint(0, nbytes - 1))
            try:
                for index in indexes:
                    modify[index] = random.randint(1, 255)
                img2 = Image.open(b)
                im_bytes = img2.tobytes()
                break
            except Exception as e:
                pass
        img = Image.frombytes("RGB", size, im_bytes)
        images.append(img)
    images.append(gifDuration)
    return images


def giffify(img, dur=60, num=30):
    images = [img.convert("RGBA")]*num
    images.append(dur)
    return images


def jitter(img, amt):
    size = img.size
    il = img.load()
    for x in range(size[0]):
        p_arr = []
        jit = randint(-amt, amt)
        if jit > 0:
            for y in range(size[1]):
                p_arr.append(il[x, y])
            for i in range(jit):
                p_arr.insert(0, p_arr[0])
            for y in range(size[1]):
                il[x, y] = p_arr[y]
        elif jit < 0:
            for y in range(size[1]):
                p_arr.append(il[x, y])
            for i in range(-jit):
                p_arr.append(p_arr[-1])
                p_arr.pop(0)
            for y in range(size[1]):
                il[x, y] = p_arr[y]
    return img


def jitterPng(emoPng, pixl=3):
    img = emoPng.convert("RGBA")
    return jitter(img, pixl)


def jitterGif(emoGif, pixl=3):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img2 = emoGif[f].copy().convert('RGBA')
        img = jitter(img2, pixl)
        images.append(img)
    images.append(gifDuration)
    return images


def invert(img):
    size = img.size
    il = img.load()
    for x in range(size[0]):
        for y in range(size[1]):
            r, g, b, a = il[x, y]
            il[x, y] = (255-r, 255-g, 255-b, a)
    return img


def invertPng(emoPng):
    img = emoPng.convert("RGBA")
    return invert(img)


def invertGif(emoGif):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img2 = emoGif[f].copy().convert('RGBA')
        img = invert(img2)
        images.append(img)
    images.append(gifDuration)
    return images


def warp(img):
    size = img.size
    img = img.convert('RGBA')
    img2 = Image.new('RGBA', (size[0], size[1]), (0, 0, 0, 0))
    il = img.load()
    il2 = img2.load()
    dx = round(size[0] / 2)
    dy = round(size[1] / 2)
    for x in range(size[0]):
        for y in range(size[1]):
            hyp = sqrt(pow(x - dx, 2) + pow(y - dy, 2))
            wid = dx if dx < dy else dy
            max = pi * 5555
            mult = pow(max, 1/3)
            ang_off = pow((wid - hyp)/wid, 3) * mult
            # ang_off = ((1 * pi) * ((dy - hyp)/dy))
            ang = atan2(y - dy, x - dx) - ang_off
            # hyp = sqrt(pow(x - dx, 2) + pow(y - dy, 2))
            y2 = round(sin(ang) * hyp)
            x2 = round(cos(ang) * hyp)
            if hyp > wid:
                il2[x, y] = il[x, y]
                continue
            try:
                r, g, b, a = il[x2 - dx, y2 - dy]
                il2[x, y] = (r, g, b, a)
                # il2[x2, y2] = (r, g, b, a)
            except:
                pass
    return img2


def warpPng(emoPng):
    img = emoPng.convert("RGBA")
    return warp(img)


def warpGif(emoGif):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img2 = emoGif[f].copy().convert('RGBA')
        img = warp(img2)
        images.append(img)
    images.append(gifDuration)
    return images


def pad(inp, rat):
    r, g, b, a = 0, 0, 0, 0
    wid, hit = inp.size
    inp = inp.resize((round(wid * (1 + rat)), round(hit * (1 + rat))), Image.LANCZOS)
    if wid > hit:
        canv = Image.new('RGBA', (round(wid * (1 + (rat * 2))), round(wid * (1 + (rat * 2)))), (r, g, b, a))
    else:
        canv = Image.new('RGBA', (round(hit * (1 + (rat * 2))), round(hit * (1 + (rat * 2)))), (r, g, b, a))
    wid2, hit2 = canv.size
    wid, hit = inp.size
    canv.alpha_composite(inp, (round((wid2 - wid)/2), round((hit2 - hit)/2)))
    return canv


def spinPng(img, tim, mult=1):
    deg = 360 / tim
    img = pad(img.convert('RGBA'), 0.1)
    im_arr = []
    for i in range(abs(tim)):
        frame = img.copy().rotate(deg * i, Image.BICUBIC)
        im_arr.append(frame)
    im_arr.append(20 * mult)
    return im_arr


def pumpkin(img):
    pump = Image.open("pumpkindark.png").rotate(-5)  # 308, 267
    ar, ge, be, a = img.convert("RGBA").split()
    img = img.convert("RGB")
    img = ImageEnhance.Contrast(img).enhance(1.4)
    width, height = img.size
    il = img.load()
    high = 0
    for x in range(width):
        for y in range(height):
            r, g, b = il[x, y]
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if l > high:
                high = l
    val = 0.9 / high
    halfw = width / 2
    halfh = height / 2
    for x in range(width):  # hue is 28
        for y in range(height):
            r, g, b = il[x, y]
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            texture = (random.random() - 0.5) * 0.04
            lumamod = ((halfw - abs(halfw - x)) / halfw) + ((halfh - abs(halfh - y)) / halfh)
            lumamod = (lumamod / 6 + 0.66) * 0.9 + 0.1
            r, g, b = colorsys.hls_to_rgb(15 / 360 + ((15 / 360) * l), l * val * lumamod + texture, 1)
            r = round(r * 255)
            g = round(g * 255)
            b = round(b * 255)
            il[x, y] = (r, g, b)
    r, g, b = img.split()
    img = Image.merge("RGBA", (r, g, b, a))
    img = pad(img, 0).resize((140, 140), Image.LANCZOS)
    w, h = img.size
    pump.paste(img, (round((308 - w) / 2), round((267 - h) / 2) + 15), img)
    # pump = pump.resize((round(pump.size[0] / 2), round(pump.size[1] / 2)), Image.LANCZOS)
    return pump


def pumpkin2(img):
    pump = Image.open("pumpkin.png").convert("RGBA").rotate(-5)  # 308, 267
    ar, ge, be, a = img.convert("RGBA").copy().split()
    img = img.convert("RGB")
    img = ImageEnhance.Contrast(img).enhance(1.8)
    width, height = img.size
    il = img.load()
    high = 0
    low = 255
    for x in range(width):
        for y in range(height):
            r, g, b = il[x, y]
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if l > high:
                high = l
            if l < low:
                low = l
    offset = 0.35 - low
    val = (0.95 - offset) / high
    al = a.load()
    halfw = width / 2
    halfh = height / 2
    for x in range(width):  # hue is 28
        for y in range(height):
            r, g, b = il[x, y]
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            texture = (random.random() - 0.5) * 0.04
            if l > 0.92:
                l = 0.92
            lumamod = ((halfw - abs(halfw - x)) / halfw) + ((halfh - abs(halfh - y)) / halfh)
            lumamod = (lumamod / 6 + 0.66) * 0.9 + 0.1
            r, g, b = colorsys.hls_to_rgb(18 / 360 + ((24 / 360) * l), l * val * lumamod + offset + texture, .9)
            if (l * val + offset) <= .35:
                al[x, y] = 0
            r = round(r * 255)
            g = round(g * 255)
            b = round(b * 255)
            il[x, y] = (r, g, b)
    width, height = img.size
    r, g, b = img.split()
    img = Image.merge("RGBA", (r, g, b, a))
    img = pad(img, 0).resize((140, 140), Image.LANCZOS)
    w, h = img.size
    pump.paste(img, (round((308 - w) / 2), round((267 - h) / 2) + 19), img)
    # pump = pump.resize((round(pump.size[0] / 2), round(pump.size[1] / 2)), Image.LANCZOS)
    return pump


def pumpPng(emoPng):
    img = emoPng.convert("RGBA")
    return pumpkin(img)


def pumpGif(emoGif):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img2 = emoGif[f].copy().convert('RGBA')
        img = pumpkin(img2)
        images.append(img)
    images.append(gifDuration)
    return images


def pump2Png(emoPng):
    img = emoPng.convert("RGBA")
    return pumpkin2(img)


def pump2Gif(emoGif):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    images = []
    for f in range(totalFrames):
        img2 = emoGif[f].copy().convert('RGBA')
        img = pumpkin2(img2)
        images.append(img)
    images.append(gifDuration)
    return images