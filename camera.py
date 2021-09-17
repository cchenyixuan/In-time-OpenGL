import pyrr
import numpy as np


class Camera:
    def __init__(self):
        self.position = pyrr.Vector4([0.0, 0.0, 30.0, 1.0])
        self.front = pyrr.Vector4([0.0, 0.0, -1.0, 1.0])
        self.up = pyrr.Vector4([0.0, 1.0, 0.0, 1.0])

        self.projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1.0, 0.001, 1000)
        self.view = pyrr.matrix44.create_look_at(self.position.xyz, self.front.xyz, self.up.xyz)
        self.translate = pyrr.matrix44.create_identity()
        self.rotate = pyrr.matrix44.create_identity()
        self.scale = pyrr.matrix44.create_identity()

        self.mouse_left = False
        self.mouse_pos = pyrr.Vector3([0.0, 0.0, 0.0])

    def __call__(self, delta: pyrr.Vector3 = pyrr.Vector3([0.0, 0.0, 0.0])):
        if abs(self.mouse_pos.x) >= 300 or abs(self.mouse_pos.y) >= 300:
            rotation_matrix = pyrr.matrix44.create_from_axis_rotation(-np.sign((pyrr.vector3.cross(pyrr.Vector3([self.mouse_pos.x + delta.x, self.mouse_pos.y + delta.y, 0.0]),
                                                                                          pyrr.Vector3([self.mouse_pos.x, self.mouse_pos.y, 0.0])))[2])*self.front.xyz, delta.z)
            self.up = rotation_matrix @ self.up
        else:
            rotation_matrix = pyrr.matrix44.create_from_axis_rotation(self.up.xyz, -delta.x/100) @ \
                              pyrr.matrix44.create_from_axis_rotation(pyrr.vector3.cross(self.front.xyz, self.up.xyz), delta.y/100)
            self.position = rotation_matrix @ self.position
            self.front = rotation_matrix @ self.front
            self.up = rotation_matrix @ self.up

        return pyrr.matrix44.create_look_at(self.position.xyz, self.front.xyz, self.up.xyz)

