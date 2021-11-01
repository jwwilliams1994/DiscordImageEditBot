from math import pi, sin, cos, radians, floor

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import *
from direct.filter.CommonFilters import CommonFilters
from direct.particles.ParticleEffect import ParticleEffect
from PIL import Image, ImageChops
import io, os, time, threading
from panda3d.ode import OdeWorld, OdeSimpleSpace, OdeJointGroup
from panda3d.ode import OdeBody, OdeMass, OdeBoxGeom, OdePlaneGeom, OdeTriMeshData, OdeTriMeshGeom
from panda3d.core import BitMask32, CardMaker, Vec4, Quat
from random import randint, random
import random
import math


# myImage = OnscreenImage(image='testem.png', pos=(0, 0, 0))
# loadPrcFileData("", "window-type offscreen" )

def rendering3d(emoPng, yaw=1, pitch=0, roll=0):
    emojiId = random.randint(0,99999)
    base = ShowBase(windowType='offscreen')
    base.camNode.get_display_region(0).set_active(False)

    props = FrameBufferProperties()
    # Request 8 RGB bits, no alpha bits, and a depth buffer.
    props.set_rgba_bits(24, 24, 24, 24)
    props.set_rgb_color(True)
    props.set_depth_bits(24)
    # props.set_stereo(True)
    win_prop = WindowProperties.size(160, 160)
    flags = GraphicsPipe.BFFbPropsOptional | GraphicsPipe.BF_refuse_window

    buffer = base.graphicsEngine.make_output(base.pipe, "buffer", -100,
                                             props,
                                             win_prop, flags, base.win.getGsg(),
                                             base.win)
    texture = Texture()
    buffer.addRenderTexture(texture, GraphicsOutput.RTM_copy_ram)

    lens = PerspectiveLens()
    lens.setNearFar(-5, 1)
    lens.setFov(46)
    lens.setFocalLength(1.37795276)
    lens.set_interocular_distance(50)
    lens.set_convergence_distance(float('inf'))

    render = NodePath('mono')
    cam = base.makeCamera(buffer)
    cam.node().setLens(lens)
    cam.node().setScene(render)
    dp = buffer.makeDisplayRegion()
    dp.setCamera(cam)

    width, height = emoPng.size
    if width > height:
        bk = Image.new('RGBA', (width, width), (0, 0, 0, 0))
        bk.alpha_composite(emoPng, (0, round((width - height) / 2)))
    elif height > width:
        bk = Image.new('RGBA', (height, height), (0, 0, 0, 0))
        bk.alpha_composite(emoPng, (round((height - width) / 2), 0))
    else:
        bk = emoPng
    emoPng = bk
    emoPng.save(str(emojiId) + "texture.png")
    yTexture = loader.loadTexture(str(emojiId) + "texture.png")
    yTexture.setMagfilter(SamplerState.FT_nearest)
    yTexture.setMinfilter(SamplerState.FT_nearest)
    vertex_format = GeomVertexFormat.get_v3n3t2()
    vdata = GeomVertexData('name', vertex_format, Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, 'vertex')
    texcoord = GeomVertexWriter(vdata, 'texcoord')
    normal = GeomVertexWriter(vdata, 'normal')
    vertex.addData3(-2.5, 0, 2.5)
    texcoord.addData2(0, 1)
    normal.addData3(0, -1, 0)
    vertex.addData3(-2.5, 0, -2.5)
    texcoord.addData2(0, 0)
    normal.addData3(0, -1, 0)
    vertex.addData3(2.5, 0, 2.5)
    texcoord.addData2(1, 1)
    normal.addData3(0, -1, 0)
    vertex.addData3(2.5, 0, -2.5)
    texcoord.addData2(1, 0)
    normal.addData3(0, -1, 0)  # bottom right
    prim = GeomTriangles(Geom.UHStatic)
    prim.addVertices(0, 1, 2)
    prim.addVertices(3, 2, 1)
    vertex.addData3(-2.5, 0.2, 2.5)
    texcoord.addData2(0, 1)
    normal.addData3(0, 1, 0)
    vertex.addData3(-2.5, 0.2, -2.5)
    texcoord.addData2(0, 0)
    normal.addData3(0, 1, 0)
    vertex.addData3(2.5, 0.2, 2.5)
    texcoord.addData2(1, 1)
    normal.addData3(0, 1, 0)
    vertex.addData3(2.5, 0.2, -2.5)
    texcoord.addData2(1, 0)
    normal.addData3(0, 1, 0)
    prim.addVertices(6, 5, 4)
    prim.addVertices(5, 6, 7)

    geom = Geom(vdata)
    geom.addPrimitive(prim)

    node = GeomNode('gnode')
    node.addGeom(geom)

    nodePath = render.attachNewNode(node)
    nodePath.setTexture(yTexture)
    nodePath.setTransparency(True)
    nodePath.setTwoSided(False)

    images = []
    for f in range(360):
        nodePath.setHpr(f * yaw, f * pitch, f * roll)
        base.camera.setPos(0, -8, 0)
        base.camera.lookAt(0, 0, 0)
        base.graphicsEngine.renderFrame()
        peeking = texture.peek()
        width, height = peeking.getXSize(), peeking.getYSize()
        img = Image.new('RGBA', (width, height), 0)
        out = img.load()
        test = LColor()
        peeking.fetchPixel(test, 0, 0)
        for x in range(width):
            for y in range(height):
                peeking.fetchPixel(test, x, y)
                r, g, b, a = round(test.getCell(0) * 255), round(test.getCell(1) * 255), round(test.getCell(2) * 255), round(test.getCell(3) * 255)
                out[x, height - 1 - y] = (r, g, b, a)
        images.append(img)
    os.remove(str(emojiId) + "texture.png")
    images.append(20)
    return images
images = []


def rendering3d2(emoGif, yaw, pitch, roll):
    emojiId = random.randint(0,99999)
    base = ShowBase(windowType='offscreen')
    base.camNode.get_display_region(0).set_active(False)

    props = FrameBufferProperties()
    # Request 8 RGB bits, no alpha bits, and a depth buffer.
    props.set_rgba_bits(24, 24, 24, 24)
    props.set_rgb_color(True)
    props.set_depth_bits(24)
    # props.set_stereo(True)
    win_prop = WindowProperties.size(160, 160)
    flags = GraphicsPipe.BFFbPropsOptional | GraphicsPipe.BF_refuse_window

    buffer = base.graphicsEngine.make_output(base.pipe, "buffer", -100,
                                             props,
                                             win_prop, flags, base.win.getGsg(),
                                             base.win)
    texture = Texture()
    buffer.addRenderTexture(texture, GraphicsOutput.RTM_copy_ram)

    lens = PerspectiveLens()
    lens.setFov(46)
    lens.setFocalLength(1.37795276)
    lens.set_interocular_distance(50)
    lens.set_convergence_distance(float('inf'))

    render = NodePath('mono')
    cam = base.makeCamera(buffer)
    cam.node().setLens(lens)
    cam.node().setScene(render)
    dp = buffer.makeDisplayRegion()
    dp.setCamera(cam)
    testFrames = []
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    if type(gifDuration) is list:
        gifDuration = gifDuration[0]
    texList = []
    for i in range(totalFrames):
        emoPng = emoGif[i].copy().convert('RGBA')
        width, height = emoPng.size
        if width > height:
            bk = Image.new('RGBA', (width, width), (0, 0, 0, 0))
            bk.alpha_composite(emoPng, (0, round((width - height) / 2)))
        elif height > width:
            bk = Image.new('RGBA', (height, height), (0, 0, 0, 0))
            bk.alpha_composite(emoPng, (round((height - width) / 2), 0))
        else:
            bk = emoPng
        emoPng = bk
        step = io.BytesIO()
        emoPng.save(step, 'png')
        im_bytes = step.getvalue()
        myImage = PNMImage()
        myImage.read(StringStream(im_bytes))
        texList.append(myImage)
    yTexture = Texture()
    yTexture.setMagfilter(SamplerState.FT_nearest)
    yTexture.setMinfilter(SamplerState.FT_nearest)
    vertex_format = GeomVertexFormat.get_v3t2()
    vdata = GeomVertexData('name', vertex_format, Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, 'vertex')
    texcoord = GeomVertexWriter(vdata, 'texcoord')
    vertex.addData3(-2.5, 0, 2.5)
    texcoord.addData2(0, 1)
    vertex.addData3(-2.5, 0, -2.5)
    texcoord.addData2(0, 0)
    vertex.addData3(2.5, 0, 2.5)
    texcoord.addData2(1, 1)
    vertex.addData3(2.5, 0, -2.5)
    texcoord.addData2(1, 0)
    prim = GeomTriangles(Geom.UHStatic)
    prim.addVertices(0, 1, 2)
    prim.addVertices(3, 2, 1)

    geom = Geom(vdata)
    geom.addPrimitive(prim)

    node = GeomNode('gnode')
    node.addGeom(geom)

    nodePath = render.attachNewNode(node)
    nodePath.setTexture(yTexture)
    nodePath.setTransparency(True)
    nodePath.setTwoSided(True)

    maxFrames = round(totalFrames * (gifDuration / 20))
    maxFrames2 = maxFrames
    frame_ratio = (gifDuration / 20) * (maxFrames / maxFrames2)
    angRat = (360 / maxFrames2)
    print(maxFrames2, len(texList))
    maxf = 0
    for f in range(-3, maxFrames2, 1):
        framePick = int(floor((f * frame_ratio) % totalFrames))
        print(framePick, f)
        yTexture.load(texList[framePick])
        maxf = f
        nodePath.setHpr(f * yaw * angRat, f * pitch * angRat, f * roll * angRat)
        base.camera.setPos(0, -10, 1)
        base.camera.lookAt(0, 0, 0)
        base.graphicsEngine.renderFrame()
        peeking = texture.peek()
        width, height = peeking.getXSize(), peeking.getYSize()
        img = Image.new('RGBA', (width, height), 0)
        out = img.load()
        test = LColor()
        peeking.fetchPixel(test, 0, 0)
        if f >= 0:
            images.append('')
            thr = threading.Thread(target=renderFrame, args=(width, height, peeking, f))
            thr.start()
    while len(images) < maxf + 1 or images[-1] == '':
        print("waiting...")
        time.sleep(0.1)
    images.append(20)
    return images


