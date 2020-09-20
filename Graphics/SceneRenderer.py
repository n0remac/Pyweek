import arcade
from Graphics.RenderTarget import RenderTarget

#Class that controlls all rendering to ensure lighting and post processing works correctly
#it will invoke a number of callbacks to allow the application to draw during various parts of the
#rendering process
class SceheRenderer():

    #window is the arcade window object, size is tuple(x,y) screen size in pixels
    def __init__(self, window, size):
        self.window = window
        self.context = window.ctx
        #TODO: init any subsystems and allocate render targets

        #lit scene things are drawn to this
        self.primary_target = RenderTarget(self.context, size, 'f1')
        #all lighting and emissive is rendered to this and fed though post-processing
        self.final_target = RenderTarget(self.context, size, 'f2')

        self.draw_primary_callback = None
        self.draw_emissive_callback = None
        self.draw_after_post_callback = None

    #Size is tuple (x,y) size in pixels
    def on_window_resized(self,size):
        self.primary_target.resize(size)
        self.final_target.resize(size)
        
    def draw_scene(self):
        #Clear target
        self.primary_target.clear((0.0, 0.0, 0.0, 1.0))
        self.final_target.clear((0.0, 0.0, 0.0, 0.0))

        #bind primary target
        self.primary_target.bind_as_framebuffer()
        #draw scene
        if self.draw_primary_callback is not None:
            self.draw_primary_callback()
        #render lights texture

        #light to final texture

        #render emissive to final texure

        #run post processing

        #temp code, blit primary to screen
        self.window.use()
        self.primary_target.blit_to_current_target()
        pass
