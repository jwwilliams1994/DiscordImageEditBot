from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random

def JpegImage2(emoPng,times,emojiId):
    print('image')
    image_width, image_height = emoPng.size
    emoPng = emoPng.convert('YCbCr')
    emoPng = ImageEnhance.Contrast(emoPng).enhance(4)
    emoPng.save(emojiId+'Jpegged.jpg', quality=0)
    for x in range(0,times):
        print(x,'test')
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
    return (str(emojiId)+'Jpegged.jpg')

def JpegGif2(emoGif,times,emojiId):
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
        alpha = frame_image.split()[3]
        frame_image = frame_image.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
        frame_image.paste(255, mask)
        images.append(frame_image)
        os.remove(emojiId+'JpegFrame.jpg')
    images[0].save(str(emojiId)+'Jpegged.gif', save_all=True, append_images=images[1:], duration=gifDuration, loop=0, optimize=False, transparency=255, disposal=2)
    return (str(emojiId)+'Jpegged.gif')
