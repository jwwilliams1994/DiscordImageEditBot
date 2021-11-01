import math, datetime
import colorsys
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import requests, io, numpy, random


def ups(im, t):
    h, w = im.size
    cv = Image.new('RGBA', (h * t, w * t), (0, 0, 0, 0))
    for x in range(t):
        for y in range(t):
            cv.paste(im, (h * x, w * y))
    return cv


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
    canv = Image.new('RGBA', (round(wid * (1 + (rat * 2))), round(hit * (1 + (rat * 2)))), (15, 15, 15, 255))
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


def crt(inp, widt, heit, noise, curv=3, opac=1.2):
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
            xi, yi = curve(xu, yu, curv)
            pi = xu * yu * (1 - xu) * (1 - yu)
            pi = clamp2(math.pow((widt / 4) * pi, opac), 0, 1)
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


def cathodePng(img, ex, ey):
    image = crt(img, ex, ey, 0)
    return image


def cathodeGif(img, ex, ey):
    totalFrames = len(img) - 1
    gifDuration = img[-1]
    images = []
    for f in range(totalFrames):
        inp = img[f].copy()
        out = crt(inp, ex, ey, 0)
        #out = out.quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        images.append(out)
    images.append(gifDuration)
    return images


def cathodePng2(img, ex, ey, noise):
    images = []
    for f in range(10):
        image = crt(img, ex, ey, noise)
        #image = image.quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        images.append(image)
    images.append(20)
    return images


def cathodeGif2(img, ex, ey, noise):
    totalFrames = len(img) - 1
    gifDuration = img[-1]
    images = []
    for f in range(totalFrames):
        inp = img[f].copy()
        out = crt(inp, ex, ey, noise)
        #out = out.quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        images.append(out)
    images.append(gifDuration)
    return images


def paddingPng(img, r, g, b, a, rat):
    img = img.convert('RGBA')
    img = pada(img, r, g, b, a, rat)
    return img


def paddingGif(img, r, g, b, a, rat):
    totalFrames = len(img) - 1
    gifDuration = img[-1]
    images = []
    for f in range(totalFrames):
        im = img[f].copy().convert('RGBA')
        im = pada(im, r, g, b, a, rat)
        images.append(im)
    images.append(gifDuration)
    return images


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


def crtdepth(wid, hit, offset):
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
    return img


def cathodePng3(img, ex, ey, noise, curv, opac):
    images = []
    if noise > 0:
        for f in range(10):
            image = crt(img, ex, ey, noise, curv, opac)
            #image = image.quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
            images.append(image)
        images.append(20)
        return images
    else:
        image = crt(img, ex, ey, noise, curv, opac)
        return image


def cathodeGif3(img, ex, ey, noise, curv, opac):
    totalFrames = len(img) - 1
    gifDuration = img[-1]
    images = []
    for f in range(totalFrames):
        inp = img[f].copy()
        out = crt(inp, ex, ey, noise, curv, opac)
        #out = out.quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        images.append(out)
    images.append(gifDuration)
    return images


