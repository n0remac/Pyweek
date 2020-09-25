import arcade
import random
import math
from array import array

from Graphics.Particles.ParticleSystem import ParticleSystem


class Burst(ParticleSystem):
    def __init__(self, context):
        # load some shaders
        super().__init__(context)

        self.program = context.load_program(
            vertex_shader="Graphics/Particles/Fireball/Burst/burst.vs",
            geometry_shader="Graphics/Particles/Fireball/Burst/burst.gs",
            fragment_shader="Graphics/Particles/Fireball/Burst/burst.fs",
        )

        self.light_program = context.load_program(
            vertex_shader="Graphics/Particles/Fireball/Burst/burst.vs",
            geometry_shader="Graphics/Particles/Fireball/Burst/burst_light.gs",
            fragment_shader="Graphics/Particles/Fireball/Burst/burst_light.fs",
        )

        self.burst_program = context.load_program(
            vertex_shader="Graphics/Particles/Fireball/Burst/burst_emit.vs",
        )

        self.init_system(
            50000,

            '2f 2f 1f 1f', 
            ['in_position', 'in_velocity', 'in_life_offset', 'in_type'],
            [0.0, 0.0, 0.0, 0.0, 1000.0, 0.0],
            10.0)


    def do_burst(self, position, p_type):
        self.burst_program['u_position'] = position
        self.burst_program['u_type'] = p_type
        self.emit_with_program(self.burst_program, 150)

        pass

    def update(self, deltaT):
        pass

    def render_light(self, projection_matrix):
        current_time_cause_python_is_broken = self.current_time
        if current_time_cause_python_is_broken > (
            self.last_emission_time + self.max_possible_lifetime
        ):
            return  # No need to render in this case, nothing can be visable

            # set time on shader
        self.light_program["u_time"] = self.current_time
        self.light_program["u_projection"] = projection_matrix

        # draw shader w/ particle buffer
        self.vertex_array.render(self.light_program, mode=self.context.POINTS)
