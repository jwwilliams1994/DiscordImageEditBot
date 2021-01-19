from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random

def processManImage(emoPng,emojiId):
    canvas = Image.open('DickMan.png')
    image_width, image_height = emoPng.size
    if image_width >= image_height:
        hRatio = image_height/image_width
        new_image_height = round(47*hRatio)
        height_offset = 47-new_image_height
        width_offset = 0
        new_image_width = 47
    else:
        wRatio = image_width/image_height
        new_image_width = round(47*wRatio)
        width_offset = round((47-new_image_width)/2)
        height_offset = 0
        new_image_height = 47
    emoPng = emoPng.resize((new_image_width,new_image_height),Image.LANCZOS).convert('RGBA')
    canvas.alpha_composite(emoPng,(96+width_offset,0+height_offset))
    canvas.save(emojiId+'DickMan.png')
    return(str(emojiId)+'DickMan.png')

def processManGif(emoGif,emojiId):
    canvas = Image.open('DickMan.png')
    images = []
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    image_width, image_height = emoGif.size
    if image_width >= image_height:
        hRatio = image_height/image_width
        new_image_height = round(47*hRatio)
        height_offset = 47-new_image_height
        width_offset = 0
        new_image_width = 47
    else:
        wRatio = image_width/image_height
        new_image_width = round(47*wRatio)
        width_offset = round((47-new_image_width)/2)
        height_offset = 0
        new_image_height = 47
    for frame in range(0, totalFrames):
        framecanvas = canvas.copy()
        emoGif.seek(frame)
        frame_image = emoGif.copy().resize((47,new_image_height),Image.LANCZOS).convert('RGBA')
        framecanvas.alpha_composite(frame_image,(96,0+height_offset))
        alpha = framecanvas.split()[3]
        framecanvas = framecanvas.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
        framecanvas.paste(255, mask)
        images.append(framecanvas)
    images[0].save(str(emojiId)+'DickMan.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255, disposal=2)
    return (str(emojiId)+'DickMan.gif')
    
    
