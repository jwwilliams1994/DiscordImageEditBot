import math, random

from PIL import Image

sizerat = 1.6

# intens = -20
def process4headImage(emoImg, intens=84):
    intens = -intens
    w1, h1 = emoImg.size
    rat = w1 / h1
    emoImg = emoImg.convert("RGBA").copy().resize((round(100 * rat), 100), Image.LANCZOS)
    width, height = emoImg.size
    width2 = round(width * sizerat)
    height2 = round(height * sizerat)
    woff = round(width * ((sizerat-1)/2))
    hoff = round(height * ((sizerat-1)/2))
    # so b is pi*2/period
    # so offset = sin(b*dist)
    # if we want to do distance-from-center, period is diagonal distance, which is sqrt of height squared and width squared
    # distance from center would be sqrt of delta x squared plus delta y squared
    # delta x would be x minus half width, delta y would be y minus half height
    # offset would be along the slope line
    # yb = (math.pi*2)/(height)
    # yoffset = 0
    # xb = (math.pi*2)/(width)
    # xoffset = 0
    if intens <= 0:
        mod = 1.15
    else:
        mod = 1.1
    period = math.sqrt((width * width) + (height * height)) * mod
    B = (math.pi * 2) / period
    im1 = emoImg.load()
    canvas = Image.open("canvas.png").resize((width2, height2), Image.LANCZOS)
    im2 = canvas.load()
    for x in range(0, width2):
        for y in range(0, height2):
            # b = 2pi/period
            # yoff = y+(math.sin(b1*(y+offset1)))
            # yoff = round(math.sin(yb*y)*intens)
            # xoff = round(math.sin(xb*x)*intens)
            dx = (x - woff) - (width / 2)
            dy = (y - hoff) - (height / 2)
            angle = math.atan2(dy, dx)
            vect = math.sqrt((dx * dx) + (dy * dy))
            off = math.sin(vect * B) * intens
            xoff = math.cos(angle) * off
            yoff = math.sin(angle) * off
            yoff2 = y + yoff - hoff
            xoff2 = x + xoff - woff
            if yoff2 > 0 and yoff2 < height - 1 and xoff2 > 0 and xoff2 < width - 1:
                xrat = xoff2 % 1  # the result of this modulus is the amount over a whole value, and also the ratio to consider the second color
                yrat = yoff2 % 1
                xoff2 = math.floor(xoff2)
                yoff2 = math.floor(yoff2)
                r1, g1, b1, a1 = im1[xoff2, yoff2]
                r2, g2, b2, a2 = im1[xoff2 + 1, yoff2]
                r3, g3, b3, a3 = im1[xoff2, yoff2 + 1]
                r4, g4, b4, a4 = im1[xoff2 + 1, yoff2 + 1]
                r5 = round(((r1 * (1 - xrat)) + (r2 * xrat) + (r3 * (1 - yrat)) + (r4 * yrat)) / 2)
                g5 = round(((g1 * (1 - xrat)) + (g2 * xrat) + (g3 * (1 - yrat)) + (g4 * yrat)) / 2)
                b5 = round(((b1 * (1 - xrat)) + (b2 * xrat) + (b3 * (1 - yrat)) + (b4 * yrat)) / 2)
                a5 = round(((a1 * (1 - xrat)) + (a2 * xrat) + (a3 * (1 - yrat)) + (a4 * yrat)) / 2)
                # im2[x, y] = im1[xoff2, yoff2]
                im2[x, y] = (r5, g5, b5, a5)
            else:
                im2[x, y] = (0, 0, 0, 0)
    return canvas


