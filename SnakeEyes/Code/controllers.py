import pygame
from core import Game


'''
Notes:
Should the controller class manage all of the controllers or just be it's own instance for each one connected?
'''

class Controler:
  def __init__(self):
    
    pygame.joystick.init()
    
    # self.controllers = []
    
  def isConnected(self):
    # for event in pygame.event.get():
    #   if event.type == pygame.JOYDEVICEADDED:
    #     controller = pygame.joystick.Joystick(event.device_index)
    #     self.controllers.append(controller)
    for event in pygame.event.get():
      if event.type == pygame.JOYDEVICEADDED:
        print(pygame.joystick.get_count())
        
  def notConnected(self):
    for event in pygame.event.get():
      if event.type == pygame.JOYDEVICEREMOVED:
        print(pygame.joystick.get_count())
        