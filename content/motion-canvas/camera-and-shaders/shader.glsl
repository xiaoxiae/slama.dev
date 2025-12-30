#version 300 es
precision highp float;

// use defaut inputs (called 'uniforms')
#include "@motion-canvas/core/shaders/common.glsl"


void main() {
    // sample the color at the UV of the current run of the shader
    outColor = texture(sourceTexture, sourceUV);

    // generate a random-ish color to make a nice gradient effect
    vec3 col = 0.5 + 0.5 * cos(time * 3.0 + sourceUV.xyx + vec3(0, 2, 4));

    // write the resulting color to the node
    outColor.rgb = col;
}