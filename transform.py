# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/b3d_lib_int


import math
from mathutils import Matrix, Vector


class Transform:

    @staticmethod
    def rotate_object_local(obj, axis, angle, angle_unit='radians'):
        # rotate object around axis on angle
        if axis in ('X', 'Y', 'Z') and angle_unit in ('radians', 'degrees'):
            if angle_unit == 'degrees':
                angle = math.radians(angle)
            obj.rotation_euler = (obj.rotation_euler.to_matrix() @ Matrix.Rotation(angle, 3, axis)).to_euler()

    @staticmethod
    def bounding_box_center_local(obj):
        # returns bounding box center in object local coordinates
        return sum((Vector(b) for b in obj.bound_box), Vector((0.0, 0.0, 0.0))) / 8
