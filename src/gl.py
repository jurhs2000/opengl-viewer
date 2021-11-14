import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from pygame import image
from numpy import array, float32
from objLoader import Obj

class Model(object):
  def __init__(self, objName, textureName):
    self.model = Obj(objName)
    self.createVertexBuffer()
    self.pos = glm.vec3(0.0, 0.0, 0.0)
    self.rot = glm.vec3(0.0, 0.0, 0.0)
    self.scale = glm.vec3(1.0, 1.0, 1.0)

    self.textureSurface = image.load(textureName)
    self.textureData = image.tostring(self.textureSurface, "RGB", True)
    self.texture = glGenTextures(1)

  def getModelMatrix(self):
    identity = glm.mat4(1)
    translateMatrix = glm.translate(identity, self.pos)

    pitch = glm.rotate(identity, glm.radians(self.rot.x), glm.vec3(1, 0, 0))
    yaw = glm.rotate(identity, glm.radians(self.rot.y), glm.vec3(0, 1, 0))
    roll = glm.rotate(identity, glm.radians(self.rot.z), glm.vec3(0, 0, 1))

    rotationMatrix = pitch * yaw * roll
    scaleMatrix = glm.scale(identity, self.scale)
    return translateMatrix * rotationMatrix * scaleMatrix

  def createVertexBuffer(self):
    buffer = []
    for face in self.model.faces:
      for i in range(3):
        position = self.model.vertices[face[i][0] - 1]
        buffer.append(position[0])
        buffer.append(position[1])
        buffer.append(position[2])
        uvs = self.model.textcoords[face[i][1] - 1]
        buffer.append(uvs[0])
        buffer.append(uvs[1])
        normal = self.model.normals[face[i][2] - 1]
        buffer.append(normal[0])
        buffer.append(normal[1])
        buffer.append(normal[2])
    self.vertBuffer = array(buffer, dtype=float32)

    self.VBO = glGenBuffers(1) # Vertex Buffer Object
    self.VAO = glGenVertexArrays(1) # Vertex Array Object

  def renderInScene(self):
    glBindVertexArray(self.VAO)
    glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
    glBufferData(GL_ARRAY_BUFFER, self.vertBuffer.nbytes, self.vertBuffer, GL_STATIC_DRAW) # Buffer ID, Buffer size in bytes, Buffer data, Usage
    # Position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 8, ctypes.c_void_p(0)) # Attribute ID, Number of components per vertex, Data type, Normalize data, Stride, Offset
    glEnableVertexAttribArray(0)
    # Texture coords attribute
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * 8, ctypes.c_void_p(4 * 3)) # Attribute ID, Number of components per vertex, Data type, Normalize data, Stride, Offset
    glEnableVertexAttribArray(1)
    # Normal attribute
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 4 * 8, ctypes.c_void_p(4 * 5)) # Attribute ID, Number of components per vertex, Data type, Normalize data, Stride, Offset
    glEnableVertexAttribArray(2)
    # Bind texture
    glBindTexture(GL_TEXTURE_2D, self.texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.textureSurface.get_width(), self.textureSurface.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, self.textureData)
    glGenerateMipmap(GL_TEXTURE_2D)

    glDrawArrays(GL_TRIANGLES, 0, len(self.model.faces) * 3)
    #glDrawElements(GL_TRIANGLES, len(self.indexBuffer), GL_UNSIGNED_INT, None)

class Renderer(object):
  def __init__(self, screen):
    self.screen = screen
    _, _, self.width, self.height = screen.get_rect()

    glEnable(GL_DEPTH_TEST)
    glViewport(0, 0, self.width, self.height)

    self.scene = []
    self.pointLight = glm.vec3(-10, 5, -5)

    # View matrix
    self.camPos = glm.vec3(0.0, 0.0, 0.0)
    self.camRot = glm.vec3(0.0, 0.0, 0.0) # pitch, yaw, roll
    self.fov = 60
    self.currentTime = 0
    self.value = 0

    self.projectionMatrix = glm.perspective(glm.radians(self.fov), self.width / self.height, 0.1, 1000) # fov, aspect ratio, near plane, far plane

  def getViewMatrix(self):
    identity = glm.mat4(1)
    translateMatrix = glm.translate(identity, self.camPos)

    pitch = glm.rotate(identity, glm.radians(self.camRot.x), glm.vec3(1, 0, 0))
    yaw = glm.rotate(identity, glm.radians(self.camRot.y), glm.vec3(0, 1, 0))
    roll = glm.rotate(identity, glm.radians(self.camRot.z), glm.vec3(0, 0, 1))

    rotationMatrix = pitch * yaw * roll
    camMatrix = translateMatrix * rotationMatrix
    return glm.inverse(camMatrix)

  def wireframeMode(self):
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

  def filledMode(self):
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

  def setShaders(self, vertexShader, fragmentShader):
    if vertexShader is not None and fragmentShader is not None:
      self.activeShader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER), compileShader(fragmentShader, GL_FRAGMENT_SHADER))
    else:
      self.activeShader = None

  def render(self):
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUseProgram(self.activeShader)

    if self.activeShader:
        glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "viewMatrix"), 1, GL_FALSE, glm.value_ptr(self.getViewMatrix()))
        glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "projectionMatrix"), 1, GL_FALSE, glm.value_ptr(self.projectionMatrix))
        glUniform1f(glGetUniformLocation(self.activeShader, "currentTime"), self.currentTime)
        glUniform1f(glGetUniformLocation(self.activeShader, "value"), self.value)
        glUniform3f(glGetUniformLocation(self.activeShader, "pointLight"), self.pointLight.x, self.pointLight.y, self.pointLight.z)

    for obj in self.scene:
      if self.activeShader:
        glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "modelMatrix"), 1, GL_FALSE, glm.value_ptr(obj.getModelMatrix()))
      obj.renderInScene()