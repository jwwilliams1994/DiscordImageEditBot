from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random

def italicizePng(emoPng, emojiId):
    image_width, image_height = emoPng.size
    wRatio = image_width/image_height
    m = 0.3
    xshift = abs(m) * image_width
    new_width = image_width + int(round(xshift))
    emoPng = emoPng.convert('RGBA')
    italic_image = emoPng.transform((new_width,image_height), Image.AFFINE, (1,m,-xshift if m > 0 else 0,0,1,0), Image.BICUBIC)
    italic_image = italic_image.resize((160, 160), Image.LANCZOS)
    italic_image.save(str(emojiId)+'italicized.png')
    return (str(emojiId)+'italicized.png')

def italicizeGif(emoGif,emojiId):
    images = []
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    image_width, image_height = emoGif.size
    wRatio = image_width/image_height
    print(totalFrames,gifDuration)
    for frame in range(0, totalFrames, 1):
        emoGif.seek(frame)
        frame_image = emoGif.copy()
        m = 0.3
        xshift = abs(m) * image_width
        new_width = image_width + int(round(xshift))
        frame_image = frame_image.convert('RGBA')
        italic_frame = frame_image.transform((new_width,image_height), Image.AFFINE, (1,m,-xshift if m > 0 else 0,0,1,0), Image.BICUBIC)
        italic_frame = italic_frame.convert('RGBA')
        alpha = italic_frame.split()[3]
        italic_frame = italic_frame.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
        italic_frame.paste(255, mask)
        images.append(italic_frame)
    images[0].save(str(emojiId)+'italicized.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255, disposal=2)
    return (str(emojiId)+'italicized.gif')
