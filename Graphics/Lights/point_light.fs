#version 330


in float vf_radius;
in vec2 vf_light_pos;
in vec3 vf_color;


out vec4 out_color;

void main() {

    float toCenter = length(vf_light_pos);

    
    float falloff_factor = toCenter / vf_radius;

    float trashy_falloff = 1.0 - falloff_factor;
    trashy_falloff = clamp(trashy_falloff, 0.0, 1.0);

    vec3 finalLight = vf_color * trashy_falloff * trashy_falloff;//Ensure falloff is quadradic

    out_color =vec4(finalLight, 0.0);
}