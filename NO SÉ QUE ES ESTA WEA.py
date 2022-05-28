# coding=utf-8


import glfw
from OpenGL.GL import *
import numpy as np
import sys
import os.path

import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import grafica.performance_monitor as pm
from grafica.assets_path import getAssetPath

fovy=
aspecto=
near=
far=
tr.perspective(fovy,aspecto,near,far)

#Matriz de vista 
#up-> vector que ve arriba
#at-> vector hacia donde apunta
#eye-> vector posicion camara
#básicamente establece la camara 

#Mallas de polígonos
#archivos OBJ 
#   definen vert text y norm
#   guarda el indice de cada linea
#   caras indican vert/text/norm
#   f v1/vt1/vn1  v2/vt2/vn2
#usar obj_reader.py para leer archivos OBJ o OFF
#se pueden descargar figuras OBJ y OFF


##AUX 5 
#P1
#usamos coordenadas polares para hacer el Mov circular 

        view = tr.lookAt(
            np.array([1.0, 0.0, 0.0]),  # eye 
            np.array([-1.0, 1.0, 0.0]),  # at
            np.array([0.0, 0.0, 1.0]),  # up
        )

#si quiero moverme en coords polares entonces 
#X= cos(phi) * R
#Y= sen(phi) * R
