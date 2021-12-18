import glfw
import pyrr
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import os
import math
import random
from PIL import Image
from camera import Camera
from tiles import RobinsonTriangle, BtileL, BtileS, PenroseP3
from pyrr.objects.vector3 import Vector3


#print controls
print("Use wasd and mouse to control camera, shift to go up and control to go down")
print("Use arrow keys to move light cube, pgUp to go up and pgDown to go down")
cam = Camera()
cubeCam = Camera()
width = 1200
height = 1000
lastX, lastY = width / 2, height / 2
first_mouse = True
left, right, forward, backward, up, down = False, False, False, False, False, False
leftCube, rightCube, forwardCube, backwardCube, upwardCube, downwardCube = False, False, False, False, False, False
cubeL, cubeU, cubeF = 0, 0, 0
menu = True
# the keyboard input callback
def key_input_clb(window, key, scancode, action, mode):
    global left, right, forward, backward, leftCube, rightCube, forwardCube, backwardCube, upwardCube, downwardCube, up, down
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    if key == glfw.KEY_M and action == glfw.PRESS:
        openMenu()
    if key == glfw.KEY_W and action == glfw.PRESS:
        forward = True
    elif key == glfw.KEY_W and action == glfw.RELEASE:
        forward = False
    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True
    elif key == glfw.KEY_S and action == glfw.RELEASE:
        backward = False
    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True
    elif key == glfw.KEY_A and action == glfw.RELEASE:
        left = False
    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True
    elif key == glfw.KEY_D and action == glfw.RELEASE:
        right = False
    if key == glfw.KEY_LEFT_SHIFT and action == glfw.PRESS:
        up = True
    elif key == glfw.KEY_LEFT_SHIFT and action == glfw.RELEASE:
        up = False
    if key == glfw.KEY_LEFT_CONTROL and action == glfw.PRESS:
        down = True
    elif key == glfw.KEY_LEFT_CONTROL and action == glfw.RELEASE:
        down = False
    if key == glfw.KEY_UP and action == glfw.PRESS:
        forwardCube = True
    elif key == glfw.KEY_UP and action == glfw.RELEASE:
        forwardCube = False
    if key == glfw.KEY_DOWN and action == glfw.PRESS:
        backwardCube = True
    elif key == glfw.KEY_DOWN and action == glfw.RELEASE:
        backwardCube = False
    if key == glfw.KEY_LEFT and action == glfw.PRESS:
        leftCube = True
    elif key == glfw.KEY_LEFT and action == glfw.RELEASE:
        leftCube = False
    if key == glfw.KEY_RIGHT and action == glfw.PRESS:
        rightCube = True
    elif key == glfw.KEY_RIGHT and action == glfw.RELEASE:
        rightCube = False
    if key == glfw.KEY_PAGE_UP and action == glfw.PRESS:
        upwardCube = True
    elif key == glfw.KEY_PAGE_UP and action == glfw.RELEASE:
        upwardCube = False
    if key == glfw.KEY_PAGE_DOWN and action == glfw.PRESS:
        downwardCube = True
    elif key == glfw.KEY_PAGE_DOWN and action == glfw.RELEASE:
        downwardCube = False
    
def cubeMovement():
    if leftCube:
        cubeCam.process_keyboard("LEFT", 0.005)
    if rightCube:
        cubeCam.process_keyboard("RIGHT", 0.005)
    if forwardCube:
        cubeCam.process_keyboard("FORWARD", 0.005)
    if backwardCube:
        cubeCam.process_keyboard("BACKWARD", 0.005)
    if  upwardCube:
        cubeCam.process_keyboard("UP", 0.005)
    if downwardCube:
        cubeCam.process_keyboard("DOWN", 0.005)
    return cubeCam.get_view_matrix()

def do_movement():
    if left:
        cam.process_keyboard("LEFT", 0.005)
    if right:
        cam.process_keyboard("RIGHT", 0.005)
    if forward:
        cam.process_keyboard("FORWARD", 0.005)
    if backward:
        cam.process_keyboard("BACKWARD", 0.005)
    if up:
        cam.process_keyboard("UP", 0.005)
    if down:
        cam.process_keyboard("DOWN", 0.005)
    if leftCube:
        cubeCam.process_keyboard("LEFT", 0.005)
    if rightCube:
        cubeCam.process_keyboard("RIGHT", 0.005)
    if forwardCube:
        cubeCam.process_keyboard("FORWARD", 0.005)
    if backwardCube:
        cubeCam.process_keyboard("BACKWARD", 0.005)

