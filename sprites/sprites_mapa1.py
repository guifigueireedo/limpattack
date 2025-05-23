import pygame
from config import *
from battleData import *
from sprites.sprites_base import *
from npcs import npcs_data
import random

tilemap = [
    'MTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT',
    'M.............................u.....,,Np',
    'M.H..........o.....BH.........u.....,..t',
    'M.......H.................H.......,,,..M',
    'M.................................,....M',
    'M...............o.................,....M',
    'M.................................,....M',
    'M.................................,....M',
    'M..W.................W.........uuu3uuuuM',
    'M....,.................,..........,....M',
    'M....,.....,...........,.....,....,....M',
    'M....,.....,...........,.....,....,....M',
    'M....,.....,...........,.....,....,....M',
    'M....,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,....M',
    'M....,.....,.....,.....,.....,.........M',
    'M....,.....,.....,.....,.....,.........M',
    'M....,.....,.....,.....,.....,.........M',
    'M....,.....,.....,.....,.....,.........M',
    'M....,.....,.....,.....,.....,.........M',
    'M....,..e..,..e..,..e..,..e..,.........M',
    'M....,.....,.....,.....,.....,.........M',
    'M....,.....,.....,.....,.....,.........M',
    'M..ChhhF.ChhhF.ChhhF.ChhhF.ChhhF.......M',
    'M..cYYYf.cYYYf.cYYYf.cYYYf.cYYYf.......M',
    'M.1jaaai.jÇ..i.jS..i2jaaai.jS..i.......M',
    'M..jaaaiUj.ç.i.j...i.jaaai.j...i.......M',
    'M..JDDDI.JDDDI.JDDDI.JDDDI.JDDDI.......M',
    'M..LlllK.LlllK.LlllK.LlllK.LlllK.......M',
    'M.......U..............................M',
    'MttttttttttttttttttttttttttttttttttttttM',
]

def create_tiled_map(game, mapa_atual_index, mapas_visitados, fases, enemies, itens_cura):
    # Persistência de estado do NPC3 e do sabonete
    if not hasattr(game, 'mapa1_state'):
        game.mapa1_state = {
            'npc3_estado': 'bloqueando',
            'npc3_moved': False,
            'npc3_pos': None,
            'sabonete_coletado': False
        }
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            Ground(game, j, i)
            if column == ",":
                Ground2(game, j, i)
            if column == "N":
                Ground2(game, j, i)
                if not mapas_visitados[mapa_atual_index]:
                    game.player = Player(game, 5, 10)
                else:
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
            if column == "H":
                House(game, j, i)
            if column == "C":
                CercaTop1(game, j, i)
            if column == "h":
                CercaTop2(game, j, i)
            if column == "F":
                CercaTop3(game, j, i)
            if column == "c":
                CercaTopMid1(game, j, i)
            if column == "Y":
                CercaTopMid2(game, j, i)
            if column == "f":
                CercaTopMid3(game, j, i)
            if column == "j":
                CercaMid1(game, j, i)
            if column == "i":
                CercaMid2(game, j, i)
            if column == "J":
                CercaBotMid1(game, j, i)
            if column == "D":
                CercaBotMid2(game, j, i)
            if column == "I":
                CercaBotMid3(game, j, i)
            if column == "L":
                CercaBot1(game, j, i)
            if column == "l":
                CercaBot2(game, j, i)
            if column == "K":
                CercaBot3(game, j, i)
            if column == "o":
                BigTree(game, j, i)
            if column == "a":
                Arbs(game, j, i)
            if column == "e":
                Espan(game, j, i)
            if column == "Ç":
                Poco(game, j, i)
            if column == "ç":
                Poco2(game, j, i)
            if column == "S":
                Sacos(game, j, i)
            if column == "W":
                Wind(game, j, i)
            if column == "u":
                Toco(game, j, i)
            if column == "U":
                pos = (j, i)
                if not hasattr(game, 'itens_cura_coletados'):
                    game.itens_cura_coletados = set()
                if pos not in game.itens_cura_coletados:
                    item_cura = random.choices(itens_cura, weights=[60, 30, 8, 2])[0]
                    ItemCuraSprite(game, j, i, item_cura)
            if column == "1":
                NPC(game, j, i, symbol="X")
            if column == "2":
                NPC2(game, j, i, symbol="Y")
            if column == "3":
                # Sempre coloca Ground2 embaixo do NPC3
                Ground2(game, j, i)
                # Posição padrão do NPC3
                npc3_x, npc3_y = j, i
                # Se já moveu, coloca na nova posição
                if game.mapa1_state['npc3_moved'] and game.mapa1_state['npc3_pos']:
                    npc3_x, npc3_y = game.mapa1_state['npc3_pos']
                npc3 = NPC3(game, npc3_x, npc3_y, symbol="3")
                npc3.estado = game.mapa1_state['npc3_estado']
                npc3.moved = game.mapa1_state['npc3_moved']
                if npc3.moved:
                    try:
                        npc3.remove(game.blocks)
                    except Exception:
                        pass
                # Salva referência para persistência
                game.npc3_ref = npc3
            if column == "B":
                # Só cria o sabonete se não foi coletado
                if not game.mapa1_state['sabonete_coletado'] and 'sabonete' not in getattr(game, 'inventario_chave', []):
                    Sabonete(game, j, i)
    mapas_visitados[mapa_atual_index] = True

class House(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(518, 3178, 160, 256, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaTop1(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066, 1126, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaTop2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*1), 1126, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaTop3(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*2), 1126, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaTopMid1(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066, 1126+(TILESIZE*1), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaTopMid2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*1), 1126+(TILESIZE*1), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaTopMid3(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*2), 1126+(TILESIZE*1), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaMid1(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066, 1126+(TILESIZE*2), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaMid2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*2), 1126+(TILESIZE*2), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaBotMid1(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066, 1126+(TILESIZE*3), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaBotMid2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*1), 1126+(TILESIZE*3), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaBotMid3(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*2), 1126+(TILESIZE*3), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaBot1(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066, 1126+(TILESIZE*4), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaBot2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*1), 1126+(TILESIZE*4), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaBot3(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*2), 1126+(TILESIZE*4), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class BigTree(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1678, 1414, 1796-1678, 1574-1414, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Arbs(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1034, 1382, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Espan(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1034, 1414, self.width, 64, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Poco(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1162, 1350, 64, 64, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Poco2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1226, 1382, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Sacos(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(2324, 1862, 96, 64, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Wind(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(550, 3114, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Toco(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(130, 386, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class NPC3(pygame.sprite.Sprite):
    def __init__(self, game, x, y, symbol="3"):
        self.game = game
        self.symbol = symbol
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((200, 200, 80))  # Unique color for NPC3
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.estado = 'bloqueando'  # 'bloqueando', 'livre'
        self.portal_pos = (x, y)
        self.moved = False

    def update(self):
        pass  # Diálogo e movimento agora são tratados pelo Player

class Sabonete(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = pygame.image.load("img/curativo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