def sumColor(colorList):
    r = 0
    g = 0
    b = 0
    a = 1
    m = 80
    for i in colorList:
        r += i[0]
        g += i[1]
        b += i[2]
    r = r / (len(colorList) * m)
    g = g / (len(colorList) * m)
    b = b / (len(colorList) * m)
    rCol = (r, g, b, a)
    # print(rCol)
    return rCol


def rendering3dSpot(emoPng, yaw, pitch, roll, ri, gi, bi):
    emojiId = random.randint(0,99999)
    base = ShowBase(windowType='offscreen')
    base.camNode.get_display_region(0).set_active(False)

    props = FrameBufferProperties()
    # Request 8 RGB bits, no alpha bits, and a depth buffer.
    props.set_rgba_bits(24, 24, 24, 24)
    props.set_rgb_color(True)
    props.set_depth_bits(24)
    # props.set_stereo(True)
    win_prop = WindowProperties.size(160, 160)
    flags = GraphicsPipe.BFFbPropsOptional | GraphicsPipe.BF_refuse_window

    buffer = base.graphicsEngine.make_output(base.pipe, "buffer", -100,
                                             props,
                                             win_prop, flags, base.win.getGsg(),
                                             base.win)
    texture = Texture()
    buffer.addRenderTexture(texture, GraphicsOutput.RTM_copy_ram)

    lens = PerspectiveLens()
    # lens.setNearFar(0.6, 1000)
    lens.setFov(46)
    lens.setFocalLength(1.37795276)
    lens.set_interocular_distance(50)
    lens.set_convergence_distance(float('inf'))

    render = NodePath('mono')
    cam = base.makeCamera(buffer)
    cam.node().setLens(lens)
    cam.node().setScene(render)
    dp = buffer.makeDisplayRegion()
    dp.setCamera(cam)

    vFormat = GeomVertexFormat.get_v3n3c4()
    vdata2 = GeomVertexData('box', vFormat, Geom.UHStatic)
    vertx = GeomVertexWriter(vdata2, 'vertex')
    norm = GeomVertexWriter(vdata2, 'normal')
    colo = GeomVertexWriter(vdata2, 'color')
    tColor = [0.2, 0.2, 0.2, 1]
    siz = 32
    vertx.addData3(-siz, siz, siz)  # 0 top back left
    norm.addData3(1, -1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, siz, siz)  # 1 top back right
    norm.addData3(-1, -1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, siz, -siz)  # 2 bottom back right
    norm.addData3(-1, -1, 1)
    colo.addData4(*tColor)
    vertx.addData3(-siz, siz, -siz)  # 3 bottom back left
    norm.addData3(1, -1, 1)
    colo.addData4(*tColor)
    vertx.addData3(-siz, -siz, siz)  # 4 top front left
    norm.addData3(1, 1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, -siz, siz)  # 5 top front right
    norm.addData3(-1, 1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, -siz, -siz)  # 6 bottom front right
    norm.addData3(-1, 1, 1)
    colo.addData4(*tColor)
    vertx.addData3(-siz, -siz, -siz)  # 7 bottom front left
    norm.addData3(1, 1, 1)
    colo.addData4(*tColor)
    prm = GeomTriangles(Geom.UHStatic)
    prm.addVertices(2, 1, 0)
    prm.addVertices(3, 2, 0)
    prm.addVertices(6, 2, 3)
    prm.addVertices(7, 6, 3)

    geom2 = Geom(vdata2)
    geom2.addPrimitive(prm)

    node2 = GeomNode('gnode')
    node2.addGeom(geom2)

    nodePath2 = render.attachNewNode(node2)
    nodePath2.setTwoSided(False)
    width, height = emoPng.size
    if width > height:
        bk = Image.new('RGBA', (width, width), (0, 0, 0, 0))
        bk.alpha_composite(emoPng, (0, round((width - height) / 2)))
    elif height > width:
        bk = Image.new('RGBA', (height, height), (0, 0, 0, 0))
        bk.alpha_composite(emoPng, (round((height - width) / 2), 0))
    else:
        bk = emoPng
    bk.save(str(emojiId) + "texture.png")
    yTexture = loader.loadTexture(str(emojiId) + "texture.png")
    yTexture.setMagfilter(SamplerState.FT_nearest)
    yTexture.setMinfilter(SamplerState.FT_nearest)
    vertex_format = GeomVertexFormat.get_v3n3t2()
    vdata = GeomVertexData('name', vertex_format, Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, 'vertex')
    texcoord = GeomVertexWriter(vdata, 'texcoord')
    normal = GeomVertexWriter(vdata, 'normal')
    thk = 0.4
    vertex.addData3(-2.5, 0, 2.5)
    texcoord.addData2(0, 1)
    normal.addData3(0, -1, 0)
    vertex.addData3(-2.5, 0, -2.5)
    texcoord.addData2(0, 0)
    normal.addData3(0, -1, 0)
    vertex.addData3(2.5, 0, 2.5)
    texcoord.addData2(1, 1)
    normal.addData3(0, -1, 0)
    vertex.addData3(2.5, 0, -2.5)
    texcoord.addData2(1, 0)
    normal.addData3(0, -1, 0)  # bottom right
    prim = GeomTriangles(Geom.UHStatic)
    prim.addVertices(0, 1, 2)
    prim.addVertices(3, 2, 1)
    vertex.addData3(-2.5, thk, 2.5)
    texcoord.addData2(0, 1)
    normal.addData3(0, 1, 0)
    vertex.addData3(-2.5, thk, -2.5)
    texcoord.addData2(0, 0)
    normal.addData3(0, 1, 0)
    vertex.addData3(2.5, thk, 2.5)
    texcoord.addData2(1, 1)
    normal.addData3(0, 1, 0)
    vertex.addData3(2.5, thk, -2.5)
    texcoord.addData2(1, 0)
    normal.addData3(0, 1, 0)
    prim.addVertices(6, 5, 4)
    prim.addVertices(5, 6, 7)

    geom = Geom(vdata)
    geom.addPrimitive(prim)

    node = GeomNode('gnode')
    node.addGeom(geom)

    nodePath = render.attachNewNode(node)
    nodePath.setTexture(yTexture)
    nodePath.setTransparency(True)
    nodePath.setTwoSided(False)
    # nodePath.setDepthOffset(1)

    ambientLight = render.attachNewNode(AmbientLight("ambientLight"))
    # Set the color of the ambient light
    # ri, gi, bi = 256, 256, 256
    r = (ri / 256) * 6
    g = (gi / 256) * 6
    b = (bi / 256) * 6
    lColor1 = (r, g, b, 1)
    clist = [lColor1]
    ambientLight.node().setColor(sumColor(clist))

    plight = Spotlight('plight')
    plight.setColor(lColor1)
    plight.setAttenuation(LVector3(1, 0.03, 0))
    plight.setShadowCaster(True, 512, 512)
    # plight.setExponent(60)
    plight.setLens(PerspectiveLens())
    plight.getLens().setFov(70, 70)
    plnp = render.attachNewNode(plight)
    plnp.setPos(2, -10, 3)
    plnp.lookAt(0, 0, 0)
    render.setLight(plnp)

    render.setLight(ambientLight)
    perPixelEnabled = True
    render.setShaderAuto()

    # images = []
    maxf = 0
    for f in range(-3, 360):
        if f%10 == 1:
            print(str(round((f/360)*100)) + "%")
        maxf = f
        nodePath.setHpr(f * yaw, f * pitch, f * roll)
        # nodePath2.setHpr(f*yaw, f*pitch, f*roll)
        base.camera.setPos(0, -10, 1)
        base.camera.lookAt(0, 0, 0)
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        peeking = texture.peek()
        width, height = peeking.getXSize(), peeking.getYSize()
        img = Image.new('RGBA', (width, height), 0)
        out = img.load()
        # test = LColor()
        # peeking.fetchPixel(test, 0, 0)
        if f >= 0:
            images.append('')
            thr = threading.Thread(target=renderFrame, args=(width, height, peeking, f))
            thr.start()
            # for x in range(width):
            #     for y in range(height):
            #         peeking.fetchPixel(test, x, y)
            #         r, g, b, a = round(test.getCell(0) * 255), round(test.getCell(1) * 255), round(test.getCell(2) * 255), round(test.getCell(3) * 255)
            #         out[x, height - 1 - y] = (r, g, b, a)
            # alpha = img.split()[3]
            # img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
            # mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            # img.paste(255, mask)
            # images.append(img)
        if yaw == 0 and pitch == 0 and roll == 0 and f == 0:
            break
    while len(images) < maxf + 1 or images[-1] == '':
        print("waiting...")
        time.sleep(0.1)
    os.remove(str(emojiId) + "texture.png")
    images.append(20)
    return images


def renderFrame(width, height, peeks, f):
    img = Image.new('RGBA', (width, height), 0)
    out = img.load()
    colors = LColor()
    for x in range(width):
        for y in range(height):
            peeks.fetchPixel(colors, x, y)
            r, g, b, a = round(colors.getCell(0) * 255), round(colors.getCell(1) * 255), round(colors.getCell(2) * 255), round(colors.getCell(3) * 255)
            out[x, height - 1 - y] = (r, g, b, a)
    # alpha = img.split()[3]
    # img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
    # mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    # img.paste(255, mask)
    # print(f)
    images[f] = img


