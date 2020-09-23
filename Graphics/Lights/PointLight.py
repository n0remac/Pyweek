import arcade
from Graphics.Lights.Light import Light


class PointLight(Light):

    light_shader = None

    def load_shader(context):
        PointLight.light_shader = context.load_program(
            vertex_shader="Graphics/Lights/point_light.vs",
            geometry_shader="Graphics/Lights/point_light.gs",
            fragment_shader="Graphics/Lights/point_light.fs",
        )

    def __init__(self, renderer, position, color, radius):
        super(PointLight, self).__init__(renderer, position, color, radius)

    # return true if appended
    def append_to_buffer(self, window_args, buffer):
        buffer.extend(self.position)
        buffer.extend(self.color)
        buffer.append(self.radius)

#jank but probably performant for bullets
class DynamicPointLight():
    def __init__(self, color, radius):
        self.color = color
        self.radius = radius
