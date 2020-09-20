#version 330

in vec2 in_position;
in vec3 in_color;
in float in_radius;

out vec3 v_color;
out float v_radius;

void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
    v_color = in_color;
    v_radius = in_radius;
}