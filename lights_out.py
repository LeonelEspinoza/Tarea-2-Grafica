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
import grafica.text_renderer as tx

from grafica.assets_path import getAssetPath

import ModeloTarea

#ejemplo de llamada: python lights_out.py 0.8 3 5
x=float(sys.argv[1])#recomendable 0-0.5, rango 0-1 (esta variable es el largo del salto y el alto del salto)
y=int(sys.argv[2])+2#largo nivel
z=int(sys.argv[3])#tiempo luz
#x=0.5
#y=3
#z=5
# A class to store the application control
class Controller:
    def __init__(self):
        self.vista3 = True
        self.cambiovista = False
        self.IsOnGround = True
        self.victory=False
        self.lose=False
        self.GoUp=False
        self.jump=False
        self.lightOn = False
        self.playerBlockPosition=0
        self.ThisBlockFinishOn=1
###########################################################
        self.theta = np.pi
        self.eye = [0, 0, 0.3]  # Básicamente la posición del jugador
        self.at = [0, 1, 0.3]   # Hacia dónde ve el jugador
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
        if controller.at[2]>=x: #si el personaje llega a la altura maxima de salto 
                controller.GoUp = False # deja de subir

    else:                   #mientras no este activa la señal de subir
        controller.eye[2] -= vel * dt   #baja
        controller.at[2] -= vel * dt
        if controller.at[2]<=0.1:  #si llega al tope del suelo!!cambiar por la funicion suelo para caer de las plataformas
            controller.jump=False   #deja de saltar (termina el ciclo del salto)

#para saber las colisiones del piso necesito saber en que bloque esta el player 
def floorcolissions(floor,k): #floor=floorlist[i] k=coordenada x donde termina el anterior bloque
    ###rango coliciones en x
    if floor[1]==2:     #si el piso es de x
        coordX=(k,k-x)
        k=k-2*x
    elif floor[1]==3:   #si el piso es de 2x
        coordX=(k,k-2*x)
        k=k-3*x
    else:               #si el piso es del start o el finish 
        coordX=(k,k-2)
        k=k-2

    controller.ThisBlockFinishOn=k
    ###rango coliciones en y 
    if floor[0]=="center":  #si el piso es de centro
        coordY=(-(1/3),1/3)
    elif floor[0]=="right": #si el piso es deercha
        coordY=(1/3,1)    
    elif floor[0]=="left":  #si el piso es izquierda
        coordY=(-1,-(1/3))
    else:                   #si el piso es full, start o finish
        coordY=(-1,1)
    
    #retorna una tupla de tuplas que cada una contiene el rango coliciones del piso en x e y respect
    #ademas entrega la coordenada x desde donde termina este bloque 
    return (coordX,coordY)  

