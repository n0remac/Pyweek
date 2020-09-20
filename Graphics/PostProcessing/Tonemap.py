import arcade
from Graphics.PostEffect import PostEffect

class Tonemap(PostEffect):

    def __init__(self):
        super().__init__()

    def on_add(self, post_processing_chain, context, window_size):
        super(Tonemap,self).on_add(post_processing_chain, context, window_size)

        self.program = context.load_program(
            vertex_shader='Graphics/CoreShaders/fullscreen_quad.vs',
            fragment_shader='Graphics/PostProcessing/Shaders/tonemap.fs'
        )

        self.program['t_source'] = 0
        self.white_point = 10.0

    def apply(self, source_target, destination_target):
        destination_target.bind_as_framebuffer()
        source_target.bind_as_texture(0)
        PostEffect.quad.render(self.program)

    @property
    def white_point(self):
        return self._white_point

    @white_point.setter
    def white_point(self,value):
        self._white_point = value
        #pre square for shader
        self.program['u_white_point_2'] = value * value

        
