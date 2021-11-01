import json, time, multiprocessing, threading, io, random, os.path, requests, PIL
from multiprocessing.connection import Client
from multiprocessing.connection import Listener
from PIL import Image
from image_mods.DickMan import processManImage, processManGif
from image_mods.intense import intensifytext, marqueetext
from image_mods.italicize import italicizePng, italicizeGif
from image_mods.jpegify import JpegImage, JpegGif
from image_mods.jpegify2 import JpegGif2, JpegImage2
from image_mods.jpegify3 import JpegGif3, JpegImage3
from image_mods.mockingSpongebob import mockingSpongebob
from image_mods.monkaShoot import processShootImage
from image_mods.notbttv import notBttv, notBttvDef, notBttvImg, hazmatPng, hazmatGif
from image_mods.pptasty import process4headImage, process4headGif, processwormholeImage, processwormholeGif, processSnapImage, processSnapImage2, \
    processSnapGif2, \
    processSnapImage3, processSnapGif3, processSnapImage4, processSnapGif4
from image_mods.shook import processMoreShookImage, processNukeImage, processCrazyShookImage, processShookImage, processGifImageT, processGifImageF, \
    processStaticImage, processNukeGif, processShookGif, processMoreShookGif, processStaticRangeImage, processShookImage2
from image_mods.space import processSpaceGif, processSpaceImage
from image_mods.speed import speedtext
from image_mods.peeking import peekingImage, peekingGif, peekingImage2, peekingGif2
from image_mods.simpleMod import rotateImg, rotateGif, flipImg, flipGif, hyperImg, hyperGif, information, information2, widen, widenGif, resize, resizeGif, \
    crop, cropGif, thinking, thinkingGif, transparency, transparencyGif, save, saveGif, append, appendGif, getUrl, areyousure, justdoit, couch, manydoors,\
    maskingPng, maskingGif, maskingPng2, maskingGif2, maskingOne, maskingTwo, maskingPng4, maskingGif4, lcdPng, lcdGif, lcdPng2, lcdGif2, lcdPng3, lcdGif3,\
    lcdPng4, lcdGif4, intoGif, intoMp4, getMp4asGif, emboss, embossGif, aggressivePng, border, borderGif, border2, borderGif2, enchant, halve,\
    upscalePng, upscaleGif, downscalePng, downscaleGif, palettePng, paletteGif, palettePng2, paletteGif2, stitchwPng, stitchwGif, stitchhPng, stitchhGif, fixGif, \
    brightnessImg, brightnessGif, contrastImg, contrastGif, gaussImg, gaussGif, saturationImg, saturationGif, palettePng3, paletteGif3, diffractPng, diffractGif, \
    diffractAni, glitchPng, glitchGif, giffify, jitterPng, jitterGif, invertPng, invertGif, warpPng, warpGif, spinPng, pumpPng, pumpGif, pump2Png, pump2Gif
from image_mods.textual import magicConch
from image_mods.ThreeDrendering import rendering3d, rendering3d2, rendering3dSpot, rendering3dSpotGif, renderingShrink3d, renderingShrink3dGif, \
    rendering3dSpotvol, \
    rendering3dSpotCop, renderingDice
from image_mods.wobbling import wobble, wobbleGif
# from image_mods.Atmograph import atmograph2
from image_mods.crtfilter import cathodePng, cathodeGif, cathodePng2, cathodeGif2, paddingPng, paddingGif, crtdepth, cathodePng3, cathodeGif3, cathodePng4, cathodeGif4, \
    ntscPng, ntscGif
