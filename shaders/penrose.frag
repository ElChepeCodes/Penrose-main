#version 330
        out vec4 Color;
        uniform vec3 triangleColor;
        void main() {
                Color = vec4(triangleColor.x, triangleColor.y, triangleColor.z, 0.3f);
        }