def process_on_key(dt):
    vel =2
    if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS) and (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
        if controller.eye[1]>-0.9:
            controller.eye[1] -= vel * dt
            controller.at[1] -= vel * dt
        controller.eye[0] -= vel * dt
        controller.at[0] -= vel * dt

    elif (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS) and (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
        if controller.eye[1]<0.9:
            controller.eye[1] += vel * dt
            controller.at[1] += 1 * dt
        controller.eye[0] -= vel * dt
        controller.at[0] -= vel * dt

    elif glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        if controller.eye[1]>-0.9:
            controller.eye[1] -= vel * dt
            controller.at[1] -= vel * dt

    elif glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        if controller.eye[1]<0.9:
            controller.eye[1] += vel * dt
            controller.at[1] += 1 * dt

    elif glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        controller.eye[0] -= vel * dt
        controller.at[0] -= vel * dt

    elif glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        if controller.eye[0]<1:
            controller.eye[0] += vel * dt
            controller.at[0] += vel * dt
    
    elif glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
        if controller.IsOnGround:   #si esta en la tierra
            controller.jump=True    #da la señal de saltar  
            controller.GoUp=True    #y empieza a subir

def process_on_key3(dt):
    vel = 2
    if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS) and (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
        if controller.at[1]>-0.9:
            controller.eye[1] -= vel * dt
            controller.at[1] -= vel * dt
        controller.eye[0] -= vel * dt
        controller.at[0] -= vel * dt

    elif (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS) and (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
        if controller.at[1]<0.9:
            controller.eye[1] += vel * dt
            controller.at[1] += vel * dt
        controller.eye[0] -= vel * dt
        controller.at[0] -= vel * dt

    elif glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        if controller.at[1]>-0.9:
            controller.eye[1] -= vel * dt
            controller.at[1] -= vel * dt

    elif glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        if controller.at[1]<0.9:
            controller.eye[1] += vel * dt
            controller.at[1] += vel * dt

    elif glfw.get_key(window, glfw.KEY_W) == glfw.PRESS: #este no necesita limite porque le quitare el control al jugador al llegar al final
        controller.eye[0] -= vel * dt
        controller.at[0] -= vel * dt

    elif glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        if controller.eye[0]<1:
            controller.eye[0] += vel * dt
            controller.at[0] += vel * dt
    
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
    
    if key == glfw.KEY_E:
        controller.lightOn=True

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
    textureLightShaderProgram = ls.SimpleTextureGouraudShaderProgram()
    textPipeline = tx.TextureTextRendererShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    textBitsTexture = tx.generateTextBitsTexture()
    gpuText3DTexture = tx.toOpenGLTexture(textBitsTexture)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    INFOlevel = ModeloTarea.create_level(textureShaderProgram,x,y)
    level= INFOlevel[0]
    d=INFOlevel[1]
    floorlist=INFOlevel[2]
    print(floorlist)
    
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
    tl=0

    floorcol=floorcolissions(floorlist[controller.playerBlockPosition],1)
    floorXstartat=floorcol[0][0]     #donde comienza el piso en x
    floorXfinishat=floorcol[0][1]    #donde termina el piso en x
    floorYstartat=floorcol[1][0]     #donde comienza el piso en y
    floorYfinishat=floorcol[1][1]    #donde termina el piso en y

    headerText = "YOU LOSE"
    headerCharSize = 0.1
    headerCenterX = headerCharSize * len(headerText) / 2
    headerShape = tx.textToShape(headerText, headerCharSize, headerCharSize)
    gpuHeader = es.GPUShape().initBuffers()
    textPipeline.setupVAO(gpuHeader)
    gpuHeader.fillBuffers(headerShape.vertices, headerShape.indices, GL_STATIC_DRAW)
    gpuHeader.texture = gpuText3DTexture
    headerTransform = tr.translate(0,-0.5,0)
    
    headerText2 = "YOU WIN"
    headerCharSize2 = 0.1
    headerCenterX2 = headerCharSize2 * len(headerText2) / 2
    headerShape2 = tx.textToShape(headerText2, headerCharSize2, headerCharSize2)
    gpuHeader2 = es.GPUShape().initBuffers()
    textPipeline.setupVAO(gpuHeader2)
    gpuHeader2.fillBuffers(headerShape2.vertices, headerShape2.indices, GL_STATIC_DRAW)
    gpuHeader2.texture = gpuText3DTexture
    headerTransform = tr.translate(0,-0.5,0)

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
            
            if controller.at[0] <=controller.ThisBlockFinishOn:
                controller.playerBlockPosition+=1
                floorcol = floorcolissions(floorlist[controller.playerBlockPosition],controller.ThisBlockFinishOn)
                ##retorna una tupla de tuplas que cada una contiene el rango coliciones del piso en x e y respect
                floorXstartat=floorcol[0][0]     #donde comienza el piso en x
                floorXfinishat=floorcol[0][1]    #donde termina el piso en x
                floorYstartat=floorcol[1][0]     #donde comienza el piso en y
                floorYfinishat=floorcol[1][1]    #donde termina el piso en y
            
            if floorXstartat>=controller.at[0] and controller.at[0]+0.17>=floorXfinishat and floorYstartat<=controller.at[1] and controller.at[1]<=floorYfinishat and 0.15>=controller.at[2] and controller.at[2]>=0.05:        #Si esta detntro del piso en x //las coords en x estan en negativo
                #Si esta detntro del piso en x //las coords en x estan en negativo
                #si esta dentro del piso en y
                #si esta cerca del piso en z
                #entonces esta en el piso y no cae
                controller.IsOnGround=True
                
            else:
                controller.IsOnGround=False
                if not controller.jump and not controller.lose:
                    controller.eye[2] -= 3 * dt   #baja//cae
                    controller.at[2] -= 3 * dt
                    if controller.at[2]<-0.5:
                        controller.lose=True
                
            
            #if controller.at[2]<=0.1: #esta bajo o en el nivel de la tierra
            #    controller.IsOnGround = True #esta en tierra               
            #else:                     #esta sobre el nivel de la tierra
            #    controller.IsOnGround = False #no esta en tierra

            if controller.at[0]>=-d-1 and not controller.lose:  #aun no llego al final del nivel
                process_on_key3(dt) #puede usar los controles
            elif not controller.lose:                       #llego al final del nivel
                controller.victory=True #no puede usar los controles y salta pantalla ganador

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

            if controller.eye[0] <=controller.ThisBlockFinishOn:
                controller.playerBlockPosition+=1
                floorcol = floorcolissions(floorlist[controller.playerBlockPosition],controller.ThisBlockFinishOn)
                ##retorna una tupla de tuplas que cada una contiene el rango coliciones del piso en x e y respect
                floorXstartat=floorcol[0][0]     #donde comienza el piso en x
                floorXfinishat=floorcol[0][1]    #donde termina el piso en x
                floorYstartat=floorcol[1][0]     #donde comienza el piso en y
                floorYfinishat=floorcol[1][1]    #donde termina el piso en y
            
            if floorXstartat>=controller.eye[0] and controller.eye[0]+0.17>=floorXfinishat and floorYstartat<=controller.at[1] and controller.at[1]<=floorYfinishat and 0.15>=controller.at[2] and controller.at[2]>=0.05:        #Si esta detntro del piso en x //las coords en x estan en negativo
                #Si esta detntro del piso en x //las coords en x estan en negativo
                #si esta dentro del piso en y
                #si esta cerca del piso en z
                #entonces esta en el piso y no cae
                controller.IsOnGround=True
                
            else:
                controller.IsOnGround=False
                if not controller.jump and not controller.lose:
                    controller.eye[2] -= 3 * dt   #baja//cae
                    controller.at[2] -= 3 * dt
                    if controller.at[2]<-0.5:
                        controller.lose=True

#            if controller.eye[2]<=0.1:  #esta bajo o en el nivel de la tierra
#                controller.IsOnGround = True   #esta en la tierra
#            else:                       #esta sobre el nivel de la tierra
#                controller.IsOnGround = False    #no esta en la tierra
            
            if controller.eye[0]>=-d-1 and not controller.lose:  #aun no llego al final del nivel
                process_on_key(dt) #puede usar los controles
            elif not controller.lose:                       #llego al final del nivel
                controller.victory=True
            
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
            
        if controller.lightOn and tl>=z:
            controller.lightOn = False
            tl=0
        elif controller.lightOn:
            tl+=dt

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        ###DIBUJO LEVEL###
        glUseProgram(textureLightShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        if controller.lightOn:
            textureLightShaderProgram.set_light_attributes(controller.at[0],controller.at[1],controller.at[2]+1,1)
        else:
            textureLightShaderProgram.set_light_attributes(controller.at[0],controller.at[1],controller.at[2]+1,10)
        sg.drawSceneGraphNode(level, textureLightShaderProgram, 'model')
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
            if controller.lightOn:
                lightShaderProgram.set_light_attributes(controller.at[0],controller.at[1],controller.at[2]+1,1)
            else:
                lightShaderProgram.set_light_attributes(controller.at[0],controller.at[1],controller.at[2]+1,10)

            lightShaderProgram.drawCall(gpuSuzanne)
            
        if controller.victory:
            controller.lightOn=True
            tl=1
            glUseProgram(textPipeline.shaderProgram)
            glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "fontColor"), 1, 1, 1, 1)
            glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "backColor"), 0, 0, 0, 1)
            glUniformMatrix4fv(glGetUniformLocation(textPipeline.shaderProgram, "transform"), 1, GL_TRUE, headerTransform)
            textPipeline.drawCall(gpuHeader2)
            #pantalla victoria
            
        if controller.lose:
            controller.lightOn=True
            tl=1
            glUseProgram(textPipeline.shaderProgram)
            glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "fontColor"), 1, 1, 1, 1)
            glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "backColor"), 0, 0, 0, 1)
            glUniformMatrix4fv(glGetUniformLocation(textPipeline.shaderProgram, "transform"), 1, GL_TRUE, headerTransform)
            textPipeline.drawCall(gpuHeader)
            #pantalla derrota

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
