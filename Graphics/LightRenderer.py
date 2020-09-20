import arcade
from Graphics.RenderTarget import RenderTarget

class LightRenderer():
    __instance = None

    def __init__(self, context, size):
        if LightRenderer.__instance is not None:
            raise Exception()#Can only be one to make apis easy

        LightRenderer.__instance = self
        self.context = context
        self.ambient_light = (1.0,1.0,1.0)

        #HDR target
        self.light_buffer = RenderTarget(context, size, 'f2')

        #Apply lights shader
        self.apply_lights_program = context.load_program(
            vertex_shader='Graphics/CoreShaders/fullscreen_quad.vs',
            fragment_shader='Graphics/CoreShaders/apply_lights.fs'
        )

        self.apply_lights_program['t_scene'] = 0
        self.apply_lights_program['t_lights'] = 1

        self.fullscreen_quad = arcade.gl.geometry.quad_2d_fs()

        pass

    def resize(self, size):
        self.light_buffer.resize(size)
        pass

    #called by the scene renderer, do not call from application code
    def draw_lights(self):
        pass

    def apply_lights(self, scene_rendertarget, final_rendertarget):
        self.apply_lights_program['u_ambient'] = self.ambient_light

        final_rendertarget.bind_as_framebuffer()
        scene_rendertarget.bind_as_texture(0)
        self.light_buffer.bind_as_texture(1)

        self.fullscreen_quad.render(self.apply_lights_program)
        pass
    
