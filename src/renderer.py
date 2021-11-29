import pygame
from pygame.locals import *
from gl import Renderer, Model
import shaders

width = 1366
height = 768

models = [
  {
    "obj": "../models/face/model.obj",
    "texture": "../models/face/model.bmp",
    "texture2": "../models/face/model_normal.bmp",
    "normal": "../models/face/model_normal.bmp",
    "scale": [1, 1, 1],
    "pos": [0, 0, 0],
  },
  {
    "obj": "../models/lugia/lugia.obj",
    "texture": "../models/lugia/Lugia-TextureMap.jpg",
    "texture2": "../models/lugia/Lugia-TextureMap2.jpg",
    "normal": "../models/lugia/Lugia-NormalMap.jpg",
    "scale": [0.7, 0.7, 0.7],
    "pos": [0, 0, 0],
  },
  {
    "obj": "../models/boo/source/boo.obj",
    "texture": "../models/boo/textures/BooTexture.png",
    "texture2": None,
    "normal": None,
    "scale": [1, 1, 1],
    "pos": [0, -0.3, 0],
  },
  {
    "obj": "../models/bowser/source/pose.obj",
    "texture": "../models/bowser/textures/DryKoopaAll.png",
    "texture2": "../models/bowser/textures/DryKoopaAllGlow.png",
    "normal": None,
    "scale": [0.4, 0.4, 0.4],
    "pos": [0, -1, 0],
  },
  {
    "obj": "../models/earth/earth.obj",
    "texture": "../models/earth/earthDay.bmp",
    "texture2": "../models/earth/earthNight.bmp",
    "normal": None,
    "scale": [1, 1, 1],
    "pos": [0, 0, 0],
  },
  {
    "obj": "../models/lakitu/source/lakitu.obj",
    "texture": "../models/lakitu/textures/lakitu.png",
    "texture2": None,
    "normal": None,
    "scale": [0.3, 0.3, 0.3],
    "pos": [0, -1, 0],
  },
  {
    "obj": "../models/piranha/piranha.obj",
    "texture": "../models/piranha/npc072_body.png",
    "texture2": None,
    "normal": "../models/piranha/npc072_body_nml.png",
    "scale": [1, 1, 1],
    "pos": [0, -0.6, 0],
  }
]

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.setShaders(shaders.default["vertex"], shaders.default["fragment"])

for model in models:
  rend.scene.append(Model(models.index(model), model["obj"], model["texture"], model["texture2"], model["normal"], model["scale"], model["pos"]))

isMoving = False # Para saber si se esta moviendo la camara con el mouse
lastPos = (0, 0) # Ultima posicion del mouse
deltaTime = 0.0
isRunning = True
while isRunning:
  keys = pygame.key.get_pressed()
  # distance between camera and object
  d = ((rend.camPos.x - rend.target.x)**2 + (rend.camPos.y - rend.target.y)**2 + (rend.camPos.z - rend.target.z)**2)**0.5
  if keys[K_d]:
    if (d <= rend.cameraMaxDistance): rend.cameraMovement('right')
  if keys[K_a]:
    if (d <= rend.cameraMaxDistance): rend.cameraMovement('left')
  if keys[K_w]:
    if (d >= rend.cameraMinDistance): rend.cameraMovement('up')
  if keys[K_s]:
    if (d <= rend.cameraMaxDistance): rend.cameraMovement('down')

  if keys[K_LEFT]:
    if rend.value >= 0: rend.value -= 0.1 * deltaTime
    else: rend.value = 0
  if keys[K_RIGHT]:
    if rend.value >= 0: rend.value += 0.1 * deltaTime
    else: rend.value = 0

  if keys[K_i]:
    rend.moveModel('up')
  if keys[K_k]:
    rend.moveModel('down')
  if keys[K_j]:
    rend.moveModel('left')
  if keys[K_l]:
    rend.moveModel('right')
  if keys[K_o]:
    rend.moveModel('forward')
  if keys[K_u]:
    rend.moveModel('backward')

  for ev in pygame.event.get():
    if ev.type == pygame.QUIT:
      isRunning = False
    if ev.type == pygame.KEYDOWN:
      if ev.key == pygame.K_ESCAPE:
        isRunning = False
      if ev.key == K_q:
        rend.changeModel("previous")
      if ev.key == K_e:
        rend.changeModel("next")
      if ev.key == K_1:
        rend.filledMode()
      if ev.key == K_2:
        rend.wireframeMode()
      if ev.key == K_3:
        rend.setShaders(shaders.default["vertex"], shaders.default["fragment"])
      if ev.key == K_4:
        rend.setShaders(shaders.toon["vertex"], shaders.toon["fragment"])
      if ev.key == K_5:
        rend.setShaders(shaders.gradient["vertex"], shaders.gradient["fragment"])
      if ev.key == K_6:
        rend.setShaders(shaders.highlight["vertex"], shaders.highlight["fragment"])
      if ev.key == K_7:
        rend.setShaders(shaders.textureBlend["vertex"], shaders.textureBlend["fragment"])
      if ev.key == K_8:
        rend.setShaders(shaders.normalMap["vertex"], shaders.normalMap["fragment"])
      if ev.key == K_9:
        rend.setShaders(shaders.wave["vertex"], shaders.wave["fragment"])
    # mouse scroll
    if ev.type == pygame.MOUSEBUTTONDOWN:
      if ev.button == 4:
        if (d >= rend.cameraMinDistance): rend.cameraMovement('forward')
      if ev.button == 5:
        if (d <= rend.cameraMaxDistance): rend.cameraMovement('backward')
      if ev.button == 1:
        isMoving = True
        lastPos = pygame.mouse.get_pos()
    elif ev.type == pygame.MOUSEBUTTONUP:
      if ev.button == 1:
        isMoving = False
    if ev.type == pygame.MOUSEMOTION:
      if isMoving:
        x, y = pygame.mouse.get_pos()
        movX = x - lastPos[0]
        movY = y - lastPos[1]
        if movX > 20:
          if (d <= rend.cameraMaxDistance): rend.cameraMovement('left')
        if movX < -20:
          if (d <= rend.cameraMaxDistance): rend.cameraMovement('right')
        if movY > 20:
          if (d <= rend.cameraMaxDistance): rend.cameraMovement('up')
        if movY < -20:
          if (d <= rend.cameraMaxDistance): rend.cameraMovement('down')

  rend.currentTime += deltaTime
  deltaTime = clock.tick(60) / 1000
  rend.render()
  pygame.display.flip()

pygame.quit()
