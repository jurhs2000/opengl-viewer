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
rend.setShaders(shaders.vertex, shaders.fragment)

face = Model('../models/face/model.obj', '../models/face/model.bmp')
rend.scene.append(face)

deltaTime = 0.0
isRunning = True
while isRunning:
  keys = pygame.key.get_pressed()
  # distance between camera and object
  d = ((rend.camPos.x - 0.0)**2 + (rend.camPos.z - 0.0)**2)**0.5
  d2 = ((rend.camPos.y - 0.0)**2 + (rend.camPos.z - 0.0)**2)**0.5
  if keys[K_d]:
    if (d <= rend.cameraMaxDistance): rend.cameraMovement('right', d)
  if keys[K_a]:
    if (d <= rend.cameraMaxDistance): rend.cameraMovement('left', d)
  if keys[K_w]:
    if (d >= rend.cameraMinDistance): rend.cameraMovement('up', d2)
  if keys[K_s]:
    if (d <= rend.cameraMaxDistance): rend.cameraMovement('down', d2)
  if keys[K_q]:
    rend.camRot.y += 0.1
  if keys[K_e]:
    rend.camRot.y -= 0.1
  if keys[K_z]:
    rend.camRot.x += 0.1
  if keys[K_c]:
    rend.camRot.x -= 0.1
  if keys[K_y]:
    rend.camRot.z += 0.1
  if keys[K_h]:
    rend.camRot.z -= 0.1

  if keys[K_LEFT]:
    if rend.value >= 0: rend.value -= 0.1 * deltaTime
    else: rend.value = 0
  if keys[K_RIGHT]:
    if rend.value >= 0: rend.value += 0.1 * deltaTime
    else: rend.value = 0

  #rend.scene[0].rot.x += 10 * deltaTime
  #rend.scene[0].rot.y += 10 * deltaTime
  #rend.scene[0].rot.z += 10 * deltaTime

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
        rend.setShaders(shaders.vertex, shaders.fragment)
      if ev.key == K_4:
        rend.setShaders(shaders.toon_vertex, shaders.toon_fragment)
    # mouse scroll
    if ev.type == pygame.MOUSEBUTTONDOWN:
      if ev.button == 4:
        if (d <= rend.cameraMaxDistance): rend.cameraMovement('forward', d)
      if ev.button == 5:
        if (d <= rend.cameraMaxDistance): rend.cameraMovement('backward', d)

  rend.currentTime += deltaTime
  deltaTime = clock.tick(60) / 1000
  rend.render()
  pygame.display.flip()

pygame.quit()
