from PIL import Image
import numpy as np
import cv2, os, math
import torch
import urllib.request

import matplotlib.pyplot as plt


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


def stereo(inp, depth, emojiId):
    inp = inp.convert('RGB')
    inp.save(emojiId+'st.png')
    filename = emojiId+'st.png'

    use_large_model = True

    if use_large_model:
        midas = torch.hub.load("intel-isl/MiDaS", "MiDaS")
    else:
        midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    midas.to(device)
    midas.eval()
    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

    if use_large_model:
        transform = midas_transforms.default_transform
    else:
        transform = midas_transforms.small_transform
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    input_batch = transform(img).to(device)
    with torch.no_grad():
        prediction = midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    output = prediction.cpu().numpy()
    plt.imsave("depth"+filename, output)

    print('whuh')

    image = Image.open("depth"+filename).convert('HSV')
    image2 = Image.open(filename).convert('RGBA')
    il2 = image2.load()
    width, height = image.size
    canvas = Image.new('RGBA', (round(width * 2)+60, round(height)), (0, 0, 0, 0))
    cl = canvas.load()
    il = image.load()
    for y in range(height):
        ar = [*range(width)]
        ar2 = [*range(width)]
        for x in range(width):
            h = il[x, y][0]
            xo = (180 - h) / round(depth)
            xg = clamp(x - xo, 0, width - 1)
            ar[x] = [h, xg, x]
            x2 = (width * 2) - x
            x3 = width - x - 1
            h = il[x3, y][0]
            xo = (180 - h) / round(depth)
            xg = clamp(x2 + xo, width, width * 2 - 1)
            ar2[x] = [h, xg, x]
            # cl2[ix, y] = *il[x3, y], 255
        # print(len(ar))
        ar.sort(reverse=True)
        for i in ar:
            cl[i[1]+10, y] = il2[i[2], y]
        ar2.sort(reverse=True)
        for i in ar2:
            cl[i[1]+30, y] = il2[-i[2], y]
    width = width+30
    for x in range(width, -1, -1):
        for y in range(height):
            if cl[x, y][-1] == 0:
                cl[x, y] = cl[clamp(x + 2, 0, width - 1), y]
            x2 = width * 2 - x - 1
            if cl[x2, y][-1] == 0:
                cl[x2, y] = cl[clamp(x2 - 2, width, width * 2 - 1), y]
    print('saving?')
    os.remove('depth'+filename)
    canvas.save(str(emojiId) + 'stereo.png')
    return str(emojiId) + 'stereo.png'


def stereo2(inp, emojiId):
    inp = inp.convert('RGB')
    inp.save(emojiId+'st.png')
    filename = emojiId+'st.png'

    use_large_model = True

    if use_large_model:
        midas = torch.hub.load("intel-isl/MiDaS", "MiDaS")
    else:
        midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    midas.to(device)
    midas.eval()
    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

    if use_large_model:
        transform = midas_transforms.default_transform
    else:
        transform = midas_transforms.small_transform
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    input_batch = transform(img).to(device)
    with torch.no_grad():
        prediction = midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    output = prediction.cpu().numpy()
    plt.imsave(str(emojiId) + "stereo.png", output)
    return str(emojiId) + 'stereo.png'


def framing(inp, depth, emojiId, midas, device, transform):
    inp = inp.convert('RGB')
    # inp.save(emojiId + 'st.png')
    filename = emojiId + 'st.png'

    use_large_model = True
    open_cv_image = np.array(inp)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    # if use_large_model:
    #     midas = torch.hub.load("intel-isl/MiDaS", "MiDaS")
    # else:
    #     midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
    # device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    midas.to(device)
    midas.eval()
    # midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
    #
    # if use_large_model:
    #     transform = midas_transforms.default_transform
    # else:
    #     transform = midas_transforms.small_transform
    # img = cv2.imread(np.array(inp))
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = open_cv_image

    input_batch = transform(img).to(device)
    with torch.no_grad():
        prediction = midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    output = prediction.cpu().numpy()
    plt.imsave("depth" + filename, output)

    print('whuh')

    image = Image.open("depth" + filename).convert('HSV')
    image2 = inp.convert('RGBA')
    il2 = image2.load()
    width, height = image.size
    canvas = Image.new('RGBA', (round(width * 2)+60, round(height)), (0, 0, 0, 0))
    cl = canvas.load()
    il = image.load()
    for y in range(height):
        ar = [*range(width)]
        ar2 = [*range(width)]
        for x in range(width):
            h = il[x, y][0]
            xo = (180 - h) / round(depth)
            xg = clamp(x - xo, 0, width - 1)
            ar[x] = [h, xg, x]
            x2 = (width * 2) - x
            x3 = width - x - 1
            h = il[x3, y][0]
            xo = (180 - h) / round(depth)
            xg = clamp(x2 + xo, width, width * 2 - 1)
            ar2[x] = [h, xg, x]
            # cl2[ix, y] = *il[x3, y], 255
        # print(len(ar))
        ar.sort(reverse=True)
        for i in ar:
            cl[i[1]+10, y] = il2[i[2], y]
        ar2.sort(reverse=True)
        for i in ar2:
            cl[i[1]+30, y] = il2[-i[2], y]
    width = width+30
    for x in range(width, -1, -1):
        for y in range(height):
            if cl[x, y][-1] == 0:
                cl[x, y] = cl[clamp(x + 2, 0, width - 1), y]
            x2 = width * 2 - x - 1
            if cl[x2, y][-1] == 0:
                cl[x2, y] = cl[clamp(x2 - 2, width, width * 2 - 1), y]
    #os.remove('depth' + filename)
    return canvas


