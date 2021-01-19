import math, random

from PIL import Image

sizerat = 1.6

# intens = -20
def process4headImage(emoImg, intens, emojiId):
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
    canvas.save(str(emojiId) + "pp4head.png")
    return str(emojiId) + "pp4head.png"


def process4headGif(emoGif, intens, emojiId):
    images = []
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    intens = -intens
    w1, h1 = emoGif.size
    rat = w1 / h1
    for f in range(0, totalFrames, 1):
        # print(f,"of",totalFrames)
        emoGif.seek(f)
        emoImg = emoGif.copy()
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
        alpha = canvas.split()[3]
        canvas = canvas.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canvas.paste(255, mask)
        canvas.convert("P")
        images.append(canvas)
    images[0].save(str(emojiId) + 'pp4head.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + "pp4head.gif"


def processwormholeImage(emoImg, emojiId):
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
        alpha = canvas.split()[3]
        canvas = canvas.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canvas.paste(255, mask)
        images.append(canvas)
    images[0].save(str(emojiId) + 'wormhole.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + "wormhole.gif"


def processwormholeGif(emoGif, emojiId):
    images = []
    w1, h1 = emoGif.size
    rat = w1 / h1
    # emoImg = emoImg.convert("RGBA").copy().resize((round(100*rat),100),Image.LANCZOS)
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
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
        emoGif.seek(framePick)
        emoImg = emoGif.copy().convert("RGBA").copy().resize((round(100 * rat), 100), Image.LANCZOS)
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
        alpha = canvas.split()[3]
        canvas = canvas.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canvas.paste(255, mask)
        images.append(canvas)
    images[0].save(str(emojiId) + 'wormhole2.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + "wormhole2.gif"

def processSnapImage(emoImg, emojiId):
    images = []
    w1, h1 = emoImg.size
    rat = w1 / h1
    emoImg = emoImg.convert("RGBA").copy().resize((round(100 * rat), 100), Image.LANCZOS)
    width, height = emoImg.size
    width2 = round(width)
    height2 = round(height)
    wedge = width2 - 1
    mod = 60
    im1 = emoImg.load()
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
                    for i in range(0, 100):
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
            for y in range(1, 100):
                if intens < 50:
                    break
                try:
                    for i in range(0, 100):
                        if y+i > 99:
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
        canvas = emoImg
        alpha = canvas.split()[3]
        canvas2 = canvas.copy().convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canvas2.paste(255, mask)
        images.append(canvas2)
        if breaking:
            break
    images[0].save(str(emojiId) + 'snap.gif', save_all=True, append_images=images[1:], duration=20, optimize=False, transparency=255, disposal=2)
    return str(emojiId) + "snap.gif"

def processSnapImage2(emoImg, emojiId):
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
        if intens == 0:
            canvas.save("0frame.png")
        alpha = canvas.split()[3]
        canvas2 = canvas.copy().convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canvas2.paste(255, mask)
        images.append(canvas2)
        if breaking:
            break
    images[0].save(str(emojiId) + 'snap2.gif', save_all=True, append_images=images[1:], duration=20, optimize=False, transparency=255, disposal=2)
    return str(emojiId) + "snap2.gif"

def processSnapGif2(emoGif, emojiId):
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    if gifDuration < 20:
        gifDuration = 20
    frame_ratio = 20 / gifDuration
    pList = []
    images = []
    w1, h1 = emoGif.size
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
        emoGif.seek(framePick)
        emoImg = emoGif.copy().convert("RGBA").resize((width,height),Image.LANCZOS)
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
        alpha = canvas.split()[3]
        canvas2 = canvas.copy().convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canvas2.paste(255, mask)
        images.append(canvas2)
    images[0].save(str(emojiId) + 'snap2.gif', save_all=True, append_images=images[1:], duration=20, optimize=False, transparency=255, disposal=2)
    return str(emojiId) + "snap2.gif"

def processSnapImage3(emoImg, testr, mod, mod2, emojiId):
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
        alpha = canvas.split()[3]
        canvas2 = canvas.copy().convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canvas2.paste(255, mask)
        images.append(canvas2)
        if breaking:
            break
    images[0].save(str(emojiId) + 'snap2.gif', save_all=True, append_images=images[1:], duration=20, optimize=False, transparency=255, disposal=2)
    return str(emojiId) + "snap2.gif"

def processSnapGif3(emoGif, testr, mod, mod2, emojiId):
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    if gifDuration < 20:
        gifDuration = 20
    frame_ratio = 20 / gifDuration
    pList = []
    images = []
    w1, h1 = emoGif.size
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
        emoGif.seek(framePick)
        emoImg = emoGif.copy().convert("RGBA").resize((width,height),Image.LANCZOS)
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
        canvas2 = canvas.copy().convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canvas2.paste(255, mask)
        images.append(canvas2)
        if breaking:
            break
    images[0].save(str(emojiId) + 'snap2.gif', save_all=True, append_images=images[1:], duration=20, optimize=False, transparency=255, disposal=2)
    return str(emojiId) + "snap2.gif"

def processSnapImage4(emoImg, testr, mod, mod2, emojiId):
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
        alpha = canvas.split()[3]
        canvas2 = canvas.copy().convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canvas2.paste(255, mask)
        images.append(canvas2)
        if breaking:
            break
    images[0].save(str(emojiId) + 'snap2.gif', save_all=True, append_images=images[1:], duration=20, optimize=False, transparency=255, disposal=2)
    return str(emojiId) + "snap2.gif"

def processSnapGif4(emoGif, testr, mod, mod2, emojiId):
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    if gifDuration < 20:
        gifDuration = 20
    frame_ratio = 20 / gifDuration
    pList = []
    images = []
    w1, h1 = emoGif.size
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
        emoGif.seek(framePick)
        emoImg = emoGif.copy().convert("RGBA").resize((width,height),Image.LANCZOS)
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
        alpha = canvas.split()[3]
        canvas2 = canvas.copy().convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canvas2.paste(255, mask)
        images.append(canvas2)
        if breaking:
            break
    images[0].save(str(emojiId) + 'snap2.gif', save_all=True, append_images=images[1:], duration=20, optimize=False, transparency=255, disposal=2)
    return str(emojiId) + "snap2.gif"

if __name__ == '__main__':
    testy = Image.open("testem.png")
    print(processSnapImage2(testy, "98"))
