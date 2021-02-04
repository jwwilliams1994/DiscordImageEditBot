import math, datetime
import colorsys
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import requests, io, numpy, random


def clamp(inp, low, high):
    out = 0
    if inp < low:
        out = low
    elif inp > high:
        out = high
    else:
        out = inp
    return int(math.floor(out))


def clamp2(inp, low, high):
    out = 0
    if inp < low:
        out = low
    elif inp > high:
        out = high
    else:
        out = inp
    return out


def curve(xo, yo, curv):
    xo = (xo * 2) - 1
    yo = (yo * 2) - 1
    xo2 = abs(yo) / curv
    yo2 = abs(xo) / curv
    xo = xo + (xo * xo2 * xo2)
    yo = yo + (yo * yo2 * yo2)
    xo = (xo * 0.5) + 0.5
    yo = (yo * 0.5) + 0.5
    return xo, yo


def sli(uv, res, opacity):
    intens = math.sin(uv * res * math.pi * 2)
    intens = ((0.5 * intens) + 0.5) * 0.9 + 0.1
    return math.pow(intens, opacity)


def pad(inp, rat):
    wid, hit = inp.size
    inp = inp.resize((round(wid * (1 + rat)), round(hit * (1 + rat))), Image.LANCZOS)
    canv = Image.new('RGBA', (round(wid * (1 + (rat * 2))), round(hit * (1 + (rat * 2)))), (30, 30, 30, 255))
    wid2, hit2 = canv.size
    wid, hit = inp.size
    canv.alpha_composite(inp, (round((wid2 - wid)/2), round((hit2 - hit)/2)))
    return canv


def pada(inp, r, g, b, a, rat):
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


# def VI(x, y, width, height, opacity):
#     i = x * y * (1 - x) * (1 - y)
#     i = clamp()


def crt(inp, widt, heit, noise):
    inp = pad(inp.convert('RGBA'), 0)
    width, height = round((widt)/4), round((heit)/4)
    width2, height2 = inp.size
    # canv = Image.new('RGBA', (width2, height2), (30, 30, 30, 255))
    # inp = inp.resize((round(width2*0.6), round(height2*0.6)), Image.LANCZOS)
    # canv.alpha_composite(inp, (round(width2*0.2), round(height2*0.2)))
    wratio1 = height / width
    wratio2 = height2 / width2
    img2 = inp.convert('RGBA')
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
    if noise > 0:
        xd, yd = img2.size
        nl = img2.load()
        for x in range(xd):
            for y in range(yd):
                nadd = random.randint(-noise, noise)
                r, g, b, a = nl[x, y]
                r = clamp(r + nadd, 0, 255)
                g = clamp(g + nadd, 0, 255)
                b = clamp(b + nadd, 0, 255)
                nl[x, y] = r, g, b, a
    input = img2.resize((widt, heit), Image.BILINEAR)
    screen = Image.new('RGB', (widt, heit), (40, 40, 40))
    inl = input.load()
    scl = screen.load()
    for x in range(widt):
        for y in range(heit):
            xu = (x+0.5) / widt
            yu = (y+0.5) / heit
            curv = 3
            xi, yi = curve(xu, yu, curv)
            pi = xu * yu * (1 - xu) * (1 - yu)
            pi = clamp2(math.pow((widt / 4) * pi, 1.2), 0, 1)
            # xsi = math.sin((xi) * heit * math.pi * 2)
            # xsi = (((0.5 * xsi) + 0.5) * 0.9) + 0.1
            # ysi = math.sin((yi) * widt * math.pi * 2)
            # ysi = (((0.5 * ysi) + 0.5) * 0.9) + 0.1
            xsi = sli(xi, (heit/4), 0.5)
            ysi = sli(yi, (widt/4), 0.5)
            if 1 > xi > 0 and 1 > yi > 0:
                r, g, b, a = inl[widt*xi, heit*yi]
                r = round(r * pi * pi * xsi * ysi * 1.2)
                g = round(g * pi * pi * xsi * ysi * 1.2)
                b = round(b * pi * pi * xsi * ysi * 1.2)
                a = 255
                scl[x, y] = r, g, b
            else:
                scl[x, y] = 0, 0, 0
    screen = screen.filter(ImageFilter.GaussianBlur(radius=0.5))
    screen = ImageEnhance.Brightness(screen).enhance(1.4)
    screen = ImageEnhance.Contrast(screen).enhance(1.2)
    return screen


def cathodePng(img, ex, ey, emojiId):
    image = crt(img, ex, ey, 0)
    image.save(str(emojiId) + "crt.png")
    return str(emojiId) + "crt.png"


