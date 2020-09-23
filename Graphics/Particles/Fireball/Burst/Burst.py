import arcade
import random
import math
from array import array

from Graphics.Particles.ParticleSystem import ParticleSystem

class Burst(ParticleSystem):


    def __init__(self, context):
        #load some shaders
        super().__init__(context)

        self.program = context.load_program(
            vertex_shader='Graphics/Particles/Fireball/Burst/burst.vs',
            geometry_shader='Graphics/Particles/Fireball/Burst/burst.gs',
            fragment_shader='Graphics/Particles/Fireball/Burst/burst.fs',
        )

        self.burst_program = context.load_program(
            vertex_shader='Graphics/Particles/Fireball/Burst/burst_emit.vs',      
        )

        self.init_system(
            5000,
            '2f 2f 1f', 
            ['in_position', 'in_velocity', 'in_life_offset'],
            [0.0, 0.0, 0.0, 0.0, 1000.0],
            4.0)


    def do_burst(self, position):
        self.burst_program['u_position'] = position
        self.emit_with_program(self.burst_program, 400)
        pass

    def update(self, deltaT):
        pass