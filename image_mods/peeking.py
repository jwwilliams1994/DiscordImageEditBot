import math

from PIL import Image

stages = [100,200,300,400]
def peekingImage(emoPng, emojiId):
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
        alpha = canvas.split()[3]
        canvas = canvas.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canvas.paste(255, mask)
        images.append(canvas)
    images[0].save(str(emojiId) + 'peek.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return (str(emojiId) + 'peek.gif')

def peekingGif(emoGif, emojiId):
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
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
    for f in range(0,400):
        framePick = int(math.floor((f * frame_ratio) % totalFrames))
        emoGif.seek(framePick)
        emoPng = emoGif.copy().convert("RGBA").resize((width, height), Image.LANCZOS)
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
        alpha = canvas.split()[3]
        canvas = canvas.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canvas.paste(255, mask)
        images.append(canvas)
    images[0].save(str(emojiId) + 'peek.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return (str(emojiId) + 'peek.gif')

def peekingImage2(emoPng, intensity, emojiId):
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
        alpha = canvas.split()[3]
        canvas = canvas.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canvas.paste(255, mask)
        images.append(canvas)
    images[0].save(str(emojiId) + 'peek.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return (str(emojiId) + 'peek.gif')

def peekingGif2(emoGif, intensity, emojiId):
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
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
        emoGif.seek(framePick)
        emoPng = emoGif.copy().convert("RGBA").resize((width, height), Image.LANCZOS)
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
        alpha = canvas.split()[3]
        canvas = canvas.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        canvas.paste(255, mask)
        images.append(canvas)
    images[0].save(str(emojiId) + 'peek.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return (str(emojiId) + 'peek.gif')