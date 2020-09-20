import arcade

class Light():

    def __init__(self, renderer, position, color, radius):
        self.renderer = renderer
        self.position = position
        self.color = color
        self.radius = radius
        #Toggle enabled to turn light on and off
        self.enabled = True

    def destroy(self):
        self.renderer.destroy_light(self)