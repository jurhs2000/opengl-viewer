import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from pygame import image
from numpy import array, float32
import math
from objLoader import Obj

class Model(object):
  def __init__(self, id, objName, textureName, textureName2, normalMapName, scale, pos):
    self.id = id
    self.model = Obj(objName)
    self.createVertexBuffer()
    self.pos = glm.vec3(pos[0], pos[1], pos[2])
    self.rot = glm.vec3(0.0, 0.0, 0.0)
    self.scale = glm.vec3(scale[0], scale[1], scale[2])

    self.textureSurface = image.load(textureName)
    self.textureData = image.tostring(self.textureSurface, "RGB", True)
    self.texture = glGenTextures(1)

    if textureName2 != None:
      self.textureSurface2 = image.load(textureName2)
      self.textureData2 = image.tostring(self.textureSurface2, "RGB", True)
      self.texture2 = glGenTextures(1)
    else:
      self.texture2 = None

    if normalMapName != None:
      self.normalMapSurface = image.load(normalMapName)
      self.normalMapData = image.tostring(self.normalMapSurface, "RGB", True)
      self.normalMap = glGenTextures(1)
    else:
      self.normalMap = None

    self.maxY = -float('inf')
    self.minY = float('inf')
    for face in self.model.faces:
      for v in face:
        self.maxY = max(self.maxY, self.model.vertices[v[0] - 1][1])
        self.minY = min(self.minY, self.model.vertices[v[0] - 1][1])

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
      vertCount = len(face)
      if vertCount == 3:
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
          A = self.model.vertices[face[0][0] - 1]
          B = self.model.vertices[face[1][0] - 1]
          C = self.model.vertices[face[2][0] - 1]
          uvsA = self.model.textcoords[face[0][1] - 1]
          uvsB = self.model.textcoords[face[1][1] - 1]
          uvsC = self.model.textcoords[face[2][1] - 1]
          edge1 = [B[0] - A[0], B[1] - A[1], B[2] - A[2]]
          edge2 = [C[0] - A[0], C[1] - A[1], C[2] - A[2]]
          deltaUV1 = [uvsB[0] - uvsA[0], uvsB[1] - uvsA[1]]
          deltaUV2 = [uvsC[0] - uvsA[0], uvsC[1] - uvsA[1]]
          try:
            f = 1.0 / (deltaUV1[0] * deltaUV2[1] - deltaUV1[1] * deltaUV2[0])
          except ZeroDivisionError:
            f = 999999
          tangent = glm.vec3((f * (deltaUV2[1] * edge1[0] - deltaUV1[1] * edge2[0])), (f * (deltaUV2[1] * edge1[1] - deltaUV1[1] * edge2[1])), (f * (deltaUV2[1] * edge1[2] - deltaUV1[1] * edge2[2])))
          self.tangent = glm.normalize(tangent)
          bitangent = glm.vec3((f * (-deltaUV2[0] * edge1[0] + deltaUV1[0] * edge2[0])), (f * (-deltaUV2[0] * edge1[1] + deltaUV1[0] * edge2[1])), (f * (-deltaUV2[0] * edge1[2] + deltaUV1[0] * edge2[2])))
          self.bitangent = glm.normalize(bitangent)
          buffer.append(self.tangent.x)
          buffer.append(self.tangent.y)
          buffer.append(self.tangent.z)
          buffer.append(self.bitangent.x)
          buffer.append(self.bitangent.y)
          buffer.append(self.bitangent.z)
      elif vertCount == 4:
        for i in range(3):
          if i == 0:
            position = self.model.vertices[face[0][0] - 1]
            uvs = self.model.textcoords[face[0][1] - 1]
            normal = self.model.normals[face[0][2] - 1]
          if i == 1:
            position = self.model.vertices[face[1][0] - 1]
            uvs = self.model.textcoords[face[1][1] - 1]
            normal = self.model.normals[face[1][2] - 1]
          if i == 2:
            position = self.model.vertices[face[2][0] - 1]
            uvs = self.model.textcoords[face[2][1] - 1]
            normal = self.model.normals[face[2][2] - 1]
          buffer.append(position[0])
          buffer.append(position[1])
          buffer.append(position[2])
          buffer.append(uvs[0])
          buffer.append(uvs[1])
          buffer.append(normal[0])
          buffer.append(normal[1])
          buffer.append(normal[2])
          A = self.model.vertices[face[0][0] - 1]
          B = self.model.vertices[face[1][0] - 1]
          C = self.model.vertices[face[2][0] - 1]
          uvsA = self.model.textcoords[face[0][1] - 1]
          uvsB = self.model.textcoords[face[1][1] - 1]
          uvsC = self.model.textcoords[face[2][1] - 1]
          edge1 = [B[0] - A[0], B[1] - A[1], B[2] - A[2]]
          edge2 = [C[0] - A[0], C[1] - A[1], C[2] - A[2]]
          deltaUV1 = [uvsB[0] - uvsA[0], uvsB[1] - uvsA[1]]
          deltaUV2 = [uvsC[0] - uvsA[0], uvsC[1] - uvsA[1]]
          try:
            f = 1.0 / (deltaUV1[0] * deltaUV2[1] - deltaUV1[1] * deltaUV2[0])
          except ZeroDivisionError:
            f = 999999
          tangent = glm.vec3((f * (deltaUV2[1] * edge1[0] - deltaUV1[1] * edge2[0])), (f * (deltaUV2[1] * edge1[1] - deltaUV1[1] * edge2[1])), (f * (deltaUV2[1] * edge1[2] - deltaUV1[1] * edge2[2])))
          self.tangent = glm.normalize(tangent)
          bitangent = glm.vec3((f * (-deltaUV2[0] * edge1[0] + deltaUV1[0] * edge2[0])), (f * (-deltaUV2[0] * edge1[1] + deltaUV1[0] * edge2[1])), (f * (-deltaUV2[0] * edge1[2] + deltaUV1[0] * edge2[2])))
          self.bitangent = glm.normalize(bitangent)
          buffer.append(self.tangent.x)
          buffer.append(self.tangent.y)
          buffer.append(self.tangent.z)
          buffer.append(self.bitangent.x)
          buffer.append(self.bitangent.y)
          buffer.append(self.bitangent.z)
        
        for i in range(3):
          if i == 0:
            position = self.model.vertices[face[0][0] - 1]
            uvs = self.model.textcoords[face[0][1] - 1]
            normal = self.model.normals[face[0][2] - 1]
          if i == 1:
            position = self.model.vertices[face[2][0] - 1]
            uvs = self.model.textcoords[face[2][1] - 1]
            normal = self.model.normals[face[2][2] - 1]
          if i == 2:
            position = self.model.vertices[face[3][0] - 1]
            uvs = self.model.textcoords[face[3][1] - 1]
            normal = self.model.normals[face[3][2] - 1]
          buffer.append(position[0])
          buffer.append(position[1])
          buffer.append(position[2])
          buffer.append(uvs[0])
          buffer.append(uvs[1])
          buffer.append(normal[0])
          buffer.append(normal[1])
          buffer.append(normal[2])
          A = self.model.vertices[face[0][0] - 1]
          B = self.model.vertices[face[1][0] - 1]
          C = self.model.vertices[face[2][0] - 1]
          uvsA = self.model.textcoords[face[0][1] - 1]
          uvsB = self.model.textcoords[face[1][1] - 1]
          uvsC = self.model.textcoords[face[2][1] - 1]
          edge1 = [B[0] - A[0], B[1] - A[1], B[2] - A[2]]
          edge2 = [C[0] - A[0], C[1] - A[1], C[2] - A[2]]
          deltaUV1 = [uvsB[0] - uvsA[0], uvsB[1] - uvsA[1]]
          deltaUV2 = [uvsC[0] - uvsA[0], uvsC[1] - uvsA[1]]
          try:
            f = 1.0 / (deltaUV1[0] * deltaUV2[1] - deltaUV1[1] * deltaUV2[0])
          except ZeroDivisionError:
            f = 999999
          tangent = glm.vec3((f * (deltaUV2[1] * edge1[0] - deltaUV1[1] * edge2[0])), (f * (deltaUV2[1] * edge1[1] - deltaUV1[1] * edge2[1])), (f * (deltaUV2[1] * edge1[2] - deltaUV1[1] * edge2[2])))
          self.tangent = glm.normalize(tangent)
          bitangent = glm.vec3((f * (-deltaUV2[0] * edge1[0] + deltaUV1[0] * edge2[0])), (f * (-deltaUV2[0] * edge1[1] + deltaUV1[0] * edge2[1])), (f * (-deltaUV2[0] * edge1[2] + deltaUV1[0] * edge2[2])))
          self.bitangent = glm.normalize(bitangent)
          buffer.append(self.tangent.x)
          buffer.append(self.tangent.y)
          buffer.append(self.tangent.z)
          buffer.append(self.bitangent.x)
          buffer.append(self.bitangent.y)
          buffer.append(self.bitangent.z)
          
    self.vertBuffer = array(buffer, dtype=float32)

    self.VBO = glGenBuffers(1) # Vertex Buffer Object
    self.VAO = glGenVertexArrays(1) # Vertex Array Object

  def renderInScene(self):
    glBindVertexArray(self.VAO)
    glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
    glBufferData(GL_ARRAY_BUFFER, self.vertBuffer.nbytes, self.vertBuffer, GL_STATIC_DRAW) # Buffer ID, Buffer size in bytes, Buffer data, Usage
    # Position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 14, ctypes.c_void_p(0)) # Attribute ID, Number of components per vertex, Data type, Normalize data, Stride, Offset
    glEnableVertexAttribArray(0)
    # Texture coords attribute
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * 14, ctypes.c_void_p(4 * 3)) # Attribute ID, Number of components per vertex, Data type, Normalize data, Stride, Offset
    glEnableVertexAttribArray(1)
    # Normal attribute
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 4 * 14, ctypes.c_void_p(4 * 5)) # Attribute ID, Number of components per vertex, Data type, Normalize data, Stride, Offset
    glEnableVertexAttribArray(2)
    # Tangent attribute
    glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 4 * 14, ctypes.c_void_p(4 * 8)) # Attribute ID, Number of components per vertex, Data type, Normalize data, Stride, Offset
    glEnableVertexAttribArray(3)
    # Bitangent attribute
    glVertexAttribPointer(4, 3, GL_FLOAT, GL_FALSE, 4 * 14, ctypes.c_void_p(4 * 11)) # Attribute ID, Number of components per vertex, Data type, Normalize data, Stride, Offset
    glEnableVertexAttribArray(4)
    # Bind texture
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, self.texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.textureSurface.get_width(), self.textureSurface.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, self.textureData)
    glGenerateMipmap(GL_TEXTURE_2D)
    # Bind texture 2
    if self.texture2 != None:
      glActiveTexture(GL_TEXTURE1)
      glBindTexture(GL_TEXTURE_2D, self.texture2)
      glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.textureSurface2.get_width(), self.textureSurface2.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, self.textureData2)
      glGenerateMipmap(GL_TEXTURE_2D)
    # Bind normal map
    if self.normalMap != None:
      glActiveTexture(GL_TEXTURE2)
      glBindTexture(GL_TEXTURE_2D, self.normalMap)
      glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.normalMapSurface.get_width(), self.normalMapSurface.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, self.normalMapData)
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
    self.pointLight = glm.vec3(8, 5, 5)

    # View matrix
    self.camPos = glm.vec3(0.0, 0.0, -10.0)
    self.camRotRef = glm.vec3(0.0, 0.0, 0.0) # pitch, yaw, roll
    self.fov = 60
    self.currentTime = 0
    self.value = 0
    self.actualModel = 0
    self.cameraMinDistance = 1
    self.cameraMaxDistance = 25
    self.target = glm.vec3(0.0, 0.0, 0.0)
    self.viewMatrix = glm.lookAt(self.target - self.camPos, self.target, glm.vec3(0, 1, 0))

    self.projectionMatrix = glm.perspective(glm.radians(self.fov), self.width / self.height, 0.1, 1000) # fov, aspect ratio, near plane, far plane

  def cameraMovement(self, type):
    dx = ((self.camPos.x - self.target.x)**2 + (self.camPos.z - self.target.z)**2)**0.5
    dy = ((self.camPos.y - self.target.y)**2 + (self.camPos.z - self.target.z)**2)**0.5
    if type == "forward":
      # move camera forward along the direction it is facing
      self.camPos -= glm.vec3(self.camPos.x - self.target.x, self.camPos.y - self.target.y, self.camPos.z - self.target.z) * 0.1
    elif type == "backward":
      self.camPos += glm.vec3(self.camPos.x - self.target.x, self.camPos.y - self.target.y, self.camPos.z - self.target.z) * 0.1
    elif type == "left":
      if math.copysign(1, self.camPos.z) != math.copysign(1, -glm.cos(glm.radians(self.camRotRef.x - 1)) * dx):
        self.camRotRef += glm.vec3(0, 0, 180)
      self.camRotRef += glm.vec3(-1, 0, 0)
      self.camPos.x = -glm.sin(glm.radians(self.camRotRef.x)) * dx
      self.camPos.z = -glm.cos(glm.radians(self.camRotRef.x)) * dx
    elif type == "right":
      if math.copysign(1, self.camPos.z) != math.copysign(1, -glm.cos(glm.radians(self.camRotRef.x + 1)) * dx):
        self.camRotRef += glm.vec3(0, 0, 180)
      self.camRotRef -= glm.vec3(-1, 0, 0)
      self.camPos.x = -glm.sin(glm.radians(self.camRotRef.x)) * dx
      self.camPos.z = -glm.cos(glm.radians(self.camRotRef.x)) * dx
    elif type == "up":
      if math.copysign(1, self.camPos.z) == math.copysign(1, -glm.cos(glm.radians(self.camRotRef.z + 1)) * dy):
        self.camRotRef -= glm.vec3(0, -1, -1)
        self.camPos.y = -glm.sin(glm.radians(self.camRotRef.y)) * dy
        self.camPos.z = -glm.cos(glm.radians(self.camRotRef.z)) * dy
    elif type == "down":
      if math.copysign(1, self.camPos.z) == math.copysign(1, -glm.cos(glm.radians(self.camRotRef.z - 1)) * dy):
        self.camRotRef += glm.vec3(0, -1, -1)
        self.camPos.y = -glm.sin(glm.radians(self.camRotRef.y)) * dy
        self.camPos.z = -glm.cos(glm.radians(self.camRotRef.z)) * dy
    self.viewMatrix = glm.lookAt(self.target - self.camPos, self.target, glm.vec3(0, 1, 0))

  def getForwardVector(self):
    forward = glm.normalize(self.target - self.camPos)
    self.forwardVector = glm.vec3(forward.x * 1.0, forward.y * 1.0, forward.z * 1.0)

  def wireframeMode(self):
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

  def filledMode(self):
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

  def changeModel(self, action):
    if action == "next":
      self.actualModel += 1
      if self.actualModel >= len(self.scene):
        self.actualModel = 0
    elif action == "previous":
      self.actualModel -= 1
      if self.actualModel < 0:
        self.actualModel = len(self.scene) - 1

  def setShaders(self, vertexShader, fragmentShader):
    if vertexShader is not None and fragmentShader is not None:
      self.activeShader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER), compileShader(fragmentShader, GL_FRAGMENT_SHADER))
    else:
      self.activeShader = None

  def moveModel(self, action):
    for model in self.scene:
      if model.id == self.actualModel:
        if action == "up":
          model.pos += glm.vec3(0, 0.01, 0)
        elif action == "down":
          model.pos += glm.vec3(0, -0.01, 0)
        elif action == "left":
          model.pos += glm.vec3(-0.01, 0, 0)
        elif action == "right":
          model.pos += glm.vec3(0.01, 0, 0)
        elif action == "forward":
          model.pos += glm.vec3(0, 0, -0.01)
        elif action == "backward":
          model.pos += glm.vec3(0, 0, 0.01)

  def render(self):
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUseProgram(self.activeShader)
    self.getForwardVector()

    if self.activeShader:
      glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "viewMatrix"), 1, GL_FALSE, glm.value_ptr(self.viewMatrix))
      glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "projectionMatrix"), 1, GL_FALSE, glm.value_ptr(self.projectionMatrix))
      glUniform1f(glGetUniformLocation(self.activeShader, "currentTime"), self.currentTime)
      glUniform1f(glGetUniformLocation(self.activeShader, "value"), self.value)
      glUniform3f(glGetUniformLocation(self.activeShader, "pointLight"), self.pointLight.x, self.pointLight.y, self.pointLight.z)
      glUniform3f(glGetUniformLocation(self.activeShader, "forwardVector"), self.forwardVector.x, self.forwardVector.y, self.forwardVector.z)
      glUniform3f(glGetUniformLocation(self.activeShader, "camPos"), self.camPos.x, self.camPos.y, self.camPos.z)

    for obj in self.scene:
      if obj.id == self.actualModel:
        if self.activeShader:
          glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "modelMatrix"), 1, GL_FALSE, glm.value_ptr(obj.getModelMatrix()))
          glUniform1i(glGetUniformLocation(self.activeShader, "textureSampler"), 0)
          glUniform1i(glGetUniformLocation(self.activeShader, "textureSampler2"), 1)
          glUniform1i(glGetUniformLocation(self.activeShader, "normalMap"), 2)
          glUniform1f(glGetUniformLocation(self.activeShader, "maxY"), obj.maxY)
          glUniform1f(glGetUniformLocation(self.activeShader, "minY"), obj.minY)
        obj.renderInScene()