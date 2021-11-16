# GLSL

vertex = """
#version 450
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 textCoords;
layout(location = 2) in vec3 normal;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float currentTime;
uniform float value;
uniform vec3 pointLight;

out vec3 outColor;
out vec2 outTextCoords;

void main()
{
  vec4 norm = vec4(normal, 0.0);
  vec4 pos = vec4(position, 1.0) + norm * value;
  pos = modelMatrix * pos;
  vec4 light = vec4(pointLight, 1.0);
  float intensity = dot(modelMatrix * norm, normalize(light - pos));

  gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
  outColor = vec3(1.0, 1.0 - value, 1.0 - value) * intensity;
  outTextCoords = textCoords;
}
"""

fragment = """
#version 450
layout(location = 0) out vec4 fragColor;

in vec3 outColor;
in vec2 outTextCoords;

uniform sampler2D textureSampler;

void main()
{
  fragColor = vec4(outColor, 1.0) * texture(textureSampler, outTextCoords);
}
"""

# toon shader
toon_vertex = """
#version 450
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 textCoords;
layout(location = 2) in vec3 normal;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float currentTime;
uniform vec3 pointLight;

out float intensity;
out vec2 outTextCoords;

void main()
{
  vec4 norm = vec4(normal, 0.0);
  vec4 pos = vec4(position, 1.0);
  pos = modelMatrix * pos;
  vec4 light = vec4(pointLight, 1.0);
  intensity = dot(modelMatrix * norm, normalize(light - pos));

  gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
  // toon shader relative to intensity
  
  outTextCoords = textCoords;
}
"""

toon_fragment = """
#version 450
layout(location = 0) out vec4 fragColor;

in float intensity;
in vec2 outTextCoords;

uniform sampler2D textureSampler;

void main()
{
  if (intensity > 0.9) {
    fragColor = vec4(1.0, 1.0, 1.0, 1.0) * texture(textureSampler, outTextCoords);
  } else if (intensity > 0.6) {
    fragColor = vec4(0.8, 0.8, 0.8, 1.0) * texture(textureSampler, outTextCoords);
  } else if (intensity > 0.3) {
    fragColor = vec4(0.6, 0.6, 0.6, 1.0) * texture(textureSampler, outTextCoords);
  } else {
    fragColor = vec4(0.3, 0.3, 0.3, 1.0) * texture(textureSampler, outTextCoords);
  }
}
"""
