#version 330

uniform sampler2D t_source;

const int samples = 11;
const int midpoint = samples/2;

uniform float u_weights[11];
uniform float u_weight_sum;
uniform vec2 u_texel_size;

uniform float u_power;//Scale bloom effect up or down in intensity

in vec2 v_uv;
out vec4 out_color;

void main() 
{
    vec3 color = texture(t_source, v_uv).rgb;

    vec2 sample_pos = v_uv;
    sample_pos.y -= midpoint * u_texel_size.y;

    vec3 final_color = vec3(0.0);

    for(int i = 0; i < samples; i++)
    {
        vec3 sample = texture(t_source, sample_pos).xyz;

        //Apply guassian weight
        final_color += sample * u_weights[i];
        //Advance sample position
        sample_pos.y += u_texel_size.y;
    }

    //Divide by weight sum to ensure no gain or loss of energy
    final_color /= u_weight_sum;

    //Apply power
    final_color *= u_power;

    out_color = vec4(final_color, 1.0);
}