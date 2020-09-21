import arcade
import random
import math
from array import array

class TestParticleSystem():


    def __init__(self, context):
        #load some shaders

        self.context = context
        self.program = context.load_program(
            vertex_shader='Graphics/Particles/test.vs',
            geometry_shader='Graphics/Particles/test.gs',
            fragment_shader='Graphics/Particles/test.fs'
        )

        #create some buffers
        data = []

        for x in range(10000):
            self.append_particle(data)
        
        asArray = array('f', data)
        self.buffer = self.context.buffer(data=asArray)
        buffer_description = arcade.gl.BufferDescription(self.buffer,
                                                        '2f 2f 1f',
                                                        ['in_position', 'in_velocity', 'in_life_offset'])
        self.vao = self.context.geometry([buffer_description])


    def append_particle(self, list):
        #Format
        # X,Y post
        list.append(600.0)
        list.append(600.0)
        # X,Y velocity
        angle = random.uniform(0.0, 2.0 * math.pi)
        velocity = random.uniform(75.0,105.0)
        list.append(math.sin(angle) * velocity)
        list.append(math.cos(angle) * velocity)

        # Start_offset
        list.append(random.uniform(0.0, 1.0))


    def render(self, current_time, projection_matrix):

        #transform time
        transformed_time = current_time % 4.0

        #set time on shader
        self.program['u_time'] = transformed_time
        self.program['u_projection'] = projection_matrix

        #draw shader w/ particle buffer
        self.vao.render(self.program, mode=self.context.POINTS)        

        pass