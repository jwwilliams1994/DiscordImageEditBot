from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random


def italicizePng(emoPng):
    image_width, image_height = emoPng.size
    wRatio = image_width/image_height
    m = 0.3
    xshift = abs(m) * image_width
    new_width = image_width + int(round(xshift))
    emoPng = emoPng.convert('RGBA')
    italic_image = emoPng.transform((new_width,image_height), Image.AFFINE, (1,m,-xshift if m > 0 else 0,0,1,0), Image.BICUBIC)
    italic_image = italic_image.resize((160, 160), Image.LANCZOS)
    return italic_image


def italicizeGif(emoGif):
    images = []
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    image_width, image_height = emoGif.size
    wRatio = image_width/image_height
    print(totalFrames,gifDuration)
    for frame in range(0, totalFrames, 1):
        frame_image = emoGif[frame].copy()
        m = 0.3
        xshift = abs(m) * image_width
        new_width = image_width + int(round(xshift))
        frame_image = frame_image.convert('RGBA')
        italic_frame = frame_image.transform((new_width,image_height), Image.AFFINE, (1,m,-xshift if m > 0 else 0,0,1,0), Image.BICUBIC)
        italic_frame = italic_frame.convert('RGBA')
        images.append(italic_frame)
    images.append(gifDuration)
    return images