def process4headGif(emoGif, intens=84):
    images = []
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    intens = -intens
    w1, h1 = emoGif[0].size
    rat = w1 / h1
    for f in range(0, totalFrames, 1):
        # print(f,"of",totalFrames)
        emoImg = emoGif[f].copy()
        emoImg = emoImg.resize((round(100 * rat), 100), Image.LANCZOS).convert("RGBA")
        width, height = emoImg.size
        width2 = round(width * sizerat)
        height2 = round(height * sizerat)
        woff = round(width * ((sizerat-1)/2))
        hoff = round(height * ((sizerat-1)/2))
        if intens <= 0:
            mod = 1.15
        else:
            mod = 1.1
        period = math.sqrt((width * width) + (height * height)) * mod
        B = (math.pi * 2) / period
        im1 = emoImg.load()
        canvas = Image.open("canvas.png").resize((width2, height2), Image.LANCZOS).convert("RGBA")
        # canvas = emoImg.copy().resize((width2, height2), Image.LANCZOS)
        # canvas = Image.new(mode="RGBA", size=(width2, height2), color=(0, 0, 0, 0))
        im2 = canvas.load()
        for x in range(0, width2):
            for y in range(0, height2):
                dx = (x - woff) - (width / 2)
                dy = (y - hoff) - (height / 2)
                angle = math.atan2(dy, dx)
                vect = math.sqrt((dx * dx) + (dy * dy))
                off = math.sin(vect * B) * intens
                xoff = math.cos(angle) * off
                yoff = math.sin(angle) * off
                yoff2 = y + yoff - hoff
                xoff2 = x + xoff - woff
                if yoff2 > 0 and yoff2 < height - 1 and xoff2 > 0 and xoff2 < width - 1:
                    # xrat = xoff2 % 1  # the result of this modulus is the amount over a whole value, and also the ratio to consider the second color
                    # yrat = yoff2 % 1
                    # xoff2 = math.floor(xoff2)
                    # yoff2 = math.floor(yoff2)
                    # r1, g1, b1, a1 = im1[xoff2, yoff2]
                    # r2, g2, b2, a2 = im1[xoff2 + 1, yoff2]
                    # r3, g3, b3, a3 = im1[xoff2, yoff2 + 1]
                    # r4, g4, b4, a4 = im1[xoff2 + 1, yoff2 + 1]
                    # r5 = round(((r1 * (1 - xrat)) + (r2 * xrat) + (r3 * (1 - yrat)) + (r4 * yrat)) / 2)
                    # g5 = round(((g1 * (1 - xrat)) + (g2 * xrat) + (g3 * (1 - yrat)) + (g4 * yrat)) / 2)
                    # b5 = round(((b1 * (1 - xrat)) + (b2 * xrat) + (b3 * (1 - yrat)) + (b4 * yrat)) / 2)
                    # a5 = round(((a1 * (1 - xrat)) + (a2 * xrat) + (a3 * (1 - yrat)) + (a4 * yrat)) / 2)
                    # if a5 < 255:
                    #     a5 = 0
                    im2[x, y] = im1[round(xoff2), round(yoff2)]
                    # im2[x, y] = (r5, g5, b5, a5)
                else:
                    im2[x, y] = (0, 0, 0, 0)
                    # im2[x, y] = (255)
                # if im2[x ,y] == (0):
                #     im2[x, y] = (255)
        images.append(canvas)
    images.append(gifDuration)
    return images


def processwormholeImage(emoImg):
    images = []
    w1, h1 = emoImg.size
    rat = w1 / h1
    emoImg = emoImg.convert("RGBA").copy().resize((round(100 * rat), 100), Image.LANCZOS)
    width, height = emoImg.size
    width2 = round(width * sizerat)
    height2 = round(height * sizerat)
    woff = round(width * ((sizerat-1)/2))
    hoff = round(height * ((sizerat-1)/2))
    mod = 1.15
    period = math.sqrt((width * width) + (height * height)) * mod
    B = (math.pi * 2) / period
    im1 = emoImg.load()
    canvas1 = Image.open("canvas.png").resize((width2, height2), Image.LANCZOS)
    for intens in range(80, -300, -1):
        canvas = canvas1.copy()
        im2 = canvas.load()
        for x in range(0, width2):
            for y in range(0, height2):
                dx = (x - woff) - (width / 2)
                dy = (y - hoff) - (height / 2)
                angle = math.atan2(dy, dx)
                vect = math.sqrt((dx * dx) + (dy * dy))
                off = math.sin(vect * B) * intens
                xoff = math.cos(angle) * off
                yoff = math.sin(angle) * off
                yoff2 = y + yoff - hoff
                xoff2 = x + xoff - woff
                if yoff2 > 0 and yoff2 < height - 1 and xoff2 > 0 and xoff2 < width - 1:
                    # xrat = xoff2 % 1  # the result of this modulus is the amount over a whole value, and also the ratio to consider the second color
                    # yrat = yoff2 % 1
                    # xoff2 = math.floor(xoff2)
                    # yoff2 = math.floor(yoff2)
                    # r1, g1, b1, a1 = im1[xoff2, yoff2]
                    # r2, g2, b2, a2 = im1[xoff2 + 1, yoff2]
                    # r3, g3, b3, a3 = im1[xoff2, yoff2 + 1]
                    # r4, g4, b4, a4 = im1[xoff2 + 1, yoff2 + 1]
                    # r5 = round(((r1 * (1 - xrat)) + (r2 * xrat) + (r3 * (1 - yrat)) + (r4 * yrat)) / 2)
                    # g5 = round(((g1 * (1 - xrat)) + (g2 * xrat) + (g3 * (1 - yrat)) + (g4 * yrat)) / 2)
                    # b5 = round(((b1 * (1 - xrat)) + (b2 * xrat) + (b3 * (1 - yrat)) + (b4 * yrat)) / 2)
                    # a5 = round(((a1 * (1 - xrat)) + (a2 * xrat) + (a3 * (1 - yrat)) + (a4 * yrat)) / 2)
                    im2[x, y] = im1[round(xoff2), round(yoff2)]
                    # im2[x, y] = (r5, g5, b5, a5)
                else:
                    im2[x, y] = (0, 0, 0, 0)
        images.append(canvas)
    images.append(20)
    return images


