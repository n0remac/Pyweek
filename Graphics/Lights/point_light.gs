#version 330 core
layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

in vec3 v_color[];
in float v_radius[];

uniform mat4x4 u_projection;

out float vf_radius;
out vec2 vf_light_pos;
out vec3 vf_color;

void EmitVert(vec2 offset)
{
    vec2 localPos = offset * v_radius[0];
    vec2 posWorldSpace = gl_in[0].gl_Position.xy +localPos;

    vec4 finalPositionWorldSpace = vec4(posWorldSpace, 0.0, 1.0);//Expand to vec4 for matrix multiplication
    vec4 finalPositionClip = u_projection * finalPositionWorldSpace; //Multiply by projection matrix to take camera position and zoom into account

    gl_Position = finalPositionClip;
    vf_light_pos = localPos;//Use this local pos to make light calculations easy
    vf_color = v_color[0];//Pass color to fragment shader
    vf_radius = v_radius[0];
    EmitVertex();
}

void main() 
{
    //Emit all 4 corners for a quad
    EmitVert(vec2(-1.0, -1.0));
    EmitVert(vec2(-1.0, 1.0));
    EmitVert(vec2(1.0, -1.0));
    EmitVert(vec2(1.0, 1.0));
    EndPrimitive();
}  