def crt2(inp, widt, heit, res=3, noise=0, curv=3, opac=1.2):
    # img2 = Image.open("decomp/pepehands.png").convert('RGBA')
    inp = pad(inp, 0)
    if noise > 0:
        xd, yd = inp.size
        nl = inp.load()
        for x in range(xd):
            for y in range(yd):
                nadd = random.randint(-noise, noise)
                r, g, b, a = nl[x, y]
                r = clamp(r + nadd, 0, 255)
                g = clamp(g + nadd, 0, 255)
                b = clamp(b + nadd, 0, 255)
                nl[x, y] = r, g, b, a
    mk = Image.open("TileableLinearSlotMaskTall15Wide9And4d5Horizontal9d14VerticalSpacing.png").convert('RGBA')
    h, w = mk.size
    mk = ups(mk, res)
    h, w = inp.size
    inp = inp.resize((h * 4, w * 4), Image.LANCZOS)
    mk = mk.resize(inp.size, Image.LANCZOS)
    il2 = inp.load()
    il = mk.load()
    w, h = mk.size
    for x in range(w):
        for y in range(h):
            r, g, b, a = il[x, y]
            r2, g2, b2, a2 = il2[x, y]
            r3 = round(r2 * (r / 255) * (a2 / 255))
            g3 = round(g2 * (g / 255) * (a2 / 255))
            b3 = round(b2 * (b / 255) * (a2 / 255))
            il[x, y] = (r3, g3, b3, a)
    inp = mk.copy()
    width, height = round((widt)/1), round((heit)/1)
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
    widt = widt * 3
    heit = heit * 3
    input = img2.resize((widt, heit), Image.LANCZOS)
    screen = Image.new('RGB', (widt, heit), (30, 30, 30))
    inl = input.load()
    scl = screen.load()
    for x in range(widt):
        for y in range(heit):
            xu = (x+0.5) / widt
            yu = (y+0.5) / heit
            xi, yi = curve(xu, yu, curv)
            pi = xu * yu * (1 - xu) * (1 - yu)
            pi = clamp2(pow((widt / 4) * pi, opac), 0, 1)
            if 1 > xi > 0 and 1 > yi > 0:
                r, g, b, a = inl[widt*xi, heit*yi]
                r = round(r * pi * pi * 1.2)
                g = round(g * pi * pi * 1.2)
                b = round(b * pi * pi * 1.2)
                a = 255
                scl[x, y] = r, g, b
            else:
                scl[x, y] = 0, 0, 0
    widt = round(widt / 3)
    heit = round(heit / 3)
    screen = screen.resize((widt, heit))
    screen = screen.filter(ImageFilter.GaussianBlur(radius=0.1))
    screen = ImageEnhance.Brightness(screen).enhance(1.4)
    screen = ImageEnhance.Contrast(screen).enhance(1.2)
    return screen


def cathodePng4(img, ex, ey, res=4, noise=0):
    image = crt2(img, ex, ey, res, noise)
    return image


def cathodeGif4(img, ex, ey, res=4, noise=0):
    totalFrames = len(img) - 1
    gifDuration = img[-1]
    images = []
    for f in range(totalFrames):
        inp = img[f].copy().convert('RGBA')
        out = crt2(inp, ex, ey, res, noise)
        #out = out.quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        images.append(out)
    images.append(gifDuration)
    return images


def ntsc(img, amp=1):
    img = img.convert('RGBA')
    ic = img.resize((round(img.size[0] / 2), img.size[1])).copy()
    cl = ic.load()
    i_arr = []
    q_arr = []
    ia = []
    qa = []
    for x in range(ic.size[0]):
        for y in range(ic.size[1]):
            r, g, b, a = cl[x, y]
            l, i, q = colorsys.rgb_to_yiq(r * (a / 255) / 255, g * (a / 255) / 255, b * (a / 255) / 255)
            ia.append(i)
            qa.append(q)
        i_arr.append(ia)
        q_arr.append(qa)
        ia = []
        qa = []
    img = img.convert("L")
    cv = Image.new("RGB", img.size, (0, 0, 0))
    il = img.load()
    cl = cv.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            l = il[x, y]
            i = i_arr[math.floor(clamp2(x / 2 + (ic.size[0] * 0.02 * amp), 0, len(i_arr)-1))][y]
            q = q_arr[math.floor(clamp2(x / 2 + (ic.size[0] * -0.02 * amp), 0, len(i_arr)-1))][y]
            r, g, b = colorsys.yiq_to_rgb(l/255, i, q)
            r = round(r * 255)
            g = round(g * 255)
            b = round(b * 255)
            cl[x, y] = (r, g, b)
    return cv


def ntscPng(img, amp):
    image = ntsc(img, amp).convert('RGBA')
    return image


def ntscGif(img, amp):
    totalFrames = len(img) - 1
    gifDuration = img[-1]
    images = []
    for f in range(totalFrames):
        inp = img[f].copy().convert('RGBA')
        out = ntsc(inp, amp)
        images.append(out)
    images.append(gifDuration)
    return images