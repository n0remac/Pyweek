#version 330


in float vf_time;
in vec2 vf_uv;
in float vf_velocity;
flat in int vf_type;

out vec4 out_color;

const float LIFE = 0.8;

 vec3 ColorA[3] = vec3[](
    vec3(1.0, 0.3, 0.05),
    vec3(0.05, 0.3, 1.00),
    vec3(0.8, 0.93, 0.85)
 );

void main() {

    float toCenter = length(vf_uv);

    
    float falloff_factor = toCenter / 1.0;

    float trashy_falloff = 1.0 - falloff_factor;
    trashy_falloff = clamp(trashy_falloff, 0.0, 1.0);

    //vec3 finalLight = vec3(1.0, 0.3, 0.05) * trashy_falloff * trashy_falloff;//Ensure falloff is quadradic
    vec3 finalLight = trashy_falloff * trashy_falloff * ColorA[vf_type] * mix(1.5, 3.0, pow(vf_velocity, 3)) ;



    finalLight *= smoothstep(0.0, LIFE, LIFE - vf_time);

    finalLight = max(vec3(0.0), finalLight);

    out_color =vec4(finalLight, 1.0);
}