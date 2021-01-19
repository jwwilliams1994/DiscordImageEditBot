import json, time, multiprocessing, threading, io, random, os.path, requests, PIL
from multiprocessing.connection import Client
from multiprocessing.connection import Listener
from PIL import Image
from image_mods.DickMan import processManImage, processManGif
from image_mods.intense import intensifytext
from image_mods.italicize import italicizePng, italicizeGif
from image_mods.jpegify import JpegImage, JpegGif
from image_mods.jpegify2 import JpegGif2, JpegImage2
from image_mods.jpegify3 import JpegGif3, JpegImage3
from image_mods.mockingSpongebob import mockingSpongebob
from image_mods.monkaShoot import processShootImage
from image_mods.notbttv import notBttv, notBttvDef, notBttvImg
from image_mods.pptasty import process4headImage, process4headGif, processwormholeImage, processwormholeGif, processSnapImage, processSnapImage2, \
    processSnapGif2, \
    processSnapImage3, processSnapGif3, processSnapImage4, processSnapGif4
from image_mods.shook import processMoreShookImage, processNukeImage, processCrazyShookImage, processShookImage, processGifImageT, processGifImageF, \
    processStaticImage, \
    processNukeGif, processShookGif, processMoreShookGif
from image_mods.space import processSpaceGif, processSpaceImage
from image_mods.speed import speedtext
from image_mods.peeking import peekingImage, peekingGif, peekingImage2, peekingGif2
from image_mods.simpleMod import rotateImg, rotateGif, flipImg, flipGif, hyperImg, hyperGif, information, information2, widen, widenGif, resize, resizeGif, \
    crop, cropGif, \
    thinking, thinkingGif, transparency, transparencyGif, save, saveGif, append, appendGif, getUrl, areyousure, justdoit, couch, manydoors, maskingPng, \
    maskingGif, \
    maskingPng2, maskingGif2, maskingOne, maskingTwo, maskingPng4, maskingGif4
from image_mods.textual import magicConch
from image_mods.ThreeDrendering import rendering3d, rendering3d2, rendering3dSpot, rendering3dSpotGif, renderingShrink3d, renderingShrink3dGif, \
    rendering3dSpotvol, \
    rendering3dSpotCop
from image_mods.wobbling import wobble, wobbleGif
from image_mods.Atmograph import atmograph2
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
        "mask2": [maskingPng2, maskingGif2], "mask3": [maskingOne, maskingOne], "overlaying": [maskingTwo, maskingTwo], "mask4": [maskingPng4, maskingGif4]}


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


def findList(inp):  # basically just looks backwards for a ']' and outputs the position of it in the input list as a negative number
    for i in range(len(inp)):
        if inp[-i] == ']':
            return -i
    return 0  # 0 is just a good value for 'it didn't find anything'... although I suppose this should maybe output an error


def listify(inp):  # takes the sterilized string and converts into nested lists
    odict = []  # this is for output, hence odict... although I suppose it's a list not a dict now
    for i in range(len(inp)):
        if inp[i] == '[':
            sep = findList(inp)
            if sep != 0 and sep != -1:  # there's probably an edge case here, but haven't found it yet
                odict = [*inp[:i], listify(inp[i + 1:sep]), *inp[sep + 1:]]
            else:
                odict = [*inp[:i], listify(inp[i + 1:sep])]
            if type(odict[0]) is list:
                odict[0] = ' '.join(odict[0])
            return odict
        else:
            if i == (len(inp) - 1):
                return inp
            else:
                sep = findList(inp)


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
            except Exception as e:
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
                olist.append(i)
                pass
    return olist


def imageProcessing(inp):  # here we take the nested processing list and start chunking out images
    olist = []
    for i in range(len(inp)):  # maybe wait until we reach the end to try running it as a command? lets us run logic first...
        if str(inp[i]) in dict:
            cmd = inp[i]
            if type(inp[i + 1]) is list:
                args = correctTypes(formatting(imageProcessing(inp[i + 1])))  # makes the next lines a cleaner read
                if type(args[0]) is PIL.GifImagePlugin.GifImageFile:  # probably a legacy feature? makes more sense to have this branch internal in the future
                    inp[i + 1] = dict[cmd][1](*args, str(random.randint(10000, 999999)))
                else:
                    inp[i + 1] = dict[cmd][0](*args, str(random.randint(10000, 999999)))
            else:  # if the value immediately following a command isn't a list, we assume the command only takes 1 input...
                inp[i + 1] = dict[cmd][0](*formatting(inp[i + 1]), str(random.randint(10000, 999999)))
        else:
            olist.append(inp[i])
    return olist


def processing(inp):
    testy = listify(sterilize(str(inp['userinput'])))
    try:
        inp['output'] = imageProcessing(testy.copy())[0]
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