def processwormholeGif(emoGif):
    images = []
    w1, h1 = emoGif[0].size
    rat = w1 / h1
    # emoImg = emoImg.convert("RGBA").copy().resize((round(100*rat),100),Image.LANCZOS)
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    if type(gifDuration) is list:
        gifDuration = gifDuration[0]
    if gifDuration < 20:
        gifDuration = 100
    frame_ratio = 20 / gifDuration
    # width, height = emoGif.size
    width = round(100 * rat)
    height = 100
    width2 = round(width * sizerat)
    height2 = round(height * sizerat)
    woff = round(width * ((sizerat-1)/2))
    hoff = round(height * ((sizerat-1)/2))
    mod = 1.15
    period = math.sqrt((width * width) + (height * height)) * mod
    B = (math.pi * 2) / period
    # im1 = emoImg.load()
    canvas1 = Image.open("canvas.png").resize((width2, height2), Image.LANCZOS)
    for intens in range(80, -300, -1):
        framePick = int(math.floor((intens * frame_ratio) % totalFrames))
        emoImg = emoGif[framePick].copy().convert("RGBA").copy().resize((round(100 * rat), 100), Image.LANCZOS)
        im1 = emoImg.load()
        canvas = canvas1.copy()
        im2 = canvas.load()
        for x in range(0, width2):
            for y in range(0, height2):
                dx = (x - woff) - (width / 2)
                dy = (y - hoff) - (height / 2)
                angle = math.atan2(dy, dx)
                vect = math.sqrt((dx * dx) + (dy * dy))
                off = math.sin(vect * B) * intens
                xoff = math.cos(angle) * off
                yoff = math.sin(angle) * off
                yoff2 = y + yoff - hoff
                xoff2 = x + xoff - woff
                if yoff2 > 0 and yoff2 < height - 1 and xoff2 > 0 and xoff2 < width - 1:
                    # xrat = xoff2 % 1  # the result of this modulus is the amount over a whole value, and also the ratio to consider the second color
                    # yrat = yoff2 % 1
                    # xoff2 = math.floor(xoff2)
                    # yoff2 = math.floor(yoff2)
                    # r1, g1, b1, a1 = im1[xoff2, yoff2]
                    # r2, g2, b2, a2 = im1[xoff2 + 1, yoff2]
                    # r3, g3, b3, a3 = im1[xoff2, yoff2 + 1]
                    # r4, g4, b4, a4 = im1[xoff2 + 1, yoff2 + 1]
                    # r5 = round(((r1 * (1 - xrat)) + (r2 * xrat) + (r3 * (1 - yrat)) + (r4 * yrat)) / 2)
                    # g5 = round(((g1 * (1 - xrat)) + (g2 * xrat) + (g3 * (1 - yrat)) + (g4 * yrat)) / 2)
                    # b5 = round(((b1 * (1 - xrat)) + (b2 * xrat) + (b3 * (1 - yrat)) + (b4 * yrat)) / 2)
                    # a5 = round(((a1 * (1 - xrat)) + (a2 * xrat) + (a3 * (1 - yrat)) + (a4 * yrat)) / 2)
                    im2[x, y] = im1[round(xoff2), round(yoff2)]
                    # im2[x, y] = (r5, g5, b5, a5)
                else:
                    im2[x, y] = (0, 0, 0, 0)
        images.append(canvas)
    images.append(20)
    return images


