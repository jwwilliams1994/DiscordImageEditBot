from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random


def JpegImage2(emoPng,times=2):
    emojiId = str(random.randint(0, 99999))
    print('image')
    image_width, image_height = emoPng.size
    emoPng = emoPng.convert('YCbCr')
    emoPng = ImageEnhance.Contrast(emoPng).enhance(4)
    emoPng.save(emojiId+'Jpegged.jpg', quality=0)
    for x in range(0,times):
        emoPng = Image.open(emojiId+'Jpegged.jpg')
        mod2 = (x+1)/10
        if x!=0:
            if round(x/2) == x/2:
                mod = 1.5*mod2
            else:
                mod = 0.5/mod2
        else:
            mod = 0.5/mod2
        emoPng = emoPng.resize((round(image_width*mod),round(image_height*mod)),resample=Image.BILINEAR)
        emoPng = ImageEnhance.Contrast(emoPng).enhance(4)
        if x==times-1:
            emoPng = emoPng.resize((image_width,image_height),resample=Image.BILINEAR)
        emoPng.save(str(emojiId)+'Jpegged.jpg', quality=0)
    img = Image.open(str(emojiId)+'Jpegged.jpg')
    os.remove(str(emojiId)+'Jpegged.jpg')
    return img


def JpegGif2(emoGif,times=2):
    emojiId = str(random.randint(0, 99999))
    images = []
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    image_width, image_height = emoGif[0].size
    print(totalFrames,gifDuration)
    for frame in range(0, totalFrames, 1):
        frame_image = emoGif[frame].copy()
        frame_image = frame_image.convert('YCbCr')
        frame_image = ImageEnhance.Contrast(frame_image).enhance(4)
        frame_image.save(emojiId+'JpegFrame.jpg', quality=0)
        for x in range(0,times):
            frame_image = Image.open(emojiId+'JpegFrame.jpg')
            mod2 = (x+1)/10
            if x!=0:
                if round(x/2) == x/2:
                    mod = 1.5*mod2
                else:
                    mod = 0.5/mod2
            else:
                mod = 0.5/mod2
            frame_image = frame_image.resize((round(image_width*mod),round(image_height*mod)),resample=Image.BILINEAR)
            frame_image = ImageEnhance.Contrast(frame_image).enhance(4)
            if x==times-1:
                frame_image = frame_image.resize((image_width,image_height),resample=Image.BILINEAR)
            frame_image.save(emojiId+'JpegFrame.jpg', quality=0)
        frame_image = frame_image.convert('RGBA')
        images.append(frame_image)
        os.remove(emojiId+'JpegFrame.jpg')
    images.append(gifDuration)
    return images