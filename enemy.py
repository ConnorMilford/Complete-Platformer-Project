import random
import pygame


# -- Basic AI implentation --
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, surface, tilemap):
        super(Enemy, self).__init__()
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 30, self.image.get_height() - 40))
        self.rect = self.image.get_rect(topleft=pos)
        self.health = 20
        self.tilemap = tilemap

        # -- Movement Attributes --
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 0.8
        self.jump_speed = -16
        self.moveDir = 0


        # -- Direction Faced --
        self.on_left = False
        self.on_right = False
        self.on_ground = False
        self.on_ceiling = False

    def move(self):
        self.rect.x += (self.moveDir * self.speed)

    def apply_gravity(self):

        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.move()
        self.apply_gravity()