def processSnapImage(emoImg):
    images = []
    w1, h1 = emoImg.size
    rat = w1 / h1
    emoImg = emoImg.convert("RGBA").copy()# .resize((round(100 * rat), 100), Image.LANCZOS)
    width, height = emoImg.size
    width2 = round(width)
    height2 = round(height)
    wedge = width2 - 1
    mod = 60
    im1 = emoImg.load()
    dur_arr = []
    for intens in range(0, 650, 1):
        if intens > 50:
            mod = 40
        if intens > 300:
            mod = 30
        if intens > 450:
            mod = 5
        for test in range(0, 2):
            # print(test)
            for x in range(width2-1, -1, -1):
                if intens < 50:
                    break
                try:
                    for i in range(0, width2):
                        if x-i < 0:
                            break
                        r, g, b, a = im1[x-i,i]
                        if a > 128:
                            im1[x-i,i] = (0, 0, 0, 0)
                            if x-i+1 > wedge:
                                break
                            if i-1 < 0:
                                break
                            im1[x-i+1,i-1] = (r, g, b, a)
                            if random.randint(0,100) < mod-test*25:
                                break
                except:
                    pass
            for y in range(1, height2):
                if intens < 50:
                    break
                try:
                    for i in range(0, height2):
                        if y+i > (height2 - 1):
                            break
                        r, g, b, a = im1[wedge-i, y+i]
                        if a > 128:
                            im1[wedge-i,y+i] = (0, 0, 0, 0)
                            if i-1 < 0:
                                break
                            if y+1 > 99:
                                break
                            im1[wedge-i+1,y+i-1] = (r, g, b, a)
                            if random.randint(0,100) < mod-test*25:
                                break
                except:
                    pass
        breaking = True
        for x in range(width2):
            for y in range(height2):
                r, g, b, a = im1[x, y]
                if a > 128:
                    breaking = False
                    break
        images.append(emoImg.copy())
        if breaking:
            break
    for i in images:
        dur_arr.append(20)
    dur_arr[-1] = 900
    print(dur_arr[-1])
    images.append(dur_arr)
    return images


def processSnapImage2(emoImg):
    # apList= [[]*100 for i in range(100)]
    apList = []
    pList = []
    images = []
    w1, h1 = emoImg.size
    rat = w1 / h1
    emoImg = emoImg.convert("RGBA").copy().resize((round(100 * rat), 100), Image.LANCZOS)
    width, height = emoImg.size
    aList = list(emoImg.getdata(3))
    # print(aList)
    # print(len(aList))
    wedge = width - 1
    mod = 60
    for y in range(0, height):
        ayList = []
        ypList = []
        for x in range(0, width):
            index = x+(y*100)
            # print(index)
            ypList.append([x,y])
            ayList.append(aList[index])
        pList.append(ypList)
        apList.append(ayList)
    im1 = emoImg.load()
    can = Image.open("canvas.png").resize((width,height))
    for intens in range(0, 650, 1):
        canvas = can.copy()
        if intens > 50:
            mod = 40
        if intens > 300:
            mod = 30
        if intens > 450:
            mod = 5
        for test in range(0, 2):
            # print(test)
            for x in range(wedge, -1, -1):
                if intens < 50:
                    break
                try:
                    for i in range(0, 100):
                        if x-i < 0:
                            break
                        # xy = pList[x-i][i]
                        xy = pList[i][x-i]
                        if xy != []:
                            # pList[x-i][i] = []
                            pList[i][x-i] = []
                            if x-i+1 > wedge:
                                break
                            if i-1 < 0:
                                break
                            try:
                                # pList[x-i+1][i-1] = xy
                                pList[i-1][x-i+1] = xy
                            except:
                                pass
                            if random.randint(0, 100) < mod - test * 25:
                                break
                except:
                    pass
            for y in range(1, 100):
                if intens < 50:
                    break
                try:
                    for i in range(0, 100):
                        if y+i > 99:
                            break
                        # xy = pList[wedge-i][y+i]
                        xy = pList[y+i][wedge-i]
                        if xy != []:
                            # pList[wedge-i][y+i] = []
                            pList[y+i][wedge-i] = []
                            if i-1 < 0:
                                break
                            if y+1 > 99:
                                break
                            try:
                                # pList[wedge-i+i][y+i-1] = xy
                                pList[y+i-1][wedge-i+1] = xy
                            except:
                                pass
                            if random.randint(0, 100) < mod - test * 25:
                                break
                except:
                    pass
        breaking = True
        im2 = canvas.load()
        for yp in range(0, height):
            for xp in range(0, width):
                xy = pList[yp][xp]
                if xy != []:
                    breaking = False
                    xg, yg = xy
                    im2[xp,yp] = im1[xg, yg]
                    if xp == 50 and yp == 50:
                        pass
                        # print(xp,yp,xg,yg)
                        # print(im2[xp,yp])
                        # print(im1[xg,yg])
        images.append(canvas)
        if breaking:
            break
    images.append(20)
    return images


