from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random


def processManImage(emoPng):
    canvas = Image.open('DickMan.png').copy()
    image_width, image_height = emoPng.size
    if image_width >= image_height:
        hRatio = image_height / image_width
        new_image_height = round(47 * hRatio)
        height_offset = 47 - new_image_height
        width_offset = 0
        new_image_width = 47
    else:
        wRatio = image_width / image_height
        new_image_width = round(47 * wRatio)
        width_offset = round((47 - new_image_width) / 2)
        height_offset = 0
        new_image_height = 47
    emoPng = emoPng.resize((new_image_width, new_image_height), Image.LANCZOS).convert('RGBA')
    canvas.alpha_composite(emoPng, (96 + width_offset, 0 + height_offset))
    return canvas


def processManGif(emoGif):
    canvas = Image.open('DickMan.png').copy()
    images = []
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    image_width, image_height = emoGif[0].size
    if image_width >= image_height:
        hRatio = image_height / image_width
        new_image_height = round(47 * hRatio)
        height_offset = 47 - new_image_height
        width_offset = 0
        new_image_width = 47
    else:
        wRatio = image_width / image_height
        new_image_width = round(47 * wRatio)
        width_offset = round((47 - new_image_width) / 2)
        height_offset = 0
        new_image_height = 47
    for frame in range(0, totalFrames):
        framecanvas = canvas.copy()
        frame_image = emoGif[frame].copy().resize((47, new_image_height), Image.LANCZOS).convert('RGBA')
        framecanvas.alpha_composite(frame_image, (96, 0 + height_offset))
        images.append(framecanvas)
    images.append(gifDuration)
    return images

# img = Image.open('hazmat.png')
# processManImage(img).show()
