#version 330

in vec2 v_uv;
out vec4 out_color;

uniform sampler2D t_scene;
uniform sampler2D t_lights;

uniform vec3 u_ambient;

void main() {
    vec4 scene_color = texture(t_scene, v_uv);
    vec3 light = texture(t_lights, v_uv).rgb;

    vec4 final_color = scene_color;
    final_color.rgb *= (light + u_ambient);

    out_color = final_color;
}