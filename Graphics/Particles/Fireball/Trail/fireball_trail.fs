#version 330


in float vf_time;
in vec2 vf_uv;

out vec4 out_color;

const float LIFE = 4.0;

void main() {

    float toCenter = length(vf_uv);

    
    float falloff_factor = toCenter / 1.0;

    float trashy_falloff = 1.0 - falloff_factor;
    trashy_falloff = clamp(trashy_falloff, 0.0, 1.0);

    //vec3 finalLight = vec3(1.0, 0.3, 0.05) * trashy_falloff * trashy_falloff;//Ensure falloff is quadradic
    vec3 finalLight = vec3(1.0, 0.3, 0.05) * 2.0;

    finalLight *= 1.0 - smoothstep(1.0, 3.0, vf_time);

    out_color =vec4(finalLight, 1.0);
}