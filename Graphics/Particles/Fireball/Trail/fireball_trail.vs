#version 330

in vec2 in_position;
in vec2 in_velocity;
in float in_life_offset;

out vec2 v_position;
out float v_time;

uniform float u_time;


const float start_cross = 0.1;
const float end_cross = 0.75;
const float cross_time = end_cross - start_cross;

const float drift_power = 20.0;

const float decel = 0.5;

float rand_no_seed(float val){
    return fract(sin((val + gl_VertexID * 6.74)) * 64884.0);
}


vec2 get_drift(float adjustedTime){

   float flr = floor(adjustedTime);
   float frac = fract(adjustedTime);

   float mix_val = smoothstep(0.0,1.0,frac);

    //Jank continuous noise stuff
   float x = mix(rand_no_seed(flr) , rand_no_seed(flr+1.0) , mix_val);
   float y = mix(rand_no_seed(flr+10.0) , rand_no_seed(flr+11.0) , mix_val);

   return vec2(x,y);
}

float inverse_lerp(float a, float b, float x){
    return clamp((x-a) / (b-a), 0.0, 1.0);
}

void main() {

    float adjustedTime = u_time - in_life_offset;

    float blend_time = inverse_lerp(start_cross,end_cross, adjustedTime);

    float first_time = min(start_cross, adjustedTime);

    float second_time = clamp(adjustedTime - start_cross, 0.0, 1.0 /  decel);
    float calculus = 1.0 * second_time + (0.5 * -decel * second_time * second_time);

    vec2 final_position = in_position + (in_velocity * (first_time + calculus)) + (get_drift(adjustedTime * 0.8) * blend_time * drift_power);

    gl_Position = vec4(final_position, 0.0, 1.0);
    v_time = adjustedTime;
}