vertex_src = """
# version 330 core
layout(location=0) in vec3 vertex_position;
layout(location=1) in vec3 vertex_normal;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 model;
out vec2 z_t;
void main(){
    gl_Position=projection*view*model*vec4(vertex_position, 1.0);
    z_t = vec2(vertex_position.z/7.8, vertex_normal.z);
}
"""

fragment_src = """
# version 330 core
in vec2 z_t;
uniform vec4 color;
out vec4 FragColor;

void main(){
    FragColor=vec4((z_t.x)*(z_t.x), -4*(z_t.x)*(z_t.x)+4*z_t.x, 1-z_t.x*(z_t.x), 1.0);
}
"""
