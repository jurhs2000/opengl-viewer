# GLSL

default = {
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
    uniform float value;

    out float intensity;
    out vec2 outTextCoords;
    out float outValue;

    void main()
    {
      vec4 norm = vec4(normal, 0.0);
      vec4 pos = vec4(position, 1.0);
      pos = modelMatrix * pos;
      vec4 light = vec4(pointLight, 1.0);
      intensity = dot(modelMatrix * norm, normalize(light - pos));

      gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
      outTextCoords = textCoords;
      outValue = value;
    }
  """,
  "fragment": """
    #version 450
    layout(location = 0) out vec4 fragColor;

    in float intensity;
    in vec2 outTextCoords;
    in float outValue;

    uniform sampler2D textureSampler;

    void main()
    {
      if (intensity > 0.9 * (outValue + 0.9)) {
        fragColor = vec4(1.0, 1.0, 1.0, 1.0) * texture(textureSampler, outTextCoords);
      } else if (intensity > 0.75 * (outValue + 0.8)) {
        fragColor = vec4(0.8, 0.8, 0.8, 1.0) * texture(textureSampler, outTextCoords);
      } else if (intensity > 0.6 * (outValue + 0.7)) {
        fragColor = vec4(0.6, 0.6, 0.6, 1.0) * texture(textureSampler, outTextCoords);
      } else if (intensity > 0.3 * (outValue + 0.6)) {
        fragColor = vec4(0.4, 0.4, 0.4, 1.0) * texture(textureSampler, outTextCoords);
      } else {
        fragColor = vec4(0.2, 0.2, 0.2, 1.0) * texture(textureSampler, outTextCoords);
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
    uniform float value;

    out vec3 outColor;
    out vec3 outPosition;
    out float outCurrentTime;
    out float outValue;

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
      outValue = value;
    }
  """,
  "fragment": """
    #version 450
    layout(location = 0) out vec4 fragColor;

    in vec3 outColor;
    in vec3 outPosition;
    in float outCurrentTime;
    in float outValue;

    uniform float maxY;
    uniform float minY;

    void main()
    {
      float height = maxY - minY;
      float y = outPosition.y;
      vec3 upColor = vec3(abs(sin(outCurrentTime / 5)), 0.0 + (1 * (outValue)), 1 - abs(sin(outCurrentTime / 5)));
      vec3 downColor = vec3(abs(cos(outCurrentTime / 5)), 0.0 + (1 * (outValue)), 1 - abs(cos(outCurrentTime / 5)));
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
    uniform float value;

    out vec3 outNormal;
    out vec2 outTextCoords;
    out float outValue;

    void main()
    {
      vec4 pos = vec4(position, 1.0);
      pos = modelMatrix * pos;

      gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
      outTextCoords = textCoords;
      outNormal = normal;
      outValue = value;
    }
  """,
  "fragment": """
    #version 450
    layout(location = 0) out vec4 fragColor;

    in vec3 outNormal;
    in vec2 outTextCoords;
    in float outValue;

    uniform sampler2D textureSampler;
    uniform vec3 forwardVector;

    void main()
    {
      float parallel = dot(outNormal, forwardVector);
      fragColor = vec4(1.0 * (1 - outValue), 1.0 * (1 - outValue), 0.0 + outValue, 1.0) * vec4(1 - parallel, 1 - parallel, 1 - parallel, 1.0) * 2;
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

normalMap = {
  "vertex": """
    #version 450
    layout(location = 0) in vec3 position;
    layout(location = 1) in vec2 textCoords;
    layout(location = 2) in vec3 normal;
    layout(location = 3) in vec3 tangent;
    layout(location = 4) in vec3 bitangent;

    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;
    uniform vec3 pointLight;
    uniform vec3 camPos;

    out vec2 outTextCoords;
    out float outIntensity;
    out mat3 TBN;
    out vec3 outCamPos;

    void main()
    {
      vec4 norm = vec4(normal, 0.0);
      vec4 pos = vec4(position, 1.0);
      pos = modelMatrix * pos;
      vec4 light = vec4(pointLight, 1.0);
      float intensity = dot(modelMatrix * norm, normalize(light - pos));

      vec3 T = normalize(vec3(modelMatrix * vec4(tangent, 0.0)));
      vec3 B = normalize(vec3(modelMatrix * vec4(bitangent, 0.0)));
      vec3 N = normalize(vec3(modelMatrix * vec4(normal, 0.0)));
      TBN = mat3(T, B, N);

      gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
      outTextCoords = textCoords;
      outIntensity = intensity;
      outCamPos = camPos;
    }
  """,
  "fragment": """
    #version 450
    layout(location = 0) out vec4 fragColor;

    in vec2 outTextCoords;
    in float outIntensity;
    in mat3 TBN;
    in vec3 outCamPos;

    uniform sampler2D textureSampler;
    uniform sampler2D normalMap;

    vec3 matMult(mat3 m, vec3 v) {
      vec3 result;
      for (int i = 0; i < 3; i++) {
        float element = 0.0;
        for (int j = 0; j < 3; j++) {
          element += m[i][j] * v[j];
        }
        result[i] = element;
      }
      return result;
    }

    void main()
    {
      vec4 textureNormal = vec4(1.0, 1.0, 1.0, 1.0) * texture(normalMap, outTextCoords);
      vec3 textureNormalTan = matMult(TBN, vec3(textureNormal.x, textureNormal.y, textureNormal.z));
      textureNormalTan = normalize(textureNormalTan);
      float intensity = dot(textureNormalTan, vec3(-outCamPos.x, -outCamPos.y, -outCamPos.z));
      fragColor = texture(textureSampler, outTextCoords) * vec4(intensity, intensity, intensity, 1.0);
    }
  """
}

wave = {
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
    uniform float value;

    out vec3 outColor;
    out vec3 outPosition;
    out float outCurrentTime;

    void main()
    {
      vec4 norm = vec4(normal, 0.0);
      vec4 pos = vec4(position.x + sin(currentTime * (value+1) * 3 + position.y) * 0.1 * (value+1), position.y, position.z, 1.0);
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

    float PHI = 1.61803398874989484820459;  // Φ = Golden Ratio   

    highp float rand(vec2 co)
    {
      highp float a = 12.9898;
      highp float b = 78.233;
      highp float c = 43758.5453;
      highp float dt= dot(co.xy ,vec2(a,b));
      highp float sn= mod(dt,3.14);
      return fract(sin(sn) * c);
    }
    void main()
    {
      float height = maxY - minY;
      float y = outPosition.y;
      fragColor = vec4(rand(vec2(outPosition.x, y)), rand(vec2(outPosition.x, y)), rand(vec2(outPosition.x, y)), 1.0) * vec4(outColor, 1.0);
    }
  """
}