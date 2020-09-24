import arcade
from Graphics.PostEffect import PostEffect


class Vignette(PostEffect):
    def __init__(self):
        super().__init__()

    def on_add(self, post_processing_chain, context, window_size):
        super(Vignette, self).on_add(post_processing_chain, context, window_size)

        self.program = context.load_program(
            vertex_shader="Graphics/CoreShaders/fullscreen_quad.vs",
            fragment_shader="Graphics/PostProcessing/Shaders/vignette.fs",
        )

        self.program["t_source"] = 0

        self.inner_distance = 1.0
        self.outer_distance = 2.0
        self.color = (0.0, 0.0, 0.0, 1.0)

    def apply(self, source_target, destination_target):
        destination_target.bind_as_framebuffer()
        source_target.bind_as_texture(0)
        PostEffect.quad.render(self.program)

    @property
    def outer_distance(self):
        return self._outer_distance

    @outer_distance.setter
    def outer_distance(self, value):
        self._outer_distance = value
        self.program["u_outer_distance"] = value

    @property
    def inner_distance(self):
        return self._inner_distance

    @inner_distance.setter
    def inner_distance(self, value):
        self._inner_distance = value
        self.program["u_inner_distance"] = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.program["u_color"] = value
