import pygame
from config import *
import math
import random

class Spritesheet:
    #carrega um spritesheet e extrai sprites individuais
    def __init__(self, file):
        #carrega a imagem do spritesheet
        self.sheet = pygame.image.load(file).convert()
    
    def get_sprite(self, x, y, width, height, bg_colors):
        #retorna um sprite do spritesheet com fundo transparente
        sprite = pygame.Surface([width, height], pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))

        pixel_array = pygame.PixelArray(sprite)
        for color in bg_colors:
            pixel_array.replace(color, (0, 0, 0, 0))
        del pixel_array

        return sprite

class Player(pygame.sprite.Sprite): #gerencia movimento colisao e animacao do player
    def __init__(self, game, x, y): #inicia o player com posicao tamanho e sprite inicial
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        self.image = self.game.character_spritesheet.get_sprite(1, 1, self.width, self.height, bg_colors)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y #define alvo de movimento e estado de movimento
        
        self.target_x = self.rect.x
        self.target_y = self.rect.y
        self.moving = False
    
    def update(self): #atualiza o player a cada frame: movimentacao animacao e colisao
        self.grid_movement()
        self.animation()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.collide_enemy('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.collide_enemy('y')

        self.x_change = 0
        self.y_change = 0

    def grid_movement(self): #gerencia a movimentacao do player por tile no grid
        if self.game.in_battle:
            return
        
        keys = pygame.key.get_pressed()
        if not self.moving:
            dx, dy = 0, 0

            if keys[pygame.K_a]:
                self.facing = 'left'
                dx = -TILESIZE
            elif keys[pygame.K_d]:
                self.facing = 'right'
                dx = TILESIZE
            elif keys[pygame.K_w]:
                self.facing = 'up'
                dy = -TILESIZE
            elif keys[pygame.K_s]:
                self.facing = 'down'
                dy = TILESIZE

            if dx != 0 or dy != 0: #verifica se ha colisao antes do movimento
                next_rect = self.rect.copy()
                next_rect.x += dx
                next_rect.y += dy

                will_collide = any(next_rect.colliderect(block.rect) for block in self.game.blocks)
                will_collide_enemy = any(next_rect.colliderect(enemy.rect) for enemy in self.game.enemy)

                if not will_collide and not will_collide_enemy:
                    self.target_x = self.rect.x + dx
                    self.target_y = self.rect.y + dy
                    self.moving = True

        if self.moving:
            if self.rect.x < self.target_x:
                self.x_change = min(PLAYER_SPEED, self.target_x - self.rect.x)
            elif self.rect.x > self.target_x:
                self.x_change = -min(PLAYER_SPEED, self.rect.x - self.target_x)

            if self.rect.y < self.target_y:
                self.y_change = min(PLAYER_SPEED, self.target_y - self.rect.y)
            elif self.rect.y > self.target_y:
                self.y_change = -min(PLAYER_SPEED, self.rect.y - self.target_y)

            if self.rect.x == self.target_x and self.rect.y == self.target_y:
                self.moving = False

    def collide_blocks(self, direction): #impede o player de atravessar blocos
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collide_enemy(self, direction): #impede o player de atravessar enemy
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.enemy, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    print("não me teste!!!!")
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    print("vou acabar com tua raça!!!!")

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.enemy, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    print("sai daqui!!!!")
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    print("você não é páreo!!!!")
    
    def animation(self): #seleciona a sprites de acordo com direcao e movimento
        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        down_animations = [self.game.character_spritesheet.get_sprite(1, 1, self.width, self.height, bg_colors),
                          self.game.character_spritesheet.get_sprite(1, 37, self.width, self.height, bg_colors),
                          self.game.character_spritesheet.get_sprite(34, 37, self.width, self.height, bg_colors),
                          self.game.character_spritesheet.get_sprite(67, 37, self.width, self.height, bg_colors)]
        
        up_animations = [self.game.character_spritesheet.get_sprite(83, 1, self.width, self.height, bg_colors),
                          self.game.character_spritesheet.get_sprite(1, 106, self.width, self.height, bg_colors),
                          self.game.character_spritesheet.get_sprite(34, 106, self.width, self.height, bg_colors),
                          self.game.character_spritesheet.get_sprite(67, 106, self.width, self.height, bg_colors)]
        
        left_animations = [self.game.character_spritesheet.get_sprite(34, 3, 47, 32, bg_colors),
                          self.game.character_spritesheet.get_sprite(1, 72, 47, 32, bg_colors),
                          self.game.character_spritesheet.get_sprite(50, 72, 47, 32, bg_colors),
                          self.game.character_spritesheet.get_sprite(99, 72, 47, 32, bg_colors)]
        
        right_animations = [self.game.character_spritesheet.get_sprite(116, 3, 47, 32, bg_colors),
                          self.game.character_spritesheet.get_sprite(1, 143, 47, 32, bg_colors),
                          self.game.character_spritesheet.get_sprite(50, 143, 47, 32, bg_colors),
                          self.game.character_spritesheet.get_sprite(99, 143, 47, 32, bg_colors)]
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 1, self.width, self.height, bg_colors)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.3
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(83, 1, self.width, self.height, bg_colors)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.3
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(34, 3, 47, 32, bg_colors)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.3
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(116, 3, 47, 32, bg_colors)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.3
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Enemy(pygame.sprite.Sprite): #enemy com movimento automatico e inicio de batalha
    enemy_counter = 0

    def __init__(self, game, x, y): #inicializa enemy com sprite e posicao no mapa
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.enemy
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        self.image = self.game.enemy_spritesheet.get_sprite(0, 0, self.width, self.height, bg_colors)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self): #se move e verifica proximidade com jogador
        if hasattr(self.game, "player"):
            player_tile_x = self.game.player.rect.x // TILESIZE
            player_tile_y = self.game.player.rect.y // TILESIZE
            enemy_tile_x = self.rect.x // TILESIZE
            enemy_tile_y = self.rect.y // TILESIZE

            if abs(player_tile_x - enemy_tile_x) <= 1 and abs(player_tile_y - enemy_tile_y) <= 1:
                if not self.game.battle_started:
                    self.game.in_battle = True
                    self.game.battle_started = True
                    self.game.battle_enemy = self
                    print("⚔️ BATALHA INICIADA!")
                    self.game.handle_battle()
                return

        if self.game.in_battle:
            return

        self.game.battle_turn = "fox"
        self.game.fox_hp = 100
        self.game.bacteria_hp = 5

        if not hasattr(self, 'move_timer'):
            self.move_timer = 0
        self.move_timer += 1

        if self.move_timer < 30: #espera 30 frames antes de mover novamente
            return
        self.move_timer = 0

        directions = [(0, -TILESIZE), (0, TILESIZE), (-TILESIZE, 0), (TILESIZE, 0)]
        dx, dy = random.choice(directions)

        next_rect = self.rect.copy()
        next_rect.x += dx
        next_rect.y += dy

        will_collide = any(next_rect.colliderect(block.rect) for block in self.game.blocks) or \
                       any(next_rect.colliderect(enemy.rect) for enemy in self.game.enemy if enemy != self)

        if not will_collide: #move o inimigo se nao houver colisao
            self.rect.x += dx
            self.rect.y += dy

