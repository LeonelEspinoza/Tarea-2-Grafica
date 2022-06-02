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
import grafica.lighting_shaders as ls
import off_obj_reader as obj
from grafica.assets_path import getAssetPath

import ModeloTarea


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.vista3 = False
        self.cambiovista = False
###########################################################
        self.theta = np.pi
        self.eye = [0, 0, 0.1]  # Básicamente la posición del jugador
        self.at = [0, 1, 0.1]   # Hacia dónde ve el jugador
        self.up = [0, 0, 1]     # Un vector hacia arriba
###########################################################


# global controller as communication with the callback function
controller = Controller()

def process_on_key(dt):
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        controller.theta += 2 * dt

    elif glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        controller.theta -= 2 * dt

    elif glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        controller.eye += (controller.at - controller.eye) * dt
        controller.at += (controller.at - controller.eye) * dt

    elif glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        controller.eye -= (controller.at - controller.eye) * dt
        controller.at -= (controller.at - controller.eye) * dt
    
    elif glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
        controller.eye[2] -= 0.1 * dt
        controller.at[2] -= 0.1 * dt
    
    elif glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
        controller.eye[2] += 0.1 * dt
        controller.at[2] += 0.1 * dt

def process_on_key3(dt):
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        controller.eye[1] -= 1 * dt
        controller.at[1] -= 1 * dt

    elif glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        controller.eye[1] += 1 * dt
        controller.at[1] += 1 * dt

    elif glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        controller.eye[0] -= 1 * dt
        controller.at[0] -= 1 * dt

    elif glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        controller.eye[0] += 1 * dt
        controller.at[0] += 1 * dt
    
    elif glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
        controller.eye[2] -= 1 * dt
        controller.at[2] -= 1 * dt
    
    elif glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
        controller.eye[2] += 1 * dt
        controller.at[2] += 1 * dt
    
def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS and action != glfw.REPEAT:
        return
    
    global controller
    
    if key == glfw.KEY_F:
        controller.vista3 = not controller.vista3

    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    #else:
    #    print('Unknown key')


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 1500
    height = 1000

    window = glfw.create_window(width, height, "Crash lights out", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colors
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()
    lightShaderProgram = ls.SimpleGouraudShaderProgram()
    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    level = ModeloTarea.create_level(textureShaderProgram,0,3)

    # Creamos una GPUShape a partir de un obj
    # Acá pueden poner carrot.obj, eiffel.obj, suzanne.obj
    shapeSuzanne = obj.readOBJ(getAssetPath('eiffel.obj'), (1.0, 0.0, 0.0))
    gpuSuzanne = es.GPUShape().initBuffers()
    lightShaderProgram.setupVAO(gpuSuzanne)
    gpuSuzanne.fillBuffers(shapeSuzanne.vertices, shapeSuzanne.indices, GL_STATIC_DRAW)

    # View and projection
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100) #fovy  aspect  near  far

    t0 = glfw.get_time()

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    t1 = glfw.get_time()

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        #vista primera-tercera persona
        if (controller.vista3):  
            if not (controller.cambiovista):  
                controller.at = controller.eye                                  #la camara mira a donde está el personaje
                controller.eye= controller.eye - np.array([-0.7, 0, -0.3])      #la camara retrocede en x y sube en z, no cambia en y
                controller.cambiovista = True
            process_on_key3(dt)

            view = tr.lookAt(
                controller.eye,
                controller.at,
                controller.up
            )
            #que la camara sea en tercera persona
            #la camara debe apuntar al obj 
            #la camara no se debe mover hacia el at, sino que con el obj
            

        else: #vista primera persona
            if (controller.cambiovista):
                controller.at = controller.at + np.array([0,1,0])               #la camara mira justo en frente de donde está el personaje
                controller.eye = controller.eye + np.array([-0.7, 0, -0.3])     #la camara avanza en x y baja en z, no cambia en y
                controller.cambiovista = False
            
            process_on_key(dt)
            
            at_x = controller.eye[0] + np.cos(controller.theta)
            at_y = controller.eye[1] + np.sin(controller.theta)
            controller.at = np.array([at_x, at_y, controller.at[2]])

            view = tr.lookAt(
                controller.eye,
                controller.at,
                controller.up
            )

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Procesar input
        #process_on_key(dt)

        #at_x = controller.eye[0] + np.cos(controller.theta)
        #at_y = controller.eye[1] + np.sin(controller.theta)
        #controller.at = np.array([at_x, at_y, controller.at[2]])

        #view = tr.lookAt(
        #    controller.eye,
        #    controller.at,
        #    controller.up
        #)

        ###DIBUJO LEVEL###
        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        #glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        
        sg.drawSceneGraphNode(level, textureShaderProgram, 'model')
        ###---###

        ###DIBUJO OBJ###
        # Dibujamos el modelo de Suzanne con OBJ:
        # Indicamos que usamos el modelo de luz
        # Se escala, se rota y se sube, en ese orden
        if controller.vista3:    
            suzanne_transform = tr.matmul(
                [
                    tr.translate(controller.at[0],controller.at[1]+0.1,controller.at[2]),
                    tr.rotationX(np.pi/2),
                    tr.uniformScale(0.00003),
                ]
            )
        else:
            suzanne_transform = tr.matmul(
                [
                    tr.translate(0,0,-2),
                    tr.rotationX(np.pi/2),
                    tr.uniformScale(0.00003),
                ]
            )
            
        glUseProgram(lightShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(lightShaderProgram.shaderProgram, "model"), 1, GL_TRUE, suzanne_transform)
        glUniformMatrix4fv(glGetUniformLocation(lightShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(lightShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        # Esto es para indicarle al shader de luz parámetros, pero por ahora no lo veremos
        lightShaderProgram.set_light_attributes() # IGNORAR
        lightShaderProgram.drawCall(gpuSuzanne)
        ###---###

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()