from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random


def JpegImage(emoPng):
    emojiId = str(random.randint(0, 99999))
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
    return emoPng


def JpegGif(emoGif):
    emojiId = str(random.randint(0, 99999))
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
        images.append(frame_image)
    images.append(gifDuration)
    return images
