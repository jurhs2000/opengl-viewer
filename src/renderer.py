import pygame
from pygame.locals import *
import numpy as np
from gl import Renderer, Model
import shaders

width = 1366
height = 768

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.setShaders(shaders.normal["vertex"], shaders.normal["fragment"])

face = Model('../models/face/model.obj', '../models/face/model.bmp', '../models/face/model_normal.bmp')
rend.scene.append(face)

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

  for ev in pygame.event.get():
    if ev.type == pygame.QUIT:
      isRunning = False
    if ev.type == pygame.KEYDOWN:
      if ev.key == pygame.K_ESCAPE:
        isRunning = False
      if ev.key == K_1:
        rend.filledMode()
      if ev.key == K_2:
        rend.wireframeMode()
      if ev.key == K_3:
        rend.setShaders(shaders.normal["vertex"], shaders.normal["fragment"])
      if ev.key == K_4:
        rend.setShaders(shaders.toon["vertex"], shaders.toon["fragment"])
      if ev.key == K_5:
        rend.setShaders(shaders.gradient["vertex"], shaders.gradient["fragment"])
      if ev.key == K_6:
        rend.setShaders(shaders.highlight["vertex"], shaders.highlight["fragment"])
      if ev.key == K_7:
        rend.setShaders(shaders.textureBlend["vertex"], shaders.textureBlend["fragment"])
    # mouse scroll
    if ev.type == pygame.MOUSEBUTTONDOWN:
      if ev.button == 4:
        if (d >= rend.cameraMinDistance): rend.cameraMovement('forward')
      if ev.button == 5:
        if (d <= rend.cameraMaxDistance): rend.cameraMovement('backward')

  rend.currentTime += deltaTime
  deltaTime = clock.tick(60) / 1000
  rend.render()
  pygame.display.flip()

pygame.quit()
