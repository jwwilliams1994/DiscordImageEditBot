from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random

def JpegImage(emoPng,emojiId):
    image_width, image_height = emoPng.size
    emoPng = emoPng.convert('YCbCr')
    emoPng = ImageEnhance.Contrast(emoPng).enhance(4)
    emoPng.save(emojiId+'Jpegged.jpg', quality=0)
    emoPng = Image.open(emojiId+'Jpegged.jpg')
    emoPng = emoPng.resize((round(image_width*0.5),round(image_height*0.5)),resample=Image.BILINEAR)
    emoPng = ImageEnhance.Contrast(emoPng).enhance(4)
    emoPng.save(emojiId+'Jpegged.jpg', quality=0)
    emoPng = Image.open(emojiId+'Jpegged.jpg')
    emoPng = emoPng.resize((round(image_width*1.5),round(image_height*1.5)),resample=Image.BILINEAR)
    emoPng = ImageEnhance.Contrast(emoPng).enhance(4)
    emoPng.save(str(emojiId)+'Jpegged.jpg', quality=0)
    return (str(emojiId)+'Jpegged.jpg')

def JpegGif(emoGif,emojiId):
    images = []
    totalFrames = emoGif.n_frames
    gifDuration = emoGif.info['duration']
    image_width, image_height = emoGif.size
    print(totalFrames,gifDuration)
    for frame in range(0, totalFrames, 1):
        emoGif.seek(frame)
        frame_image = emoGif.copy()
        frame_image = frame_image.convert('YCbCr')
        frame_image = ImageEnhance.Contrast(frame_image).enhance(4)
        frame_image.save(emojiId+'JpegFrame.jpg', quality=0)
        frame_image = Image.open(emojiId+'JpegFrame.jpg')
        frame_image = frame_image.resize((round(image_width*0.5),round(image_height*0.5)),resample=Image.BILINEAR)
        frame_image = ImageEnhance.Contrast(frame_image).enhance(4)
        frame_image.save(emojiId+'JpegFrame.jpg', quality=0)
        frame_image = Image.open(emojiId+'JpegFrame.jpg')
        frame_image = frame_image.resize((round(image_width*1.5),round(image_height*1.5)),resample=Image.BILINEAR)
        frame_image = ImageEnhance.Contrast(frame_image).enhance(4)
        frame_image = frame_image.convert('RGBA')
        alpha = frame_image.split()[3]
        frame_image = frame_image.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
        frame_image.paste(255, mask)
        images.append(frame_image)
    images[0].save(str(emojiId)+'Jpegged.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255, disposal=2)
    return (str(emojiId)+'Jpegged.gif')
