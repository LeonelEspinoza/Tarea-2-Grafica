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

x=0.8#recomendable 0-0.5, rango 0-1 (esta variable es el largo del salto y el alto del salto)
y=8#largo
z=5#tiempo luz


# A class to store the application control
class Controller:
    def __init__(self):
        self.vista3 = True
        self.cambiovista = False
        self.IsOnGround = True
        self.end=False
        self.GoUp=False
        self.jump=False
###########################################################
        self.theta = np.pi
        self.eye = [0, 0, 0.1]  # Básicamente la posición del jugador
        self.at = [0, 1, 0.1]   # Hacia dónde ve el jugador
        self.up = [0, 0, 1]     # Un vector hacia arriba
###########################################################


# global controller as communication with the callback function
controller = Controller()

def jump(dt):
    #esta funcion se llama dentro del while por tanto la logica es como un while
    #ademas solo se llama mientras este la señal de salto
    vel=2
    if controller.GoUp:  #mientras este activa la señal de subir
        controller.eye[2] += vel * dt #sube
        controller.at[2] += vel * dt
        if controller.vista3:   #si vista en tercera persona
            if controller.at[2]>=x: #si el personaje llega a la altura maxima de salto 
                controller.GoUp = False # deja de subir
        else:
            if controller.eye[2]>=x: #si llegamos a la altura maxima de salto
                controller.GoUp = False #deja de subir

    else:                   #mientras no este activa la señal de subir
        controller.eye[2] -= vel * dt   #baja
        controller.at[2] -= vel * dt
        if controller.at[2]<=0.1:  #si llega al tope del suelo!!cambiar por la funicion suelo para caer de las plataformas
            controller.jump=False   #deja de saltar (termina el ciclo del salto)



