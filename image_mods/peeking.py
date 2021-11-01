import math

from PIL import Image

stages = [100,200,300,400]
def peekingImage(emoPng):
    images = []
    emoPng = emoPng.convert("RGBA")
    width, height = emoPng.size
    wRatio = width / height
    width = round(wRatio * 100)
    height = 100
    emoPng = emoPng.resize((width, height), Image.LANCZOS)
    blank = Image.new(mode="RGBA", size=(width, height*2), color=(0, 0, 0, 0))
    yoff = height
    yref = 0
    print("starting loop")
    stage = 0
    for f in range(0,400):
        if f > stages[stage]:
            stage += 1
        if stage > 3:
            stage = 3
        if stage%2 == 0:
            yv = -2
        else:
            yv = 6
        if stage > 1:
            limit = -height
        else:
            limit = -round(height/2)
        yref += yv
        if yref < limit:
            yref = limit
        if yref > 0:
            yref = 0
        # print(stage,yv,yref)
        canvas = blank.copy()
        img = emoPng.copy()
        yr = round(yoff + yref)
        if yr < 0:
            yr = 0
        canvas.alpha_composite(img, (0, yr))
        canvas = canvas.crop((0, 0, width, height))
        images.append(canvas)
    images.append(20)
    return images


def peekingGif(emoGif):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    if type(gifDuration) is list:
        gifDuration = gifDuration[0]
    if gifDuration < 20:
        gifDuration = 20
    frame_ratio = 20 / gifDuration
    print("starting")
    images = []
    # emoPng = emoPng.convert("RGBA")
    width, height = emoGif[0].size
    wRatio = width / height
    width = round(wRatio * 100)
    height = 100
    # emoPng = emoPng.resize((width, height), Image.LANCZOS)
    blank = Image.new(mode="RGBA", size=(width, height*2), color=(0, 0, 0, 0))
    yoff = height
    yref = 0
    print("starting loop")
    stage = 0
    for f in range(0,400):
        framePick = int(math.floor((f * frame_ratio) % totalFrames))
        emoPng = emoGif[framePick].copy().convert("RGBA").resize((width, height), Image.LANCZOS)
        if f > stages[stage]:
            stage += 1
        if stage > 3:
            stage = 3
        if stage%2 == 0:
            yv = -2
        else:
            yv = 6
        if stage > 1:
            limit = -height
        else:
            limit = -round(height/2)
        yref += yv
        if yref < limit:
            yref = limit
        if yref > 0:
            yref = 0
        # print(stage,yv,yref)
        canvas = blank.copy()
        img = emoPng.copy()
        yr = round(yoff + yref)
        if yr < 0:
            yr = 0
        canvas.alpha_composite(img, (0, yr))
        canvas = canvas.crop((0, 0, width, height))
        images.append(canvas)
    images.append(20)
    return images


def peekingImage2(emoPng, intensity):
    print("starting")
    images = []
    emoPng = emoPng.convert("RGBA")
    width, height = emoPng.size
    wRatio = width / height
    width = round(wRatio * 100)
    height = 100
    emoPng = emoPng.resize((width, height), Image.LANCZOS)
    blank = Image.new(mode="RGBA", size=(width, height*2), color=(0, 0, 0, 0))
    yoff = height
    yref = 0
    print("starting loop")
    stage = 0
    for f in range(0,200):
        if f > stages[stage]:
            stage += 1
        if stage > 3:
            stage = 3
        if stage%2 == 0:
            yv = -2
        else:
            yv = 6
        if stage > 1:
            limit = -height
        else:
            limit = -round(height*(intensity))
        yref += yv
        if yref < limit:
            yref = limit
        if yref > 0:
            yref = 0
        # print(stage,yv,yref)
        canvas = blank.copy()
        img = emoPng.copy()
        yr = round(yoff + yref)
        if yr < 0:
            yr = 0
        canvas.alpha_composite(img, (0, yr))
        canvas = canvas.crop((0, 0, width, height))
        images.append(canvas)
    images.append(20)
    return images


def peekingGif2(emoGif, intensity):
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    if type(gifDuration) is list:
        gifDuration = gifDuration[0]
    if gifDuration < 20:
        gifDuration = 20
    frame_ratio = 20 / gifDuration
    print("starting")
    images = []
    # emoPng = emoPng.convert("RGBA")
    width, height = emoGif.size
    wRatio = width / height
    width = round(wRatio * 100)
    height = 100
    # emoPng = emoPng.resize((width, height), Image.LANCZOS)
    blank = Image.new(mode="RGBA", size=(width, height*2), color=(0, 0, 0, 0))
    yoff = height
    yref = 0
    print("starting loop")
    stage = 0
    for f in range(0,200):
        framePick = int(math.floor((f * frame_ratio) % totalFrames))
        emoPng = emoGif[framePick].copy().convert("RGBA").resize((width, height), Image.LANCZOS)
        if f > stages[stage]:
            stage += 1
        if stage > 3:
            stage = 3
        if stage%2 == 0:
            yv = -2
        else:
            yv = 6
        if stage > 1:
            limit = -height
        else:
            limit = -round(height*(intensity))
        yref += yv
        if yref < limit:
            yref = limit
        if yref > 0:
            yref = 0
        # print(stage,yv,yref)
        canvas = blank.copy()
        img = emoPng.copy()
        yr = round(yoff + yref)
        if yr < 0:
            yr = 0
        canvas.alpha_composite(img, (0, yr))
        canvas = canvas.crop((0, 0, width, height))
        images.append(canvas)
    images.append(20)
    return images