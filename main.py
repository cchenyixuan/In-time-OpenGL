import ctypes
import os
import numpy as np
import pyrr
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from threading import Thread
from shader_src import vertex_src, fragment_src
import time
import traceback
import re

# globals
play = True
time_interval = 0.01
r, g, b, a = (0.0, 0.0, 0.0, 1.0)
blender = r"C:/PycharmProjects/stl/h01blenderCache/"
simple_ware = r"C:/PycharmProjects/stl/h01simplewareCache/"
sei_ka = r"C:/PycharmProjects/stl/h01seikaCache/"
projection = pyrr.matrix44.create_perspective_projection(45, 1.0, 0.001, 1000)
view = pyrr.matrix44.create_look_at(pyrr.Vector3([20, 0, 3]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))
model = pyrr.matrix44.create_from_translation(pyrr.Vector3([-36, 19, -468.7]))

modelb = model
def load(directory: str):
    opt_list = os.listdir(directory)
    vao = {i: [glGenVertexArrays(1)] for i in range(len(opt_list))}
    for i in vao.keys():
        glBindVertexArray(vao[i][0])
        buffer = np.load(directory+"/"+"{}.npz".format(i))
        vertices = buffer["vertices"]
        indices = buffer["indices"]
        vao[i].append(len(indices)*3)
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

# init window
def mainloop():
    global r, g, b, a, projection, view, model, modelb, play, time_interval
    if not glfw.init():
        raise Exception("GLFW Initialization Failed!")
    window = glfw.create_window(800, 800, "Main", None, None)
    glfw.set_window_pos(window, 200, 200)
    glfw.make_context_current(window)
    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                            compileShader(fragment_src, GL_FRAGMENT_SHADER))
    glUseProgram(shader)

    vao = load(r"C:\PycharmProjects\stl\h01seikaCache")
    vaob = load(r"C:\PycharmProjects\stl\h01blenderCache")
    vaoc = load(r"C:\PycharmProjects\stl\h01simplewareCache")

    proj_loc = glGetUniformLocation(shader, "projection")
    view_loc = glGetUniformLocation(shader, "view")
    model_loc = glGetUniformLocation(shader, "model")
    color_loc = glGetUniformLocation(shader, "color")

    glUniform4fv(color_loc, 1, pyrr.Vector4([0.7, 0.7, 0.2, 0.5]))

    glEnable(GL_DEPTH_TEST)


    i=0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(r, g, b, a)

        glUniform4fv(color_loc, 1, pyrr.Vector4([0.2, 0.2, 0.2, 0.7]))
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glBindVertexArray(vao[i][0])
        glDrawElements(GL_TRIANGLES, vao[i][1], GL_UNSIGNED_INT, None)

        glUniform4fv(color_loc, 1, pyrr.Vector4([0.7, 0.7, 0.7, 1.0]))
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBindVertexArray(vaob[int(i/100*90)][0])
        glDrawElements(GL_TRIANGLES, vaob[int(i/100*90)][1], GL_UNSIGNED_INT, None)

        glUniform4fv(color_loc, 1, pyrr.Vector4([0.9, 0.2, 0.5, 1.0]))
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBindVertexArray(vaoc[int(i / 100 * 15)][0])
        glDrawElements(GL_TRIANGLES, vaoc[int(i / 100 * 15)][1], GL_UNSIGNED_INT, None)
        if play:
            i += 1
            i = i%100
            time.sleep(time_interval)
        glfw.swap_buffers(window)
    glfw.terminate()


class Console:
    def __init__(self):

        self.code = """"""
        self.times = 1
        pass

    def fetch_input(self):
        raw_code = []
        tab = 0
        line = 0
        while True:
            line += 1
            if line == 1:
                sentence = input("In[{}]:".format(self.times) + "    " * tab)
            else:
                sentence = input("." * len("In[{}]:".format(self.times)) + "    " * tab)
            raw_code.append("   " * tab + sentence + "\n")
            if sentence == "":
                tab -= 1
            if tab < 0:
                break
            # check tab
            try:
                if sentence[-1] == ":":
                    tab += 1
            except IndexError:
                pass
            try:
                if sentence[:6] == "return":
                    tab -= 1
            except IndexError:
                pass
            try:
                if sentence[:5] == "break":
                    tab -= 1
            except IndexError:
                pass
            try:
                if sentence[:8] == "continue":
                    tab -= 1
            except IndexError:
                pass
            try:
                if sentence[:4] == "pass":
                    tab -= 1
            except IndexError:
                pass
        for item in raw_code:
            self.code += item

    def run_in_global(self):
        find_equal = re.compile(r"(.*)=(.*)", re.S)
        code = self.code.split("\n")
        for row in code:
            try:
                name_1, name_2 = re.findall(find_equal, row)[0]
                self.code = "global {}\n".format(name_1) + self.code
            except IndexError:
                pass

    def __call__(self):
        while True:
            self.fetch_input()
            print(self.code)
            self.run_in_global()
            if self.code == """quit\n\n""" or self.code == """exit\n\n""":
                break
            try:
                ans = eval(self.code)
                if ans is not None:
                    print(ans)
            except:
                try:
                    exec(self.code)
                except:
                    traceback.print_exc()
            self.code = """"""
            self.times += 1


if __name__ == '__main__':
    t1 = Thread(target=mainloop, name="MainLoop")
    t1.start()
    console = Console()
    t2 = Thread(target=console)
    t2.start()


