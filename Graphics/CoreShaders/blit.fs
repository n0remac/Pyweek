#version 330

uniform sampler2D s_texture;

in vec2 v_uv;
out vec4 out_color;

void main() {
    vec4 color = texture(texture0, v_uv);
    out_color = color;
}