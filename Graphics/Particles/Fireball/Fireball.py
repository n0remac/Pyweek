import arcade

from Graphics.Particles.ParticleSystem import ParticleSystem
from Graphics.Particles.Fireball.Burn.FireballBurn import FireballBurn
from Graphics.Particles.Fireball.Trail.FireballTrail import FireballTrail

#Overall controller class for all fireball effects in the scene. This is composed of multiple particle systems
class FireBall():


    def __init__(self, context, physics):
        self.context = context
        self.physics = physics

        self.fireball_burn = FireballBurn(context, physics)
        self.fireball_trail = FireballTrail(context, physics)



    def render(self, projection_matrix, projectile_list):
        self.fireball_burn.render(projection_matrix, projectile_list)
        self.fireball_trail.render(projection_matrix, projectile_list)
