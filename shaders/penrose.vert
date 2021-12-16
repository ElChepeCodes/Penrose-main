#version 330
        layout (location = 0) in vec3 position;
        uniform mat4 traslation;
        uniform mat4 rotation;
        uniform mat4 scaling;
        uniform mat4 view;
        uniform mat4 projection;
        out vec3 v_color;
        out vec2 v_texture;
        void main() {
        gl_Position = projection * view * scaling * rotation * vec4(position.x * 1.5, position.y * 1.5, position.z * 1.5, 1.0);

    }