import arcade
import random
import math
from array import array

from Graphics.Particles.ParticleSystem import ParticleSystem


class TestParticleSystem(ParticleSystem):
    def __init__(self, context):
        # load some shaders
        super().__init__(context)

        self.program = context.load_program(
            vertex_shader="Graphics/Particles/test.vs",
            geometry_shader="Graphics/Particles/test.gs",
            fragment_shader="Graphics/Particles/test.fs",
        )

        self.burst_program = context.load_program(
            vertex_shader="Graphics/Particles/test_emit.vs"
        )

        self.init_system(
            5000,
            "2f 2f 1f",
            ["in_position", "in_velocity", "in_life_offset"],
            [0.0, 0.0, 0.0, 0.0, 1000.0],
            4.0,
        )

    def append_particle(self, list):
        # Format
        # X,Y post
        list.append(600.0)
        list.append(600.0)
        # X,Y velocity
        angle = random.uniform(0.0, 2.0 * math.pi)
        velocity = random.uniform(75.0, 105.0)
        list.append(math.sin(angle) * velocity)
        list.append(math.cos(angle) * velocity)

        # Start_offset
        list.append(random.uniform(0.0, 1.0))

    def do_burst(self, position):
        self.burst_program["u_position"] = position
        self.emit_with_program(self.burst_program, 150)
        pass
