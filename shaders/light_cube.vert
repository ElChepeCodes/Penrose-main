#version 330 core
layout (location = 0) in vec3 aPos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 rotation;
void main()
{
    gl_Position = projection * view * inverse(model) * rotation * vec4(aPos, 1.0);
}