def cathodeGif(img, ex, ey, emojiId):
    totalFrames = img.n_frames
    gifDuration = img.info['duration']
    images = []
    for f in range(totalFrames):
        img.seek(f)
        inp = img.copy()
        out = crt(inp, ex, ey, 0)
        out = out.quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        images.append(out)
    images[0].save(str(emojiId) + 'crt.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, disposal=2)
    return str(emojiId) + 'crt.gif'


def cathodePng2(img, ex, ey, noise, emojiId):
    images = []
    for f in range(10):
        image = crt(img, ex, ey, noise)
        image = image.quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        images.append(image)
    images[0].save(str(emojiId) + 'crt.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, disposal=2)
    return str(emojiId) + 'crt.gif'


def cathodeGif2(img, ex, ey, noise, emojiId):
    totalFrames = img.n_frames
    gifDuration = img.info['duration']
    images = []
    for f in range(totalFrames):
        img.seek(f)
        inp = img.copy()
        out = crt(inp, ex, ey, noise)
        out = out.quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        images.append(out)
    images[0].save(str(emojiId) + 'crt.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, disposal=2)
    return str(emojiId) + 'crt.gif'


def paddingPng(img, r, g, b, a, rat, emojiId):
    img = img.convert('RGBA')
    img = pada(img, r, g, b, a, rat)
    img.save(str(emojiId) + 'pad.png')
    return str(emojiId) + 'pad.png'


def paddingGif(img, r, g, b, a, rat, emojiId):
    totalFrames = img.n_frames
    gifDuration = img.info['duration']
    images = []
    for f in range(totalFrames):
        img.seek(f)
        im = img.copy()
        im = im.convert('RGBA')
        im = pada(im, r, g, b, a, rat)
        if a == 255:
            im = im.convert('RGB').quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        else:
            alpha = im.split()[3]
            im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
            mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            im.paste(255, mask)
        images.append(im)
    images[0].save(str(emojiId) + 'pad.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, disposal=2)
    return str(emojiId) + 'pad.gif'


def crtd(inp, widt, heit, offset):
    inp = inp.convert('RGBA')
    width, height = round((widt)/4), round((heit)/4)
    width2, height2 = inp.size
    wratio1 = height / width
    wratio2 = height2 / width2
    img2 = inp.convert('RGBA')
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
    input = img2.resize((widt, heit), Image.BILINEAR)
    screen = Image.new('RGB', (widt, heit), (40, 40, 40))
    inl = input.load()
    scl = screen.load()
    for x in range(widt):
        for y in range(heit):
            xu = (x+0.5) / widt
            yu = (y+0.5) / heit
            curv = 3
            xi, yi = curve(xu, yu, curv)
            # pi = xu * yu * (1 - xu) * (1 - yu)
            # pi = clamp(math.pow((widt / 4) * pi, 1.5), 0, 1)
            if 1 > xi > 0 and 1 > yi > 0:
                r, g, b, a = inl[widt*xi, heit*yi]
                # r = round(r * (pi * pi) * xsi * ysi * 1.2 * (a/255))
                # g = round(g * (pi * pi) * xsi * ysi * 1.2 * (a/255))
                # b = round(b * (pi * pi) * xsi * ysi * 1.2 * (a/255))
                r = round(r)
                g = round(g)
                b = round(b)
                a = 255
                scl[x, y] = r, g, b
            else:
                ar, ag, ab = colorsys.hsv_to_rgb((280/360)-offset, 255, 255)
                scl[x, y] = math.floor(ar), math.floor(ag), math.floor(ab)
    # screen = screen.filter(ImageFilter.GaussianBlur(radius=0.5))
    # screen = ImageEnhance.Brightness(screen).enhance(1.4)
    # screen = ImageEnhance.Contrast(screen).enhance(1.2)
    return screen


def crtdepth(wid, hit, offset, emojiId='0'):
    if emojiId == '0':
        emojiId = offset
        offset = 0
    offset = clamp(offset, 0, 75)
    wid = int(wid)
    hit = int(hit)
    img = Image.new("HSV", (wid, hit), (0, 0, 255))
    il = img.load()
    width, height = img.size
    arr = []
    r = 30
    for i in range(-400, 401):
        theta = ((i / 10) / 180) * math.pi
        x = math.sin(theta) * r
        d = math.cos(theta) * r
        arr.append([x, d])
    darr = []
    mid = round(len(arr) / 2)
    depth = arr[mid][1] - arr[0][1]
    doff = arr[mid][1] - depth
    max = 64
    dratio = max / depth

    xdist = abs(arr[0][0] - arr[-1][0])
    xratio = (width) / (xdist)
    print(xdist, xratio)
    for y in range(height):
        for i in arr:
            x = clamp((i[0] * xratio) + (width / 2), 0, width - 1)
            depth = i[-1] - doff
            depth = depth * dratio
            if clamp(depth, 0, 255) > il[x, y][0]:
                h, s, v = il[x, y]
                il[x, y] = clamp(depth + 64, 0, 255), s, v
    xdist = abs(arr[0][0] - arr[-1][0])
    yratio = (height) / (xdist)
    print(xdist, xratio)
    for x in range(width):
        for i in arr:
            y = clamp((i[0] * yratio) + (height / 2), 0, height - 1)
            depth = i[-1] - doff
            depth = depth * dratio
            if clamp(depth, 0, 255) > il[x, y][1]:
                h, s, v = il[x, y]
                il[x, y] = h, clamp(depth + 64, 0, 255), v
    for x in range(width):
        for y in range(height):
            h, s, v = il[x, y]
            h = 180 - math.floor((h + s) / 2) - offset
            il[x, y] = h, 255, 255
    img = img.convert('RGB')
    img = crtd(img, *img.size, offset)
    img.save(str(emojiId) + 'depth.png')
    return str(emojiId) + 'depth.png'
