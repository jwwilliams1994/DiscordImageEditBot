from PIL import Image, ImageFilter, GifImagePlugin, ImageSequence, ImageChops, ImageDraw, ImageEnhance, ImageOps
import os, glob, time, asyncio
import math, random

def notBttvDef(emoPng, arg, emojiId):
    return notBttv(emoPng, arg, 0, 0, 0, 1, emojiId)

def notBttv(emoPng, arg, ex, ey, roty, scale, emojiId):
    maskedArgs = ['hazmat','hazmatf']
    emoPng = emoPng.convert('RGBA')
    overlay = Image.open(arg+'.png').convert('RGBA')
    canvas80 = Image.open('canvas.png').resize((80,80))
    canvas2 = canvas80.copy()
    ratio = emoPng.height/emoPng.width
    ratio2 = canvas80.height/canvas80.width
    if arg in maskedArgs:
        needMask = True
    else:
        needMask = False
    if emoPng.width > 70:
        image = emoPng.copy().resize((70,round(70*ratio)), Image.BICUBIC)
    else:
        image = emoPng.copy().resize((70,round(70*ratio)), Image.NEAREST)
    if overlay.width > 80:
        image2 = overlay.copy().resize((80,round(80*ratio2)), Image.BICUBIC)
    else:
        image2 = overlay.copy().resize((80,round(80*ratio2)), Image.NEAREST)
    if needMask:
        if scale < 1: ##rescaling if scale is not 1
            image = image.copy().resize((round(image.width*scale),round(image.height*scale)), Image.BICUBIC)
        elif scale > 1:
            image = image.copy().resize((round(image.width*scale),round(image.height*scale)), Image.NEAREST)
        image = image.rotate(float(roty), Image.BICUBIC, expand=1)
        if image.height > 70 or image.width > 70:
            image = image.crop((((image.width-70)/2),((image.height-70)/2),image.width-((image.width-70)/2),image.height-((image.height-70)/2)))
        canvas80.alpha_composite(image,(round((80-image.width)/2)+5+ex,round((80-image.height)/2)+5+ey))
        mask = Image.open(arg+'mask.png').convert('RGBA')
        mask = mask.copy().resize((80,round(80*ratio2)), Image.NEAREST)
        canvas2.alpha_composite(mask,(round((80-image2.width)/2),0))
        mask = canvas2.convert('L')
        maskL = mask.load()
        canvasL = canvas80.load()
        for y in range(0,80,1):
            for x in range(0,80,1):
                num = math.floor((maskL[x,y]*10)/256)
                if maskL[x,y] > 10:
                    canvasL[x,y] = (0,0,0,0)
    if needMask:
        canvas80.alpha_composite(image2,(round((80-image2.width)/2),0))
    else:
        canvas80.alpha_composite(image,(round((80-image.width)/2)+5,round((80-image.height)/2)+5))
        image2 = image2.rotate(float(roty), Image.BICUBIC, expand=1)
        image2 = ImageChops.offset(image2,ex,ey)
        if scale < 1: ##rescaling if scale is not 1
            image2 = image2.copy().resize((round(image2.width*scale),round(image2.height*scale)), Image.BICUBIC)
        elif scale > 1:
            image2 = image2.copy().resize((round(image2.width*scale),round(image2.height*scale)), Image.NEAREST)
        image2 = image2.crop((((image2.width-80)/2),((image2.height-80)/2),image2.width-((image2.width-80)/2),image2.height-((image2.height-80)/2)))
        canvas80.alpha_composite(image2,(round((80-image2.width)/2),round((80-image2.height)/2)))
    canvas80.convert('RGBA')
    canvas80.save(emojiId+'overlay.png')
    return (str(emojiId)+'overlay.png')

