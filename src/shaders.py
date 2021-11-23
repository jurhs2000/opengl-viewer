# GLSL

normal = {
  "vertex": """
    #version 450
    layout(location = 0) in vec3 position;
    layout(location = 1) in vec2 textCoords;
    layout(location = 2) in vec3 normal;

    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;
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
  """,
  "fragment": """
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
}

toon = {
  "vertex": """
    #version 450
    layout(location = 0) in vec3 position;
    layout(location = 1) in vec2 textCoords;
    layout(location = 2) in vec3 normal;

    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;
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
      outTextCoords = textCoords;
    }
  """,
  "fragment": """
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
}

gradient = {
  "vertex": """
    #version 450
    layout(location = 0) in vec3 position;
    layout(location = 1) in vec2 textCoords;
    layout(location = 2) in vec3 normal;

    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;
    uniform vec3 pointLight;
    uniform float currentTime;

    out vec3 outColor;
    out vec3 outPosition;
    out float outCurrentTime;

    void main()
    {
      vec4 norm = vec4(normal, 0.0);
      vec4 pos = vec4(position, 1.0);
      pos = modelMatrix * pos;
      vec4 light = vec4(pointLight, 1.0);
      float intensity = dot(modelMatrix * norm, normalize(light - pos));

      gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
      outColor = vec3(1.0, 1.0, 1.0) * intensity;
      outPosition = position;
      outCurrentTime = currentTime;
    }
  """,
  "fragment": """
    #version 450
    layout(location = 0) out vec4 fragColor;

    in vec3 outColor;
    in vec3 outPosition;
    in float outCurrentTime;

    uniform float maxY;
    uniform float minY;

    void main()
    {
      float height = maxY - minY;
      float y = outPosition.y;
      vec3 upColor = vec3(abs(sin(outCurrentTime / 5)), 0.0, 1 - abs(sin(outCurrentTime / 5)));
      vec3 downColor = vec3(abs(cos(outCurrentTime / 5)), 0.0, 1 - abs(cos(outCurrentTime / 5)));
      float b = (((y+abs(minY)) / height) * (upColor.x - downColor.x) + downColor.x);
      float g = (((y+abs(minY)) / height) * (upColor.y - downColor.y) + downColor.y);
      float r = (((y+abs(minY)) / height) * (upColor.z - downColor.z) + downColor.z);
      fragColor = vec4(r, g, b, 1.0) * vec4(outColor, 1.0);
    }
  """
}

highlight = {
  "vertex": """
    #version 450
    layout(location = 0) in vec3 position;
    layout(location = 1) in vec2 textCoords;
    layout(location = 2) in vec3 normal;

    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;

    out vec3 outNormal;
    out vec2 outTextCoords;

    void main()
    {
      vec4 pos = vec4(position, 1.0);
      pos = modelMatrix * pos;

      gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
      outTextCoords = textCoords;
      outNormal = normal;
    }
  """,
  "fragment": """
    #version 450
    layout(location = 0) out vec4 fragColor;

    in vec3 outNormal;
    in vec2 outTextCoords;

    uniform sampler2D textureSampler;
    uniform vec3 forwardVector;

    void main()
    {
      float parallel = dot(outNormal, forwardVector);
      fragColor = vec4(1.0, 1.0, 0.0, 1.0) * vec4(1 - parallel, 1 - parallel, 1 - parallel, 1.0) * 2;
      fragColor = fragColor * texture(textureSampler, outTextCoords);
    }
  """
}

textureBlend = {
  "vertex": """
    #version 450
    layout(location = 0) in vec3 position;
    layout(location = 1) in vec2 textCoords;
    layout(location = 2) in vec3 normal;

    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;
    uniform vec3 pointLight;

    out vec2 outTextCoords;
    out float outIntensity;

    void main()
    {
      vec4 norm = vec4(normal, 0.0);
      vec4 pos = vec4(position, 1.0);
      pos = modelMatrix * pos;
      vec4 light = vec4(pointLight, 1.0);
      float intensity = dot(modelMatrix * norm, normalize(light - pos));

      gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
      outTextCoords = textCoords;
      outIntensity = intensity;
    }
  """,
  "fragment": """
    #version 450
    layout(location = 0) out vec4 fragColor;

    in vec2 outTextCoords;
    in float outIntensity;

    uniform sampler2D textureSampler;
    uniform sampler2D textureSampler2;

    void main()
    {
      fragColor = vec4(outIntensity, outIntensity, outIntensity, 1.0) * texture(textureSampler, outTextCoords);
      fragColor = fragColor + vec4(1 - outIntensity, 1 - outIntensity, 1 - outIntensity, 1.0) * texture(textureSampler2, outTextCoords);
    }
  """
}