from image_mods.stereograph import stereo, stereoGif, stereo2, stereo3, stereo3gif
from image_mods.drawCalendar import make_calendar, add_event, get_events, remove_events
from image_mods.HereLies import herelay, imagine
# from image_mods.stocks import graph_crypto
# for the time being, I've deprecated deep dream... maybe later I'll re-implement
# from image_mods.deepdream2 import *
# from image_mods.deepdream import *
taskQueue = []
dict = {"intense": [intensifytext], "speed": [speedtext], "mocking": [mockingSpongebob], "space": [processSpaceImage, processSpaceGif],
        "shoot": [processShootImage], "italics": [italicizePng, italicizeGif], "jpeg": [JpegImage, JpegGif], "man": [processManImage, processManGif],
        "jpeg2": [JpegImage2, JpegGif2], "jpeg3": [JpegImage3, JpegGif3], "weee": [processCrazyShookImage], "shake": [processShookImage, processShookGif],
        "nuke": [processNukeImage, processNukeGif], "moreshake": [processMoreShookImage, processMoreShookGif], "hold": [processStaticImage, processGifImageF],
        "hold2": [processStaticImage, processGifImageT], "overlay2": [notBttvDef], "overlay": [notBttvImg], "4head": [process4headImage, process4headGif],
        "wormhole": [processwormholeImage, processwormholeGif], "peek": [peekingImage, peekingGif], "rotate": [rotateImg, rotateGif],
        "peek2": [peekingImage2, peekingGif2], "flip": [flipImg, flipGif], "hyper": [hyperImg, hyperGif], "info": [information, information2],
        "8ball": [magicConch], "snap": [processSnapImage], "snap2": [processSnapImage2, processSnapGif2], "snap3": [processSnapImage3, processSnapGif3],
        "3d": [rendering3d, rendering3d2], "3dlit": [rendering3dSpot, rendering3dSpotGif], "wide": [widen, widenGif], "resize": [resize, resizeGif],
        "wobble": [wobble, wobbleGif], "crop": [crop, cropGif], "shrink": [renderingShrink3d, renderingShrink3dGif], "shrink2": [rendering3dSpotvol],
        "think": [thinking, thinkingGif], "alpha": [transparency, transparencyGif], "illegal": [rendering3dSpotCop], "save": [save, saveGif],
        "append": [append, appendGif], "snap4": [processSnapImage4, processSnapGif4], "atmograph": [atmograph2], "geturl": [getUrl],
        "areyousure": [areyousure], "justdoit": [justdoit], "couch": [couch], "manydoors": [manydoors], "mask": [maskingPng, maskingGif],
        "mask2": [maskingPng2, maskingGif2], "mask3": [maskingOne, maskingOne], "overlaying": [maskingTwo, maskingTwo], "mask4": [maskingPng4, maskingGif4],
        "lcd": [lcdPng, lcdGif], "lcd2": [lcdPng2, lcdGif2], "lcd3": [lcdPng3, lcdGif3], "marquee": [marqueetext], "held3": [processStaticRangeImage],
        "lcd4": [lcdPng4, lcdGif4], "crt": [cathodePng, cathodeGif], "crt2": [cathodePng2, cathodeGif2], "pad": [paddingPng, paddingGif], "test": [intoGif],
        "mp4": [intoMp4], "stereo": [stereo, stereoGif], "stereo2": [stereo2], "stereo3": [stereo3, stereo3gif], "crtd": [crtdepth],
        "shake2": [processShookImage2], "getMp4": [getMp4asGif], "crt3": [cathodePng3, cathodeGif3], "emboss": [emboss, embossGif], "aggressive": [aggressivePng],
        "border": [border, borderGif], "border2": [border2, borderGif2], "enchant": [enchant], "halve": [halve], "upscale": [upscalePng, upscaleGif],
        "downscale": [downscalePng, downscaleGif], "palette": [palettePng, paletteGif], "palette2": [palettePng2, paletteGif2], "stitchw": [stitchwPng, stitchwGif],
        "stitchh": [stitchhPng, stitchhGif], "fix": [fixGif], "brightness": [brightnessImg, brightnessGif], "contrast": [contrastImg, contrastGif],
        "blur": [gaussImg, gaussGif], "roll": [renderingDice], "saturation": [saturationImg, saturationGif], "palette3": [palettePng3, paletteGif3], "rip": [herelay],
        "diffract": [diffractPng, diffractGif], "diffract2": [diffractAni], "glitch": [glitchPng, glitchGif], "gifify": [giffify], "hazmat": [hazmatPng, hazmatGif],
        "crypto": [graph_crypto], "jitter": [jitterPng, jitterGif], "invert": [invertPng, invertGif], "warp": [warpPng, warpGif], "crt4": [cathodePng4, cathodeGif4],
        "ntsc": [ntscPng, ntscGif], "spin": [spinPng], "pumpkin2": [pumpPng, pumpGif], "pumpkin": [pump2Png, pump2Gif], "imagine": [imagine]}


