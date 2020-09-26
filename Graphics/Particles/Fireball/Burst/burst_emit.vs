#version 330

in float in_placeholder;

out vec2 out_position;
out vec2 out_velocity;
out float out_life_offset;
out float out_type;

uniform float u_seed;
uniform float u_time;
uniform vec2 u_position;
uniform float u_type;

const float[] min_vel = float[](25.0,5.0, 25.0);

float rand(float val){
    return fract(sin((val + u_seed + gl_VertexID)) * 15649.085);
}



float get_life_offset(){
    if(u_type == 1.0){

        if(gl_VertexID % 5 > 0){
            return u_time - 1000.0;
        }

        return u_time + floor(rand(2.0) * 3.0 ) * 0.4;
        //return u_time + 0.1;

    }

    return  u_time + rand(1.0) * 0.3 - 0.3;
}

void main() 
{

    out_position = u_position;


    float rot = float(gl_VertexID) / 100.0;
    rot += u_seed;
    rot *= 3.1415926 * 2.0;

    float rv = rand(1.0);
    out_velocity = vec2(sin(rot), cos(rot)) * mix(25.0,200.0, rv * rv * rv);
    out_life_offset = get_life_offset();
    out_type = u_type;

}