import arcade
import random
import math
from array import array

from Graphics.Particles.ParticleSystem import ParticleSystem


class FireballTrail(ParticleSystem):


    def __init__(self, context, physics):
        #load some shaders
        super().__init__(context)

        self.frame_count = 0
        self.physics = physics

        self.program = context.load_program(
            vertex_shader='Graphics/Particles/Fireball/Trail/fireball_trail.vs',
            geometry_shader='Graphics/Particles/Fireball/Trail/fireball_trail.gs',
            fragment_shader='Graphics/Particles/Fireball/Trail/fireball_trail.fs'
        )

        self.burst_program = context.load_program(
            vertex_shader='Graphics/Particles/Fireball/Trail/fireball_trail_emit.vs', 
        )

        self.init_system(
            5000,
            '2f 2f 1f 1f', 
            ['in_position', 'in_velocity', 'in_life_offset', 'in_type'],
            [0.0, 0.0, 0.0, 0.0, 1000.0, 0.0],
            4.0)



    def render(self, projection_matrix, projectile_list):
        self.frame_count += 1
        if (self.frame_count % 2 == 0):
            self.do_emission(projectile_list)

        super().render(projection_matrix)


    def do_emission(self, projectile_list):
        if len(projectile_list) == 0:
            return
        vao = self.build_buffer(projectile_list)
        self.emit_with_program(self.burst_program, len(projectile_list), vao=vao)
        print(len(projectile_list))
        pass

    def build_projectile_data(self, projectile_list):
        data = []
        for projectile in projectile_list:
            data.append(projectile.center_x)
            data.append(projectile.center_y)

            velocity = self.physics.get_physics_object(sprite=projectile).body.velocity

            data.append(velocity[0])
            data.append(velocity[1])
            data.append(0.0)
        return data


    def build_buffer(self, projectile_list):

        projectile_data = self.build_projectile_data(projectile_list)

        asArray = array('f', projectile_data)
        buffer = self.context.buffer(data=asArray)
        buffer_description = arcade.gl.BufferDescription(buffer,
                                                        '2f 2f 1f',
                                                        ['in_position', 'in_base_vel', 'in_type'])
        vao = self.context.geometry([buffer_description])
        return vao