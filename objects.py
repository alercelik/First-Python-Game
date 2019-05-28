import pygame
from pygame.locals import *

screen_width = 0
screen_height = 0
ground_height = 0
player_width = 0
player_height = 0
spawning_width = 0
spawning_height = 0

def init(screen_w, screen_h, ground_h):
	global screen_width
	screen_width = screen_w

	global screen_height
	screen_height = screen_h

	global ground_height
	ground_height = ground_h

	print "objects.py inited with screen res", screen_width, screen_height

class Player:
	def __init__(self, left_looking_image_name, pos, right_looking_image_name=None):
		self.frame_left = pygame.image.load(left_looking_image_name)

		if right_looking_image_name is None:
			self.frame_right = pygame.transform.flip(self.frame_left, True, False)
		else:
			self.frame_right = pygame.image.load(right_looking_image_name)

		self.size = self.frame_left.get_rect().size
		self.width = self.size[0]
		self.height = self.size[1]

		global player_width
		player_width = self.width

		global player_height
		player_height = self.height

		self.x = pos[0]
		self.y = pos[1]
		self.y -= self.height


		self.looking_left = True
		self.x_normal_speed = 3

		self.jumping = False
		self.x_jump_speed = 2

		self.crouching = False
		self.x_crouch_speed = 1

		self.x_speed = x_normal_speed
		self.y_speed = 0

		print "player created at ", self.x, "-", self.y, "."

	def get_frame(self):
		if self.looking_left:
			return self.frame_left
		else:
			return self.frame_right

	def get_pos(self):
		return (self.x, self.y)

	def move_left(self):
		if not self.jumping:
			self.looking_left = True

			if self.x > screen_width / 5:
				self.x -= self.speed
		else:
			pass

	def move_right(self):
		if not self.jumping:
			self.looking_left = False

			if self.x + self.width < screen_width * 4 / 5:
				self.x += self.x_speed
		else:
			pass

	def jump():
		if self.jumping:
			pass
		else:
			# here
			pass

	def crouch():
		if self.jumping:
			pass
		else:
			# here
			pass

	def shoot(self):
		pass


class Spawning:
	speed = 3

	def __init__(self, left_looking_image_name, pos, right_looking_image_name = None):
		self.frame_left = pygame.image.load(left_looking_image_name)

		if right_looking_image_name is None:
			self.frame_right = pygame.transform.flip(self.frame_left, True, False)
		else:
			self.frame_right = pygame.image.load(right_looking_image_name)

		self.size = self.frame_left.get_rect().size
		self.width = self.size[0]
		self.height = self.size[1]

		self.x = pos[0]
		self.y = pos[1]
		self.y -= self.height

		global spawning_width
		spawning_width = self.width

		global spawning_height
		spawning_height = self.height

		self.created = False

		if self.x < 0:
			self.looking_left = False
		else:
			self.looking_left = True

	def get_frame(self):
		if self.looking_left:
			return self.frame_left
		else:
			return self.frame_right

	def get_pos(self):
		return (self.x, self.y)

	def move(self):
		if self.created:
			if self.looking_left:
				self.x -= Spawning.speed
			else:
				self.x += Spawning.speed

			# print self.x, self.y
		else:
			self.created = True

	def dir_left(self):
		return self.looking_left

	def hits_player(self, player_pos):
		if self.looking_left:
			if self.x < player_pos[0] + player_width:
				print "spawning hit player"
				return True
		else:
			if self.x + self.width > player_pos[0]:
				print "spawning hit player"
				return True

		return False

	def is_out(self):
		if self.looking_left:
			return self.x + self.width < 0
		else:
			return self.x > screen_width


class Bullet:
	speed = 6

	def __init__(self, left_looking_image_name, shooter_pos, shooter_width, shooter_looking_left, bullet_height):
		self.frame_left = pygame.image.load(left_looking_image_name)
		self.frame_right = pygame.transform.flip(self.frame_left, True, False)
		self.size = self.frame_left.get_rect().size
		self.width = self.size[0]
		self.height = self.size[1]

		self.y = bullet_height

		if shooter_looking_left:
			self.looking_left = True
			self.x = shooter_pos[0] - self.width
		else:
			self.looking_left = False
			self.x = shooter_pos[0] + shooter_width


		self.fired = False

		print "bullet created at ", self.x, self.y, "."

	def get_frame(self):
		if self.looking_left:
			return self.frame_left
		else:
			return self.frame_right

	def get_pos(self):
		return (self.x, self.y)

	def dir_left(self):
		return self.looking_left

	def move(self):
		if self.fired:
			if self.looking_left:
				self.x -= Bullet.speed
			else:
				self.x += Bullet.speed

			# print self.x, self.y
		else:
			self.fired = True

	def is_out(self):
		return self.x < 0 or self.x > screen_width

	def hits_spawning(self, spawning_pos):
		if self.looking_left:
			if self.x < spawning_pos[0] + spawning_width:
				return True
		else:
			if self.x > spawning_pos[0]:
				return True

		return False