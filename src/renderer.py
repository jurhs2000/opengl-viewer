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
face.pos.z = -5.0
rend.scene.append(face)

deltaTime = 0.0
isRunning = True
while isRunning:
  keys = pygame.key.get_pressed()
  if keys[K_d]:
    rend.camPos.x += 1 * deltaTime
  if keys[K_a]:
    rend.camPos.x -= 1 * deltaTime
  if keys[K_w]:
    rend.camPos.z -= 1 * deltaTime
  if keys[K_s]:
    rend.camPos.z += 1 * deltaTime

  if keys[K_q]:
    rend.camRot.y += 15 * deltaTime
  if keys[K_e]:
    rend.camRot.y -= 15 * deltaTime

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

  rend.currentTime += deltaTime
  deltaTime = clock.tick(60) / 1000
  rend.render()
  pygame.display.flip()

pygame.quit()
