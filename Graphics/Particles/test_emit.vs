#version 330

in float in_placeholder;

out vec2 out_position;
out vec2 out_velocity;
out float out_life_offset;

uniform float u_seed;
uniform float u_time;
uniform vec2 u_position;


float rand(float val){
    return fract(sin((val + u_seed + gl_VertexID)) * 156489.085);
}

void main() 
{

    out_position = u_position;


    float rot = float(gl_VertexID) / 100.0;
    rot += u_seed;
    rot *= 3.1415926 * 2.0;
    out_velocity = vec2(sin(rot), cos(rot)) * mix(75,105, rand(1.0));
    out_life_offset = u_time + rand(1.0) * 0.0;    


}