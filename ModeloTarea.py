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

def create_FINISH_BOX(pipeline,z):
    shapeFINISH = bs.createTextureFINISH('wall.jfif')
    gpuFINISH = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFINISH)
    gpuFINISH.fillBuffers(shapeFINISH.vertices, shapeFINISH.indices, GL_STATIC_DRAW)
    gpuFINISH.texture = es.textureSimpleSetup(getAssetPath("wall.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    FINISHbox = sg.SceneGraphNode("finish")
    FINISHbox.transform = tr.matmul([tr.translate(-2*z, 0, 0.3), tr.uniformScale(2)])
    FINISHbox.childs += [gpuFINISH]

    return FINISHbox

def create_floor(pipeline,n):
    x=2*n
    shapeFloor = bs.createTextureQuad(8, 8)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(getAssetPath("floor.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    floor = sg.SceneGraphNode("floor"+str(n))
    floor.transform = tr.matmul([tr.translate(-x, 0, 0),tr.scale(2, 2, 1)])
    floor.childs += [gpuFloor]

    return floor

def create_level(pipeline,x,z):

    STARTbox=create_START_BOX(pipeline)
    
    ###necesito crear tubos secuencialmente### 
    tubes=sg.SceneGraphNode("tubes")
    tubes.transform=tr.uniformScale(1)
    n=1
    while z-1-n >0: #no quiero cambiar z para los pisos y le resto uno porque ya está puesto el start
        TUBEbox=create_TUBE(pipeline,n)
        tubes.childs += [TUBEbox]
        n+=1
    ###---###

    ###necesito crear pisos secuencialmente###
    floors=sg.SceneGraphNode("floors")
    floors.transform = tr.uniformScale(1)
    n=0
    while z-n >0:
        floor=create_floor(pipeline,n)
        floors.childs += [floor]
        n+=1
    ###---###

    FINISHbox=create_FINISH_BOX(pipeline,z-1)

    level=sg.SceneGraphNode("level")
    level.transform = tr.uniformScale(0.5)
    level.childs += [STARTbox,tubes,FINISHbox,floors]
    return level