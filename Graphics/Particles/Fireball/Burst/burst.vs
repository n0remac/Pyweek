#version 330

in vec2 in_position;
in vec2 in_velocity;
in float in_life_offset;
in float in_type;

out vec2 v_position;
out float v_time;
out float v_velocity;
out int v_type;

uniform float u_time;

float inverse_lerp(float a, float b, float x){
    return clamp((x-a) / (b-a), 0.0, 1.0);
}


const float jank_a = 0.5;
const float jank_b = 1.25;

void main() {

    float adjustedTime = u_time - in_life_offset;

    float animTime = min(jank_a, adjustedTime) + inverse_lerp(jank_a,jank_b, adjustedTime);

    vec2 final_position = in_position + in_velocity * animTime;

    gl_Position = vec4(final_position, 0.0, 1.0);
    v_time = adjustedTime;
    v_velocity = length(in_velocity);
    v_type = int(in_type);
}