#version 330

uniform sampler2D t_texture;

in vec2 v_uv;
out vec4 out_color;

void main() {
    vec4 color = texture(t_texture, v_uv);
    out_color = color;
}