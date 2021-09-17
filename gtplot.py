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
from camera import Camera
from Coordinates import Euler

# globals
play = True
time_interval = 0.01
r, g, b, a = (0.0, 0.0, 0.0, 1.0)
blender = r"C:/PycharmProjects/stl/h01blenderCache/"
simple_ware = r"C:/PycharmProjects/stl/h01simplewareCache/"
sei_ka = r"C:/PycharmProjects/stl/h01seikaCache/"
projection = pyrr.matrix44.create_perspective_projection(45, 1.0, 0.001, 1000)
view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 30]), pyrr.Vector3([0, 0, -1]), pyrr.Vector3([0, 1, 0]))
model = pyrr.matrix44.create_from_z_rotation(0.0)

modelb = model


def load(directory: str):
    vao = {i: glGenVertexArrays(1) for i in range(100)}
    buffer = np.load(directory+"/"+"data.npy")
    for i in vao.keys():
        print(i)
        glBindVertexArray(vao[i])
        
        vertices = buffer[i]
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    return vao

# init window
def mainloop():
    global r, g, b, a, projection, view, model, modelb, play, time_interval, vertices, indices
    camera = Camera()
    if not glfw.init():
        raise Exception("GLFW Initialization Failed!")
    window = glfw.create_window(800, 800, "Main", None, None)
    glfw.set_window_pos(window, 200, 200)

    def mouse_button_clb(window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            camera.mouse_left = True
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE:
            camera.mouse_left = False
    def mouse_position_clb(window, x_pos, y_pos):
        global view
        x_pos -= 400
        y_pos *= -1
        y_pos += 400
        if camera.mouse_left == False:
            camera.mouse_pos = pyrr.Vector3([x_pos, y_pos, 0.0])
        else:
            dx = camera.mouse_pos.x - x_pos
            dy = camera.mouse_pos.y - y_pos
            camera.mouse_pos = pyrr.Vector3([x_pos, y_pos, 0.0])
            delta = pyrr.Vector3([dx, dy, np.sqrt(dx**2+dy**2)/100])
            view = camera(delta)
    def mouse_scroll_clb(window, x_offset, y_offset):
        global view
        def smooth():
            global view
            if sum([abs(item) for item in camera.position.xyz]) <= 1.01:
                if y_offset >= 0:
                    return
            for i in range(5):
                camera.position += camera.front*y_offset*0.2
                camera.position = pyrr.Vector4([*camera.position.xyz, 1.0])
                view = camera()
                time.sleep(0.005)
                if abs(sum([*camera.position.xyz])) <= 1.01:
                    if y_offset >= 0:
                        return

        t = Thread(target=smooth)
        t.start()

    glfw.set_mouse_button_callback(window, mouse_button_clb)
    glfw.set_cursor_pos_callback(window, mouse_position_clb)
    glfw.set_scroll_callback(window, mouse_scroll_clb)

    glfw.make_context_current(window)
    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                            compileShader(fragment_src, GL_FRAGMENT_SHADER))
    glUseProgram(shader)

    vao = load(r"./")
    euler = Euler()

    proj_loc = glGetUniformLocation(shader, "projection")
    view_loc = glGetUniformLocation(shader, "view")
    model_loc = glGetUniformLocation(shader, "model")
    color_loc = glGetUniformLocation(shader, "color")

    glUniform4fv(color_loc, 1, pyrr.Vector4([0.7, 0.7, 0.2, 0.5]))

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    play_list = [i for i in range(100)] + [99-i for i in range(100)]
    i=0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(r, g, b, a)
        glPointSize(3)
        glUniform4fv(color_loc, 1, pyrr.Vector4([0.2, 0.2, 0.6, 0.7]))
        glBindVertexArray(vao[play_list[i]])
        glDrawArrays(GL_POINTS, 0, 640000)
        glBindVertexArray(0)

        # glBindVertexArray(euler.vao)
        # glDrawElements(GL_TRIANGLES, 9, GL_UNSIGNED_INT, None)
        # glBindVertexArray(0)

        if play:
            i += 1
            i = i % 200
            time.sleep(time_interval)
        glfw.swap_buffers(window)
    glfw.terminate()


class Console:
    def __init__(self):
        print("This is a Interactive Python Console.")
        print("\n")
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
                sentence = input("In[{}]:".format(self.times)+"    "*tab)
            else:
                sentence = input("."*len("In[{}]:".format(self.times))+"    "*tab)
            raw_code.append("   "*tab+sentence+"\n")
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
                assert name_1[-1] != "+"
                assert name_1[-1] != "-"
                assert name_1[-1] != "*"
                assert name_1[-1] != "/"
                assert name_1[-1] != "!"
                assert name_1[-1] != "="

                if name_1 != row.split("=")[0]:  # multiple "=" in sentence
                    name_1 = row.split("=")[0]
                self.code = "global {}\n".format(name_1) + self.code
            except IndexError:
                pass
            except AssertionError:
                pass

    def __call__(self):
        while True:
            self.fetch_input()
            if self.code == """\n""":
                print(self.code)
                self.times -= 1
            self.run_in_global()
            if self.code == """quit\n\n""" or self.code == """exit\n\n""":
                break
            try:
                ans = eval(self.code)
                if ans is not None:
                    print("Out[{}]:".format(self.times)+str(ans)+"\n")
            except:
                try:
                    exec(self.code)
                except:
                    traceback.print_exc()
            self.code = """"""
            self.times += 1


if __name__ == '__main__':
    t1 = Thread(target=mainloop)
    t1.start()

    console = Console()
    t2 = Thread(target=console)
    t2.start()