class Block(pygame.sprite.Sprite): #bloco solido que impede passagem
    def __init__(self, game, x, y): #inicializa bloco com sprite e posicao
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(518, 2602, self.width, self.height, bg_colors)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Tree1(pygame.sprite.Sprite): #arvore (sprite de baixo) que bloqueia o caminho
    def __init__(self, game, x, y): #inicializa arvore com sprite especifico e posicao
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(1130, 2570, self.width, self.height, bg_colors)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y    

class Tree2(pygame.sprite.Sprite): #arvore (sprite de cima) que bloqueia o caminho
    def __init__(self, game, x, y):  #inicializa arvore com sprite especifico e posicao
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(1130, 2602, self.width, self.height, bg_colors)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Tree3(pygame.sprite.Sprite): #arvore (sprite de baixo+cima) que bloqueia o caminho
    def __init__(self, game, x, y): #inicializa arvore com sprite especifico e posicao
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        self.image = self.game.tree_spritesheet.get_sprite(0, 0, self.width, self.height, bg_colors)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Portal(pygame.sprite.Sprite): #passagem de um mapa pra outro
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.portals
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(550, 386, self.width, self.height, bg_colors)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class ClosedPortal(pygame.sprite.Sprite): #passagem fechada para o jogador
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(582, 386, self.width, self.height, bg_colors)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite): #chao do mapa
    def __init__(self, game, x, y):
        self. game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(518, 2442, self.width, self.height, bg_colors)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y