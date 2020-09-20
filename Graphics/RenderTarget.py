import arcade

class RenderTarget():

    def __init__(self, context, size, format):

        self.context = context
        self.size = size
        self.format = format

        self.texture = None
        self.framebuffer_object = None

        self.is_valid = False
        #resize triggers allocatio so re-use code here
        self.resize(size)

    def resize(self, size):
        #Release stuff before resize
        self.release()

        self.texture = arcade.gl.Texture(
            context,
            size,
            components=4,
            dtype=format,
            wrap_x=arcade.gl.CLAMP_TO_EDGE,
            wrap_y=arcade.gl.CLAMP_TO_EDGE
        )

        self.framebuffer_object = arcade.gl.Framebuffer(
            self.context,
            color_attachments=[self.texture]
        )

        self.is_valid = True
        

    def release(self):
        if self.texture is not None
            self.texture.release()
        
        if self.framebuffer_object is not None
            self.framebuffer_object.release()

    #Bind this render target to a given texture slot
    def bind_as_texture(self, slot):
        self.texture.use(slot)

    #Bind the render target as the current target for rendering
    def bind_as_framebuffer(self):
        self.framebuffer_object.use()