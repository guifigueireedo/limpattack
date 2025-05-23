import pygame
from config import *
from battleData import *
import math
import random
from npcs import npcs_data

# class Base(pygame.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.game = game
#         self._layer = BLOCK_LAYER
#         self.groups = self.game.all_sprites, self.game.blocks
#         pygame.sprite.Sprite.__init__(self, self.groups)
#         self.x = x * TILESIZE
#         self.y = y * TILESIZE
#         self.width = TILESIZE
#         self.height = TILESIZE
#         bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
#         self.image = self.game.terrain_spritesheet.get_sprite(x, y, self.width, self.height, bg_colors)
#         self.rect = self.image.get_rect()
#         self.rect.x = self.x
#         self.rect.y = self.y

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
    def get_sprite(self, x, y, width, height, bg_colors):
        sprite = pygame.Surface([width, height], pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        pixel_array = pygame.PixelArray(sprite)
        for color in bg_colors:
            pixel_array.replace(color, (0, 0, 0, 0))
        del pixel_array
        return sprite
    
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
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
        self.rect.y = self.y
        self.target_x = self.rect.x
        self.target_y = self.rect.y
        self.moving = False
    def update(self):
        self.grid_movement()
        self.animation()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.x_change = 0
        self.y_change = 0
        for item in pygame.sprite.spritecollide(self, self.game.all_sprites, False):
            if hasattr(self.game, 'mapa1_state'):
                if item.__class__.__name__ == 'Sabonete':
                    if 'sabonete' not in self.game.inventario_chave:
                        self.game.inventario_chave.append('sabonete')
                        item.kill()
                        self.game.mapa1_state['sabonete_coletado'] = True
                if item.__class__.__name__ == 'ItemCuraSprite':
                    pos = (item.rect.x // TILESIZE, item.rect.y // TILESIZE)
                    if not hasattr(self.game, 'itens_cura_coletados'):
                        self.game.itens_cura_coletados = set()
                    if pos not in self.game.itens_cura_coletados:
                        self.game.inventario_cura.append(item.item_cura)
                        self.game.itens_cura_coletados.add(pos)
                        item.kill()
        self.check_enemy_proximity()
    def check_enemy_proximity(self):
        if self.game.in_battle:
            return
        for enemy in self.game.enemy:
            dx = abs(self.rect.centerx - enemy.rect.centerx) // TILESIZE
            dy = abs(self.rect.centery - enemy.rect.centery) // TILESIZE
            if dx <= 1 and dy <= 1:
                print("⚔️ Iniciando batalha por proximidade!")
                self.game.in_battle = True
                self.game.battle_enemy = enemy
                self.game.handle_battle()
                break
    def grid_movement(self):
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
            if dx != 0 or dy != 0:
                next_rect = self.rect.copy()
                next_rect.x += dx
                next_rect.y += dy
                npc_hit = None
                for npc in self.game.all_sprites:
                    if npc.__class__.__name__ in ['NPC', 'NPC2', 'NPC3', 'NPC4'] and next_rect.colliderect(npc.rect):
                        npc_hit = npc
                        break
                if npc_hit and not self.game.npc_dialog_active:
                    npc_symbol = npc_hit.symbol if hasattr(npc_hit, "symbol") else None
                    if npc_symbol == 'C':  # <-- troque '3' por 'C'
                        if hasattr(self.game, 'inventario_chave') and 'sabonete' in self.game.inventario_chave and getattr(npc_hit, 'estado', None) == 'bloqueando':
                            npc_hit.estado = 'livre'
                            self.game.npc_dialog_active = True
                            self.game.npc_dialog_texts = npcs_data['C']['dialogos_entrega']
                            self.game.npc_dialog_index = 0
                            self.game.npc_dialog_current = ""
                            self.game.npc_dialog_char_index = 0
                            self.game.npc_dialog_last_update = pygame.time.get_ticks()
                            self.game.npc_dialog_npc_symbol = 'C'
                            if not getattr(npc_hit, 'moved', False):
                                npc_hit.remove(self.game.blocks)
                                npc_hit.rect.x += TILESIZE
                                npc_hit.rect.y -= TILESIZE
                                npc_hit.moved = True
                            if hasattr(self.game, 'mapa1_state'):
                                if 'sabonete' in self.game.inventario_chave:
                                    self.game.inventario_chave.remove('sabonete')
                                self.game.mapa1_state['npc3_estado'] = 'livre'
                                self.game.mapa1_state['npc3_moved'] = True
                                self.game.mapa1_state['npc3_pos'] = (npc_hit.rect.x // TILESIZE, npc_hit.rect.y // TILESIZE)
                            self.moving = False
                            return
                        elif getattr(npc_hit, 'estado', None) == 'bloqueando':
                            self.game.npc_dialog_active = True
                            self.game.npc_dialog_texts = npcs_data['C']['dialogos_bloqueando']
                            self.game.npc_dialog_index = 0
                            self.game.npc_dialog_current = ""
                            self.game.npc_dialog_char_index = 0
                            self.game.npc_dialog_last_update = pygame.time.get_ticks()
                            self.game.npc_dialog_npc_symbol = 'C'
                            self.moving = False

                            if not self.game.sabonete_spawned:
                                print("DEBUG: Tentando criar sabonete...")
                                Sabonete(self.game, 19, 2)
                                self.game.sabonete_spawned = True
                                print("DEBUG: Sabonete spawnado!")
                            return
                        elif getattr(npc_hit, 'estado', None) == 'livre':
                            self.game.npc_dialog_active = True
                            self.game.npc_dialog_texts = npcs_data['C']['dialogos_livre']
                            self.game.npc_dialog_index = 0
                            self.game.npc_dialog_current = ""
                            self.game.npc_dialog_char_index = 0
                            self.game.npc_dialog_last_update = pygame.time.get_ticks()
                            self.game.npc_dialog_npc_symbol = 'C'
                            self.moving = False
                            return
                    npc_info = npcs_data.get(npc_symbol)
                    if npc_info:
                        self.game.npc_dialog_active = True
                        if "dialogos" in npc_info:
                            self.game.npc_dialog_texts = npc_info["dialogos"]
                        elif "dialogos_bloqueando" in npc_info:
                            self.game.npc_dialog_texts = npc_info["dialogos_bloqueando"]
                        elif "dialogos_entrega" in npc_info:
                            self.game.npc_dialog_texts = npc_info["dialogos_entrega"]
                        elif "dialogos_livre" in npc_info:
                            self.game.npc_dialog_texts = npc_info["dialogos_livre"]
                        else:
                            self.game.npc_dialog_texts = ["..."]
                        self.game.npc_dialog_index = 0
                        self.game.npc_dialog_current = ""
                        self.game.npc_dialog_char_index = 0
                        self.game.npc_dialog_last_update = pygame.time.get_ticks()
                        self.game.npc_dialog_npc_symbol = npc_symbol
                        self.moving = False
                    return
                if self.game.npc_dialog_active:
                    return
                will_collide = any(next_rect.colliderect(block.rect) for block in self.game.blocks)
                will_collide_enemy = any(next_rect.colliderect(enemy.rect) for enemy in self.game.enemy)
                if not will_collide and not will_collide_enemy and not npc_hit:
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
    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            hits += [npc for npc in self.game.all_sprites if (isinstance(npc, NPC) or isinstance(npc, NPC2)) and self.rect.colliderect(npc.rect)]
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            hits += [npc for npc in self.game.all_sprites if (isinstance(npc, NPC) or isinstance(npc, NPC2)) and self.rect.colliderect(npc.rect)]
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
    def animation(self):
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, enemy_name):
        bg_colors = [CHARACTER_BG]
        self.game = game
        self.enemy_name = enemy_name
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.enemy
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = 64
        self.height = 64
        self.spritesheet = Spritesheet(enemy_spritesheets[enemy_name])
        self.animation_frames = enemy_animations[enemy_name]
        self.animation_loop = 0
        self.image = self.spritesheet.get_sprite(0, 0, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    def update(self):
        self.animate()
        self.random_movement()
    def animate(self):
        frame = self.animation_frames[math.floor(self.animation_loop)]
        self.image = self.spritesheet.get_sprite(frame[0], frame[1], self.width, self.height, [CHARACTER_BG])
        self.animation_loop += 0.3
        
        if self.animation_loop >= len(self.animation_frames):
            self.animation_loop = 0
    def random_movement(self):
        if random.random() < 0.02:
            dx, dy = random.choice([(0, -TILESIZE), (0, TILESIZE), (-TILESIZE, 0), (TILESIZE, 0)])
            next_rect = self.rect.copy()
            next_rect.x += dx
            next_rect.y += dy
            if not any(next_rect.colliderect(block.rect) for block in self.game.blocks) and \
               not any(next_rect.colliderect(enemy.rect) for enemy in self.game.enemy if enemy != self):
                self.rect.x += dx
                self.rect.y += dy

class Ground(pygame.sprite.Sprite):
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

class Ground2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(518, 4722, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Tree1(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1130, 2570, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y    

class Tree2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1130, 2602, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Tree3(pygame.sprite.Sprite):
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
        self.image = self.game.tree_spritesheet.get_sprite(0, 0, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Portal(pygame.sprite.Sprite):
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

class ClosedPortal(pygame.sprite.Sprite):
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

class ItemCuraSprite(pygame.sprite.Sprite):
    def __init__(self, game, x, y, item_cura):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.item_cura = item_cura
        imagens = {
            "Curativo": "img/curativo.png",
            "Pomada": "img/pomada.png",
            "Xarope": "img/xarope.png",
            "Chá Natural": "img/cha.png"
        }
        img_path = imagens.get(item_cura.nome, "img/curativo.png")
        self.spritesheet = Spritesheet(img_path)
        bg_colors = [CHARACTER_BG]
        self.image = self.spritesheet.get_sprite(0, 0, 32, 32, bg_colors)
        self.rect = self.image.get_rect(topleft=(10, 10))
        self.rect.x = self.x
        self.rect.y = self.y

class HudItemCuraSprite(pygame.sprite.Sprite):
    def __init__(self, hud_x, hud_y, img_path, quantidade):
        super().__init__()
        bg_colors = [CHARACTER_BG]
        spritesheet = Spritesheet(img_path)
        self.image = spritesheet.get_sprite(0, 0, 32, 32, bg_colors)
        self.rect = self.image.get_rect(topleft=(hud_x, hud_y))
        self.quantidade = quantidade

    def draw(self, surface, font):
        surface.blit(self.image, self.rect)
        qtd_surface = font.render(f"x{self.quantidade}", True, (255,255,255))
        surface.blit(qtd_surface, (self.rect.right - 18, self.rect.bottom - 18))

class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y, symbol="X"):
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
        self.image.fill((255, 105, 180))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class NPC2(pygame.sprite.Sprite):
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

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    def update(self, target):
        x = -target.rect.centerx + WIN_WIDTH // 2
        y = -target.rect.centery + WIN_HEIGHT // 2
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIN_WIDTH), x)
        y = max(-(self.height - WIN_HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)

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
        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        self.image = self.game.sabonete_spritesheet.get_sprite(0, 0, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
