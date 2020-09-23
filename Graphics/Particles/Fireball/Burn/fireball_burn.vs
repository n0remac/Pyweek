#version 330

in vec2 in_position;
in vec2 in_velocity;
in float in_life_offset;
in float in_type;

out vec2 v_position;
out float v_time;
out int v_type;

uniform float u_time;

const float rot_speed = 7.0;

float rand_no_seed(float val){
    return fract(sin((val + gl_VertexID * 6.74)) * 156489.085);
}

vec2 get_final_pos(float adjustedTime){
    if(in_type < 0.9){
        return in_position + in_velocity * adjustedTime;
    }
    else if(in_type < 1.9){
        //Frost Spiral
        float direction = gl_VertexID % 2 == 0 ? -1.0 : 1.0;
        direction = 1.0;

        float angle = rand_no_seed(1.0) * 2.0 * 3.1415926;
        angle += rot_speed * adjustedTime * direction;

        vec2 offset = vec2(cos(angle), sin(angle));
        offset *= adjustedTime * 50.0;

        return in_position + in_velocity * adjustedTime + offset;
    }
    else{
        //Who knows yet
        return in_position + in_velocity * adjustedTime;
    }
}

void main() {

    float adjustedTime = u_time - in_life_offset;

    vec2 final_position = get_final_pos(adjustedTime);

    gl_Position = vec4(final_position, 0.0, 1.0);
    v_time = adjustedTime;

    v_type = int(in_type);
}