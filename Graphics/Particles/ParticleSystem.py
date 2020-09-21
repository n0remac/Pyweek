import arcade
import math
import random
from array import array
from pyglet import gl
import time

#Base class for particles, let's see how this all works out
class ParticleSystem():

    scaling_factor = 1.0
    emission_buffer = None
    max_emission_count = 10000
    start_time = 0.0

    #scaling factor lets you tune for perf
    def configure_particles(scaling_factor):
        ParticleSystem.scaling_factor = scaling_factor


    def __init__(self, context):
        self.context = context
        ParticleSystem.init_emission(context)

    #called by child classes to set stuff up
    def init_system(self, max_particles, buffer_format, buffer_attributes, buffer_template, max_possible_lifetime):

        #Save this for later
        self.max_possible_lifetime = max_possible_lifetime

        #compute max particles based off scaling factor
        self.max_particles = max_particles * ParticleSystem.scaling_factor
        self.max_particles = int(math.ceil(self.max_particles))

        #allocate the buffer
        data = buffer_template * self.max_particles
        self.particle_byte_length = len(buffer_template) * 4

        asArray = array('f', data)
        self.buffer = self.context.buffer(data=asArray)
        buffer_description = arcade.gl.BufferDescription(self.buffer,
                                                        buffer_format,
                                                        buffer_attributes)
        self.vertex_array = self.context.geometry([buffer_description])

        #setup the values used to manage this
        self.last_emission_time = -1000.0
        self.current_emission_index = 0

    def init_emission(context):
        if ParticleSystem.emission_buffer is not None:
            return

        data = [0.0] * ParticleSystem.max_emission_count

        asArray = array('f', data)
        ParticleSystem.___buffer = context.buffer(data=asArray)
        buffer_description = arcade.gl.BufferDescription(ParticleSystem.___buffer,
                                                        '1f',
                                                        ['in_placeholder'])

        ParticleSystem.emission_buffer = context.geometry([buffer_description])
        ParticleSystem.start_time = time.time()

    def emit_with_program(self, program, count):

        program['u_seed'] = random.uniform(0, 1.0)
        program['u_time'] = self.current_time

        count = int(math.ceil(count * ParticleSystem.scaling_factor))
        self.last_emission_time = self.current_time

        #a few cases for emission, as we have a circular particle buffer
        if count >= self.max_particles:
            #total emission of every possible slot
            count = self.max_particles
            self.current_emission_index = 0

            self.emit_internal(program, 0, count, 0)

            return

        if count + self.current_emission_index < self.max_particles:
            #single emission

            self.emit_internal(program, 0, count, self.particle_byte_length * self.current_emission_index)

            self.current_emission_index += count

        else:
            #wrapped emission useing the start and end of the rolling buffer
            first_burst = self.max_particles - self.current_emission_index
            second_burst = count - first_burst
        
            self.emit_internal(program, 0, first_burst, self.particle_byte_length * self.current_emission_index)

            self.emit_internal(program, first_burst, second_burst, 0)

            self.current_emission_index = second_burst


    def emit_internal(self, program, first, vertex_count, buffer_offset):

        #HELLA GOOD HACK
        if buffer_offset > 0:
            gl.glBindBufferRange(
                gl.GL_TRANSFORM_FEEDBACK_BUFFER,
                0,
                self.buffer.glo,
                buffer_offset,
                vertex_count * self.particle_byte_length)
                

        ParticleSystem.emission_buffer.transform(
            program,
            self.buffer,
            first=first,
            vertices=vertex_count,
            buffer_offset=buffer_offset
        )
   
    def render(self, projection_matrix):
        current_time_cause_python_is_broken = self.current_time
        if current_time_cause_python_is_broken > (self.last_emission_time + self.max_possible_lifetime):
            return #No need to render in this case, nothing can be visable

                #set time on shader
        self.program['u_time'] = self.current_time
        self.program['u_projection'] = projection_matrix

        #draw shader w/ particle buffer
        self.vertex_array.render(self.program, mode=self.context.POINTS)     

    @property
    def current_time(self):
        return time.time() - ParticleSystem.start_time