def rendering3dSpotGif(emoGif, yaw, pitch, roll, ri, gi, bi):
    emojiId = random.randint(0,99999)
    base = ShowBase(windowType='offscreen')
    base.camNode.get_display_region(0).set_active(False)

    props = FrameBufferProperties()
    # Request 8 RGB bits, no alpha bits, and a depth buffer.
    props.set_rgba_bits(24, 24, 24, 24)
    props.set_rgb_color(True)
    props.set_depth_bits(24)
    # props.set_stereo(True)
    win_prop = WindowProperties.size(160, 160)
    flags = GraphicsPipe.BFFbPropsOptional | GraphicsPipe.BF_refuse_window

    buffer = base.graphicsEngine.make_output(base.pipe, "buffer", -100,
                                             props,
                                             win_prop, flags, base.win.getGsg(),
                                             base.win)
    texture = Texture()
    buffer.addRenderTexture(texture, GraphicsOutput.RTM_copy_ram)

    lens = PerspectiveLens()
    # lens.setNearFar(0.6, 1000)
    lens.setFov(46)
    lens.setFocalLength(1.37795276)
    lens.set_interocular_distance(50)
    lens.set_convergence_distance(float('inf'))

    render = NodePath('mono')
    cam = base.makeCamera(buffer)
    cam.node().setLens(lens)
    cam.node().setScene(render)
    dp = buffer.makeDisplayRegion()
    dp.setCamera(cam)

    vFormat = GeomVertexFormat.get_v3n3c4()
    vdata2 = GeomVertexData('box', vFormat, Geom.UHStatic)
    vertx = GeomVertexWriter(vdata2, 'vertex')
    norm = GeomVertexWriter(vdata2, 'normal')
    colo = GeomVertexWriter(vdata2, 'color')
    tColor = [0.2, 0.2, 0.2, 1]
    siz = 32
    vertx.addData3(-siz, siz, siz)  # 0 top back left
    norm.addData3(1, -1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, siz, siz)  # 1 top back right
    norm.addData3(-1, -1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, siz, -siz)  # 2 bottom back right
    norm.addData3(-1, -1, 1)
    colo.addData4(*tColor)
    vertx.addData3(-siz, siz, -siz)  # 3 bottom back left
    norm.addData3(1, -1, 1)
    colo.addData4(*tColor)
    vertx.addData3(-siz, -siz, siz)  # 4 top front left
    norm.addData3(1, 1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, -siz, siz)  # 5 top front right
    norm.addData3(-1, 1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, -siz, -siz)  # 6 bottom front right
    norm.addData3(-1, 1, 1)
    colo.addData4(*tColor)
    vertx.addData3(-siz, -siz, -siz)  # 7 bottom front left
    norm.addData3(1, 1, 1)
    colo.addData4(*tColor)
    prm = GeomTriangles(Geom.UHStatic)
    prm.addVertices(2, 1, 0)
    prm.addVertices(3, 2, 0)
    prm.addVertices(6, 2, 3)
    prm.addVertices(7, 6, 3)

    geom2 = Geom(vdata2)
    geom2.addPrimitive(prm)

    node2 = GeomNode('gnode')
    node2.addGeom(geom2)

    nodePath2 = render.attachNewNode(node2)
    nodePath2.setTwoSided(False)

    testFrames = []
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    if type(gifDuration) is list:
        gifDuration = gifDuration[0]
    texList = []
    for i in range(totalFrames):
        emoPng = emoGif[i].copy().convert('RGBA')
        width, height = emoPng.size
        if width > height:
            bk = Image.new('RGBA', (width, width), (0, 0, 0, 0))
            bk.alpha_composite(emoPng, (0, round((width - height) / 2)))
        elif height > width:
            bk = Image.new('RGBA', (height, height), (0, 0, 0, 0))
            bk.alpha_composite(emoPng, (round((height - width) / 2), 0))
        else:
            bk = emoPng
        emoPng = bk
        step = io.BytesIO()
        emoPng.save(step, 'png')
        im_bytes = step.getvalue()
        myImage = PNMImage()
        myImage.read(StringStream(im_bytes))
        texList.append(myImage)
    yTexture = Texture()
    yTexture.setMagfilter(SamplerState.FT_nearest)
    yTexture.setMinfilter(SamplerState.FT_nearest)
    vertex_format = GeomVertexFormat.get_v3n3t2()
    vdata = GeomVertexData('name', vertex_format, Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, 'vertex')
    texcoord = GeomVertexWriter(vdata, 'texcoord')
    normal = GeomVertexWriter(vdata, 'normal')
    thk = 0.4
    vertex.addData3(-2.5, 0, 2.5)
    texcoord.addData2(0, 1)
    normal.addData3(0, -1, 0)
    vertex.addData3(-2.5, 0, -2.5)
    texcoord.addData2(0, 0)
    normal.addData3(0, -1, 0)
    vertex.addData3(2.5, 0, 2.5)
    texcoord.addData2(1, 1)
    normal.addData3(0, -1, 0)
    vertex.addData3(2.5, 0, -2.5)
    texcoord.addData2(1, 0)
    normal.addData3(0, -1, 0)  # bottom right
    prim = GeomTriangles(Geom.UHStatic)
    prim.addVertices(0, 1, 2)
    prim.addVertices(3, 2, 1)
    vertex.addData3(-2.5, thk, 2.5)
    texcoord.addData2(0, 1)
    normal.addData3(0, 1, 0)
    vertex.addData3(-2.5, thk, -2.5)
    texcoord.addData2(0, 0)
    normal.addData3(0, 1, 0)
    vertex.addData3(2.5, thk, 2.5)
    texcoord.addData2(1, 1)
    normal.addData3(0, 1, 0)
    vertex.addData3(2.5, thk, -2.5)
    texcoord.addData2(1, 0)
    normal.addData3(0, 1, 0)
    prim.addVertices(6, 5, 4)
    prim.addVertices(5, 6, 7)

    geom = Geom(vdata)
    geom.addPrimitive(prim)

    node = GeomNode('gnode')
    node.addGeom(geom)

    nodePath = render.attachNewNode(node)
    nodePath.setTexture(yTexture)
    nodePath.setTransparency(True)
    nodePath.setTwoSided(False)
    # nodePath.setDepthOffset(1)

    ambientLight = render.attachNewNode(AmbientLight("ambientLight"))
    # Set the color of the ambient light
    # ri, gi, bi = 256, 256, 256
    r = (ri / 256) * 6
    g = (gi / 256) * 6
    b = (bi / 256) * 6
    lColor1 = (r, g, b, 1)
    clist = [lColor1]
    ambientLight.node().setColor(sumColor(clist))

    plight = Spotlight('plight')
    plight.setColor(lColor1)
    plight.setAttenuation(LVector3(1, 0.03, 0))
    plight.setShadowCaster(True, 512, 512)
    # plight.setExponent(60)
    plight.setLens(PerspectiveLens())
    plight.getLens().setFov(70, 70)
    plnp = render.attachNewNode(plight)
    plnp.setPos(2, -10, 3)
    plnp.lookAt(0, 0, 0)
    render.setLight(plnp)

    render.setLight(ambientLight)
    perPixelEnabled = True
    render.setShaderAuto()

    # if totalFrames < 360:
    #     maxFrames = totalFrames * round(360 / totalFrames)
    # else:
    #     maxFrames = totalFrames
    # angRat = 360 / maxFrames
    maxFrames = round(totalFrames * (gifDuration / 20))
    maxFrames2 = maxFrames
    frame_ratio = 20/gifDuration
    angRat = (360 / maxFrames2)
    print(maxFrames2, len(texList))
    maxf = 0
    for f in range(-3, maxFrames2, 1):
        if f%10 == 1:
            print(str(round((f/maxFrames2)*100)) + "%")
        framePick = int(floor((f * frame_ratio) % totalFrames))
        #print(framePick, f)
        yTexture.load(texList[framePick])
        maxf = f
        nodePath.setHpr(f * yaw * angRat, f * pitch * angRat, f * roll * angRat)
        base.camera.setPos(0, -10, 1)
        base.camera.lookAt(0, 0, 0)
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        time.sleep(0.1)
        base.graphicsEngine.renderFrame()
        peeking = texture.peek()
        width, height = peeking.getXSize(), peeking.getYSize()
        if f >= 0:
            images.append('')
            thr = threading.Thread(target=renderFrame, args=(width, height, peeking, f))
            thr.start()
    while len(images) < maxf + 1 or images[-1] == '':
        print("waiting...")
        time.sleep(0.1)
    images.append(20)
    return images