def grabImage(urll):  # if you direct link to a png/gif/etc, it will directly return it as a bytestream of the image
    r = requests.get(urll, allow_redirects=True)
    r.close()
    return io.BytesIO(r.content)


def get_emoji_url(emoji_string):
    id_string = emoji_string[emoji_string.rfind(':') + 1:-1]
    url = "https://cdn.discordapp.com/emojis/" + str(id_string)
    return url


def exists(path):  # checks if url exists
    r = requests.head(path)
    return r.status_code == requests.codes.ok


def getUrl(text):
    image = Image.open(grabImage(text))
    return image


def listening():  # constantly listens for an input on port 4001, then adds the received json to the list of tasks
    listener = Listener(('', 4001))
    while True:
        try:
            conn = listener.accept()
            msg = json.loads(conn.recv())
            taskQueue.append(msg)
        except Exception as e:
            print(e)
        time.sleep(0.1)


# def findList(inp):  # basically just looks backwards for a ']' and outputs the position of it in the input list as a negative number
#     for i in range(len(inp)):
#         if inp[-i] == ']':
#             return -i
#     return 0  # 0 is just a good value for 'it didn't find anything'... although I suppose this should maybe output an error
#
#
# def listify(inp):  # takes the sterilized string and converts into nested lists
#     odict = []  # this is for output, hence odict... although I suppose it's a list not a dict now
#     for i in range(len(inp)):
#         if inp[i] == '[':
#             sep = findList(inp)
#             if sep != 0 and sep != -1:  # there's probably an edge case here, but haven't found it yet
#                 odict = [*inp[:i], listify(inp[i + 1:sep]), *inp[sep + 1:]]
#             else:
#                 odict = [*inp[:i], listify(inp[i + 1:sep])]
#             if type(odict[0]) is list:
#                 odict[0] = ' '.join(odict[0])
#             return odict
#         else:
#             if i == (len(inp) - 1):
#                 return inp
#             else:
#                 sep = findList(inp)


def findList(start, inp):
    m = -1  # first character is [ so it'll immediately add?
    for i in range(start, len(inp)):
        if inp[i] == '[':
            m = m + 1
        if inp[i] == ']' and m == 0:
            return i
        if inp[i] == ']':
            m = m - 1
    return 0  # 0 is just a good value for 'it didn't find anything'... although I suppose this should maybe output an error


def listify(inp):  # takes the sterilized string and converts into nested lists
    odict = []  # this is for output, hence odict... although I suppose it's a list not a dict now
    next = 0
    for i in range(len(inp)):
        if i >= next: # I guess just leave this here to prevent repeat appends
            if inp[i] == '[':
                # take and listify all between the corresponding [ and ] and make next equal to ] + 1
                sep = findList(i, inp)
                print(sep, inp[i+1:sep])
                odict.append(listify(inp[i+1:sep]))
                next = sep
                pass
            else:
                if inp[i] != ']':
                    odict.append(inp[i])
                pass
    return odict


def sterilize(inp2):
    listy = inp2.split(' ')
    lim = len(listy)
    i = 0
    while i < lim:  # this removes any index of the resultant list that's empty
        if listy[i] == '' or listy[i] == ' ':
            listy.remove(listy[i])
            lim = lim - 1
        else:
            i = i + 1
    return listy


def is_file(inp):  # because os.path.isfile throws an annoying exception if the input is not a string...
    try:
        return os.path.isfile(inp)
    except:
        return False


