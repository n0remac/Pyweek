#version 330

in vec2 in_position;
in vec2 in_base_vel;
in float in_type;

out vec2 out_position;
out vec2 out_velocity;
out float out_life_offset;
out float out_type;

uniform float u_seed;
uniform float u_time;


float rand(float val){
    return fract(sin((val + u_seed + gl_VertexID * 6.74)) * 156489.085);
}

vec2 rand_dir(float val){
    float rand_val = rand(val);

    rand_val *= 3.1415926 * 2.0;

    return vec2(cos(rand_val), sin(rand_val));
}

void main() 
{

    out_position = in_position;

    if(in_type < 0.9){
    out_velocity = in_base_vel + rand_dir(2.0) * mix(50,75, rand(1.0));
    }
    else if(in_type < 1.9)
    {
    out_velocity = in_base_vel + rand_dir(2.0) * mix(10,15, rand(1.0));
    }
    else{
    out_velocity = in_base_vel + rand_dir(2.0) * mix(70,200, rand(1.0));
    }
    out_life_offset = u_time + rand(1.0) * 0.0;    

    out_type = in_type;
}