def renderingShrink3d(emoPng, pace, iDist):
    emojiId = random.randint(0, 99999)
    base = ShowBase(windowType='offscreen')
    base.camNode.get_display_region(0).set_active(False)

    props = FrameBufferProperties()
    # Request 8 RGB bits, no alpha bits, and a depth buffer.
    props.set_rgba_bits(24, 24, 24, 24)
    props.set_rgb_color(True)
    props.set_depth_bits(24)
    # props.set_stereo(True)
    win_prop = WindowProperties.size(120, 120)
    flags = GraphicsPipe.BFFbPropsOptional | GraphicsPipe.BF_refuse_window

    buffer = base.graphicsEngine.make_output(base.pipe, "buffer", -100,
                                             props,
                                             win_prop, flags, base.win.getGsg(),
                                             base.win)
    texture = Texture()
    buffer.addRenderTexture(texture, GraphicsOutput.RTM_copy_ram)

    lens = PerspectiveLens()
    #lens.setNearFar(-5, 1)
    lens.setFov(46)
    lens.setFocalLength(1.37795276)
    lens.set_interocular_distance(50)
    lens.set_convergence_distance(float('inf'))

    render = NodePath('mono')
    cam = base.makeCamera(buffer)
    cam.node().setLens(lens)
    cam.node().setScene(render)
    dp = buffer.makeDisplayRegion()
    dp.setCamera(cam)

    width, height = emoPng.size
    if width > height:
        bk = Image.new('RGBA', (width, width), (0, 0, 0, 0))
        bk.alpha_composite(emoPng, (0, round((width - height) / 2)))
        emoPng = bk
    elif height > width:
        bk = Image.new('RGBA', (height, height), (0, 0, 0, 0))
        bk.alpha_composite(emoPng, (round((height - width) / 2), 0))
        emoPng = bk
    emoPng.save(str(emojiId) + "texture.png")
    yTexture = loader.loadTexture(str(emojiId) + "texture.png")
    yTexture.setMagfilter(SamplerState.FT_nearest)
    yTexture.setMinfilter(SamplerState.FT_nearest)
    vertex_format = GeomVertexFormat.get_v3n3t2()
    vdata = GeomVertexData('name', vertex_format, Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, 'vertex')
    texcoord = GeomVertexWriter(vdata, 'texcoord')
    normal = GeomVertexWriter(vdata, 'normal')
    vertex.addData3(-2.5, 0, 2.5)
    texcoord.addData2(0, 1)
    normal.addData3(0, -1, 0)
    vertex.addData3(-2.5, 0, -2.5)
    texcoord.addData2(0, 0)
    normal.addData3(0, -1, 0)
    vertex.addData3(2.5, 0, 2.5)
    texcoord.addData2(1, 1)
    normal.addData3(0, -1, 0)
    vertex.addData3(2.5, 0, -2.5)
    texcoord.addData2(1, 0)
    normal.addData3(0, -1, 0)  # bottom right
    prim = GeomTriangles(Geom.UHStatic)
    prim.addVertices(0, 1, 2)
    prim.addVertices(3, 2, 1)
    vertex.addData3(-2.5, 0.2, 2.5)
    texcoord.addData2(0, 1)
    normal.addData3(0, 1, 0)
    vertex.addData3(-2.5, 0.2, -2.5)
    texcoord.addData2(0, 0)
    normal.addData3(0, 1, 0)
    vertex.addData3(2.5, 0.2, 2.5)
    texcoord.addData2(1, 1)
    normal.addData3(0, 1, 0)
    vertex.addData3(2.5, 0.2, -2.5)
    texcoord.addData2(1, 0)
    normal.addData3(0, 1, 0)
    prim.addVertices(6, 5, 4)
    prim.addVertices(5, 6, 7)

    geom = Geom(vdata)
    geom.addPrimitive(prim)

    node = GeomNode('gnode')
    node.addGeom(geom)

    nodePath = render.attachNewNode(node)
    nodePath.setTexture(yTexture)
    nodePath.setTransparency(True)
    nodePath.setTwoSided(False)
    base.camera.lookAt(0, 0, 0)

    for f in range(400):
        if f%10 == 1:
            print(str(round((f/400)*100)) + "%")
        # nodePath.setHpr(f * yaw, f * pitch, f * roll)
        base.camera.setPos(0, (-6 - ((pace/10)*f) - (40 * iDist)), 0)
        #base.camera.lookAt(0, 0, 0)
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        peeking = texture.peek()
        width, height = peeking.getXSize(), peeking.getYSize()
        if f >= 0:
            images.append('')
            # renderFrame(width, height, peeking, f)
            thr = threading.Thread(target=renderFrame, args=(width, height, peeking, f))
            thr.start()
    while len(images) < 400 or images[-1] == '':
        print("waiting...")
        time.sleep(0.2)
    os.remove(str(emojiId) + "texture.png")
    images.append(20)
    return images


def renderingShrink3dGif(emoGif, pace, iDist):
    emojiId = random.randint(0,99999)
    base = ShowBase(windowType='offscreen')
    base.camNode.get_display_region(0).set_active(False)

    props = FrameBufferProperties()
    # Request 8 RGB bits, no alpha bits, and a depth buffer.
    props.set_rgba_bits(24, 24, 24, 24)
    props.set_rgb_color(True)
    props.set_depth_bits(24)
    # props.set_stereo(True)
    win_prop = WindowProperties.size(120, 120)
    flags = GraphicsPipe.BFFbPropsOptional | GraphicsPipe.BF_refuse_window

    buffer = base.graphicsEngine.make_output(base.pipe, "buffer", -100,
                                             props,
                                             win_prop, flags, base.win.getGsg(),
                                             base.win)
    texture = Texture()
    buffer.addRenderTexture(texture, GraphicsOutput.RTM_copy_ram)

    lens = PerspectiveLens()
    lens.setFov(46)
    lens.setFocalLength(1.37795276)
    lens.set_interocular_distance(50)
    lens.set_convergence_distance(float('inf'))

    render = NodePath('mono')
    cam = base.makeCamera(buffer)
    cam.node().setLens(lens)
    cam.node().setScene(render)
    dp = buffer.makeDisplayRegion()
    dp.setCamera(cam)
    testFrames = []
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    if type(gifDuration) is list:
        gifDuration = gifDuration[0]
    texList = []
    for i in range(totalFrames):
        emoPng = emoGif[i].copy().convert('RGBA')
        width, height = emoPng.size
        if width > height:
            bk = Image.new('RGBA', (width, width), (0, 0, 0, 0))
            bk.alpha_composite(emoPng, (0, round((width - height) / 2)))
        elif height > width:
            bk = Image.new('RGBA', (height, height), (0, 0, 0, 0))
            bk.alpha_composite(emoPng, (round((height - width) / 2), 0))
        else:
            bk = emoPng
        emoPng = bk
        step = io.BytesIO()
        emoPng.save(step, 'png')
        im_bytes = step.getvalue()
        myImage = PNMImage()
        myImage.read(StringStream(im_bytes))
        texList.append(myImage)
    yTexture = Texture()
    yTexture.setMagfilter(SamplerState.FT_nearest)
    yTexture.setMinfilter(SamplerState.FT_nearest)
    vertex_format = GeomVertexFormat.get_v3t2()
    vdata = GeomVertexData('name', vertex_format, Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, 'vertex')
    texcoord = GeomVertexWriter(vdata, 'texcoord')
    vertex.addData3(-2.5, 0, 2.5)
    texcoord.addData2(0, 1)
    vertex.addData3(-2.5, 0, -2.5)
    texcoord.addData2(0, 0)
    vertex.addData3(2.5, 0, 2.5)
    texcoord.addData2(1, 1)
    vertex.addData3(2.5, 0, -2.5)
    texcoord.addData2(1, 0)
    prim = GeomTriangles(Geom.UHStatic)
    prim.addVertices(0, 1, 2)
    prim.addVertices(3, 2, 1)

    geom = Geom(vdata)
    geom.addPrimitive(prim)

    node = GeomNode('gnode')
    node.addGeom(geom)

    nodePath = render.attachNewNode(node)
    nodePath.setTexture(yTexture)
    nodePath.setTransparency(True)
    nodePath.setTwoSided(True)

    frame_ratio = (gifDuration / 80)
    base.camera.lookAt(0, 0, 0)
    for f in range(400):
        if f%10 == 1:
            print(str(round((f/400)*100)) + "%") # frame pick logic needs redoing...
        # framePick = int(floor((f * frame_ratio) % totalFrames))
        framePick = floor(f * (20 / gifDuration)) % (totalFrames)
        yTexture.load(texList[int(framePick)]) # input here is 0 - max frame in int
        #nodePath.setHpr(f * yaw * angRat, f * pitch * angRat, f * roll * angRat)
        base.camera.setPos(0, (-6 - ((pace/10)*f) - (40 * iDist)), 0)
        #base.camera.lookAt(0, 0, 0)
        base.graphicsEngine.renderFrame()
        time.sleep(0.05)
        base.graphicsEngine.renderFrame()
        peeking = texture.peek()
        width, height = peeking.getXSize(), peeking.getYSize()
        if f >= 0:
            images.append('')
            thr = threading.Thread(target=renderFrame, args=(width, height, peeking, f))
            thr.start()
    while len(images) < 400 or images[-1] == '':
        print("waiting...")
        time.sleep(0.2)
    # os.remove(str(emojiId) + "texture.png")
    images.append(20)
    return images


def sumColor2(colorList):
    r = 0
    g = 0
    b = 0
    a = 1
    m = 20
    for i in colorList:
        r += i[0]
        g += i[1]
        b += i[2]
    r = r / (len(colorList) * m)
    g = g / (len(colorList) * m)
    b = b / (len(colorList) * m)
    rCol = (r, g, b, a)
    # print(rCol)
    return rCol


