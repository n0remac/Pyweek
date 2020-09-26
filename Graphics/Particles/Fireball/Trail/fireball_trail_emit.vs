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

vec2 rand_dir_range(float val, vec2 base, float range){
    float rand_val = rand(val);

    rand_val *= 3.1415926 * 2.0;

    return vec2(cos(rand_val), sin(rand_val));
}

const float TRAIL_POWER[] = float[](1.0, 1.0,6.0);

vec2 perpendicular(vec2 val){
    return vec2(val.y, -val.x);
}

void main() 
{

    out_position = in_position;

    out_velocity = -0.1 * TRAIL_POWER[int(in_type)] * in_base_vel + 0.125 * TRAIL_POWER[int(in_type)] * perpendicular(in_base_vel) * (rand(1.0) -0.5) * 2.0;
    out_life_offset = u_time + rand(1.0) * 0.0;    

    out_type = in_type;
}