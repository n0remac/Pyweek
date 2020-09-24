#version 330 core
layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

in float v_time[];
in int v_type[];

uniform float u_time;
uniform mat4x4 u_projection;

out float vf_time;
out vec2 vf_uv;
flat out int vf_type;

const float SIZE[] = float[](6.0, 3.0, 6.0);

const float size_start_c = -0.;
const float size_end_c = 1.3;

const float LIFE[] = float[](0.35, 0.35, 0.45);


float GetLifePercent(){
    return v_time[0] / LIFE[v_type[0]];
}

float GetSize(){

    if(v_type[0] == 2){
        float scale = max(1.0, 4.0 - 30.0 * v_time[0]);
        return scale;
    }

    float f = cos(mix(size_start_c, size_end_c, GetLifePercent()));
    return SIZE[v_type[0]] * f;
}

void EmitVert(vec2 offset)
{
    vec2 localPos = offset * GetSize();
    vec2 posWorldSpace = gl_in[0].gl_Position.xy +localPos;

    vec4 finalPositionWorldSpace = vec4(posWorldSpace, 0.0, 1.0);//Expand to vec4 for matrix multiplication
    vec4 finalPositionClip = u_projection * finalPositionWorldSpace; //Multiply by projection matrix to take camera position and zoom into account

    gl_Position = finalPositionClip;
    vf_uv = offset;
    vf_time = v_time[0];
    vf_type = v_type[0];
    EmitVertex();
}

void main() 
{
    float time = v_time[0];

    if(time < 0.0 || time >= LIFE[v_type[0]]){
        return;
    }



    //Emit all 4 corners for a quad
    EmitVert(vec2(-1.0, -1.0));
    EmitVert(vec2(-1.0, 1.0));
    EmitVert(vec2(1.0, -1.0));
    EmitVert(vec2(1.0, 1.0));
    EndPrimitive();
}  