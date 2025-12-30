#version 300 es
precision highp float;

#include "@motion-canvas/core/shaders/common.glsl"


void main() {
    outColor = texture(destinationTexture, destinationUV);

    // write the resulting color to the node
    outColor.rgb = vec3(outColor.r, outColor.g, outColor.b);
}