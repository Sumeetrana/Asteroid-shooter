import pygame, sys
from random import randint, uniform

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroid shooter")

def display_score():
  score_text = f'Score: {total_score}'
  text_surf = font.render(score_text, True, (255, 255, 255))
  text_rect = text_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
  display_surface.blit(text_surf, text_rect)

# import images
ship_surf = pygame.image.load('./graphics/ship.png').convert_alpha()
# Rectangles to place Surfaces
ship_rect = ship_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)) 

background_surf = pygame.image.load('./graphics/background.png').convert()
laser_surf = pygame.image.load('./graphics/laser.png')
laser_list = []

asteroid_surf = pygame.image.load('./graphics/meteor.png')
asteroid_list = []

# import text
font = pygame.font.Font('./graphics/subatomic.ttf', 50)

# limit the framerate
clock = pygame.time.Clock()

# asteroid timer
asteroid_timer = pygame.event.custom_type()
pygame.time.set_timer(asteroid_timer, 500)

total_score = 0

# import sound
laser_sound = pygame.mixer.Sound('./sounds/laser.ogg')
explosion_sound = pygame.mixer.Sound('./sounds/explosion.wav')
background_music = pygame.mixer.Sound('./sounds/music.wav')
background_music.play(loops = -1)
# keeps the code going
while True:
  # 1. input -> events (mouse click, mouse movement, press of a button, controller)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    # if event.type == pygame.MOUSEMOTION:
    #   ship_rect.center = event.pos
    if event.type == pygame.MOUSEBUTTONDOWN:  
      laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)
      laser_list.append(laser_rect)
      
      # play laser sound
      laser_sound.play()
    if event.type == asteroid_timer:
      x_pos = randint(50, WINDOW_WIDTH - 50)
      asteroid_rect = asteroid_surf.get_rect(center = (x_pos, -50))
      asteroid_list.append({"rect": asteroid_rect,"direction": uniform(-0.5, 0.5)})

  # framerate limit
  dt = clock.tick(60) / 1000

  # input
  ship_rect.center = pygame.mouse.get_pos()

  # 2. updates
  display_surface.blit(background_surf, (0, 0))

  # for loop that draws the laser surface where the rects are
  for laser in laser_list:
    laser.y -= round(300 * dt)
    display_surface.blit(laser_surf, laser)
    if(laser.bottom < 0):
      laser_list.remove(laser)

  # for loop that draws the asteroid surface
  for asteroid in asteroid_list:
    asteroid["rect"].y += round(300 * dt)
    asteroid["rect"].x += round(300 * dt * asteroid["direction"])
    display_surface.blit(asteroid_surf, asteroid["rect"])
    if asteroid["rect"].top > WINDOW_HEIGHT:
      asteroid_list.remove(asteroid)

  # asteroid - ship collisions
  for asteroid in asteroid_list:
    asteroid_rect = asteroid["rect"]
    if ship_rect.colliderect(asteroid_rect):
      pygame.quit()
      sys.exit() 

  # laser - asteroid collision
  for laser_rect in laser_list:
    for asteroid in asteroid_list:
      asteroid_rect = asteroid["rect"]
      if laser_rect.colliderect(asteroid_rect):
        explosion_sound.play()
        asteroid_list.remove(asteroid)
        laser_list.remove(laser_rect)
        total_score += 1

  display_score()
  display_surface.blit(ship_surf, ship_rect)
  
  # 3. show the frame to the player / update the display surface
  pygame.display.update()