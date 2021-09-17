import numpy as np
from OpenGL.GL import *


class Euler:
    def __init__(self):
        self.scale = 1.0
        vertices = np.array([0.0, 0.0, -0.1, 7.8, 0.0, 0.0,
                             8.0, 0.0, 0.0, 7.8, 0.0, 0.0,
                             0.0, 0.0, 0.1, 7.8, 0.0, 0.0,

                             -0.1, 0.0, 0.0, 7.8, 0.0, 0.0,
                             0.0, 8.0, 0.0, 7.8, 0.0, 0.0,
                             0.1, 0.0, 0.0, 7.8, 0.0, 0.0,

                             0.0, -0.1, 0.0, 7.8, 0.0, 0.0,
                             0.0, 0.0, 8.0, 7.8, 0.0, 0.0,
                             0.0, 0.1, 0.0, 7.8, 0.0, 0.0,
                             ], dtype=np.float32)
        indices = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8], dtype=np.uint32)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        vbo, ebo = glGenBuffers(2)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