def rendering3dSpotvol(emoPng, pace, iDist, ri, gi, bi, emojiId):
    base = ShowBase(windowType='offscreen')
    base.camNode.get_display_region(0).set_active(False)

    props = FrameBufferProperties()
    # Request 8 RGB bits, no alpha bits, and a depth buffer.
    props.set_rgba_bits(24, 24, 24, 24)
    props.set_rgb_color(True)
    props.set_depth_bits(24)
    # props.set_stereo(True)
    win_prop = WindowProperties.size(160, 160)
    flags = GraphicsPipe.BFFbPropsOptional #| GraphicsPipe.BF_refuse_window

    buffer = base.graphicsEngine.make_output(base.pipe, "buffer", -100,
                                             props,
                                             win_prop, flags, base.win.getGsg(),
                                             base.win)
    texture = Texture()
    buffer.addRenderTexture(texture, GraphicsOutput.RTM_copy_ram)

    lens = PerspectiveLens()
    # lens.setNearFar(0.6, 1000)
    lens.setFov(46)
    lens.setFocalLength(1.37795276)
    lens.set_interocular_distance(50)
    lens.set_convergence_distance(float('inf'))

    render = NodePath('mono')
    cam = base.makeCamera(buffer)
    cam.node().setLens(lens)
    cam.node().setScene(render)
    dp = buffer.makeDisplayRegion()
    dp.setCamera(cam)

    vFormat = GeomVertexFormat.get_v3n3c4()
    vdata2 = GeomVertexData('box', vFormat, Geom.UHStatic)
    vertx = GeomVertexWriter(vdata2, 'vertex')
    norm = GeomVertexWriter(vdata2, 'normal')
    colo = GeomVertexWriter(vdata2, 'color')
    #tColor = [0.47, 0.71, 1, 1]
    tColor = [0, 0, 0, 1]
    siz = 100
    vertx.addData3(-siz, siz, siz)  # 0 top back left
    norm.addData3(1, -1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, siz, siz)  # 1 top back right
    norm.addData3(-1, -1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, siz, -siz)  # 2 bottom back right
    norm.addData3(-1, -1, 1)
    colo.addData4(*tColor)
    vertx.addData3(-siz, siz, -siz)  # 3 bottom back left
    norm.addData3(1, -1, 1)
    colo.addData4(*tColor)
    vertx.addData3(-siz, -siz, siz)  # 4 top front left
    norm.addData3(1, 1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, -siz, siz)  # 5 top front right
    norm.addData3(-1, 1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, -siz, -siz)  # 6 bottom front right
    norm.addData3(-1, 1, 1)
    colo.addData4(*tColor)
    vertx.addData3(-siz, -siz, -siz)  # 7 bottom front left
    norm.addData3(1, 1, 1)
    colo.addData4(*tColor)
    prm = GeomTriangles(Geom.UHStatic)
    prm.addVertices(2, 1, 0)
    prm.addVertices(3, 2, 0)
    prm.addVertices(6, 2, 3)
    prm.addVertices(7, 6, 3)

    geom2 = Geom(vdata2)
    geom2.addPrimitive(prm)

    node2 = GeomNode('gnode')
    node2.addGeom(geom2)

    nodePath2 = render.attachNewNode(node2)
    nodePath2.setTwoSided(False)
    width, height = emoPng.size
    if width > height:
        bk = Image.new('RGBA', (width, width), (0, 0, 0, 0))
        bk.alpha_composite(emoPng, (0, round((width - height) / 2)))
    elif height > width:
        bk = Image.new('RGBA', (width, width), (0, 0, 0, 0))
        bk.alpha_composite(emoPng, (round((height - width) / 2), 0))
    else:
        bk = emoPng
    bk.save(str(emojiId) + "texture.png")
    yTexture = loader.loadTexture(str(emojiId) + "texture.png")
    yTexture.setMagfilter(SamplerState.FT_nearest)
    yTexture.setMinfilter(SamplerState.FT_nearest)
    vertex_format = GeomVertexFormat.get_v3n3t2()
    vdata = GeomVertexData('name', vertex_format, Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, 'vertex')
    texcoord = GeomVertexWriter(vdata, 'texcoord')
    normal = GeomVertexWriter(vdata, 'normal')
    thk = 0.8
    vertex.addData3(-2.5, 0, 2.5)
    texcoord.addData2(0, 1)
    normal.addData3(0, -1, 0)
    vertex.addData3(-2.5, 0, -2.5)
    texcoord.addData2(0, 0)
    normal.addData3(0, -1, 0)
    vertex.addData3(2.5, 0, 2.5)
    texcoord.addData2(1, 1)
    normal.addData3(0, -1, 0)
    vertex.addData3(2.5, 0, -2.5)
    texcoord.addData2(1, 0)
    normal.addData3(0, -1, 0)  # bottom right
    prim = GeomTriangles(Geom.UHStatic)
    prim.addVertices(0, 1, 2)
    prim.addVertices(3, 2, 1)
    vertex.addData3(-2.5, thk, 2.5)
    texcoord.addData2(0, 1)
    normal.addData3(0, 1, 0)
    vertex.addData3(-2.5, thk, -2.5)
    texcoord.addData2(0, 0)
    normal.addData3(0, 1, 0)
    vertex.addData3(2.5, thk, 2.5)
    texcoord.addData2(1, 1)
    normal.addData3(0, 1, 0)
    vertex.addData3(2.5, thk, -2.5)
    texcoord.addData2(1, 0)
    normal.addData3(0, 1, 0)
    # prim.addVertices(6, 5, 4)
    # prim.addVertices(5, 6, 7)

    geom = Geom(vdata)
    geom.addPrimitive(prim)

    node = GeomNode('gnode')
    node.addGeom(geom)
    nodePath = render.attachNewNode(node)
    nodePath.setTexture(yTexture)
    nodePath.setTransparency(True)
    nodePath.setTwoSided(True)

    lColor1 = (ri, gi, bi, 1)
    ambientLight = render.attachNewNode(AmbientLight("ambientLight"))
    ambientLight.node().setColor((0.5, 0.5, 0.5, 1))

    # plight = Spotlight('plight')
    plight = PointLight('plight')
    plight.setColor(lColor1)
    plight.setAttenuation(LVector3(0, 1, 0))
    # plight.setShadowCaster(True, 512, 512)
    # plight.setExponent(60)
    # plight.setLens(PerspectiveLens())
    # plight.getLens().setFov(70, 70)
    plnp = render.attachNewNode(plight)
    plnp.setPos(-10, 70, -10)
    #plnp.lookAt(0, 0, 0)
    sphere = loader.loadModel("models/sphere")
    sphere.reparentTo(plnp)
    sphere.setPos(10, 0, 10)
    sphere.setScale(2)
    #nodlPath.reparentTo(plnp)
    render.setLight(plnp)
    #plnp.reparentTo(nodlPath)

    render.setLight(ambientLight)
    perPixelEnabled = True
    base.camera.lookAt(0, 0, 0)
    base.camera.setPos(0, -6, 0)
    cf = CommonFilters(buffer, cam)
    cf.setVolumetricLighting(plnp,256,1,0.96,0.1)
    render.setShaderAuto()
    #base.camera.lookAt(0, 0, 0)

    # images = []
    for f in range(-3, 360):
        if f%10 == 1:
            print(str(round((f/360)*100)) + "%")
        nodePath.setHpr(f, f, f)
        # nodePath2.setHpr(f*yaw, f*pitch, f*roll)
        base.camera.setPos(0, (-6 - ((pace/10)*f) - (40 * iDist)), 0)
        #base.camera.lookAt(0, 0, 0)
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        peeking = texture.peek()
        width, height = peeking.getXSize(), peeking.getYSize()
        if f >= 0:
            images.append('')
            thr = threading.Thread(target=renderFrame, args=(width, height, peeking, f))
            thr.start()
    while len(images) < 360 or images[-1] == '':
        print("waiting...")
        time.sleep(0.1)
    os.remove(str(emojiId) + "texture.png")
    images.append(20)
    return images


