#version 330 core
layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

in float v_time[];
in float v_velocity[];
in int v_type[];

uniform float u_time;
uniform mat4x4 u_projection;

out float vf_time;
out float vf_scale;
out float vf_velocity;
out vec2 vf_uv;
flat out int vf_type;

out float vf_radius;
out vec2 vf_light_pos;

const float LIFE = 0.8;

const float size_spark = 64.0;
const float size_flame = 16.0;

float inverse_lerp(float a, float b, float x){
    return clamp((x-a) / (b-a), 0.0, 1.0);
}

void EmitVert(vec2 offset, float scale)
{
    vec2 localPos = offset * scale;
    vec2 posWorldSpace = gl_in[0].gl_Position.xy +localPos;

    vec4 finalPositionWorldSpace = vec4(posWorldSpace, 0.0, 1.0);//Expand to vec4 for matrix multiplication
    vec4 finalPositionClip = u_projection * finalPositionWorldSpace; //Multiply by projection matrix to take camera position and zoom into account

    gl_Position = finalPositionClip;
    vf_uv = offset;
    vf_time = v_time[0] + (1.0 - (v_velocity[0] / 300.0)) * v_time[0] * 0.5;
    vf_velocity = v_velocity[0] / 300.0;

    vf_radius = scale;
    vf_light_pos = localPos;//Use this local pos to make light calculations easy
    vf_type = v_type[0];

    EmitVertex();
}

void main() 
{
    float time = v_time[0];

    if(time < 0.0 || time >= LIFE){
        return;
    }
    else
    {
    float scale = mix(size_spark, size_flame, (1.0 - clamp(v_velocity[0] / 250.0, 0.0, 1.0)));

    //Emit all 4 corners for a quad
    EmitVert(vec2(-1.0, -1.0), scale);
    EmitVert(vec2(-1.0, 1.0), scale);
    EmitVert(vec2(1.0, -1.0), scale);
    EmitVert(vec2(1.0, 1.0), scale);
    EndPrimitive();
    }


}  