def pil_to_list(inp):
    total_frames = inp.n_frames
    im_arr = []
    dur_arr = []
    for f in range(total_frames):
        inp.seek(f)
        dur_arr.append(inp.info['duration'])
        im_arr.append(inp.copy())
    #     for d in range(0, dur_arr[-1], 20):  # this 'fix' is here until we change functions to work with and accept duration arrays...
    #         im_arr.append(inp.copy())
    im_arr.append(dur_arr)  # for now, the last value in the array will be an int that represents the duration
    return im_arr  # when we're ready, we'll use a list for durations instead of int in the last spot


def formatting(inp):
    # this goes over the input list and checks the string entries to see if they might correspond to a file or something, and replaces accordingly
    if type(inp) is not list and type(inp) is not str:  # I'm not sure this'll be an issue, but just in case...
        return [inp]
    if type(inp) is not list:  # minor edge case coverage
        inp = [inp]
    for i in range(len(inp)):
        if type(inp[i]) is str:
            try:
                emoTest = inp[i].encode('unicode_escape')
                # if this and inp[i] become different at this phase, then inp[i] is or contains a nonstandard unicode character
                if str(emoTest)[2: -1] != inp[i]:
                    # if inp[i] is a unicode character, it'll output the file url for it, then later pick up as a local file image
                    stripped = str(emoTest)[2: -1].replace("\\\\u", "-").replace("\\\\U000", "-")[1:]
                    if is_file("emoji/" + stripped[:-5] + ".png"):  # I have a giant folder full of unicode emoji, conveniently named with their unicode string
                        stripped = stripped[:-5]
                    inp[i] = "emoji/" + stripped + ".png"  # congratulations, now we have the filename of a unicode emoji image
                if exists(get_emoji_url(inp[i])):  # if, with some string magic, the result is a valid url leading to a discord-hosted image...
                    inp[i] = get_emoji_url(inp[i])  # get dat url
                if inp[i][:4] == "http":  # we assume in good faith that any string starting with http will become a link to an image
                    inp[i] = getUrl(inp[i])
                if is_file(inp[i]):  # is inp[i] a string that's also a valid local file? try to open it as an image
                    image = Image.open(inp[i])
                    if inp[i][0:5].isdigit():  # with the save command, you'll occasionally see images that are meant to burn after use
                        os.remove(inp[i])  # I make a global assumption that any image with at least 5 digits leading in the name is meant to be temporary
                    inp[i] = image
                if type(inp[i]) is PIL.GifImagePlugin.GifImageFile:
                    inp[i] = pil_to_list(inp[i])
            except Exception as e:
                print("failure happened in formatting stage...")
                print(e)
                return e
                pass
        else:
            pass
    return inp


def types(inp):  # function to get the types of a list of things and output a list of types
    olist = []
    for i in inp:
        olist.append(type(i))
    return olist


def correctTypes(inp):  # brute force try to change to int/float
    olist = []
    for i in inp:
        try:
            olist.append(int(i))
        except:
            try:
                olist.append(float(i))
            except:
                if type(i) is list and type(i[0]) is not PIL.Image.Image:
                    olist.append(' '.join(i))
                else:
                    olist.append(i)
                pass
    return olist


