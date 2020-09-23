#version 330 core
layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

in float v_time[];

uniform float u_time;
uniform mat4x4 u_projection;

out float vf_time;
out vec2 vf_uv;

const float SIZE = 1.5;

void EmitVert(vec2 offset)
{
    vec2 localPos = offset * SIZE;
    vec2 posWorldSpace = gl_in[0].gl_Position.xy +localPos;

    vec4 finalPositionWorldSpace = vec4(posWorldSpace, 0.0, 1.0);//Expand to vec4 for matrix multiplication
    vec4 finalPositionClip = u_projection * finalPositionWorldSpace; //Multiply by projection matrix to take camera position and zoom into account

    gl_Position = finalPositionClip;
    vf_uv = offset;
    vf_time = v_time[0];
    EmitVertex();
}

void main() 
{
    float time = v_time[0];

    if(time < 0.0 || time >= 2.0){
        return;
    }

    //Emit all 4 corners for a quad
    EmitVert(vec2(-1.0, -1.0));
    EmitVert(vec2(-1.0, 1.0));
    EmitVert(vec2(1.0, -1.0));
    EmitVert(vec2(1.0, 1.0));
    EndPrimitive();
}  