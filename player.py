import pygame

pygame.init()
pygame.mixer.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()
        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 30, self.image.get_height() - 40))
        self.rect = self.image.get_rect(topleft=pos)
        self.health = 20

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        # player status
        self.score = 0
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # music
        self.boingNoise = pygame.mixer.Sound('boing.wav')
        self.boingNoise.set_volume(2.0)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_w] and self.on_ground:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.boingNoise.play()

    def update(self):
        self.get_input()
