import arcade

from Graphics.Particles.ParticleSystem import ParticleSystem
from Graphics.Particles.Fireball.Burn.FireballBurn import FireballBurn
from Graphics.Particles.Fireball.Trail.FireballTrail import FireballTrail
from Graphics.Particles.Fireball.Burst.Burst import Burst

# Overall controller class for all fireball effects in the scene. This is composed of multiple particle systems
class FireBall:
    def __init__(self, context, physics):
        self.context = context
        self.physics = physics

        self.fireball_burn = FireballBurn(context, physics)
        self.fireball_trail = FireballTrail(context, physics)
        self.fireball_burst = Burst(context)

    def on_particle_death(self, sprite):
        position = (sprite.center_x, sprite.center_y)
        self.fireball_burst.do_burst(position)

    def render(self, projection_matrix, projectile_list):
        self.fireball_burn.render(projection_matrix, projectile_list)
        self.fireball_trail.render(projection_matrix, projectile_list)
        self.fireball_burst.render(projection_matrix)

    def render_lights(self, projection_matrix, projectile_list):
        self.fireball_burst.render_light(projection_matrix)
