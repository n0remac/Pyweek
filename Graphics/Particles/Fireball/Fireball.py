import arcade

from Graphics.Particles.ParticleSystem import ParticleSystem


#Overall controller class for all fireball effects in the scene. This is composed of multiple particle systems
class FireBall():


    def __init__(self, context):
        self.context = context