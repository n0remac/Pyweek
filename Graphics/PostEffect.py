import arcade

class PostEffect():
    quad = None
    def __init__(self):
        if PostEffect.quad == None:
            PostEffect.quad = arcade.gl.geometry.quad_2d_fs()
        #can be used to disable the effect
        self.enabled = True

    def on_add(self, post_processing_chain, context, window_size):
        self.post_processing_chain = post_processing_chain
        self.context = context
        self.window_size = window_size

    def resize(self, window_size):
        self.window_size = window_size

    def apply(self, source_target, destination_target):
        raise Exception()