def processSnapGif2(emoGif):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    if gifDuration < 20:
        gifDuration = 20
    frame_ratio = 20 / gifDuration
    pList = []
    images = []
    w1, h1 = emoGif[0].size
    rat = w1 / h1
    width = round(100 * rat)
    height = 100
    wedge = width - 1
    mod = 60
    for y in range(0, height):
        ypList = []
        for x in range(0, width):
            index = x+(y*100)
            ypList.append([x,y])
        pList.append(ypList)
    can = Image.open("canvas.png").resize((width,height))
    for intens in range(0, 650, 1):
        framePick = int(math.floor((intens * frame_ratio) % totalFrames))
        emoImg = emoGif[framePick].copy().convert("RGBA").resize((width,height),Image.LANCZOS)
        im1 = emoImg.load()
        canvas = can.copy()
        if intens > 50:
            mod = 40
        if intens > 300:
            mod = 30
        if intens > 450:
            mod = 5
        for test in range(0, 2):
            # print(test)
            for x in range(wedge, -1, -1):
                if intens < 50:
                    break
                try:
                    for i in range(0, 100):
                        if x-i < 0:
                            break
                        # xy = pList[x-i][i]
                        xy = pList[i][x-i]
                        if xy != []:
                            # pList[x-i][i] = []
                            pList[i][x-i] = []
                            if x-i+1 > wedge:
                                break
                            if i-1 < 0:
                                break
                            try:
                                # pList[x-i+1][i-1] = xy
                                pList[i-1][x-i+1] = xy
                            except:
                                pass
                            if random.randint(0, 100) < mod - test * 25:
                                break
                except:
                    pass
            for y in range(1, 100):
                if intens < 50:
                    break
                try:
                    for i in range(0, 100):
                        if y+i > 99:
                            break
                        # xy = pList[wedge-i][y+i]
                        xy = pList[y+i][wedge-i]
                        if xy != []:
                            # pList[wedge-i][y+i] = []
                            pList[y+i][wedge-i] = []
                            if i-1 < 0:
                                break
                            if y+1 > 99:
                                break
                            try:
                                # pList[wedge-i+i][y+i-1] = xy
                                pList[y+i-1][wedge-i+1] = xy
                            except:
                                pass
                            if random.randint(0, 100) < mod - test * 25:
                                break
                except:
                    pass
        im2 = canvas.load()
        for yp in range(0, height):
            for xp in range(0, width):
                xy = pList[yp][xp]
                if xy != []:
                    xg, yg = xy
                    im2[xp,yp] = im1[xg, yg]
                    if xp == 50 and yp == 50:
                        pass
                        # print(xp,yp,xg,yg)
                        # print(im2[xp,yp])
                        # print(im1[xg,yg])
        images.append(canvas)
    dur_arr = []
    for i in range(0, len(images)):
        if i < len(images):
            dur_arr.append(20)
        else:
            dur_arr.append(500)
    images.append(dur_arr)
    return images