def process_on_key(dt):
    vel =2
    if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS) and (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
        if controller.eye[1]>-1:
            controller.eye[1] -= vel * dt
            controller.at[1] -= vel * dt
        controller.eye[0] -= vel * dt
        controller.at[0] -= vel * dt

    elif (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS) and (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
        if controller.eye[1]<1:
            controller.eye[1] += vel * dt
            controller.at[1] += 1 * dt
        controller.eye[0] -= vel * dt
        controller.at[0] -= vel * dt

    elif glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        controller.theta += 2 * dt

    elif glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        controller.theta -= 2 * dt

    elif glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        if controller.eye[1]>-1:
            controller.eye[1] -= vel * dt
            controller.at[1] -= vel * dt

    elif glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        if controller.eye[1]<1:
            controller.eye[1] += vel * dt
            controller.at[1] += 1 * dt

    elif glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        controller.eye[0] -= vel * dt
        controller.at[0] -= vel * dt

    elif glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        if controller.eye[0]<1:
            controller.eye[0] += vel * dt
            controller.at[0] += vel * dt
    
    elif glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
        if controller.eye[2]>0.1:
            controller.eye[2] -= vel * dt
            controller.at[2] -= vel * dt
    
    elif glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
        if controller.IsOnGround:   #si esta en la tierra
            controller.jump=True    #da la señal de saltar  
            controller.GoUp=True    #y empieza a subir

def process_on_key3(dt):
    vel = 2
    if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS) and (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
        if controller.at[1]>-1:
            controller.eye[1] -= vel * dt
            controller.at[1] -= vel * dt
        controller.eye[0] -= vel * dt
        controller.at[0] -= vel * dt

    elif (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS) and (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
        if controller.at[1]<1:
            controller.eye[1] += vel * dt
            controller.at[1] += vel * dt
        controller.eye[0] -= vel * dt
        controller.at[0] -= vel * dt

    elif glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        if controller.at[1]>-1:
            controller.eye[1] -= vel * dt
            controller.at[1] -= vel * dt

    elif glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        if controller.at[1]<1:
            controller.eye[1] += vel * dt
            controller.at[1] += vel * dt

    elif glfw.get_key(window, glfw.KEY_W) == glfw.PRESS: #este no necesita limite porque le quitare el control al jugador al llegar al final
        controller.eye[0] -= vel * dt
        controller.at[0] -= vel * dt

    elif glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        if controller.eye[0]<1:
            controller.eye[0] += vel * dt
            controller.at[0] += vel * dt
    
    elif glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
        if controller.at [2]>0.1:
            controller.eye[2] -= vel * dt
            controller.at[2] -= vel * dt
    
    elif glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
        if controller.IsOnGround:   #si esta en la tierra
            controller.jump=True    #da la señal de saltar  
            controller.GoUp=True    #y empieza a subir

    
def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS and action != glfw.REPEAT:
        return
    
    global controller
    
    if key == glfw.KEY_L:
        controller.vista3 = not controller.vista3

    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        #glfw.set_window_should_close(window, True)
        glfw.terminate

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
    INFOlevel = ModeloTarea.create_level(textureShaderProgram,x,y)
    level= INFOlevel[0]
    d=INFOlevel[1]
    
    # Creamos una GPUShape a partir de un obj
    # Acá pueden poner carrot.obj, eiffel.obj, suzanne.obj
    shapeSuzanne = obj.readOBJ(getAssetPath('crash_pose.obj'), (1.0, 0.0, 0.0))
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
        if controller.vista3:  #vista tercera persona
            if not (controller.cambiovista):  
                controller.at = controller.eye                                  #la camara mira a donde está el personaje
                controller.eye= controller.eye - np.array([-0.8, 0, -0.4])      #la camara retrocede en x y sube en z, no cambia en y
                controller.cambiovista = True                                   #se completo el cambio de vista a primera persona
            
            if controller.at[2]<=0.1: #esta bajo o en el nivel de la tierra
                controller.IsOnGround = True #esta en tierra
                
            else:                     #esta sobre el nivel de la tierra
                controller.IsOnGround = False #no esta en tierra

            if controller.at[0]>=-d-1:  #no llego al final del nivel
                process_on_key3(dt) #puede usar los controles
            else:                       #llego al final del nivel
                controller.end=True #no puede usar los controles y salta pantalla ganador

            if controller.jump: #si se da la señal de saltar
                jump(dt)        #salta
                
            view = tr.lookAt(
                controller.eye,
                controller.at,
                controller.up
            )

        else: #vista primera persona
            if controller.cambiovista:
                controller.at = controller.at + np.array([0,1,0])               #la camara mira justo en frente de donde está el personaje
                controller.eye = controller.eye + np.array([-0.8, 0, -0.4])     #la camara avanza en x y baja en z, no cambia en y
                controller.cambiovista = False                                  #se completo el cambio de vista a tercera persona

            if controller.eye[2]<=0.1:  #esta bajo o en el nivel de la tierra
                controller.IsOnGround = True   #esta en la tierra
            else:                       #esta sobre el nivel de la tierra
                controller.IsOnGround = False    #no esta en la tierra
            
            if controller.eye[0]>=-d-1: #no llego al final del nivel
                process_on_key(dt)  #puede usar los controles
            else:                       #llego al final del nivel
                controller.end=True #no puede usar los controles y aparece pantalla ganador
            
            if controller.jump: #si se da la señal de saltar
                jump(dt)        #salta
            

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


        ###DIBUJO LEVEL###
        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        #glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        
        sg.drawSceneGraphNode(level, textureShaderProgram, 'model')
        ###---###

        
        if controller.vista3:   #si esta en tercera persona dibujar el OBJ 
            ###DIBUJO OBJ###
            # Dibujamos el modelo de Suzanne con OBJ:
            # Indicamos que usamos el modelo de luz
            # Se escala, se rota y se sube, en ese orden
            suzanne_transform = tr.matmul(
                [
                    tr.translate(controller.at[0]-0.8,controller.at[1]-0.3,controller.at[2]+0.1), 
                    tr.rotationX(np.pi/2),
                    tr.rotationY(np.pi/-2),
                    tr.uniformScale(0.2),
                ]
            )
            glUseProgram(lightShaderProgram.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(lightShaderProgram.shaderProgram, "model"), 1, GL_TRUE, suzanne_transform)
            glUniformMatrix4fv(glGetUniformLocation(lightShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(lightShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
            # Esto es para indicarle al shader de luz parámetros
            lightShaderProgram.set_light_attributes()
            lightShaderProgram.drawCall(gpuSuzanne)
            
        

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
