import pygame
from config import *
from battleData import *
from sprites.sprites_base import *
from npcs import npcs_data
import random

tilemap = [
    'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT',
    'pN,,...............U...................p',
    't..,..Z.....X.....Z...........Z........t',
    'M..,...................................M',
    'M..,...................................M',
    'M..,...................................M',
    'M..,...................................M',
    'M..,...................................M',
    'M..,...................................M',
    'M..,...................................M',
    'M..,...................................M',
    'M..,...................................M',
    'M..,...................................M',
    'M..,...................................M',
    'M..,...................................M',
    'M..,........Z........QQQQQQQQQQQQQQQ...M',
    'M..,.................Q.............Q...M',
    'M..,.................Q.............Q...M',
    'M..,.................Q......U......Q...M',
    'M..,................1Q.............Q...M',
    'M..,...............................Q...M',
    'M..,.................Q......O...U..Q...M',
    'M..,.................Q.............Q...M',
    'M..,.................Q.............Q...M',
    'M..,.................Q.............Q...M',
    'M..,.................Q.............Q...M',
    'M..,.................QQQQQQQQQQQQQQQ...M',
    'M......................................M',
    'M......................................M',
    'MttttttttttttttttttttttttttttttttttttttM',
]

def create_tiled_map(game, mapa_atual_index, mapas_visitados, fases, enemies, itens_cura):
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            Ground(game, j, i)
            if column == ",":
                Ground2(game, j, i)
            if column == "N":
                game.player = Player(game, j, i)
                Ground2(game, j, i)
            if column == "E" and fases[mapa_atual_index]:
                enemy_name = random.choice(list(enemies.keys()))
                game.battle_enemy = Enemy(game, j, i, enemy_name)
            if column == "t":
                Tree1(game, j, i)
            if column == "T":
                Tree2(game, j, i)
            if column == "M":
                Tree3(game, j, i)
            if column == "p":
                ClosedPortal(game, j, i)
            if column == "p" and len(game.enemy) == 0:
                Portal(game, j, i)
            if column == "Z":
                House2(game, j, i)
            if column == "P":
                Porta(game, j, i)
            if column == "s":
                Escada(game, j, i)
            if column == "V":
                Vaso(game, j, i)
            if column == "O":
                Fonte(game, j, i)
            if column == "Q":
                Flores(game, j, i)
            if column == "U":
                item_cura = random.choices(itens_cura, weights=[60, 30, 8, 2])[0]
                ItemCuraSprite(game, j, i, item_cura)
            if column == "1":
                NPC4(game, j, i, symbol="D")
    mapas_visitados[mapa_atual_index] = True

class House2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1034, 1638, 159, 319, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Porta(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1068, 1574, 27, 63, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y    

class Escada(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1317, 1992, 48, 29, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y   

class Vaso(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(586, 1382, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Fonte(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1070 , 2993 , 92, 86, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y   

class Flores(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1100, 2574, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class NPC4(pygame.sprite.Sprite):
    def __init__(self, game, x, y, symbol="Y"):
        self.game = game
        self.symbol = symbol
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((180, 180, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y