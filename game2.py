# 1 - Import library
import objects

from random import randint

import pygame
from pygame.locals import *

# 2 - Initialize the game
pygame.init()
screen_width, screen_height = 640, 480
screen=pygame.display.set_mode((screen_width, screen_height))


# music
pygame.mixer.init()
pygame.mixer.music.load("resources/music/osman_pasha.wav")
pygame.mixer.music.play(-1)


#init objects.py

ground_height = 100


objects.init(screen_width, screen_height, ground_height)


# 3 - Load images
#full_bg
full_bg = pygame.image.load("resources/images/full_bg.png")
full_bg_size = full_bg.get_rect().size
full_bg_width = int(full_bg_size[0])
full_bg_height = int(full_bg_size[1])


#player

# osman_pasa = objects.Player("resources/images/osman_pasa_renkli.png", [screen_width / 3, screen_height - ground_height], "resources/images/osman_pasa_sag_renkli.png")

osman_pasa = objects.Player("resources/images/spawning.png", [screen_width / 3, screen_height - ground_height])

# attributes
bullets = []
spawnings = []

keys = [False, False, False, False]
initialize_shoot = False

shoot_start_tick_counter = -2000
spawning_create_tick_counter = 0


# operational functions

def shoot():
	global shoot_start_tick_counter
	tick = pygame.time.get_ticks()

	if tick - shoot_start_tick_counter > 0.3 * 1000:
		shoot_start_tick_counter = tick

		global bullets
		bullets.append(objects.Bullet("resources/images/bullet.png", osman_pasa.get_pos(), osman_pasa.width, osman_pasa.looking_left, osman_pasa.y + 39))


# visual functions
def move_bullets():
    for bullet in bullets:
        bullet.move()

        if bullet.is_out():
        	bullets.remove(bullet)
        elif bullet_hits_spawning(bullet):
        	bullets.remove(bullet)


def bullet_hits_spawning(bullet):
	bullet_direction = bullet.dir_left()

	global spawnings
	for spawning in spawnings:
		if not spawning.dir_left() == bullet_direction:
			if bullet.hits_spawning(spawning.get_pos()):
				print "bullet hit spawning"
				spawnings.remove(spawning)
				return True
	return False


def create_spawnings():
	global spawning_create_tick_counter
	if (pygame.time.get_ticks() - spawning_create_tick_counter)  > 5 * 1000:
		spawning_create_tick_counter = pygame.time.get_ticks()
		if 0 == randint(0, 1):
			# spawn at left
			global spawnings
			spawnings.append(objects.Spawning("resources/images/osman_pasa_renkli.png", (0 - screen_width / 5, screen_height - ground_height)))
		else:
			# spawn at right
			spawnings.append(objects.Spawning("resources/images/osman_pasa_renkli.png", (screen_width * 6 / 5, screen_height - ground_height)))


def move_spawnings(player_pos):
    for spawning in spawnings:
        spawning.move()

        if spawning.hits_player(player_pos):
        	# global full_bg
        	# full_bg = pygame.image.load("resources/images/white.png")
        	spawnings.remove(spawning)
        elif spawning.is_out():
        	print "deleted a spawning"
        	spawnings.remove(spawning)


def show_spawnings():
    for spawning in spawnings:
        screen.blit(spawning.get_frame(), spawning.get_pos())


def show_bullets():
    for bullet in bullets:
        screen.blit(bullet.get_frame(), bullet.get_pos())


def show_player():
    screen.blit(osman_pasa.get_frame(), osman_pasa.get_pos())


def clean_screen():
    screen.fill(0)
    screen.blit(full_bg, (0, 0))


def display():
    pygame.display.flip()


# 4 - keep looping through
while True:
	# print len(spawnings)

	clean_screen()

	create_spawnings()

	move_spawnings(osman_pasa.get_pos())

	move_bullets()

	show_player()

	show_bullets()

	show_spawnings()

	display()

	# print bullet_pos

	# 8 - loop through the events
	for event in pygame.event.get():
	    # check if the event is the X button 
	    if event.type==pygame.QUIT:
	        # if it is quit the game
	        pygame.quit() 
	        exit(0)
	    if event.type == pygame.KEYDOWN:
	        if event.key==K_w:
	            keys[0]=True
	        elif event.key==K_a:
	            keys[1]=True
	        elif event.key==K_s:
	            keys[2]=True
	        elif event.key==K_d:
	            keys[3]=True
	        elif event.key == K_SPACE:
	            initialize_shoot = True
	    if event.type == pygame.KEYUP:
	        if event.key==pygame.K_w:
	            keys[0]=False
	        elif event.key==pygame.K_a:
	            keys[1]=False
	        elif event.key==pygame.K_s:
	            keys[2]=False
	        elif event.key==pygame.K_d:
	            keys[3]=False
	        elif event.key == K_SPACE:
	            initialize_shoot = False

	# 9 - Move player
	#up or down
	if keys[0]:
	    if(player_pos[1] > 0):
	        # player_pos[1]-=speed_normal
	        pass
	elif keys[2]:
	    if(player_pos[1] + ground_height + player_height < screen_height):
	        player_pos[1]+=speed_normal

	#left or right
	if keys[1]:
	    osman_pasa.move_left()
	elif keys[3]:
	    osman_pasa.move_right()

	#check shooting
	if initialize_shoot:
	    shoot()