def notBttvImg(emoPng, arg, ex, ey, roty, scale, alpha, emojiId):
    maskedArgs = ['hazmat','hazmatf']
    emoPng = emoPng.convert('RGBA')
    print(type(arg))
    if type(arg) is not str:
        overlay = arg.copy().convert("RGBA")
    else:
        overlay = Image.open(arg+'.png').convert('RGBA')
    if arg in maskedArgs:
        needMask = True
    else:
        needMask = False
    width, height = emoPng.size
    if not needMask:
        if width > height:
            overlay = overlay.resize((round(height * scale), round(height * scale)), Image.LANCZOS)
            xOff = round((width - height) / 2)
            yOff = 0
        if width < height:
            overlay = overlay.resize((round(width * scale), round(width * scale)), Image.LANCZOS)
            yOff = round((height - width) / 2)
            xOff = 0
        if width == height:
            overlay = overlay.resize((round(width * scale), round(height * scale)), Image.LANCZOS)
            xOff = 0
            yOff = 0
    else:
        emoPng = emoPng.resize((round(width * scale),round(height * scale)), Image.LANCZOS)
        emoPng = emoPng.rotate(roty, resample=Image.BICUBIC, expand=0)
    # canvas = Image.new("RGBA", overlay.size, (0, 0, 0, 0))
    ovX, ovY = overlay.size
    if alpha < 1:
        lod = overlay.load()
        for x in range(ovX):
            for y in range(ovY):
                r, g, b, a = lod[x, y]
                a = round(a * alpha)
                lod[x, y] = (r, g, b, a)
    if needMask:
        width, height = emoPng.size
        # emoPng = emoPng.crop((round(ex * width), round(ey * height), round(ovX + (ex * width)), round(ovY + (ey * height))))
        emoPng = emoPng.crop((round((ex - 0.5) * width), round((ey - 0.5) * height), round(ovX + ((ex - 0.5) * width)), round(ovY + ((ey - 0.5) * height))))
        # emoPng = emoPng.crop((round((ex - 0.5) * width), height - round(ovY + ((ey - 0.5) * height)), round(ovX + ((ex - 0.5) * width)), height - round((ey - 0.5) * height)))
        width, height = emoPng.size
        # canvas80.alpha_composite(emoPng, (0, 0))
        mask = Image.open(arg+'mask.png').resize(overlay.size, Image.NEAREST)
        mask = mask.convert('L')
        maskL = mask.load()
        imgL = emoPng.load()
        for y in range(0, width, 1):
            for x in range(0, height, 1):
                num = math.floor((maskL[x,y]*10)/256)
                if maskL[x,y] > 10:
                    imgL[x,y] = (0,0,0,0)
        emoPng.alpha_composite(overlay, (0, 0))
    else:
        width, height = emoPng.size
        overlay = overlay.rotate(roty, resample=Image.BICUBIC, expand=1)
        canvas = Image.new("RGBA", (width * 2, height * 2), (0, 0, 0, 0))
        canvas.alpha_composite(overlay, (round((width * ex) - (ovX / 2) + (width / 2)), round((height - (height * ey)) - (ovY / 2) + (height / 2))))
        canvas = canvas.crop((round(width / 2), round(height / 2), round(width * 1.5), round(height * 1.5)))
        canvas.show()
        ovX, ovY = overlay.size
        print(emoPng.size, overlay.size)
        print(round((width * ex) - (ovX / 2)), round((height * ey) - (ovY / 2)))
        #emoPng.alpha_composite(canvas, (round((width * ex) - (ovX / 2)), round((height * ey) - (ovY / 2))))
        emoPng.alpha_composite(canvas, (0, 0))
    emoPng.convert('RGBA')
    emoPng.save(emojiId+'overlay.png')
    return str(emojiId)+'overlay.png'

def overlayGif(emoGif, overlayed, ex, ey, roty, scale, alpha, emojiId):
    width, height = emoGif.size
    gif1, gif2 = False, False
    if emoGif.info == {}:
        gif1 = True
    if overlayed.info == {}:
        gif2 = True
    if gif1 == gif2:
        return "wrong, idiot"

# img = Image.open("testem2.png")
# notBttvImg(img, "think", 0.5, 0.5, 0, 0.1, 0.5, "88")