def processSnapImage3(emoImg, testr, mod, mod2):
    # apList= [[]*100 for i in range(100)]
    apList = []
    pList = []
    images = []
    w1, h1 = emoImg.size
    rat = w1 / h1
    emoImg = emoImg.convert("RGBA").copy().resize((round(100 * rat), 100), Image.LANCZOS)
    width, height = emoImg.size
    aList = list(emoImg.getdata(3))
    # print(aList)
    # print(len(aList))
    wedge = width - 1
    # mod = 60
    if mod < 0:
        mod = 0
    if mod > 100:
        mod = 100
    for y in range(0, height):
        ayList = []
        ypList = []
        for x in range(0, width):
            index = x+(y*100)
            # print(index)
            ypList.append([x,y])
            ayList.append(aList[index])
        pList.append(ypList)
        apList.append(ayList)
    im1 = emoImg.load()
    can = Image.open("canvas.png").resize((width,height))
    if testr < 1:
        testr = 1
    if testr > 10:
        testr = 10
    if mod2 < 0:
        mod2 = 0
    if mod2 > 100:
        mod2 = 100
    for intens in range(0, 2600, 1):
        canvas = can.copy()
        # if intens > 50:
        #     mod = 40
        # if intens > 300:
        #     mod = 30
        # if intens > 450:
        #     mod = 5
        for test in range(0, testr):
            # print(test)
            for x in range(wedge, -1, -1):
                if intens < 50:
                    break
                try:
                    for i in range(0, 100):
                        if x-i < 0:
                            break
                        # xy = pList[x-i][i]
                        xy = pList[i][x-i]
                        if xy != []:
                            # pList[x-i][i] = []
                            pList[i][x-i] = []
                            if x-i+1 > wedge:
                                break
                            if i-1 < 0:
                                break
                            try:
                                # pList[x-i+1][i-1] = xy
                                pList[i-1][x-i+1] = xy
                            except:
                                pass
                            if random.randint(0, 100) < mod - test * mod2:
                                break
                except:
                    pass
            for y in range(1, 100):
                if intens < 50:
                    break
                try:
                    for i in range(0, 100):
                        if y+i > 99:
                            break
                        # xy = pList[wedge-i][y+i]
                        xy = pList[y+i][wedge-i]
                        if xy != []:
                            # pList[wedge-i][y+i] = []
                            pList[y+i][wedge-i] = []
                            if i-1 < 0:
                                break
                            if y+1 > 99:
                                break
                            try:
                                # pList[wedge-i+i][y+i-1] = xy
                                pList[y+i-1][wedge-i+1] = xy
                            except:
                                pass
                            if random.randint(0, 100) < mod - test * mod2:
                                break
                except:
                    pass
        im2 = canvas.load()
        breaking = True
        for yp in range(0, height):
            for xp in range(0, width):
                xy = pList[yp][xp]
                if xy != []:
                    breaking = False
                    xg, yg = xy
                    im2[xp,yp] = im1[xg, yg]
                    if xp == 50 and yp == 50:
                        pass
                        # print(xp,yp,xg,yg)
                        # print(im2[xp,yp])
                        # print(im1[xg,yg])
        if intens == 0:
            canvas.save("0frame.png")
        images.append(canvas)
        if breaking:
            break
    images.append(20)
    return images


