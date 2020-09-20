#version 330

uniform sampler2D t_source;

uniform sampler2D t_half;
uniform sampler2D t_quater;

in vec2 v_uv;
out vec4 out_color;

void main() 
{
    vec4 finalColor = texture(t_source, v_uv).rgba;

    vec3 half_bloom = texture(t_half, v_uv).rgb;
    vec3 quater_bloom = texture(t_quater, v_uv).rgb; 

    finalColor.rgb += half_bloom;
    finalColor.rgb += quater_bloom;

    out_color = finalColor;
}