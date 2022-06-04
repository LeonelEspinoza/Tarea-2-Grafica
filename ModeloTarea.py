# coding=utf-8
"""Textures and transformations in 3D"""
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.scene_graph as sg
from grafica.assets_path import getAssetPath



############################################################################
def create_START_BOX(pipeline):
    shapeSky = bs.createTextureSTART('wall.jfif')
    gpuSky = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuSky)
    gpuSky.fillBuffers(shapeSky.vertices, shapeSky.indices, GL_STATIC_DRAW)
    gpuSky.texture = es.textureSimpleSetup(
        getAssetPath("wall.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    skybox = sg.SceneGraphNode("start")
    skybox.transform = tr.matmul([tr.translate(0, 0, 0.3), tr.uniformScale(2)])
    skybox.childs += [gpuSky]

    return skybox

def create_TUBE(pipeline,n):
    x= 2*n
    shapeTUBE = bs.createTextureTUBE('wall.jfif')
    gpuTUBE = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTUBE)
    gpuTUBE.fillBuffers(shapeTUBE.vertices, shapeTUBE.indices, GL_STATIC_DRAW)
    gpuTUBE.texture = es.textureSimpleSetup(getAssetPath("wall.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    TUBEbox = sg.SceneGraphNode("tube"+str(n))
    TUBEbox.transform = tr.matmul([tr.translate(-x, 0, 0.3), tr.uniformScale(2)])
    TUBEbox.childs += [gpuTUBE]

    return TUBEbox

def create_FINISH_BOX(pipeline,d):
    shapeFINISH = bs.createTextureFINISH('wall.jfif')
    gpuFINISH = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFINISH)
    gpuFINISH.fillBuffers(shapeFINISH.vertices, shapeFINISH.indices, GL_STATIC_DRAW)
    gpuFINISH.texture = es.textureSimpleSetup(getAssetPath("wall.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    FINISHbox = sg.SceneGraphNode("finish")
    FINISHbox.transform = tr.matmul([tr.translate(-(d+1), 0, 0.3), tr.uniformScale(2)])
    FINISHbox.childs += [gpuFINISH]

    return FINISHbox

def create_floor(pipeline,n,d):
    shapeFloor = bs.createTextureQuad(4, 4)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(getAssetPath("floor.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    floor = sg.SceneGraphNode("floor"+str(n))
    floor.transform = tr.matmul([tr.translate(-(d+1), 0, 0),tr.scale(2, 2, 1)])
    floor.childs += [gpuFloor]

    return floor

def create_JUMP_BOX1(pipeline,n,s):
    assert s<=5 and s>=0
    tube=create_TUBE(pipeline,n)
    s=s/5
    x=2*n
    shapeFloor = bs.createTextureQuad(2,2)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(getAssetPath("floor.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    leftfloor = sg.SceneGraphNode("leftfloor"+str(n))
    leftfloor.transform = tr.matmul([tr.translate(-x, -0.75, 0),tr.scale(1-s, 0.6, 1)])
    leftfloor.childs += [gpuFloor]

    rightfloor = sg.SceneGraphNode("rightfloor"+str(n))
    rightfloor.transform = tr.matmul([tr.translate(-x, 0.75, 0),tr.scale(1-s, 0.6, 1)])
    rightfloor.childs += [gpuFloor]
    
    centerfloor = sg.SceneGraphNode("centerfloor"+str(n))
    centerfloor.transform = tr.matmul([tr.translate(-x, 0, 0),tr.scale(1-s, 0.6, 1)])
    centerfloor.childs += [gpuFloor]

    startfloor = sg.SceneGraphNode("startfloor"+str(n))
    startfloor.transform = tr.matmul([tr.translate(-x+0.75, 0, 0),tr.scale(0.5, 2, 1)])
    startfloor.childs += [gpuFloor]

    finishfloor = sg.SceneGraphNode("finishfloor"+str(n))
    finishfloor.transform = tr.matmul([tr.translate(-x-0.75, 0, 0),tr.scale(0.5, 2, 1)])
    finishfloor.childs += [gpuFloor]
    
    jumpbox= sg.SceneGraphNode("jumpbox"+str(n))
    jumpbox.transform = tr.uniformScale(1)
    jumpbox.childs += [tube,rightfloor,leftfloor,startfloor,finishfloor,centerfloor]
    return jumpbox

#Crear una caja de largo 2X
def create_TUBE2(pipeline,n,d,x): #pipeline // n=tubos ya hechos // d=distancia desde 0 hasta el último tubo // x=largo salto
    shapeTUBE = bs.createTextureTUBE('wall.jfif')
    gpuTUBE = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTUBE)
    gpuTUBE.fillBuffers(shapeTUBE.vertices, shapeTUBE.indices, GL_STATIC_DRAW)
    gpuTUBE.texture = es.textureSimpleSetup(getAssetPath("wall.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    TUBEbox = sg.SceneGraphNode("tube2"+str(n))
    TUBEbox.transform = tr.matmul([tr.translate(-(d+1*x), 0, 0.3), tr.scale(2*x,2,2)])
    TUBEbox.childs += [gpuTUBE]

    return [TUBEbox, d+2*x] 

#crear una caja de largo 3X
def create_TUBE3(pipeline,n,d,x): #pipeline // n=tubos ya hechos // d=distancia desde 0 hasta el último tubo // x=largo salto 
    shapeTUBE = bs.createTextureTUBE('wall.jfif')
    gpuTUBE = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTUBE)
    gpuTUBE.fillBuffers(shapeTUBE.vertices, shapeTUBE.indices, GL_STATIC_DRAW)
    gpuTUBE.texture = es.textureSimpleSetup(getAssetPath("wall.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    TUBEbox = sg.SceneGraphNode("tube3"+str(n))
    TUBEbox.transform = tr.matmul([tr.translate(-(d+1.5*x), 0, 0.3), tr.scale(3*x,2,2)])
    TUBEbox.childs += [gpuTUBE]

    return [TUBEbox, d+3*x]

#Crear pisos izq de largo funcion de X
def create_left_floor2(pipeline,n,d,x):
    shapeFloor = bs.createTextureQuad(2,2)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(getAssetPath("floor.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    leftfloor = sg.SceneGraphNode("leftfloor2"+str(n))
    leftfloor.transform = tr.matmul([tr.translate(-(d+0.5*x), -0.75, 0),tr.scale(x, 0.6, 1)])
    leftfloor.childs += [gpuFloor]
    return [leftfloor, d+2*x, "left"]
    
def create_left_floor3(pipeline,n,d,x):
    shapeFloor = bs.createTextureQuad(2,2)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(getAssetPath("floor.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    leftfloor = sg.SceneGraphNode("leftfloor3"+str(n))
    leftfloor.transform = tr.matmul([tr.translate(-(d+x), -0.75, 0),tr.scale(2*x, 0.6, 1)])
    leftfloor.childs += [gpuFloor]
    return [leftfloor, d+3*x, "left"]

#Crear pisos centro de largo funcion de X
def create_center_floor2(pipeline,n,d,x):
    shapeFloor = bs.createTextureQuad(2,2)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(getAssetPath("floor.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    centerfloor = sg.SceneGraphNode("centerfloor2"+str(n))
    centerfloor.transform = tr.matmul([tr.translate(-(d+0.5*x), 0, 0),tr.scale(x, 0.6, 1)])
    centerfloor.childs += [gpuFloor]
    return [centerfloor,d+2*x, "center"]

def create_center_floor3(pipeline,n,d,x):
    shapeFloor = bs.createTextureQuad(2,2)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(getAssetPath("floor.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    centerfloor = sg.SceneGraphNode("centerfloor3"+str(n))
    centerfloor.transform = tr.matmul([tr.translate(-(d+x), 0, 0),tr.scale(2*x, 0.6, 1)])
    centerfloor.childs += [gpuFloor]
    return [centerfloor,d+3*x, "center"]

#Crear pisos der de largo funcion de X
def create_right_floor2(pipeline,n,d,x):
    shapeFloor = bs.createTextureQuad(2,2)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(getAssetPath("floor.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    rightfloor = sg.SceneGraphNode("rightfloor2"+str(n))
    rightfloor.transform = tr.matmul([tr.translate(-(d+0.5*x), 0.75, 0),tr.scale(x, 0.6, 1)])
    rightfloor.childs += [gpuFloor]
    return [rightfloor, d+2*x, "right"]

def create_right_floor3(pipeline,n,d,x):
    shapeFloor = bs.createTextureQuad(2,2)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(getAssetPath("floor.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    rightfloor = sg.SceneGraphNode("rightfloor3"+str(n))
    rightfloor.transform = tr.matmul([tr.translate(-(d+x), 0.75, 0),tr.scale(2*x, 0.6, 1)])
    rightfloor.childs += [gpuFloor]
    return [rightfloor, d+3*x, "right"]

#Crear pisos comlpetos de largo funcion de X
def create_full_floor2(pipeline,n,d,x):
    shapeFloor = bs.createTextureQuad(2,2)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(getAssetPath("floor.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    fullfloor = sg.SceneGraphNode("fullfloor2"+str(n))
    fullfloor.transform = tr.matmul([tr.translate(-(d+0.5*x),0,0),tr.scale(x,2,1)])
    fullfloor.childs +=[gpuFloor]
    return [fullfloor, d+2*x, "full"]

def create_full_floor3(pipeline,n,d,x):
    shapeFloor = bs.createTextureQuad(2,2)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(getAssetPath("floor.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    fullfloor = sg.SceneGraphNode("fullfloor3"+str(n))
    fullfloor.transform = tr.matmul([tr.translate(-(d+x),0,0),tr.scale(2*x,2,1)])
    fullfloor.childs +=[gpuFloor]
    return [fullfloor, d+3*x, "full"]

#crear un randomizador que no permita la creacion de izq <-> der, 
#despues de un izq puede ir un centro/izq/completo
#despues de un der puede ir un centro/der/completo
def randomfloor2(pipeline,n,d,x,anterior):
    rand=np.random.randint(100)
    if anterior=="left":
        if rand<30:
            return create_left_floor2(pipeline,n,d,x)
        elif rand<66:
            return create_center_floor2(pipeline,n,d,x)
        else:
            return create_full_floor2(pipeline,n,d,x)

    elif anterior=="right":
        if rand<30:
            return create_right_floor2(pipeline,n,d,x)
        elif rand<66:
            return create_center_floor2(pipeline,n,d,x)
        else:
            return create_full_floor2(pipeline,n,d,x)
    
    else:
        if rand<25:
            return create_left_floor2(pipeline,n,d,x)
        elif rand<50:
            return create_center_floor2(pipeline,n,d,x)
        elif rand<75:
            return create_right_floor2(pipeline,n,d,x)
        else:
            return create_full_floor2(pipeline,n,d,x)

def randomfloor3(pipeline,n,d,x,anterior):
    rand=np.random.randint(100)
    if anterior=="left":
        if rand<30:
            return create_left_floor3(pipeline,n,d,x)
        elif rand<66:
            return create_center_floor3(pipeline,n,d,x)
        else:
            return create_full_floor3(pipeline,n,d,x)

    elif anterior=="right":
        if rand<30:
            return create_right_floor3(pipeline,n,d,x)
        elif rand<66:
            return create_center_floor3(pipeline,n,d,x)
        else:
            return create_full_floor3(pipeline,n,d,x)
    
    else:
        if rand<25:
            return create_left_floor3(pipeline,n,d,x)
        elif rand<50:
            return create_center_floor3(pipeline,n,d,x)
        elif rand<75:
            return create_right_floor3(pipeline,n,d,x)
        else:
            return create_full_floor3(pipeline,n,d,x)

def create_level(pipeline,x,y):

    STARTbox=create_START_BOX(pipeline)

    hallway=sg.SceneGraphNode("hallway")
    hallway.transform=tr.uniformScale(1)
    n=1
    d=1
    anterior = "None"
    while y-1-n>0:
        rand = np.random.randint(100)
        if rand<50:
            tube=create_TUBE2(pipeline,n,d,x)
            floor=randomfloor2(pipeline,n,d,x,anterior)
            anterior = floor[2]
        else:
            tube=create_TUBE3(pipeline,n,d,x)
            floor=randomfloor3(pipeline,n,d,x,anterior)
            anterior = floor[2]

        hallway.childs += [tube[0],floor[0]]
        d=tube[1]
        n+=1
    
    floors=sg.SceneGraphNode("floors")
    floors.transform = tr.uniformScale(1)
    floor1=create_floor(pipeline,0,-1)
    floor2=create_floor(pipeline,n,d)
    floors.childs += [floor1,floor2]
    

    FINISHbox=create_FINISH_BOX(pipeline,d)

    level=sg.SceneGraphNode("level")
    level.transform = tr.uniformScale(1)
    level.childs += [STARTbox,hallway,FINISHbox,floors]
    return level