def processSnapGif3(emoGif, testr, mod, mod2):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    if type(gifDuration) is list:
        gifDuration = gifDuration[0]
    if gifDuration < 20:
        gifDuration = 20
    frame_ratio = 20 / gifDuration
    pList = []
    images = []
    w1, h1 = emoGif[0].size
    rat = w1 / h1
    width = round(100 * rat)
    height = 100
    wedge = width - 1
    # mod = 60
    if mod < 0:
        mod = 0
    if mod > 100:
        mod = 100
    if testr < 1:
        testr = 1
    if testr > 10:
        testr = 10
    if mod2 < 0:
        mod2 = 0
    if mod2 > 100:
        mod2 = 100
    for y in range(0, height):
        ypList = []
        for x in range(0, width):
            index = x+(y*100)
            ypList.append([x,y])
        pList.append(ypList)
    can = Image.open("canvas.png").resize((width,height))
    for intens in range(0, 2600, 1):
        framePick = int(math.floor((intens * frame_ratio) % totalFrames))
        emoImg = emoGif[framePick].copy().convert("RGBA").resize((width,height),Image.LANCZOS)
        im1 = emoImg.load()
        canvas = can.copy()
        # if intens > 50:
        #     mod = 40
        # if intens > 300:
        #     mod = 30
        # if intens > 450:
        #     mod = 5
        for test in range(0, testr):
            # print(test)
            for x in range(wedge, -1, -1):
                if intens < 50:
                    break
                try:
                    for i in range(0, 100):
                        if x-i < 0:
                            break
                        # xy = pList[x-i][i]
                        xy = pList[i][x-i]
                        if xy != []:
                            # pList[x-i][i] = []
                            pList[i][x-i] = []
                            if x-i+1 > wedge:
                                break
                            if i-1 < 0:
                                break
                            try:
                                # pList[x-i+1][i-1] = xy
                                pList[i-1][x-i+1] = xy
                            except:
                                pass
                            if random.randint(0, 100) < mod - test * mod2:
                                break
                except:
                    pass
            for y in range(1, 100):
                if intens < 50:
                    break
                try:
                    for i in range(0, 100):
                        if y+i > 99:
                            break
                        # xy = pList[wedge-i][y+i]
                        xy = pList[y+i][wedge-i]
                        if xy != []:
                            # pList[wedge-i][y+i] = []
                            pList[y+i][wedge-i] = []
                            if i-1 < 0:
                                break
                            if y+1 > 99:
                                break
                            try:
                                # pList[wedge-i+i][y+i-1] = xy
                                pList[y+i-1][wedge-i+1] = xy
                            except:
                                pass
                            if random.randint(0, 100) < mod - test * mod2:
                                break
                except:
                    pass
        im2 = canvas.load()
        breaking = True
        for yp in range(0, height):
            for xp in range(0, width):
                xy = pList[yp][xp]
                if xy != []:
                    breaking = False
                    xg, yg = xy
                    im2[xp,yp] = im1[xg, yg]
                    if xp == 50 and yp == 50:
                        pass
                        # print(xp,yp,xg,yg)
                        # print(im2[xp,yp])
                        # print(im1[xg,yg])
        alpha = canvas.split()[3]
        images.append(canvas)
        if breaking:
            break
    images.append(20)
    return images


def processSnapImage4(emoImg, testr, mod, mod2):
    # apList= [[]*100 for i in range(100)]
    apList = []
    pList = []
    images = []
    w1, h1 = emoImg.size
    rat = w1 / h1
    emoImg = emoImg.convert("RGBA").copy().resize((round(100 * rat), 100), Image.LANCZOS)
    width, height = emoImg.size
    aList = list(emoImg.getdata(3))
    # print(aList)
    # print(len(aList))
    wedge = width - 1
    # mod = 60
    if mod < 0:
        mod = 0
    if mod > 100:
        mod = 100
    for y in range(0, height):
        ayList = []
        ypList = []
        for x in range(0, width):
            index = x+(y*100)
            # print(index)
            ypList.append([x,y])
            ayList.append(aList[index])
        pList.append(ypList)
        apList.append(ayList)
    im1 = emoImg.load()
    can = Image.open("canvas.png").resize((width,height))
    if testr < 1:
        testr = 1
    if testr > 200:
        testr = 200
    if mod2 < 0:
        mod2 = 0
    if mod2 > 100:
        mod2 = 100
    for intens in range(0, 2600, 1):
        canvas = can.copy()
        # if intens > 50:
        #     mod = 40
        # if intens > 300:
        #     mod = 30
        # if intens > 450:
        #     mod = 5
        for test in range(0, testr):
            # print(test)
            for x in range(wedge, -1, -1):
                try:
                    for i in range(0, 100):
                        if x-i < 0:
                            break
                        # xy = pList[x-i][i]
                        xy = pList[i][x-i]
                        if xy != []:
                            # pList[x-i][i] = []
                            pList[i][x-i] = []
                            if x-i+1 > wedge:
                                break
                            if i-1 < 0:
                                break
                            try:
                                # pList[x-i+1][i-1] = xy
                                pList[i-1][x-i+1] = xy
                            except:
                                pass
                            if random.randint(0, 100) < mod - test * mod2:
                                break
                except:
                    pass
            for y in range(1, 100):
                try:
                    for i in range(0, 100):
                        if y+i > 99:
                            break
                        # xy = pList[wedge-i][y+i]
                        xy = pList[y+i][wedge-i]
                        if xy != []:
                            # pList[wedge-i][y+i] = []
                            pList[y+i][wedge-i] = []
                            if i-1 < 0:
                                break
                            if y+1 > 99:
                                break
                            try:
                                # pList[wedge-i+i][y+i-1] = xy
                                pList[y+i-1][wedge-i+1] = xy
                            except:
                                pass
                            if random.randint(0, 100) < mod - test * mod2:
                                break
                except:
                    pass
        im2 = canvas.load()
        breaking = True
        for yp in range(0, height):
            for xp in range(0, width):
                xy = pList[yp][xp]
                if xy != []:
                    breaking = False
                    xg, yg = xy
                    im2[xp,yp] = im1[xg, yg]
                    if xp == 50 and yp == 50:
                        pass
                        # print(xp,yp,xg,yg)
                        # print(im2[xp,yp])
                        # print(im1[xg,yg])
        if intens == 0:
            canvas.save("0frame.png")
        images.append(canvas)
        if breaking:
            break
    images.append(20)
    return images


