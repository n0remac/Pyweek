#version 330

in vec2 in_position;
in float in_type;

out vec2 out_position;
out vec2 out_velocity;
out float out_life_offset;

uniform float u_seed;
uniform float u_time;

float rand(float val){
    return fract(sin((val + u_seed + gl_VertexID*3.0)) * 156489.085);
}

float rand(float val, float min_val, float max_val){
    float f = fract(sin((9.689 * val + u_seed + gl_VertexID*3.0)) * 156489.085);
    return mix(min_val,max_val,f);
}

void main() 
{
    out_position = in_position;
    out_life_offset = u_time + rand(1.0) * 0.05;    


    vec2 velocity = vec2(0.0, 1.0);

    velocity.x = rand(2.0, -0.5, 0.5);

    velocity = normalize(velocity);

    out_velocity = velocity * mix(20.0,40.0, rand(1.0));

}