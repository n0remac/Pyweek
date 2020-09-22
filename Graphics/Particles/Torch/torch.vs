#version 330

in vec2 in_position;
in vec2 in_velocity;
in float in_life_offset;

out vec2 v_position;
out float v_time;

uniform float u_time;

void main() {

    float adjustedTime = u_time - in_life_offset;

    vec2 final_position = in_position + in_velocity * adjustedTime;

    vec2 perpen = normalize(in_velocity.yx);

    float sign = 1.0;

    if(gl_VertexID % 2 == 0){
        sign = -1.0;
    }

    final_position += sign * sin(3.0 * adjustedTime) * 5.0 * perpen;


    gl_Position = vec4(final_position, 0.0, 1.0);
    v_time = adjustedTime;
}