def processSnapGif4(emoGif, testr, mod, mod2):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    if type(gifDuration) is list:
        gifDuration = gifDuration[0]
    if gifDuration < 20:
        gifDuration = 20
    frame_ratio = 20 / gifDuration
    pList = []
    images = []
    w1, h1 = emoGif[0].size
    rat = w1 / h1
    width = round(100 * rat)
    height = 100
    wedge = width - 1
    # mod = 60
    if mod < 0:
        mod = 0
    if mod > 100:
        mod = 100
    if testr < 1:
        testr = 1
    if testr > 200:
        testr = 200
    if mod2 < 0:
        mod2 = 0
    if mod2 > 100:
        mod2 = 100
    for y in range(0, height):
        ypList = []
        for x in range(0, width):
            index = x+(y*100)
            ypList.append([x,y])
        pList.append(ypList)
    can = Image.open("canvas.png").resize((width,height))
    for intens in range(0, 2600, 1):
        framePick = int(math.floor((intens * frame_ratio) % totalFrames))
        emoImg = emoGif[framePick].copy().convert("RGBA").resize((width,height),Image.LANCZOS)
        im1 = emoImg.load()
        canvas = can.copy()
        # if intens > 50:
        #     mod = 40
        # if intens > 300:
        #     mod = 30
        # if intens > 450:
        #     mod = 5
        for test in range(0, testr):
            # print(test)
            for x in range(wedge, -1, -1):
                try:
                    for i in range(0, 100):
                        if x-i < 0:
                            break
                        # xy = pList[x-i][i]
                        xy = pList[i][x-i]
                        if xy != []:
                            # pList[x-i][i] = []
                            pList[i][x-i] = []
                            if x-i+1 > wedge:
                                break
                            if i-1 < 0:
                                break
                            try:
                                # pList[x-i+1][i-1] = xy
                                pList[i-1][x-i+1] = xy
                            except:
                                pass
                            if random.randint(0, 100) < mod - test * mod2:
                                break
                except:
                    pass
            for y in range(1, 100):
                try:
                    for i in range(0, 100):
                        if y+i > 99:
                            break
                        # xy = pList[wedge-i][y+i]
                        xy = pList[y+i][wedge-i]
                        if xy != []:
                            # pList[wedge-i][y+i] = []
                            pList[y+i][wedge-i] = []
                            if i-1 < 0:
                                break
                            if y+1 > 99:
                                break
                            try:
                                # pList[wedge-i+i][y+i-1] = xy
                                pList[y+i-1][wedge-i+1] = xy
                            except:
                                pass
                            if random.randint(0, 100) < mod - test * mod2:
                                break
                except:
                    pass
        im2 = canvas.load()
        breaking = True
        for yp in range(0, height):
            for xp in range(0, width):
                xy = pList[yp][xp]
                if xy != []:
                    breaking = False
                    xg, yg = xy
                    im2[xp,yp] = im1[xg, yg]
                    if xp == 50 and yp == 50:
                        pass
                        # print(xp,yp,xg,yg)
                        # print(im2[xp,yp])
                        # print(im1[xg,yg])
        images.append(canvas)
        if breaking:
            break
    images.append(20)
    return images