def imageProcessing(inp):  # here we take the nested processing list and start chunking out images
    olist = []
    for i in range(len(inp)):  # maybe wait until we reach the end to try running it as a command? lets us run logic first...
        if str(inp[i]) in dict:  # this if/else branch means that the outlist excludes commands, but includes their results...
            cmd = inp[i]
            args = []
            if type(inp[i + 1]) is list:
                args = correctTypes(formatting(imageProcessing(inp[i + 1])))  # inp[i+1] is the the list or object that follows the command read
                print("args:", args)
                # so args[0] is the result of the above image processing/formatting that gets linked files and processes commands present
            else:
                args = correctTypes(formatting(inp[i + 1]))
            if type(args[0]) is list and type(args[0][0]) is PIL.Image.Image: # probably a legacy feature? makes more sense to have this branch internal in the future
                # if type(args[0]) is PIL.Image.Image:
                #     print("gifbranch")
                #     args[0] = pil_to_list(args[0])
                # print("running with the args:", args)
                # henceforth we're assuming that all functions return an image object/array and duration/duration_array
                # presumably duration/duration_array doesn't need to be exposed to the user, at least not yet?
                inp[i + 1] = dict[cmd][-1](*args)  # we're gonna assume that frame duration will either be a list or a single value...
            else:
                # print("running with the args:", args)
                inp[i + 1] = dict[cmd][0](*args)
            # else:  # if the value immediately following a command isn't a list, we assume the command only takes 1 input...
            #     args = formatting(inp[i + 1])  # just remember that formatting() returns a list, even when fed a single value
            #     if type(args[0]) is PIL.GifImagePlugin.GifImageFile or (type(args[0]) is list and type(args[0][0]) is PIL.Image.Image):
            #         if type(args[0]) is PIL.GifImagePlugin.GifImageFile:
            #             args[0], dur_arr = pil_to_list(args[0])
            #         print("running with the args:", args)
            #         inp[i + 1] = dict[cmd][-1](*args)  # I could theoretically use 1 instead of -1, but -1 doesn't break if the function only has 1 selector
            #     else:
            #         print("running with the args:", args)
            #         inp[i + 1] = dict[cmd][0](*args)  # this replaces inp[i + 1] with the output of the func run
        else:
            olist.append(inp[i])
    print("returning:", str(olist)[:20])
    return olist  # this result essentially replaces the command and following arg(s)


def save_gif(inp, rand_id, comp=1):
    images = []
    duration = inp[-1]
    frames = len(inp) - 1
    for f in range(0, frames):
        frame = inp[f].copy().convert('RGBA')
        alpha = frame.split()[3]
        if comp == 0:
            frame = frame.quantize(24, Image.FASTOCTREE, 0, Image.WEB)
        if comp == 1:
            frame = frame.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=254)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        frame.paste(255, mask)
        images.append(frame)
    images[0].save(str(rand_id) + '.gif', save_all=True, append_images=images[1:], duration=duration, loop=0, optimize=False, transparency=255, disposal=2)
    stat = os.path.getsize(str(rand_id) + '.gif')
    if stat > 8000000 and comp == 1:
        save_gif(inp, rand_id, 0)
    return str(rand_id) + '.gif'


def processing(inp):
    print("----------------")
    sterily = sterilize(str(inp['userinput']))
    print("sterilized:", sterily)
    testy = listify(sterily)
    print("listified:", testy)
    try:
        test = imageProcessing(testy.copy())
        print("whut", type(test))
        raw_image_data = test[0]  # presumably this will either be an image object or an array of image objects, which will each need to be handled differently...
        print("processing passed...", type(raw_image_data))
        print(raw_image_data)
        rand_id = str(random.randint(11111, 999999))
        if type(raw_image_data) is PIL.Image.Image or type(raw_image_data) is PIL.JpegImagePlugin.JpegImageFile:
            raw_image_data.save(rand_id + ".png")
            file_string = rand_id + ".png"
        else:
            file_string = save_gif(raw_image_data, rand_id)
        print("file string acquired")
        # if it's an array of images, and that array is very long, we'll want to save it with a high degree of dither, like we do for the dice animations...
        # or maybe we save, get the size, then if too large, compensate repeatedly until the result is either small enough or throw exception and fail?
        # inp['output'] = imageProcessing(testy.copy())[0]
        inp['output'] = file_string
        print('output was:', inp['output'])
    except Exception as e:
        inp['output'] = e
    client = Client(('localhost', 4000))
    payload = inp  # we just pass the json with all kinds of descriptive data, with the added processed 'output'
    client.send(payload)


if __name__ == '__main__':
    thr = threading.Thread(target=listening)
    thr.start()
    # thr2 = threading.Thread(target=awaiting)
    # thr2.start()
    while True:
        while len(taskQueue) > 0:
            job = taskQueue.pop(0)  # job is dict channel/command/message
            print(job)
            p = multiprocessing.Process(target=processing, args=(job,))
            p.start()
            # processing(job["command"], job["userinput"], job["channel"])
        time.sleep(0.1)
