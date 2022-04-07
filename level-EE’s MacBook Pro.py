from tkinter import *
from settings import tile_size, screen_width, level1_map
from player import Player
from tile import Tile
from button import *
from enemy import Enemy




cloud = pygame.image.load('background_cloudA.png')
BLACK = (0, 0, 0)


class Level:
    def __init__(self, level_data, surface):

        # -- Level Setup --
        self.level = 1
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0
        self.background = pygame.image.load('backgroundForest.png')
        self.background = pygame.transform.scale(self.background,
                                                 (self.background.get_width() * 2, self.background.get_height()))
        self.playerScore = 0

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def get_enemy_on_ground(self):
        if self.enemy_on_ground:
            self.enemy_on_ground = True
        else:
            self.enemy_on_ground = False

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.chests = pygame.sprite.Group()

        # -- Iterate
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                # -- Changes tile image based on location in map --
                if cell == 'G':
                    tile = Tile((x, y), 'grassMid.png')
                    self.tiles.add(tile)
                if cell == 'X':
                    tile = Tile((x, y), 'grassCenter.png')
                    self.tiles.add(tile)
                if cell == 'B':
                    tile = Tile((x, y), 'box.png')
                    self.tiles.add(tile)
                if cell == 'C':
                    tile = Tile((x, y), 'background_cloudA.png')
                    self.tiles.add(tile)
                if cell == 'R':
                    tile = Tile((x, y), 'platformPack_tile058.png')
                    self.chests.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y), self.display_surface)
                    self.player.add(player_sprite)
                if cell == 'E':
                    enemy = Enemy((x, y), self.display_surface, level1_map)
                    self.enemies.add(enemy)

    def returnPlayer(self):
        return self.player

    def returnChests(self):
        return self.chests

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def enemy_horizontal_movement_collision(self):
        enemies = self.enemies.sprites()
        for enemy in enemies:
            enemy.rect.x += enemy.direction.x * enemy.speed

            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.x < 0:
                        enemy.rect.left = sprite.rect.right
                        enemy.on_left = True
                        self.current_x = enemy.rect.left
                    elif enemy.direction.x > 0:
                        enemy.rect.right = sprite.rect.left
                        enemy.on_right = True
                        self.current_x = enemy.rect.right

            if enemy.on_left and (enemy.rect.left < self.current_x or enemy.direction.x >= 0):
                enemy.on_left = False
            if enemy.on_right and (enemy.rect.right > self.current_x or enemy.direction.x <= 0):
                enemy.on_right = False

    def enemy_vertical_movement_collision(self):
        enemies = self.enemies.sprites()

        for enemy in enemies:
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.y > 0:
                        enemy.rect.bottom = sprite.rect.top
                        enemy.direction.y = 0
                        enemy.on_ground = True

                    elif enemy.direction.y < 0:
                        enemy.rect.top = sprite.rect.bottom
                        enemy.direction.y = 0
                        enemy.on_ceiling = True

        # -- Keep enemy y coordinate low --
        for enemy in enemies:
            for tile in self.tiles.sprites():
                if tile.rect.colliderect(enemy.rect):
                    enemy.rect.y = tile.rect.top

    def enemyMovement(self):

        enemies = self.enemies.sprites()
        player = self.player.sprite

        # -- If player to the left move left, else move right --
        for enemy in enemies:
            if enemy.rect.x - player.rect.x > 0:
                enemy.moveDir = -1
            elif enemy.rect.x == player.rect.x:
                enemy.moveDir = 0
            else:
                enemy.moveDir = 1

            # -- Iterate through tiles and check for collision --
            for index, tile in enumerate(self.tiles.sprites()):
                # -- If there is a collision check
                if tile.rect.colliderect(enemy.rect):
                    if index < len(level1_map):
                        for row in level1_map:
                            for tile in row:
                                if level1_map[index + 1] == '':
                                    pass

    def enemyCollision(self):
        enemies = self.enemies.sprites()
        player = self.player.sprite

        for enemy in enemies:
            if enemy.rect.colliderect(player.rect):
                player.health -= 0000000000.5



    def updatePlayerHealth(self):
        player = self.player.sprite
        if player.health <= 0:
            sys.exit()
        if player.rect.y >= 1000:
            player.health = 0
        else:
            return player.health

    def returnPlayerScore(self):
        return self.playerScore


    def nextLevel(self):
        self.level += 1
        return self.level

    def run(self):
        # -- Background --
        self.display_surface.blit(self.background, (0, 0))

        # -- Tiles --
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.chests.draw(self.display_surface)
        self.chests.update(self.world_shift)
        self.scroll_x()

        # -- Player --
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

        # -- Enemy --
        self.enemyMovement()
        self.enemy_horizontal_movement_collision()
        self.enemy_vertical_movement_collision()
        self.enemies.draw(self.display_surface)
        self.enemies.update()
        self.enemyCollision()



