import numpy as np
from OpenGL.GL import *
import os


def load(directory: str):
    opt_list = os.listdir(directory)
    vao = {i: glGenVertexArrays(1) for i in range(len(opt_list))}
    for i in vao.keys():
        glBindVertexArray(vao[i])
        buffer = np.load(directory+"/"+"{}.npz".format(i))
        vertices = buffer["vertices"]
        indices = buffer["indices"]
        vbo, ebo = glGenBuffers(2)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    return vao
