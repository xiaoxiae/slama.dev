#version 300 es
precision highp float;

#include "@motion-canvas/core/shaders/common.glsl"

uniform vec2 aPos;
uniform float aOpacity;
uniform vec2 aScale;

uniform vec2 bPos;
uniform float bOpacity;
uniform vec2 bScale;

/**
 * A shader that creates an effect of regions around objects A and B.
 * The intensities and colors are based on their positions, scale and opacity.
 */
void main() {
    // Convert object positions from screen coordinates to normalized (0 to 1)
    vec2 aNormalized = (aPos + resolution / 2.0) / resolution;
    vec2 bNormalized = (bPos + resolution / 2.0) / resolution;

    // Compute the distance from the UV to object A and object B
    // We have to account for the fact that resolution might not be square!
    vec2 vecA = sourceUV - aNormalized;
    vecA.x *= resolution.x / resolution.y;

    vec2 vecB = sourceUV - bNormalized;
    vecB.x *= resolution.x / resolution.y;

    float distA = pow(length(vecA), 2.0 * aScale.x);
    float distB = pow(length(vecB), 2.0 * bScale.x);

    // Normalize the influences so they sum to 1
    float totalDistance = distA + distB;
    float distInfluenceA = distA / totalDistance;
    float distInfluenceB = distB / totalDistance;

    // the colors are flipped because the larger the distance, the smaller the color
    vec3 colorA = vec3(aOpacity * 0.5, 0.0, 0.0);
    vec3 colorB = vec3(0.0, 0.0, bOpacity * 0.5);

    // Final color is a weighted blend of colorA and colorB based on influence
    vec3 blendedColor = distInfluenceB * colorA + distInfluenceA * colorB;

    // Output the final color with full opacity
    outColor = vec4(blendedColor, 1.0);
}