def stereoGif(inp, depth, emojiId):
    midas = torch.hub.load("intel-isl/MiDaS", "MiDaS")
    device = torch.device("cpu")
    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
    transform = midas_transforms.default_transform
    totalFrames = inp.n_frames
    gifDuration = inp.info['duration']
    images = []
    for f in range(totalFrames):
        inp.seek(f)
        frame = framing(inp.copy().convert('RGB'), depth, emojiId, midas, device, transform).convert('RGB').quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        images.append(frame)
    os.remove('depth' + str(emojiId) + 'st.png')
    images[0].save(str(emojiId) + 'stereo.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, disposal=2)
    return str(emojiId) + 'stereo.gif'


def stereo3(inp, inp2, depth, emojiId):
    image = inp2.convert('HSV')
    image2 = inp.convert('RGBA')
    il2 = image2.load()
    width, height = image.size
    canvas = Image.new('RGBA', (round(width * 2)+60, round(height)), (0, 0, 0, 0))
    cl = canvas.load()
    il = image.load()
    for y in range(height):
        ar = [*range(width)]
        ar2 = [*range(width)]
        for x in range(width):
            h = il[x, y][0]
            xo = (180 - h) / round(depth)
            xg = clamp(x - xo, 0, width - 1)
            ar[x] = [h, xg, x]
            x2 = (width * 2) - x
            x3 = width - x - 1
            h = il[x3, y][0]
            xo = (180 - h) / round(depth)
            xg = clamp(x2 + xo, width, width * 2 - 1)
            ar2[x] = [h, xg, x]
            # cl2[ix, y] = *il[x3, y], 255
        # print(len(ar))
        ar.sort(reverse=True)
        for i in ar:
            cl[i[1], y] = il2[i[2], y]
        ar2.sort(reverse=True)
        for i in ar2:
            cl[i[1], y] = il2[-i[2], y]

    for x in range(width, -1, -1):
        for y in range(height):
            if cl[x, y][-1] == 0:
                cl[x, y] = cl[clamp(x + 2, 0, width - 1), y]
            x2 = width * 2 - x - 1
            if cl[x2, y][-1] == 0:
                cl[x2, y] = cl[clamp(x2 - 2, width, width * 2 - 1), y]
    canvas.save(str(emojiId) + 'stereo.png')
    return str(emojiId) + 'stereo.png'


def stereo3gif(inp, inp2, depth, emojiId):
    totalFrames = inp.n_frames
    gifDuration = inp.info['duration']
    images = []
    image = inp2.convert('HSV')
    il = image.load()
    for f in range(totalFrames):
        inp.seek(f)
        image2 = inp.copy().convert('RGBA')
        il2 = image2.load()
        width, height = image.size
        canvas = Image.new('RGBA', (round(width * 2)+80, round(height)), (0, 0, 0, 0))
        cl = canvas.load()
        for y in range(height):
            ar = [*range(width)]
            ar2 = [*range(width)]
            for x in range(width):
                h = il[clamp2(x, 0, width-1), y][0]
                xo = (180 - h) / round(depth)
                xg = clamp2(x - xo, -20, width - 1 + 20)
                ar[x] = [h, xg, x]
                x2 = (width * 2) - x
                x3 = width - x - 1
                h = il[clamp2(x3, 0, width-1), y][0]
                xo = (180 - h) / round(depth)
                xg = clamp2(x2 + xo, width-20, width * 2 - 1 + 20)
                ar2[x] = [h, xg, x]
                # cl2[ix, y] = *il[x3, y], 255
            # print(len(ar))
            ar.sort(reverse=True)
            for i in ar:
                cl[i[1]+40, y] = il2[clamp2(i[2], 0, width-1), y]
            ar2.sort(reverse=True)
            for i in ar2:
                cl[i[1]+40, y] = il2[clamp(-i[2], -(width), width-1), y]
        width = width+40
        for x in range(width, -1, -1):
            for y in range(height):
                if cl[x, y][-1] == 0:
                    if cl[clamp(x - 1, 0, width - 1), y][-1] == 255:
                        cl[x, y] = cl[clamp(x + 1, 0, width - 1), y]
                x2 = width * 2 - x - 1
                if cl[x2, y][-1] == 0:
                    if cl[clamp(x2 + 1, width, width*2 - 1), y][-1] == 255:
                        cl[x2, y] = cl[clamp(x2 - 1, width, width * 2 - 1), y]
        canvas = canvas.convert('RGB').quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
        images.append(canvas)
    images[0].save(str(emojiId) + 'stereo.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, disposal=2)
    return str(emojiId) + 'stereo.gif'