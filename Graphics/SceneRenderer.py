import arcade
from Graphics.RenderTarget import RenderTarget
from Graphics.LightRenderer import LightRenderer
from Graphics.PostProcessingChain import PostProcessingChain

# Class that controlls all rendering to ensure lighting and post processing works correctly
# it will invoke a number of callbacks to allow the application to draw during various parts of the
# rendering process
class SceneRenderer:

    # window is the arcade window object, size is tuple(x,y) screen size in pixels
    def __init__(self, window):
        self.window = window
        self.context = window.ctx
        self.background_color = (0.0, 0.0, 0.0, 1.0)

        size = window.get_size()

        # TODO: init any subsystems and allocate render targets

        # lit scene things are drawn to this
        self.primary_target = RenderTarget(self.context, size, "f1")
        # all lighting and emissive is rendered to this and fed though post-processing
        self.final_target = RenderTarget(self.context, size, "f2")

        # Allocate other renderers
        self.light_renderer = LightRenderer(self.context, size)
        self.post_processing = PostProcessingChain(self.context, size)

        self.draw_primary_callback = None
        self.draw_emissive_callback = None
        self.draw_after_post_callback = None
        self.draw_to_light_bufer_callback = None

    # Size is tuple (x,y) size in pixels
    def on_window_resized(self, size):
        self.primary_target.resize(size)
        self.final_target.resize(size)

        self.light_renderer.resize(size)
        self.post_processing.resize(size)

    def draw_scene(self):
        # Clear target
        self.primary_target.clear(self.background_color)

        # don't need to clear due to blit
        # self.final_target.clear((0.0, 0.0, 0.0, 0.0))

        # bind primary target
        self.primary_target.bind_as_framebuffer()
        # draw scene
        if self.draw_primary_callback is not None:
            self.draw_primary_callback()

        # render lights texture
        self.light_renderer.draw_lights(self.context.projection_2d_matrix)

        if self.draw_to_light_bufer_callback is not None:
            self.draw_to_light_bufer_callback()

        # reset context
        self.context.enable_only()

        # light to final texture
        self.light_renderer.apply_lights(self.primary_target, self.final_target)

        # render emissive to final texure
        if self.draw_emissive_callback is not None:
            self.final_target.bind_as_framebuffer()
            self.context.enable_only(self.context.BLEND)
            self.context.blend_func = self.context.BLEND_ADDITIVE

            self.draw_emissive_callback()

            # reset context settings
            self.context.enable_only()

        # run post processing on final texture
        final_image = self.post_processing.apply_chain(self.final_target)
        final_image.texture.filter = (self.context.NEAREST, self.context.NEAREST)
        # blit final image to screen
        self.window.use()
        final_image.blit_to_current_target()

        # draw after post processing callback
        if self.draw_after_post_callback is not None:
            self.draw_after_post_callback()

    @property
    def scene_lights(self):
        return self.light_renderer
