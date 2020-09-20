import arcade

class RenderTarget():
    blit_shader = None
    blit_quad = None

    def __init__(self, context, size, texture_format):

        self.context = context
        self.size = size
        self.texture_format = texture_format

        self.texture = None
        self.framebuffer_object = None

        self.is_valid = False
        #resize triggers allocatio so re-use code here
        self.resize(size)

        #init quad for blit related things
        self.init_quad()

    def init_quad(self):
        if RenderTarget.blit_shader is not None:
            return

        RenderTarget.blit_quad = arcade.gl.geometry.quad_2d_fs()
        RenderTarget.blit_shader = self.context.load_program(
            vertex_shader='Graphics/CoreShaders/fullscreen_quad.vs',
            fragment_shader='Graphics/CoreShaders/blit.fs'
        )

        RenderTarget.blit_shader['s_texture'] = 0

    def resize(self, size):
        #Release stuff before resize
        self.release()

        self.texture = arcade.gl.Texture(
            self.context,
            size,
            components=4,
            dtype=self.texture_format,
            wrap_x=arcade.gl.CLAMP_TO_EDGE,
            wrap_y=arcade.gl.CLAMP_TO_EDGE
        )

        self.framebuffer_object = arcade.gl.Framebuffer(
            self.context,
            color_attachments=[self.texture]
        )

        self.is_valid = True
        

    def release(self):
        if self.texture is not None:
            self.texture.release()
        
        if self.framebuffer_object is not None:
            self.framebuffer_object.release()

    #Bind this render target to a given texture slot
    def bind_as_texture(self, slot):
        self.texture.use(slot)

    #Bind the render target as the current target for rendering
    def bind_as_framebuffer(self):
        self.framebuffer_object.use()

    #Copy the contents of this render target to the current render target
    def blit_to_current_target(self):
        self.bind_as_texture(0)
        RenderTarget.blit_quad.render(RenderTarget.blit_shader)

    #Clear the render target to a given color in the 0-1 range
    def clear(self, color):
        self.framebuffer_object.clear(color, normalized=True)