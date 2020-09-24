#version 330

uniform sampler2D t_source;

uniform float u_inner_distance;
uniform float u_outer_distance;
uniform vec4 u_color;

in vec2 v_uv;

out vec4 out_color;

void main() 
{
    vec3 color = texture(t_source, v_uv).rgb;

    //Remap to -1 1 so length is distance from center
    vec2 pos = (v_uv - 0.5) * 2.0;

    float dist = length(pos);

    float factor = smoothstep(u_inner_distance, u_outer_distance, dist);

    vec3 finalColor = mix(color, u_color.rgb, factor);

    out_color = vec4(finalColor, 1.0);
}