def rendering3dSpotCop(emoPng, max=40):
    emojiId = random.randint(0,99999)
    base = ShowBase(windowType='offscreen')
    base.camNode.get_display_region(0).set_active(False)

    props = FrameBufferProperties()
    # Request 8 RGB bits, no alpha bits, and a depth buffer.
    props.set_rgba_bits(24, 24, 24, 24)
    props.set_rgb_color(True)
    props.set_depth_bits(24)
    # props.set_stereo(True)
    win_prop = WindowProperties.size(300, 300)
    flags = GraphicsPipe.BFFbPropsOptional | GraphicsPipe.BF_refuse_window

    buffer = base.graphicsEngine.make_output(base.pipe, "buffer", -100,
                                             props,
                                             win_prop, flags, base.win.getGsg(),
                                             base.win)
    texture = Texture()
    buffer.addRenderTexture(texture, GraphicsOutput.RTM_copy_ram)

    lens = PerspectiveLens()
    # lens.setNearFar(0.6, 1000)
    lens.setFov(46)
    lens.setFocalLength(1.37795276)
    lens.set_interocular_distance(50)
    lens.set_convergence_distance(float('inf'))

    render = NodePath('mono')
    cam = base.makeCamera(buffer)
    cam.node().setLens(lens)
    cam.node().setScene(render)
    dp = buffer.makeDisplayRegion()
    dp.setCamera(cam)

    vFormat = GeomVertexFormat.get_v3n3c4()
    vdata2 = GeomVertexData('box', vFormat, Geom.UHStatic)
    vertx = GeomVertexWriter(vdata2, 'vertex')
    norm = GeomVertexWriter(vdata2, 'normal')
    colo = GeomVertexWriter(vdata2, 'color')
    tColor = [0.2, 0.2, 0.2, 1]
    siz = 32
    vertx.addData3(-siz, siz, siz)  # 0 top back left
    norm.addData3(1, -1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, siz, siz)  # 1 top back right
    norm.addData3(-1, -1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, siz, -siz)  # 2 bottom back right
    norm.addData3(-1, -1, 1)
    colo.addData4(*tColor)
    vertx.addData3(-siz, siz, -siz)  # 3 bottom back left
    norm.addData3(1, -1, 1)
    colo.addData4(*tColor)
    vertx.addData3(-siz, -siz, siz)  # 4 top front left
    norm.addData3(1, 1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, -siz, siz)  # 5 top front right
    norm.addData3(-1, 1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, -siz, -siz)  # 6 bottom front right
    norm.addData3(-1, 1, 1)
    colo.addData4(*tColor)
    vertx.addData3(-siz, -siz, -siz)  # 7 bottom front left
    norm.addData3(1, 1, 1)
    colo.addData4(*tColor)
    prm = GeomTriangles(Geom.UHStatic)
    prm.addVertices(2, 1, 0)
    prm.addVertices(3, 2, 0)
    prm.addVertices(6, 2, 3)
    prm.addVertices(7, 6, 3)

    geom2 = Geom(vdata2)
    geom2.addPrimitive(prm)

    node2 = GeomNode('gnode')
    node2.addGeom(geom2)

    nodePath2 = render.attachNewNode(node2)
    nodePath2.setTwoSided(False)
    width, height = emoPng.size
    if width > height:
        bk = Image.new('RGBA', (width, width), (0, 0, 0, 0))
        bk.alpha_composite(emoPng, (0, round((width - height) / 2)))
    elif height > width:
        bk = Image.new('RGBA', (width, width), (0, 0, 0, 0))
        bk.alpha_composite(emoPng, (round((height - width) / 2), 0))
    else:
        bk = emoPng
    bk.save(str(emojiId) + "texture.png")
    yTexture = loader.loadTexture(str(emojiId) + "texture.png")
    yTexture.setMagfilter(SamplerState.FT_nearest)
    yTexture.setMinfilter(SamplerState.FT_nearest)
    vertex_format = GeomVertexFormat.get_v3n3t2()
    vdata = GeomVertexData('name', vertex_format, Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, 'vertex')
    texcoord = GeomVertexWriter(vdata, 'texcoord')
    normal = GeomVertexWriter(vdata, 'normal')
    thk = 0.4
    vertex.addData3(-2.5, 0, 2.5)
    texcoord.addData2(0, 1)
    normal.addData3(0, -1, 0)
    vertex.addData3(-2.5, 0, -2.5)
    texcoord.addData2(0, 0)
    normal.addData3(0, -1, 0)
    vertex.addData3(2.5, 0, 2.5)
    texcoord.addData2(1, 1)
    normal.addData3(0, -1, 0)
    vertex.addData3(2.5, 0, -2.5)
    texcoord.addData2(1, 0)
    normal.addData3(0, -1, 0)  # bottom right
    prim = GeomTriangles(Geom.UHStatic)
    prim.addVertices(0, 1, 2)
    prim.addVertices(3, 2, 1)
    vertex.addData3(-2.5, thk, 2.5)
    texcoord.addData2(0, 1)
    normal.addData3(0, 1, 0)
    vertex.addData3(-2.5, thk, -2.5)
    texcoord.addData2(0, 0)
    normal.addData3(0, 1, 0)
    vertex.addData3(2.5, thk, 2.5)
    texcoord.addData2(1, 1)
    normal.addData3(0, 1, 0)
    vertex.addData3(2.5, thk, -2.5)
    texcoord.addData2(1, 0)
    normal.addData3(0, 1, 0)
    prim.addVertices(6, 5, 4)
    prim.addVertices(5, 6, 7)

    geom = Geom(vdata)
    geom.addPrimitive(prim)

    node = GeomNode('gnode')
    node.addGeom(geom)

    nodePath = render.attachNewNode(node)
    nodePath.setTexture(yTexture)
    nodePath.setTransparency(True)
    nodePath.setTwoSided(False)
    # nodePath.setDepthOffset(1)

    ambientLight = render.attachNewNode(AmbientLight("ambientLight"))
    # Set the color of the ambient light
    lColor1 = (6, 0.2, 0.2, 1)
    lColor2 = (0, 0, 0, 1)
    clist = [lColor1]
    ambientLight.node().setColor(sumColor(clist))

    plight = Spotlight('plight')
    plight.setColor(lColor1)
    plight.setAttenuation(LVector3(1, 0.03, 0))
    plight.setShadowCaster(True, 1024, 1024)
    # plight.setExponent(60)
    plight.setLens(PerspectiveLens())
    plight.getLens().setFov(70, 70)
    plnp = render.attachNewNode(plight)
    plnp.setPos(1.6, -10, 0.6)
    plnp.lookAt(0, 0, 0)
    render.setLight(plnp)


    plight2 = Spotlight('plight2')
    plight2.setColor(lColor2)
    plight2.setAttenuation(LVector3(1, 0.03, 0))
    plight2.setShadowCaster(True, 1024, 1024)
    # plight.setExponent(60)
    plight2.setLens(PerspectiveLens())
    plight2.getLens().setFov(70, 70)
    plnp2 = render.attachNewNode(plight2)
    plnp2.setPos(1.3, -10, 0.6)
    plnp2.lookAt(0, 0, 0)
    render.setLight(plnp2)

    render.setLight(ambientLight)
    perPixelEnabled = True
    render.setShaderAuto()
    base.camera.setPos(0, -10, 0)
    base.camera.lookAt(0, 0, 0)

    # images = []
    maxf = 0
    # max = 12
    for f in range(-2, (max*2)):
        if f%4 == 1:
            print(str(round((f/(max*2))*100)) + "%")
        maxf = f
        # print(floor(f/8)%2)
        if floor(f/max)%2 == 0: # and floor((f-1)/max)%2 == 1:
        #if f < 10:
            if floor(f/2)%2 == 0:
                lColor1 = (8, 0.2, 0.2, 1)
            else:
                lColor1 = (0.8, 0.2, 0.2, 1)
            lColor2 = (0, 0, 0, 1)
            ambientLight.node().setColor(sumColor([lColor1, lColor2]))
            plight.setColor(lColor1)
            plight2.setColor(lColor2)
            base.graphicsEngine.renderFrame()
            time.sleep(0.1)
            base.graphicsEngine.renderFrame()
        if floor(f/max)%2 == 1: # and floor((f-1)/max)%2 == 0:
            if floor(f/2)%2 == 0:
                lColor2 = (0.2, 0.2, 8, 1)
            else:
                lColor2 = (0.2, 0.2, 0.8, 1)
            lColor1 = (0, 0, 0, 1)
            ambientLight.node().setColor(sumColor([lColor1, lColor2]))
            plight.setColor(lColor1)
            plight2.setColor(lColor2)
            base.graphicsEngine.renderFrame()
            time.sleep(0.1)
            base.graphicsEngine.renderFrame()
        # nodePath.setHpr(f * yaw, f * pitch, f * roll)
        # nodePath2.setHpr(f*yaw, f*pitch, f*roll)
        # ambientLight.node().setColor(sumColor([lColor1]))
        # plight.setColor(lColor1)
        # time.sleep(0.1)
        base.graphicsEngine.renderFrame()
        time.sleep(0.05)
        base.graphicsEngine.renderFrame()
        # time.sleep(0.05)
        # base.graphicsEngine.renderFrame()
        peeking = texture.peek()
        width, height = peeking.getXSize(), peeking.getYSize()
        img = Image.new('RGBA', (width, height), 0)
        out = img.load()
        if f >= 0:
            #print(lColor1)
            images.append('')
            thr = threading.Thread(target=renderFrame, args=(width, height, peeking, f))
            thr.start()
    while len(images) < maxf + 1 or images[-1] == '':
        print("waiting...")
        time.sleep(0.1)
    os.remove(str(emojiId) + "texture.png")
    images.append(20)
    return images