def mouse_look_clb(window, xpos, ypos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)
    cubeCam.process_mouse_movement(xoffset, yoffset)

def openMenu():
    global menu
    if menu:
        menu = False
    else:
        menu = True

# A small tolerance for comparing floats for equality
TOL = 1.e-5
# psi = 1/phi where phi is the Golden ratio, sqrt(5)+1)/2
psi = (math.sqrt(5) - 1) / 2
# psi**2 = 1 - psi
psi2 = 1 - psi


def main():
    #create parameters for penrose tiling
    scale = 100
    config={'tile-opacity': 0.9, 'stroke-colour': '#800',
            'Stile-colour': '#f00', 'Ltile-colour': '#ff0'}
    tiling = PenroseP3(scale*1.5, ngen=5, config=config)

    theta = math.pi / 5
    rot = math.cos(theta) + 1j*math.sin(theta)
    A1 = scale + 0.j
    B = 0 + 0j
    C1 = C2 = A1 * rot
    A2 = A3 = C1 * rot
    C3 = C4 = A3 * rot
    A4 = A5 = C4 * rot
    C5 = -A1
    tiling.set_initial_tiles([BtileS(A1, B, C1), BtileS(A2, B, C2),
                            BtileS(A3, B, C3), BtileS(A4, B, C4),
                            BtileS(A5, B, C5)])
    tiling.make_tiling()
    


    if not glfw.init():
        return


    window = glfw.create_window(width, height, "Penrose", None, None)

    if not window:
        glfw.terminate()
        return

    # set the position callback
    glfw.set_cursor_pos_callback(window, mouse_look_clb)
    # set the keyboard input callback
    glfw.set_key_callback(window, key_input_clb)
    # capture the mouse cursor
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    # make the context current
    glfw.make_context_current(window)

    #configure opengl
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    


    verticesl = []
    verticess = []
    points = []

    #append vertices to lists
    for element in tiling.elements:
        APoint = (element.A.real/100, element.A.imag/100, 0)
        BPoint = (element.B.real/100, element.B.imag/100, 0)
        CPoint = (element.C.real/100, element.C.imag/100, 0)
        h = abs(element.A.real/100 - element.B.real/100) * 2
        points.append(APoint)
        points.append(BPoint)
        points.append(CPoint)
        if isinstance(element, BtileL):
            #base triangle
            verticesl.append(element.A.real/100)
            verticesl.append(element.A.imag/100)
            verticesl.append(-h)
            verticesl.append(element.B.real/100)
            verticesl.append(element.B.imag/100)
            verticesl.append(-h)
            verticesl.append(element.C.real/100)
            verticesl.append(element.C.imag/100)
            verticesl.append(-h)

            #roof triangle
            verticesl.append(element.A.real/100)
            verticesl.append(element.A.imag/100)
            verticesl.append(0)
            verticesl.append(element.B.real/100)
            verticesl.append(element.B.imag/100)
            verticesl.append(0)
            verticesl.append(element.C.real/100)
            verticesl.append(element.C.imag/100)
            verticesl.append(0)
            
            #wall 1-1
            verticesl.append(element.A.real/100)
            verticesl.append(element.A.imag/100)
            verticesl.append(-h)
            verticesl.append(element.B.real/100)
            verticesl.append(element.B.imag/100)
            verticesl.append(-h)
            verticesl.append(element.B.real/100)
            verticesl.append(element.B.imag/100)
            verticesl.append(0)

            #wall 1-2
            verticesl.append(element.A.real/100)
            verticesl.append(element.A.imag/100)
            verticesl.append(0)
            verticesl.append(element.B.real/100)
            verticesl.append(element.B.imag/100)
            verticesl.append(-h)
            verticesl.append(element.B.real/100)
            verticesl.append(element.B.imag/100)
            verticesl.append(-h)

            #wall 2-1
            verticesl.append(element.A.real/100)
            verticesl.append(element.A.imag/100)
            verticesl.append(-h)
            verticesl.append(element.C.real/100)
            verticesl.append(element.C.imag/100)
            verticesl.append(-h)
            verticesl.append(element.C.real/100)
            verticesl.append(element.C.imag/100)
            verticesl.append(0)

            #wall 2-2
            verticesl.append(element.A.real/100)
            verticesl.append(element.A.imag/100)
            verticesl.append(0)
            verticesl.append(element.C.real/100)
            verticesl.append(element.C.imag/100)
            verticesl.append(0)
            verticesl.append(element.C.real/100)
            verticesl.append(element.C.imag/100)
            verticesl.append(-h)

            #wall 3-1
            verticesl.append(element.C.real/100)
            verticesl.append(element.C.imag/100)
            verticesl.append(-h)
            verticesl.append(element.B.real/100)
            verticesl.append(element.B.imag/100)
            verticesl.append(-h)
            verticesl.append(element.C.real/100)
            verticesl.append(element.C.imag/100)
            verticesl.append(0)

            #wall 3-2
            verticesl.append(element.C.real/100)
            verticesl.append(element.C.imag/100)
            verticesl.append(0)
            verticesl.append(element.B.real/100)
            verticesl.append(element.B.imag/100)
            verticesl.append(0)
            verticesl.append(element.C.real/100)
            verticesl.append(element.C.imag/100)
            verticesl.append(-h)

        else:
            #base triangle
            verticess.append(element.A.real/100)
            verticess.append(element.A.imag/100)
            verticess.append(0)
            verticess.append(element.B.real/100)
            verticess.append(element.B.imag/100)
            verticess.append(0)
            verticess.append(element.C.real/100)
            verticess.append(element.C.imag/100)
            verticess.append(0)

            #roof triangle
            verticess.append(element.A.real/100)
            verticess.append(element.A.imag/100)
            verticess.append(h)
            verticess.append(element.B.real/100)
            verticess.append(element.B.imag/100)
            verticess.append(h)
            verticess.append(element.C.real/100)
            verticess.append(element.C.imag/100)
            verticess.append(h)
            
            #wall 1-1
            verticess.append(element.A.real/100)
            verticess.append(element.A.imag/100)
            verticess.append(0)
            verticess.append(element.B.real/100)
            verticess.append(element.B.imag/100)
            verticess.append(0)
            verticess.append(element.B.real/100)
            verticess.append(element.B.imag/100)
            verticess.append(h)

            #wall 1-2
            verticess.append(element.A.real/100)
            verticess.append(element.A.imag/100)
            verticess.append(h)
            verticess.append(element.B.real/100)
            verticess.append(element.B.imag/100)
            verticess.append(h)
            verticess.append(element.B.real/100)
            verticess.append(element.B.imag/100)
            verticess.append(0)

            #wall 2-1
            verticess.append(element.A.real/100)
            verticess.append(element.A.imag/100)
            verticess.append(0)
            verticess.append(element.C.real/100)
            verticess.append(element.C.imag/100)
            verticess.append(0)
            verticess.append(element.C.real/100)
            verticess.append(element.C.imag/100)
            verticess.append(h)

            #wall 2-2
            verticess.append(element.A.real/100)
            verticess.append(element.A.imag/100)
            verticess.append(h)
            verticess.append(element.C.real/100)
            verticess.append(element.C.imag/100)
            verticess.append(h)
            verticess.append(element.C.real/100)
            verticess.append(element.C.imag/100)
            verticess.append(0)

            #wall 3-1
            verticess.append(element.C.real/100)
            verticess.append(element.C.imag/100)
            verticess.append(0)
            verticess.append(element.B.real/100)
            verticess.append(element.B.imag/100)
            verticess.append(0)
            verticess.append(element.C.real/100)
            verticess.append(element.C.imag/100)
            verticess.append(h)

            #wall 3-2
            verticess.append(element.C.real/100)
            verticess.append(element.C.imag/100)
            verticess.append(h)
            verticess.append(element.B.real/100)
            verticess.append(element.B.imag/100)
            verticess.append(h)
            verticess.append(element.C.real/100)
            verticess.append(element.C.imag/100)
            verticess.append(0)
    
    verticesL = np.array(verticesl, dtype= np.float32)
    verticesS = np.array(verticess, dtype= np.float32)
    
    
    PENROSE_VERTEX_SHADER = open(os.path.join("shaders/penrose.vert"), 'r').read()
    PENROSE_FRAGMENT_SHADER = open(os.path.join("shaders/penrose.frag"), 'r').read()
    CUBE_VERTEX_SHADER = open(os.path.join("shaders/cube.vert"), 'r').read()
    CUBE_FRAGMENT_SHADER = open(os.path.join("shaders/cube.frag"), 'r').read()
    LIGHT_CUBE_VERTEX_SHADER = open(os.path.join("shaders/light_cube.vert"), 'r').read()
    LIGHT_CUBE_FRAGMENT_SHADER = open(os.path.join("shaders/light_cube.frag"), 'r').read()
    MENU_VERTEX_SHADER = open(os.path.join("shaders/overlay.vert"), 'r').read()
    MENU_FRAGMENT_SHADER = open(os.path.join("shaders/overlay.frag"), 'r').read()
    LIGHT_VERTEX_SHADER = open(os.path.join("shaders/multiple_lights.vert"), 'r').read()
    LIGHT_FRAGMENT_SHADER = open(os.path.join("shaders/multiple_lightsTransparency.frag"), 'r').read()
    # Compile The Program and shaders

    penrose_shader =  OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(PENROSE_VERTEX_SHADER,GL_VERTEX_SHADER),
                                             OpenGL.GL.shaders.compileShader(PENROSE_FRAGMENT_SHADER, GL_FRAGMENT_SHADER), validate=False)
    cube_shader =  OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(CUBE_VERTEX_SHADER,GL_VERTEX_SHADER),
                                             OpenGL.GL.shaders.compileShader(CUBE_FRAGMENT_SHADER, GL_FRAGMENT_SHADER), validate=False)
    light_cube_shader =  OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(LIGHT_CUBE_VERTEX_SHADER,GL_VERTEX_SHADER),
                                             OpenGL.GL.shaders.compileShader(LIGHT_CUBE_FRAGMENT_SHADER, GL_FRAGMENT_SHADER), validate=False)
    menu_shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(MENU_VERTEX_SHADER,GL_VERTEX_SHADER),
                                             OpenGL.GL.shaders.compileShader(MENU_FRAGMENT_SHADER, GL_FRAGMENT_SHADER), validate=False)
    lighting_shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(LIGHT_VERTEX_SHADER,GL_VERTEX_SHADER),
                                             OpenGL.GL.shaders.compileShader(LIGHT_FRAGMENT_SHADER, GL_FRAGMENT_SHADER), validate=False)
    #Configure penrose shaders

    #Create Buffers in gpu
    VBOS = glGenBuffers(1)
    VAOS = glGenVertexArrays(1)
    
    VBOL = glGenBuffers(1)
    VAOL = glGenVertexArrays(1)
    
    #Triangulos BtileS
    glBindVertexArray(VAOS)
    glBindBuffer(GL_ARRAY_BUFFER, VBOS)
    glBufferData(GL_ARRAY_BUFFER, verticesS.nbytes, verticesS, GL_STATIC_DRAW)
    
    
    position = glGetAttribLocation(penrose_shader, "position")
    glEnableVertexAttribArray(position)
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
    
    #Triangulos BtileL
    glBindVertexArray(VAOL)
    glBindBuffer(GL_ARRAY_BUFFER, VBOL)
    glBufferData(GL_ARRAY_BUFFER, verticesL.nbytes, verticesL, GL_STATIC_DRAW)
    
    position = glGetAttribLocation(penrose_shader, "position")
    glEnableVertexAttribArray(position)
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)

    #lightcube
    glUseProgram(cube_shader)
    
    vertices = [-0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
                0.5, -0.5,  0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
                0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
                -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

                -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
                0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
                0.5,  0.5, -0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
                -0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

                0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
                0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
                0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
                0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

                -0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
                -0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
                -0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
                -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

                -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
                0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
                0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
                -0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

                0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
                -0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
                -0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
                0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0]

    indices = [0,  1,  2,  2,  3,  0,
            4,  5,  6,  6,  7,  4,
            8,  9, 10, 10, 11,  8,
            12, 13, 14, 14, 15, 12,
            16, 17, 18, 18, 19, 16,
            20, 21, 22, 22, 23, 20]
    
    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)

    VAOCube = glGenVertexArrays(1)
    VBOCube = glGenBuffers(1)
    glBindVertexArray(VAOCube)
    glBindBuffer(GL_ARRAY_BUFFER, VBOCube)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    

    # Element Buffer Object
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(12))

    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(24))

    textures = glGenTextures(3)
    glBindTexture(GL_TEXTURE_2D, textures[0])

    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # load image
    image = Image.open("textures/container2.png")
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    # img_data = np.array(image.getdata(), np.uint8) # second way of getting the raw image data
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    
    glClearColor(0.1, 0.1, 0.1, 1)
    #glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    rotation_loc = glGetUniformLocation(cube_shader, "rotation")
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, .1, 500)

    #cube
    vertices2 = [-0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
                0.5, -0.5,  0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
                0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
                -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

                -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
                0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
                0.5,  0.5, -0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
                -0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

                0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
                0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
                0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
                0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

                -0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
                -0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
                -0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
                -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

                -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
                0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
                0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
                -0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

                0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
                -0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
                -0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
                0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0]

    indices2 = [0,  1,  2,  2,  3,  0,
            4,  5,  6,  6,  7,  4,
            8,  9, 10, 10, 11,  8,
            12, 13, 14, 14, 15, 12,
            16, 17, 18, 18, 19, 16,
            20, 21, 22, 22, 23, 20]
    
    vertices2 = np.array(vertices, dtype=np.float32)
    indices2 = np.array(indices, dtype=np.uint32)

    VAOCube2 = glGenVertexArrays(1)
    VBOCube2 = glGenBuffers(1)
    glBindVertexArray(VAOCube2)
    glBindBuffer(GL_ARRAY_BUFFER, VBOCube2)
    glBufferData(GL_ARRAY_BUFFER, vertices2.nbytes, vertices2, GL_STATIC_DRAW)
    

    # Element Buffer Object
    EBO2 = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO2)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices2.nbytes, indices2, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices2.itemsize * 8, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vertices2.itemsize * 8, ctypes.c_void_p(12))

    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, vertices2.itemsize * 8, ctypes.c_void_p(24))

    glBindTexture(GL_TEXTURE_2D, textures[1])

    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # load image
    image = Image.open("textures/container2_specular.png")
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    # img_data = np.array(image.getdata(), np.uint8) # second way of getting the raw image data
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    
    glClearColor(0.1, 0.1, 0.1, 1)
    #glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    rotation_loc = glGetUniformLocation(cube_shader, "rotation")
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, .1, 500)

    #menu
    glUseProgram(menu_shader)
    toggleRectangle = [ -1.0, -1.0, 0.0,    0.0, 0.0,
                        -1.0, -0.6, 0,0,    0.0, 1.0,
                        -0.3, -0.6, 0,0,    1.0, 1.0,
                        -0.3, -1.0, 0,0,    1.0, 0.0
    ] 
    toggleIndices = [
        0,1,2,
        2,3,0
    ]
    
    toggleVertices = np.array(toggleRectangle, dtype=np.float32)
    toggleIndices = np.array(toggleIndices, dtype=np.float32)

    VAOMenuToggle = glGenVertexArrays(1)
    VBOMenuToggle = glGenBuffers(1)

    glBindVertexArray(VAOMenuToggle)
    glBindBuffer(GL_ARRAY_BUFFER, VBOMenuToggle)
    glBufferData(GL_ARRAY_BUFFER, toggleVertices.nbytes, toggleVertices, GL_STATIC_DRAW)

    EBOMenu = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBOMenu)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, toggleIndices.nbytes, toggleIndices, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, toggleVertices.itemsize * 5, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, toggleVertices.itemsize * 5, ctypes.c_void_p(8))

    glBindTexture(GL_TEXTURE_2D, textures[2])

    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # load image
    imageToggle = Image.open("textures/white.png")
    imageToggle = imageToggle.transpose(Image.FLIP_TOP_BOTTOM)
    img_dataToggle = imageToggle.convert("RGBA").tobytes()
    # img_data = np.array(image.getdata(), np.uint8) # second way of getting the raw image data
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, imageToggle.width, imageToggle.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_dataToggle)
    

    #render loop
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        
        #get current run time in seconds for current loop
        currentTime = glfw.get_time()
        time = currentTime % 30

        do_movement()
        view = cam.get_view_matrix()
        
        #config lights
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [.1,.1,.1,1])
        #render cube
        glUseProgram(light_cube_shader)
        glBindVertexArray(VAOCube)
        rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())

        cubeView = glGetUniformLocation(light_cube_shader, "view");
        cubeProjection = glGetUniformLocation(light_cube_shader, "projection");
        cubeModel = glGetUniformLocation(light_cube_shader, "model");
        cubeRot = glGetUniformLocation(light_cube_shader, "rotation");
        cubeT = cubeMovement()
        cubePos = pyrr.matrix44.create_from_translation(Vector3([-1,-1,1]))
        glUniformMatrix4fv(cubeModel, 1, GL_FALSE, pyrr.matrix44.multiply(cubeT, cubePos))
        glUniformMatrix4fv(cubeProjection, 1, GL_FALSE, projection)
        glUniformMatrix4fv(cubeView, 1, GL_FALSE, view)
        glUniformMatrix4fv(cubeRot, 1, GL_FALSE, pyrr.matrix44.multiply(rot_x, rot_y))

        glDrawElements(GL_TRIANGLES, len(vertices) * 3, GL_UNSIGNED_INT, None)

        glUseProgram(cube_shader)

        #configure lights
        ambientL = glGetAttribLocation(cube_shader, "lAmbient")
        diffuseL = glGetAttribLocation(cube_shader, "lDiffuse")
        specularL = glGetAttribLocation(cube_shader, "lSpecular")

        materialS = glGetAttribLocation(cube_shader, "mShininess")

        glUniform3fv(ambientL, 1, (.3, .3, .3))
        glUniform3fv(diffuseL, 1, (.5, .5, .5))
        glUniform3fv(specularL, 1, (1, 1, 1))
        glUniform1f(materialS, 64)


        glUniformMatrix4fv(cubeModel, 1, GL_FALSE, pyrr.matrix44.multiply(view, cubePos))

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, textures[0])
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, textures[1])

        glBindVertexArray(VAOCube2)
        
        rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())

        cubeView = glGetUniformLocation(cube_shader, "view");
        cubeProjection = glGetUniformLocation(cube_shader, "projection");
        cubeModel = glGetUniformLocation(cube_shader, "model");
        cubeT = cubeMovement()
        cubePos = pyrr.matrix44.create_from_translation(Vector3([0,0,0]))
        glUniformMatrix4fv(cubeModel, 1, GL_FALSE, cubePos)
        glUniformMatrix4fv(cubeProjection, 1, GL_FALSE, projection)
        glUniformMatrix4fv(cubeView, 1, GL_FALSE, view)
        glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, pyrr.matrix44.multiply(rot_x, rot_y))

        glDrawElements(GL_TRIANGLES, len(vertices) * 3, GL_UNSIGNED_INT, None)
        #render penrose
        glUseProgram(penrose_shader)

        #create scaling matrixes
        #if(currentTime < 10):
            #scale = pyrr.Matrix44.from_scale(Vector3([currentTime/10, currentTime/10, currentTime/10]))
        scale = pyrr.Matrix44.from_scale(Vector3([1, 1, 1]))
        #create rotation matrixes
        rotZ1 = pyrr.Matrix44.from_z_rotation(currentTime/2)
        rotZ2 = pyrr.Matrix44.from_z_rotation(-1 * currentTime/2)
               
        #draw filled triangles
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        #bind uniform pointers
        uniformView = glGetUniformLocation(penrose_shader, "view");
        uniformTime = glGetUniformLocation(penrose_shader, "time");
        uniformRotation = glGetUniformLocation(penrose_shader, "rotation");
        uniform = glGetUniformLocation(penrose_shader, "triangleColor");
        uniformScale = glGetUniformLocation(penrose_shader, "scaling");
        uniformProjection = glGetUniformLocation(penrose_shader, "projection");

        glUniformMatrix4fv(uniformProjection, 1, GL_FALSE, projection)

        #BtileL
        glBindVertexArray(VAOL)
        glUniformMatrix4fv(uniformView, 1, GL_FALSE, view)
        glUniformMatrix4fv(uniformRotation, 1, GL_FALSE, rotZ2)
        glUniformMatrix4fv(uniformScale, 1, GL_FALSE, scale)
        glUniform3fv(uniform, 1, (0, 0, 1))
        glDrawArrays(GL_TRIANGLES, 0, len(verticesL))

        glUniform3fv(uniform, 1, (0.0, 0.0, 0.0))
        
        #BtileS
        glBindVertexArray(VAOS)
        glUniformMatrix4fv(uniformRotation, 1, GL_FALSE, rotZ1)
        glUniform1f(uniformTime, time)
        
        glUniform3fv(uniform, 1, (1, 0, 0))
        glDrawArrays(GL_TRIANGLES, 0, len(verticesS))
                
        glUniform3fv(uniform, 1, (0.0, 0.0, 0.0))


        
        

        #render menu
        glUseProgram(menu_shader)
        glBindVertexArray(VAOMenuToggle)
        #glDisable(GL_BLEND);
        glBindTexture(GL_TEXTURE_2D, textures[2])
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        
        #glEnable(GL_BLEND)

        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()