import pygame as pg 
from tile import AnimatedTile
from random import randint
from support import *
import random

class NPC(pg.sprite.Sprite):
	def __init__(self, pos, size, NPC, groups):
		super().__init__(groups)
		self.size = size
		self.speed = 2
		self.pos = pg.math.Vector2(pos)
		self.direction = pg.math.Vector2()
		self.velocity = pg.math.Vector2()

		# animation
		self.import_character_assets(NPC)
		self.status = 'idle'
		self.frame_index = 0
		self.animation = self.animations[self.status]
		self.animation_speed = 0.15
		self.image = self.animations['idle'][self.frame_index]
		
		# state
		self.facing_right = False
		self.hit_constraint = False

		# rect
		self.rect = self.image.get_rect()
		self.rect.center = pos
		
	def approach(self, player):
		# set vector equal to entity's position
		player_vector = pg.math.Vector2(player.rect.center)
		enemy_vector = pg.math.Vector2(self.rect.center)
		
		# get distance between the vectors
		distance = self.get_vector_distance(player_vector, enemy_vector)

		# determine direction to go if there is distance to be traveled
		if distance > 0:
			self.direction = (player_vector - enemy_vector).normalize()
		else:
			self.direction = pg.math.Vector2()
		
		# update velocity and position 
		self.velocity = self.direction * self.speed
		self.pos += self.velocity

		# apply updated position to rect
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y

	def get_vector_distance(self, v1, v2):
		return(v1 - v2).magnitude()

	def reverse(self):
		self.direction.x = -self.direction.x
		
	def patrol(self):
		left = -1
		right = 1
		up = -1
		down = 1
		self.direction.x = right

	def get_state(self):
		if self.direction.x > 0:
			self.facing_right = True
			self.status = 'run-right'
		elif self.direction.x < 0:
			self.facing_right = True
			self.status = 'run-left'
		elif self.direction.y > 0:
			self.status = 'run'
		elif self.direction.y < 0:
			self.status = 'run-back'
		else:
			self.running = False

	def import_character_assets(self, NPC):
		character_path = f'./assets/NPC/{NPC}/'
		self.animations = {'idle':[],'run-right':[],'run-left':[],'run-back':[], 'run':[]}
		
		for animation in self.animations.keys():
			full_path = character_path + animation + "/"
			self.animations[animation] = scale_images(import_folder(full_path), (self.size, self.size))

	def animate(self):
		animation = self.animations[self.status]

		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
			
		self.image = animation[int(self.frame_index)]
		if not self.facing_right:
			self.image = pg.transform.flip(self.image,True,False)

	def update(self):
		self.animate()
		self.get_state()
		self.rect.x += self.direction.x * self.speed
		# self.rect.y += self.direction.y * self.speed
		# pg.draw.rect(pg.display.get_surface(), "yellow", self.rect)
		# pg.draw.circle(pg.display.get_surface(), "red", self.rect.center, 100)
		

		
