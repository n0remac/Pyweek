#version 330

uniform sampler2D t_source;
uniform float u_white_point_2;
in vec2 v_uv;
out vec4 out_color;

void main() {
    vec3 color = texture(t_source, v_uv).rgb;

    //Basic reihnhard tonemapping
    vec3 top_fraction = color / u_white_point_2;

    vec3 numerator = color * (1.0 + (color / u_white_point_2));
    vec3 denom = 1.0 + color;

    vec3 result = numerator / denom;
    result = clamp(result, 0.0, 1.0);

    out_color = vec4(result, 1.0);
}