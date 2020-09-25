import arcade
from Graphics.Particles.ParticleSystem import ParticleSystem
from array import array


class TorchSystem(ParticleSystem):
    def __init__(self, context):
        # load some shaders
        super().__init__(context)

        self.program = context.load_program(
            vertex_shader="Graphics/Particles/Torch/torch.vs",
            geometry_shader="Graphics/Particles/Torch/torch.gs",
            fragment_shader="Graphics/Particles/Torch/torch.fs",
        )

        self.burst_program = context.load_program(
            vertex_shader="Graphics/Particles/Torch/torch_emit.vs"
        )

        self.init_system(
            5000,
            "2f 2f 1f",
            ["in_position", "in_velocity", "in_life_offset"],
            [0.0, 0.0, 0.0, 0.0, 1000.0],
            4.0,
        )

        self.torch_data = []
        self.burst_count = 0
        self.frame_count = 0

    # Torch is type 0
    # Candle is type 1
    def add_torch(self, position):
        self.add_instance(position, 0)
        self.add_instance(position, 0)
        self.add_instance(position, 0)

    def add_candle(self, position):
        self.add_instance(position, 1)

    def add_instance(self, position, light_type):
        self.torch_data.append(position[0])
        self.torch_data.append(position[1])
        self.torch_data.append(light_type)
        self.burst_count += 1

    def build_buffer(self):
        asArray = array("f", self.torch_data)
        self._emit_buffer = self.context.buffer(data=asArray)
        buffer_description = arcade.gl.BufferDescription(
            self._emit_buffer, "2f 1f", ["in_position", "in_type"]
        )
        self.custom_emission = self.context.geometry([buffer_description])

    def do_burst(self):
        self.emit_with_program(
            self.burst_program, self.burst_count, vao=self.custom_emission
        )

    def render(self, projection_matrix):
        self.frame_count += 1
        if self.frame_count % 10 == 0:
            self.do_burst()

        super().render(projection_matrix)