def rendering3dSpotCopGif(emoGif, max):
    emojiId = random.randint(0,99999)
    base = ShowBase(windowType='offscreen')
    base.camNode.get_display_region(0).set_active(False)

    props = FrameBufferProperties()
    # Request 8 RGB bits, no alpha bits, and a depth buffer.
    props.set_rgba_bits(8, 8, 8, 8)
    props.set_rgb_color(True)
    props.set_depth_bits(8)
    # props.set_stereo(True)
    win_prop = WindowProperties.size(300, 300)
    flags = GraphicsPipe.BFFbPropsOptional | GraphicsPipe.BF_refuse_window

    buffer = base.graphicsEngine.make_output(base.pipe, "buffer", -100,
                                             props,
                                             win_prop, flags, base.win.getGsg(),
                                             base.win)
    texture = Texture()
    buffer.addRenderTexture(texture, GraphicsOutput.RTM_copy_ram)

    lens = PerspectiveLens()
    # lens.setNearFar(0.6, 1000)
    lens.setFov(46)
    lens.setFocalLength(1.37795276)
    lens.set_interocular_distance(50)
    lens.set_convergence_distance(float('inf'))

    render = NodePath('mono')
    cam = base.makeCamera(buffer)
    cam.node().setLens(lens)
    cam.node().setScene(render)
    dp = buffer.makeDisplayRegion()
    dp.setCamera(cam)

    vFormat = GeomVertexFormat.get_v3n3c4()
    vdata2 = GeomVertexData('box', vFormat, Geom.UHStatic)
    vertx = GeomVertexWriter(vdata2, 'vertex')
    norm = GeomVertexWriter(vdata2, 'normal')
    colo = GeomVertexWriter(vdata2, 'color')
    tColor = [0.2, 0.2, 0.2, 1]
    siz = 32
    vertx.addData3(-siz, siz, siz)  # 0 top back left
    norm.addData3(1, -1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, siz, siz)  # 1 top back right
    norm.addData3(-1, -1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, siz, -siz)  # 2 bottom back right
    norm.addData3(-1, -1, 1)
    colo.addData4(*tColor)
    vertx.addData3(-siz, siz, -siz)  # 3 bottom back left
    norm.addData3(1, -1, 1)
    colo.addData4(*tColor)
    vertx.addData3(-siz, -siz, siz)  # 4 top front left
    norm.addData3(1, 1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, -siz, siz)  # 5 top front right
    norm.addData3(-1, 1, -1)
    colo.addData4(*tColor)
    vertx.addData3(siz, -siz, -siz)  # 6 bottom front right
    norm.addData3(-1, 1, 1)
    colo.addData4(*tColor)
    vertx.addData3(-siz, -siz, -siz)  # 7 bottom front left
    norm.addData3(1, 1, 1)
    colo.addData4(*tColor)
    prm = GeomTriangles(Geom.UHStatic)
    prm.addVertices(2, 1, 0)
    prm.addVertices(3, 2, 0)
    prm.addVertices(6, 2, 3)
    prm.addVertices(7, 6, 3)

    geom2 = Geom(vdata2)
    geom2.addPrimitive(prm)

    node2 = GeomNode('gnode')
    node2.addGeom(geom2)

    nodePath2 = render.attachNewNode(node2)
    nodePath2.setTwoSided(False)
    testFrames = []
    totalFrames = len(emoGif) - 1
    gifDuration = emoGif[-1]
    if type(gifDuration) is list:
        gifDuration = gifDuration[0]
    texList = []
    for i in range(totalFrames):
        emoPng = emoGif[i].copy().convert('RGBA')
        width, height = emoPng.size
        if width > height:
            bk = Image.new('RGBA', (width, width), (0, 0, 0, 0))
            bk.alpha_composite(emoPng, (0, round((width - height) / 2)))
        elif height > width:
            bk = Image.new('RGBA', (width, width), (0, 0, 0, 0))
            bk.alpha_composite(emoPng, (round((height - width) / 2), 0))
        else:
            bk = emoPng
        emoPng = bk
        step = io.BytesIO()
        emoPng.save(step, 'png')
        im_bytes = step.getvalue()
        myImage = PNMImage()
        myImage.read(StringStream(im_bytes))
        texList.append(myImage)
    yTexture = Texture()
    yTexture.setMagfilter(SamplerState.FT_nearest)
    yTexture.setMinfilter(SamplerState.FT_nearest)
    vertex_format = GeomVertexFormat.get_v3n3t2()
    vdata = GeomVertexData('name', vertex_format, Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, 'vertex')
    texcoord = GeomVertexWriter(vdata, 'texcoord')
    normal = GeomVertexWriter(vdata, 'normal')
    thk = 0.4
    vertex.addData3(-2.5, 0, 2.5)
    texcoord.addData2(0, 1)
    normal.addData3(0, -1, 0)
    vertex.addData3(-2.5, 0, -2.5)
    texcoord.addData2(0, 0)
    normal.addData3(0, -1, 0)
    vertex.addData3(2.5, 0, 2.5)
    texcoord.addData2(1, 1)
    normal.addData3(0, -1, 0)
    vertex.addData3(2.5, 0, -2.5)
    texcoord.addData2(1, 0)
    normal.addData3(0, -1, 0)  # bottom right
    prim = GeomTriangles(Geom.UHStatic)
    prim.addVertices(0, 1, 2)
    prim.addVertices(3, 2, 1)
    vertex.addData3(-2.5, thk, 2.5)
    texcoord.addData2(0, 1)
    normal.addData3(0, 1, 0)
    vertex.addData3(-2.5, thk, -2.5)
    texcoord.addData2(0, 0)
    normal.addData3(0, 1, 0)
    vertex.addData3(2.5, thk, 2.5)
    texcoord.addData2(1, 1)
    normal.addData3(0, 1, 0)
    vertex.addData3(2.5, thk, -2.5)
    texcoord.addData2(1, 0)
    normal.addData3(0, 1, 0)
    prim.addVertices(6, 5, 4)
    prim.addVertices(5, 6, 7)

    geom = Geom(vdata)
    geom.addPrimitive(prim)

    node = GeomNode('gnode')
    node.addGeom(geom)

    nodePath = render.attachNewNode(node)
    nodePath.setTexture(yTexture)
    nodePath.setTransparency(True)
    nodePath.setTwoSided(False)
    # nodePath.setDepthOffset(1)

    ambientLight = render.attachNewNode(AmbientLight("ambientLight"))
    # Set the color of the ambient light
    lColor1 = (6, 0.2, 0.2, 1)
    lColor2 = (0, 0, 0, 1)
    clist = [lColor1]
    ambientLight.node().setColor(sumColor(clist))

    plight = Spotlight('plight')
    plight.setColor(lColor1)
    plight.setAttenuation(LVector3(1, 0.03, 0))
    plight.setShadowCaster(True, 1024, 1024)
    # plight.setExponent(60)
    plight.setLens(PerspectiveLens())
    plight.getLens().setFov(70, 70)
    plnp = render.attachNewNode(plight)
    plnp.setPos(1.6, -10, 0.6)
    plnp.lookAt(0, 0, 0)
    render.setLight(plnp)


    plight2 = Spotlight('plight2')
    plight2.setColor(lColor2)
    plight2.setAttenuation(LVector3(1, 0.03, 0))
    plight2.setShadowCaster(True, 1024, 1024)
    # plight.setExponent(60)
    plight2.setLens(PerspectiveLens())
    plight2.getLens().setFov(70, 70)
    plnp2 = render.attachNewNode(plight2)
    plnp2.setPos(1.3, -10, 0.6)
    plnp2.lookAt(0, 0, 0)
    render.setLight(plnp2)

    render.setLight(ambientLight)
    perPixelEnabled = True
    render.setShaderAuto()
    base.camera.setPos(0, -10, 0)
    base.camera.lookAt(0, 0, 0)

    # images = []
    maxf = 0
    rame_ratio = (gifDuration / 20)
    # max = 12
    for f in range(-2, (max*2)):
        if f%4 == 1:
            print(str(round((f/(max*2))*100)) + "%")
        framePick = int(floor((f * frame_ratio) % totalFrames))
        yTexture.load(texList[framePick])
        maxf = f
        # print(floor(f/8)%2)
        if floor(f/max)%2 == 0: # and floor((f-1)/max)%2 == 1:
        #if f < 10:
            if floor(f/2)%2 == 0:
                lColor1 = (8, 0.2, 0.2, 1)
            else:
                lColor1 = (0.8, 0.2, 0.2, 1)
            lColor2 = (0, 0, 0, 1)
            ambientLight.node().setColor(sumColor([lColor1, lColor2]))
            plight.setColor(lColor1)
            plight2.setColor(lColor2)
            base.graphicsEngine.renderFrame()
            time.sleep(0.1)
            base.graphicsEngine.renderFrame()
        if floor(f/max)%2 == 1: # and floor((f-1)/max)%2 == 0:
            if floor(f/2)%2 == 0:
                lColor2 = (0.2, 0.2, 8, 1)
            else:
                lColor2 = (0.2, 0.2, 0.8, 1)
            lColor1 = (0, 0, 0, 1)
            ambientLight.node().setColor(sumColor([lColor1, lColor2]))
            plight.setColor(lColor1)
            plight2.setColor(lColor2)
            base.graphicsEngine.renderFrame()
            time.sleep(0.1)
            base.graphicsEngine.renderFrame()
        # nodePath.setHpr(f * yaw, f * pitch, f * roll)
        # nodePath2.setHpr(f*yaw, f*pitch, f*roll)
        # ambientLight.node().setColor(sumColor([lColor1]))
        # plight.setColor(lColor1)
        # time.sleep(0.1)
        base.graphicsEngine.renderFrame()
        time.sleep(0.05)
        base.graphicsEngine.renderFrame()
        # time.sleep(0.05)
        # base.graphicsEngine.renderFrame()
        peeking = texture.peek()
        width, height = peeking.getXSize(), peeking.getYSize()
        img = Image.new('RGBA', (width, height), 0)
        out = img.load()
        if f >= 0:
            #print(lColor1)
            images.append('')
            thr = threading.Thread(target=renderFrame, args=(width, height, peeking, f))
            thr.start()
    while len(images) < maxf + 1 or images[-1] == '':
        print("waiting...")
        time.sleep(0.1)
    os.remove(str(emojiId) + "texture.png")
    images[0].save(str(emojiId) + 'ThreeD2.gif', save_all=True, append_images=images[1:], duration=20, loop=0, optimize=False, transparency=255,
                   disposal=2)
    return str(emojiId) + "ThreeD2.gif"


from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape, BulletTriangleMeshShape, BulletTriangleMesh, BulletDebugNode, BulletConvexHullShape
from panda3d.core import *
import colorsys

# load_prc_file_data("", "load-display pandagl")
load_prc_file_data("", "notify-level-egldisplay spam")
# load_prc_file_data("", "gl-debug true")
loadPrcFileData("", "audio-library-name null")


def make_collision_from_model(input_model):
    # tristrip generation from static models
    # generic tri-strip collision generator begins
    geom_nodes = input_model.findAllMatches('**/+GeomNode')
    # print(len(geom_nodes))
    output_bullet_mesh = BulletTriangleMesh()
    # print(type(geom_nodes))
    for i in range(len(geom_nodes)):
        geom_nodes2 = geom_nodes.getPath(i).node()
        if i == 0:
            xoff, yoff, zoff = geom_nodes2.getTransform().getPos()
        # print(geom_nodes2.getTransform().getPos())
        geom_nodes2.clearTransform()
        # test = TransformState.makePos((-xoff, -yoff, -xoff))
        # geom_nodes2.transform = test
        # geom_nodes2.clearBounds()
        # geom_nodes2.getBounds()
        geom_target = geom_nodes2.getGeom(0)
        # print(geom_target)
        output_bullet_mesh.addGeom(geom_target)
    # tri_shape = BulletTriangleMeshShape(output_bullet_mesh, dynamic=False)
    # print(output_bullet_mesh)
    #
    # body = BulletRigidBodyNode('input_model_tri_mesh')
    # np = self.render.attachNewNode(body)
    # np.node().addShape(tri_shape)
    # np.node().setMass(0)
    # np.node().setFriction(0.5)
    # # np.setPos(0, 0, 0)
    # np.setScale(1)
    # np.setCollideMask(BitMask32.allOn())
    # world.attachRigidBody(np.node())
    return xoff, yoff, zoff, output_bullet_mesh

