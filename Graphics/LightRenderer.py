import arcade
from array import array
from Graphics.RenderTarget import RenderTarget

from Graphics.Lights.Light import Light
from Graphics.Lights.PointLight import PointLight


class LightRenderer:
    __instance = None

    def __init__(self, context, size):
        if LightRenderer.__instance is not None:
            raise Exception()  # Can only be one to make apis easy

        LightRenderer.__instance = self
        self.context = context
        self.ambient_light = (1.0, 1.0, 1.0)

        # light lists
        self.point_lights = []
        self.dynamic_point_light_buffer = []

        # HDR target
        self.light_buffer = RenderTarget(context, size, "f2")

        # Apply lights shader
        self.apply_lights_program = context.load_program(
            vertex_shader="Graphics/CoreShaders/fullscreen_quad.vs",
            fragment_shader="Graphics/CoreShaders/apply_lights.fs",
        )

        self.apply_lights_program["t_scene"] = 0
        self.apply_lights_program["t_lights"] = 1

        self.fullscreen_quad = arcade.gl.geometry.quad_2d_fs()

        self.load_light_shaders()

        pass

    def load_light_shaders(self):
        PointLight.load_shader(self.context)

    def resize(self, size):
        self.light_buffer.resize(size)
        pass

    # called by the scene renderer, do not call from application code
    def draw_lights(self, projection_matrix):

        # bind and clear light buffer
        self.light_buffer.bind_as_framebuffer()
        self.light_buffer.clear((0.0, 0.0, 0.0, 0.0))

        # send blending to additive
        self.context.enable_only(self.context.BLEND)
        self.context.blend_func = self.context.BLEND_ADDITIVE

        # draw each light type
        self.draw_point_lights(projection_matrix)

        # reset context
        self.context.enable_only()

        # reset dynamic light buffer
        self.dynamic_point_light_buffer = []

        pass

    def draw_dynamic_point_lights(self, sprite_list):
        for sprite in sprite_list:
            if not hasattr(sprite,'point_light'):
                continue
            #else append this
            self.dynamic_point_light_buffer.append(sprite.center_x)
            self.dynamic_point_light_buffer.append(sprite.center_y)
            self.dynamic_point_light_buffer.extend(sprite.point_light.color)
            self.dynamic_point_light_buffer.append(sprite.point_light.radius)

    def draw_point_lights(self, projection_matrix):
        # fill buffer from lights
        light_count = 0
        light_vertex_buffer = self.dynamic_point_light_buffer

        for light in self.point_lights:
            if light.enabled:
                light_count += 1
                light.append_to_buffer(None, light_vertex_buffer)

        if len(light_vertex_buffer) == 0:
            return

        # create vertex buffer and VBO
        asArray = array("f", light_vertex_buffer)
        buffer = self.context.buffer(data=asArray)
        buffer_description = arcade.gl.BufferDescription(
            buffer, "2f 3f 1f", ["in_position", "in_color", "in_radius"]
        )
        vao = self.context.geometry([buffer_description])
        # draw lights
        PointLight.light_shader["u_projection"] = projection_matrix
        vao.render(PointLight.light_shader, mode=self.context.POINTS)

        # buffer and vao will be released by GC
        pass

    def apply_lights(self, scene_rendertarget, final_rendertarget):
        self.apply_lights_program["u_ambient"] = self.ambient_light

        final_rendertarget.bind_as_framebuffer()
        scene_rendertarget.bind_as_texture(0)
        self.light_buffer.bind_as_texture(1)

        self.fullscreen_quad.render(self.apply_lights_program)
        pass

    def create_point_light(self, position, color, radius):
        newLight = PointLight(self, position, color, radius)
        self.point_lights.append(newLight)
        return newLight

    def destroy_light(self, light):
        if type(light) is PointLight:
            self.point_lights.remove(light)
            return
        # TODO:Other light types
