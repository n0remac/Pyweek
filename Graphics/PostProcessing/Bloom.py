import arcade
import math
from Graphics.PostEffect import PostEffect
from Graphics.RenderTarget import RenderTarget


class Bloom(PostEffect):
    def __init__(self):
        super(Bloom, self).__init__()
        pass

    def on_add(self, post_processing_chain, context, window_size):
        super(Bloom, self).on_add(post_processing_chain, context, window_size)

        self.extract_blur_x = context.load_program(
            vertex_shader="Graphics/CoreShaders/fullscreen_quad.vs",
            fragment_shader="Graphics/PostProcessing/Shaders/extract_blur_x.fs",
        )

        self.blur_y_power = context.load_program(
            vertex_shader="Graphics/CoreShaders/fullscreen_quad.vs",
            fragment_shader="Graphics/PostProcessing/Shaders/blur_y_power.fs",
        )

        self.set_universal_shader_args(self.extract_blur_x)
        self.set_universal_shader_args(self.blur_y_power)

        self.load_apply_bloom(context)

        self.extract_blur_x["t_source"] = 0
        self.blur_y_power["t_source"] = 0

        self.threshold = 1.0
        self.power = 1.0

        # Allocate the downscaled render targets and blur buffers
        self.rt_half_ping = RenderTarget(
            context, self.get_half_rt_size(window_size), "f2"
        )
        self.rt_half_pong = RenderTarget(
            context, self.get_half_rt_size(window_size), "f2"
        )

        self.rt_quater_ping = RenderTarget(
            context, self.get_quater_rt_size(window_size), "f2"
        )
        self.rt_quater_pong = RenderTarget(
            context, self.get_quater_rt_size(window_size), "f2"
        )

    def set_universal_shader_args(self, program):
        program["t_source"] = 0

        weights = self.get_blur_coefficents(11)  # must match shader
        weights_sum = 0
        for x in weights:
            weights_sum += x

        program["u_weights"] = weights
        program["u_weight_sum"] = weights_sum

    def load_apply_bloom(self, context):

        self.apply_bloom = context.load_program(
            vertex_shader="Graphics/CoreShaders/fullscreen_quad.vs",
            fragment_shader="Graphics/PostProcessing/Shaders/apply_bloom.fs",
        )

        self.apply_bloom["t_source"] = 0
        self.apply_bloom["t_half"] = 1
        self.apply_bloom["t_quater"] = 2

    def resize(self, window_size):
        super(Bloom, self).resize(window_size)

        self.rt_half_ping.resize(self.get_half_rt_size(window_size))
        self.rt_half_pong.resize(self.get_half_rt_size(window_size))

        self.rt_quater_ping.resize(self.get_quater_rt_size(window_size))
        self.rt_quater_pong.resize(self.get_quater_rt_size(window_size))

    def get_half_rt_size(self, window_size):
        return (
            int(math.ceil(window_size[0] / 2.0)),
            int(math.ceil(window_size[1]) / 2.0),
        )

    def get_quater_rt_size(self, window_size):
        return (
            int(math.ceil(window_size[0] / 4.0)),
            int(math.ceil(window_size[1]) / 4.0),
        )

    def get_blur_coefficents(self, count):
        midpoint = math.floor(count / 2)
        stdev = midpoint / 3.0  # I think this is right but #GameJam

        coefficents = [0.0] * count

        for x in range(0, midpoint + 1):
            distance = midpoint - x
            factor = self.gaussian(distance, stdev)

            coefficents[x] = factor
            coefficents[count - (1 + x)] = factor

        return coefficents

    def gaussian(self, distance, stdev):
        # See this for the math: https://en.wikipedia.org/wiki/Gaussian_blur
        preamble = 1.0 / math.sqrt(2.0 * math.pi * stdev * stdev)
        exponent = -((distance * distance) / (2.0 * stdev * stdev))

        return preamble * math.exp(exponent)

    def apply(self, source_target, destination_target):

        # Downsample main RT to half and quater size
        self.downsample_to_ping(source_target)

        # run ping pong back and forth to blur the light buffer
        self.apply_blur(self.rt_half_ping, self.rt_half_pong)
        self.apply_blur(self.rt_quater_ping, self.rt_quater_pong)

        # Apply half and quater to the main image as bloom
        destination_target.bind_as_framebuffer()
        source_target.bind_as_texture(0)
        self.rt_half_ping.bind_as_texture(1)
        self.rt_quater_ping.bind_as_texture(2)
        PostEffect.quad.render(self.apply_bloom)

    def apply_blur(self, ping, pong):

        # Set arugments for pass size
        texel_uv_size = (1.0 / ping.size[0], 1.0 / ping.size[1])

        self.extract_blur_x["u_texel_size"] = texel_uv_size
        self.blur_y_power["u_texel_size"] = texel_uv_size

        # blur ping onto pong
        pong.bind_as_framebuffer()
        ping.bind_as_texture(0)
        PostEffect.quad.render(self.extract_blur_x)

        # blur pong back to ping
        ping.bind_as_framebuffer()
        pong.bind_as_texture(0)
        PostEffect.quad.render(self.blur_y_power)
        pass

    def downsample_to_ping(self, source_target):
        self.rt_half_ping.bind_as_framebuffer()
        source_target.blit_to_current_target()

        self.rt_quater_ping.bind_as_framebuffer()
        self.rt_half_ping.blit_to_current_target()

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = value
        self.extract_blur_x["u_threshold"] = value

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        self._power = value * 0.5
        self.blur_y_power["u_power"] = value * 0.5