import numpy, sys
sys.path.append("..")
print(sys.path)
import example_cython


def renderingDice(die="d20v2", forc=2):
    celestial = False
    if die.lower() == "celestial":
        die = "d20vc2"
        celestial = True
    base = ShowBase(windowType='offscreen')
    # base = ShowBase()
    base.camNode.get_display_region(0).set_active(False)

    props = FrameBufferProperties()
    # Request 8 RGB bits, no alpha bits, and a depth buffer.
    props.set_rgba_bits(8, 8, 8, 8)
    props.set_rgb_color(True)
    props.set_depth_bits(8)
    # props.set_stereo(True)
    win_prop = WindowProperties.size(120, 120)
    flags = GraphicsPipe.BFFbPropsOptional | GraphicsPipe.BF_refuse_window

    # buffer = base.graphicsEngine.make_output(base.pipe, "buffer", -100,
    #                                          props,
    #                                          win_prop, flags, base.win.getGsg(),
    #                                          base.win)
    buffer = base.graphicsEngine.make_output(base.pipe, "buffer", -100,
                                             props,
                                             win_prop, flags, base.win.getGsg(),
                                             base.win)

    texture = Texture()
    buffer.addRenderTexture(texture, GraphicsOutput.RTM_copy_ram)

    lens = PerspectiveLens()
    lens.setNearFar(10, -10)
    lens.setFov(7)
    lens.setFocalLength(1.37795276)
    lens.set_interocular_distance(50)
    lens.set_convergence_distance(float('inf'))

    render = NodePath('mono')
    cam = base.makeCamera(buffer)
    cam.node().setLens(lens)
    cam.node().setScene(render)
    dp = buffer.makeDisplayRegion()
    dp.setCamera(cam)


    # model = loader.loadModel('models/box.egg')
    # model.flattenLight()
    # model.reparentTo(np)

    debugNode = BulletDebugNode('Debug')
    debugNode.showWireframe(True)
    debugNode.showConstraints(True)
    debugNode.showBoundingBoxes(True)
    debugNode.showNormals(False)
    debugNP = render.attachNewNode(debugNode)
    # debugNP.show()

    world = BulletWorld()
    world.setGravity(Vec3(0, 0, -9.81))
    world.setDebugNode(debugNP.node())

    shape = BulletPlaneShape(Vec3(0, 0, 1), 1) # ground
    node = BulletRigidBodyNode('Ground')
    node.addShape(shape)
    node.setFriction(1.5)
    np = render.attachNewNode(node)
    np.setPos(0, 0, 0)
    world.attachRigidBody(node)

    if os.path.isfile("models/" + str(die) + ".x"):
        pass
    else:
        raise Exception("Not an option.")
    dice = loader.loadModel("models/" + str(die) + ".x") # complex model?
    dice.reparentTo(render)
    dice.setScale(1)
    dice.setPos(0, 0, 0)
    dice.setShaderAuto()
    if os.path.isfile("models/" + str(die) + "_Normal.png"):
        ts = TextureStage('ts')
        ts.setMode(TextureStage.MHeight)
        tex = loader.loadTexture("models/" + str(die) + "_Normal.png")
        dice.setTexture(ts, tex)
    # dice.setHpr(randint(-45, 45), randint(-45, 45), randint(-45, 45))

    grnd = loader.loadModel("models/grounded5.x")  # complex model?
    grnd.setScale(1)
    grnd.lookAt(0, 0, -1)
    grnd.setPos(0, 0, 1)
    grnd.setScale(160)
    grnd.reparentTo(render)
    grnd.setDepthOffset(-1)
    # geomnodes = dice.findAllMatches('**/+GeomNode')
    # gn = geomnodes.getPath(0).node()
    # geom = gn.getGeom(0)
    # mesh = BulletTriangleMesh()
    # mesh.addGeom(make_collision_from_model(dice))

    xoff, yoff, zoff, mesh = make_collision_from_model(dice)
    shape = BulletTriangleMeshShape(mesh, dynamic=True)
    # shape = BulletConvexHullShape(mesh)
    # dice.setPos(xoff, yoff, zoff)
    node = BulletRigidBodyNode('Box')
    # node.addShape(shape)
    # shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
    node.addShape(shape)
    node.setMass(0.1)
    np = render.attachNewNode(node)
    np.setPos(0, 0, 6)
    np.setHpr(randint(-45, 45), randint(-45, 45), randint(-45, 45))
    node.setFriction(1)
    world.attachRigidBody(node)
    dice.reparentTo(np)
    dice.setDepthOffset(-1)

    dlight = DirectionalLight('dlight')
    dlight.setShadowCaster(True, 4096, 4096)
    dlnp = render.attachNewNode(dlight)
    dlnp.node().showFrustum()
    dlnp.node().getLens().setFilmSize(128, 128)
    dlnp.setPos(0, 0, 100)
    dlnp.setHpr(0, -100, -30)
    render.setLight(dlnp)

    alight = AmbientLight('alight')
    alight.setColor((0.25, 0.25, 0.25, 1))
    alnp = render.attachNewNode(alight)
    render.setLight(alnp)

    # perPixelEnabled = True
    render.setShaderAuto()

    images = []
    theta = random() * 2 * math.pi
    yf = math.sin(theta) * 300
    xf = math.cos(theta) * 300

    nebula = Image.open("Shaper4K.png").convert('RGBA').resize((1024, 1024), Image.LANCZOS)
    npn = numpy.asarray(Image.open("image_mods/Shaper1K.png").convert('RGBA')).tolist()
    node.applyCentralImpulse((xf * 0.005 * forc, yf * 0.005 * forc, 0))
    timd = 0
    end = 1
    if forc > 4:
        ts = 0.03333 + (0.03333 / 2)
        duration = 30
    else:
        ts = 0.03333
        duration = 20
    xp, yp, zp = 0, 0, 0
    foff = randint(0, 3000)
    for f in range(6000):
        world.doPhysics(ts)
        x, y, z = np.getPos()
        vect = (x - xp, y - yp, z - zp)
        # print(x, y)
        xp, yp, zp = x, y, z
        base.camera.setPos(x, y + 16, 20)
        # grnd.setPos(x, y, 1)
        dlnp.setPos(x, y, 100)
        base.camera.lookAt(x, y, 1.2 + (z / 6))
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        peeking = texture.peek()
        width, height = peeking.getXSize(), peeking.getYSize()
        # img = Image.new('RGBA', (width, height), 0)
        # out = img.load()
        # test = LColor()
        # peeking.fetchPixel(test, 0, 0)
        tex = buffer.getScreenshot()
        data = tex.getRamImageAs('RGBA')
        # image = numpy.frombuffer(data, numpy.uint8)
        # print(tex.getYSize(), tex.getXSize(), tex.getNumComponents())
        # for i in range(0, 32, 4):
        #     print(image[i:i+4])
        # image.shape = (tex.getYSize(), tex.getXSize(), tex.getNumComponents())
        img = Image.frombuffer('RGBA', (tex.getYSize(), tex.getXSize()), data).transpose(Image.FLIP_TOP_BOTTOM)
        # if celestial:
        #     xoff = round((f + foff) * 0.3)
        #     yoff = round((f + foff) * 0.6)
        #     tpn = numpy.asarray(img).tolist()
        #     yarr = example_cython.runstuff(tpn, npn, xoff, yoff)
        #     img = Image.fromarray(numpy.uint8(yarr), 'RGBA')
        #     # ul = underlay.load()
        #     # id = img.getdata()
        #     # il = img.load()
        #     # i = 1
        #     # for pixel in id:
        #     #     r, g, b, a = pixel
        #     #     x = i % (120)
        #     #     y = math.trunc(i / 120)
        #     #     i += 1
        #     #     h, s, v = colorsys.rgb_to_hsv(r, g, b)
        #     #     if h < 10/360 or h > 350/360:
        #     #         if s > 30/100 and v > 30/100:
        #     #             il[x, y] = ul[x, y]
        #
        #     # # ul = underlay.load()
        #     # il = img.load()
        #     # for x in range(width):
        #     #     for y in range(height):
        #     #         r, g, b, a = il[x, y]
        #     #         h, s, v = colorsys.rgb_to_hsv(r, g, b)
        #     #         if h < 10/360 or h > 350/360:
        #     #             if s > 30/100 and v > 30/100:
        #     #                 il[x, y] = ul[x, y]
        # alpha = img.split()[3]
        # img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        # mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        # img.paste(255, mask)
        images.append(img)
        if vect == (0, 0, 0):
            timd += 1
            if timd > 20:
                break
        else:
            timd = 0
        # if f > 50:
        #     if ImageChops.difference(images[-1], images[-2]).getbbox() is None:
        #         timd += 1
        #         end = timd
        #         if timd > 250:
        #             end = 250
        #             break
        #     else:
        #         timd = 0
        #         end = 1
    for f in range(len(images)):
        img = images[f]
        # if celestial:
        #     xoff = round((f + foff) * 0.3)
        #     yoff = round((f + foff) * 0.6)
        #     tpn = numpy.asarray(img).tolist()
        #     yarr = example_cython.runstuff(tpn, npn, xoff, yoff)
        #     img = Image.fromarray(numpy.uint8(yarr), 'RGBA')
        # alpha = img.split()[3]
        # # img = img.convert('RGB').convert('P', palette=Image.WEB, colors=64)
        # img = img.quantize(24, Image.FASTOCTREE, 0, Image.WEB)
        # mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        # img.paste(255, mask)
        images[f] = img
    images.append(duration)
    return images