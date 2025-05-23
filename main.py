import pygame
from pygame import mixer
from config import *
from sprites import *
from sprites.sprites_base import *
from sprites.sprites_mapa1 import tilemap as tilemap1, create_tiled_map as create_tiled_map1
from sprites.sprites_mapa2 import tilemap as tilemap2, create_tiled_map as create_tiled_map2
from sprites.sprites_mapa3 import tilemap as tilemap3, create_tiled_map as create_tiled_map3
from sprites.sprites_mapa4 import tilemap as tilemap4, create_tiled_map as create_tiled_map4
from sprites.sprites_mapa5 import tilemap as tilemap5, create_tiled_map as create_tiled_map5
from sprites.sprites_mapa6 import tilemap as tilemap6, create_tiled_map as create_tiled_map6
from battleData import *
from battle import *
from npcs import npcs_data
import sys
import random
sys.stdout.reconfigure(encoding='utf-8')

pygame.display.set_caption("LimpAttack")

mapas = [
    {"tilemap": tilemap1, "create": create_tiled_map1},
    {"tilemap": tilemap2, "create": create_tiled_map2},
    {"tilemap": tilemap3, "create": create_tiled_map3},
    {"tilemap": tilemap4, "create": create_tiled_map4},
    {"tilemap": tilemap5, "create": create_tiled_map5},
    {"tilemap": tilemap6, "create": create_tiled_map6}
]

class Game:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        mixer.music.load("sounds/limpattack_ost_base.mp3")
        mixer.music.set_volume(1)
        mixer.music.play(-1)
        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain1.png')
        self.tree_spritesheet = Spritesheet('img/tree_Mid.png')
        self.in_battle = False
        self.battle_started = False
        self.battle_enemy = None
        self.fox_hp = 100
        self.battle_turn = "fox"
        self.inimigos_aviso_exibido = False
        self.trocando_mapa = False
        self.game_over_flag = False
        self.inventario_cura = []
        self.inventario_chave = []
        self.npc_dialog_active = False
        self.npc_dialog_texts = []
        self.npc_dialog_index = 0
        self.npc_dialog_current = ""
        self.npc_dialog_char_index = 0
        self.npc_dialog_speed = 2
        self.npc_dialog_last_update = 0
        self.npc_dialog_btn_rect = None
        self.npc_dialog_npc_symbol = ""
        self.mapa_atual_index = 0
        self.mapa_atual = mapas[self.mapa_atual_index]["tilemap"]
        self.fases = [True] * len(mapas)
        self.mapas_visitados = [False] * len(mapas)

    def handle_battle(self):
        enemy_battle_images = {
            "Cárie": "img/carie_luta.png",
            "Mão Podre": "img/mao_podre_luta.png",
            "Caspa no Cabelo": "img/caspa_luta.png",
            "Acne": "img/acne_luta.png",
            "Bactéria de Resfriado": "img/resfriado_luta.png",
            "Bactéria do Pé": "img/pe_luta.png",
            "Gordura na Pele": "img/gordura_luta.png"
        }
        mixer.music.stop()
        mixer.music.load("sounds/limpattack_ost_luta.mp3")
        mixer.music.set_volume(1)
        mixer.music.play(-1)
        enemy_name = self.battle_enemy.enemy_name
        from copy import deepcopy
        enemy_data = deepcopy(enemies[enemy_name])
        if hasattr(enemy_data, "hp"):
            if hasattr(enemies[enemy_name], "hp"):
                enemy_data.hp = enemies[enemy_name].hp
            else:
                enemy_data.hp = enemy_data.max_hp if hasattr(enemy_data, "max_hp") else 100
        enemy_img = pygame.image.load(enemy_battle_images[enemy_name]).convert()
        enemy_img.set_colorkey((184, 200, 168))
        enemy_img = pygame.transform.scale(enemy_img, (120, 120))
        player_img = pygame.image.load("img/nala_luta.png").convert()
        player_img.set_colorkey((184, 200, 168))
        player_img = pygame.transform.scale(player_img, (120, 120))
        bg_img = pygame.transform.scale(pygame.image.load("img/luta_bg.png"), (640, 480))
        itens_selecionados = selecionar_ataques_eficazes_e_aleatorios(enemy_name)
        resultado = battle_screen(
            player_hp=self.fox_hp,
            player_max_hp=100,
            enemy=enemy_data,
            enemy_img=enemy_img,
            player_img=player_img,
            bg_img=bg_img,
            itens_selecionados=itens_selecionados,
            main_game_over_func=self.game_over,
            inventario_cura=self.inventario_cura
        )
        if isinstance(resultado, int) and resultado > 0:
            mixer.music.stop()
            mixer.music.load("sounds/limpattack_tune_vitoria.mp3")
            mixer.music.set_volume(1)
            mixer.music.play()
            pygame.time.wait(2500)
            mixer.music.stop()
            mixer.music.load("sounds/limpattack_ost_base.mp3")
            mixer.music.set_volume(1)
            mixer.music.play(-1)
        elif resultado == "derrota":
            mixer.music.stop()
            mixer.music.load("sounds/limpattack_tune_vitoria.mp3")
            mixer.music.set_volume(1)
            mixer.music.play()
            self.game_over_flag = True
        else:
            mixer.music.stop()
            mixer.music.load("sounds/limpattack_ost_base.mp3")
            mixer.music.set_volume(1)
            mixer.music.play(-1)
        if isinstance(resultado, int):
            self.fox_hp = resultado
            if self.fox_hp > 0:
                self.battle_enemy.kill()
                self.fases[self.mapa_atual_index] = False
            else:
                self.game_over_flag = True
        elif resultado == "derrota":
            self.game_over_flag = True
        self.in_battle = False
        self.battle_started = False

    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemy = pygame.sprite.LayeredUpdates()
        self.portals = pygame.sprite.LayeredUpdates()
        mapas[self.mapa_atual_index]["create"](
            self, self.mapa_atual_index, self.mapas_visitados, self.fases, enemies, itens_cura
        )
        map_width = len(mapas[self.mapa_atual_index]["tilemap"][0]) * TILESIZE
        map_height = len(mapas[self.mapa_atual_index]["tilemap"]) * TILESIZE
        self.camera = Camera(map_width, map_height)

    def verificar_portal(self):
        if len(self.enemy) > 0:
            if not self.inimigos_aviso_exibido:
                print("Ainda há inimigos no mapa! Derrote-os antes de sair.")
                self.inimigos_aviso_exibido = True
            return False
        self.inimigos_aviso_exibido = False
        for portal in self.portals:
            if self.player.rect.colliderect(portal.rect):
                if not self.trocando_mapa:
                    self.trocando_mapa = True
                    if portal.rect.centerx < self.player.rect.centerx:
                        print("tentando trocar para o mapa anterior...")
                        self.trocar_mapa("anterior")
                    else:
                        print("tentando trocar para o proximo mapa...")
                        self.trocar_mapa("proximo")
                return True
        self.trocando_mapa = False
        return False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if self.npc_dialog_active:
                if (event.type == pygame.MOUSEBUTTONDOWN and self.npc_dialog_btn_rect and self.npc_dialog_btn_rect.collidepoint(event.pos)) \
                   or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    if self.npc_dialog_char_index < len(self.npc_dialog_texts[self.npc_dialog_index]):
                        self.npc_dialog_char_index = len(self.npc_dialog_texts[self.npc_dialog_index])
                    else:
                        self.npc_dialog_index += 1
                        if self.npc_dialog_index >= len(self.npc_dialog_texts):
                            self.npc_dialog_active = False
                        else:
                            self.npc_dialog_char_index = 0
                            self.npc_dialog_last_update = pygame.time.get_ticks()

    def update(self):
        self.all_sprites.update()
        if not self.npc_dialog_active and self.player is not None:
            for sprite in self.all_sprites:
                # Lógica para todos NPCs, exceto NPC3 (deixe NPC3 controlar seu próprio diálogo)
                if hasattr(sprite, 'symbol') and sprite.symbol in ['X', 'Y'] and self.player.rect.colliderect(sprite.rect):
                    npc_symbol = sprite.symbol
                    npc_info = npcs_data.get(npc_symbol)
                    if npc_info:
                        self.npc_dialog_active = True
                        self.npc_dialog_texts = npc_info["dialogos"]
                        self.npc_dialog_index = 0
                        self.npc_dialog_current = ""
                        self.npc_dialog_char_index = 0
                        self.npc_dialog_last_update = pygame.time.get_ticks()
                        self.npc_dialog_npc_symbol = npc_symbol
                        if hasattr(self.player, "moving"):
                            self.player.moving = False
                    break
        if self.npc_dialog_active:
            self.draw_npc_dialog()
        if len(self.enemy) == 0:
            for sprite in self.blocks:
                if isinstance(sprite, ClosedPortal):
                    sprite.kill()
                    Portal(self, sprite.rect.x // TILESIZE, sprite.rect.y // TILESIZE)
        if self.verificar_portal():
            print("jogador colidiu com um portal.")
        if self.player is not None:
            self.camera.update(self.player)

    def trocar_mapa(self, direcao="proximo"):
        if direcao == "proximo":
            if self.mapa_atual_index < len(mapas) - 1:
                self.mapa_atual_index += 1
            else:
                print("ja esta no ultimo mapa. nao e possivel avancar.")
                return
        elif direcao == "anterior":
            if self.mapa_atual_index > 0:
                self.mapa_atual_index -= 1
            else:
                print("ja esta no primeiro mapa. nao e possivel voltar.")
                return
        self.mapa_atual = mapas[self.mapa_atual_index]["tilemap"]
        print(f"mudando para o mapa {self.mapa_atual_index + 1}")
        self.new()

    def draw(self):
        self.screen.fill(BLACK)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.draw_hud_itens_cura()
        if self.npc_dialog_active:
            self.draw_npc_dialog()
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
            if not any(isinstance(s, Player) for s in self.all_sprites):
                self.playing = False
                self.game_over_flag = True
            break

    def game_over(self):
        font = pygame.font.SysFont("Arial", 80)
        small_font = pygame.font.SysFont("Arial", 40)
        alpha = 0
        fade_in = True
        while self.game_over_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game_over_flag = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.mapa_atual_index = 0
                        self.mapa_atual = mapas[self.mapa_atual_index]["tilemap"]
                        self.mapas_visitados = [False] * len(mapas)
                        self.fases[:] = [True] * len(self.fases)
                        self.fox_hp = 100
                        self.game_over_flag = False
                        self.playing = True
                        mixer.music.stop()
                        mixer.music.load("sounds/limpattack_ost_base.mp3")
                        mixer.music.set_volume(1)
                        mixer.music.play(-1)
                        self.new()
                        return
            self.screen.fill(BLACK)
            if fade_in:
                alpha += 5
                if alpha >= 255:
                    alpha = 255
                    fade_in = False
            else:
                alpha -= 2
                if alpha <= 100:
                    fade_in = True
            text_surface = font.render("GAME OVER", True, (255, 0, 0))
            text_surface.set_alpha(alpha)
            rect = text_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50))
            self.screen.blit(text_surface, rect)
            info_surface = small_font.render("aperte R para voltar a recuperar a higiene", True, (255, 255, 255))
            info_rect = info_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50))
            self.screen.blit(info_surface, info_rect)
            pygame.display.update()
            self.clock.tick(FPS)

    def intro_screen(self):
        pass

    def draw_hud_itens_cura(self):
        inventario_dict = {}
        for item in self.inventario_cura:
            if item.nome not in inventario_dict:
                inventario_dict[item.nome] = {"item": item, "quantidade": 1}
            else:
                inventario_dict[item.nome]["quantidade"] += 1
        imagens = {
            "Curativo": "img/curativo.png",
            "Comprimido": "img/comprimido.png",
            "Pomada": "img/pomada.png",
            "Chá Natural": "img/cha.png"
        }
        font = pygame.font.SysFont("arial", 18)
        hud_x = 10
        hud_y = 10
        for i, (nome, data) in enumerate(inventario_dict.items()):
            img_path = imagens.get(nome, "img/curativo.png")
            sprite = HudItemCuraSprite(hud_x + i*48, hud_y, img_path, data["quantidade"])
            sprite.draw(self.screen, font)
        if hasattr(self, 'inventario_chave') and 'sabonete' in self.inventario_chave:
            sabonete_img = pygame.image.load("img/curativo.png").convert_alpha()
            sabonete_img = pygame.transform.scale(sabonete_img, (32, 32))
            self.screen.blit(sabonete_img, (hud_x, hud_y + 54))
            font2 = pygame.font.SysFont("arial", 16, bold=True)
            self.screen.blit(font2.render("Sabonete (chave)", True, (0,0,0)), (hud_x + 40, hud_y + 60))

    def draw_npc_dialog(self):
        dialog_box_rect = pygame.Rect(40, WIN_HEIGHT - 120, WIN_WIDTH - 80, 80)
        pygame.draw.rect(self.screen, (255, 255, 255), dialog_box_rect, border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), dialog_box_rect, 2, border_radius=10)
        nome_npc = ""
        npc_symbol = getattr(self, "npc_dialog_npc_symbol", None)
        if npc_symbol:
            npc_info = npcs_data.get(npc_symbol)
            if npc_info:
                nome_npc = npc_info["nome"]
        if nome_npc:
            name_box_rect = pygame.Rect(dialog_box_rect.x + 20, dialog_box_rect.y - 32, 180, 28)
            pygame.draw.rect(self.screen, (255, 230, 250), name_box_rect, border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), name_box_rect, 2, border_radius=8)
            name_font = pygame.font.SysFont("arial", 20, bold=True)
            name_text = name_font.render(nome_npc, True, (0, 0, 0))
            self.screen.blit(name_text, (name_box_rect.x + 12, name_box_rect.y + 3))
        font = pygame.font.SysFont("arial", 16)
        now = pygame.time.get_ticks()
        if self.npc_dialog_char_index < len(self.npc_dialog_texts[self.npc_dialog_index]):
            if now - self.npc_dialog_last_update > 20:
                self.npc_dialog_char_index += self.npc_dialog_speed
                self.npc_dialog_last_update = now
        self.npc_dialog_current = self.npc_dialog_texts[self.npc_dialog_index][:self.npc_dialog_char_index]
        text_surface = font.render(self.npc_dialog_current, True, (0, 0, 0))
        self.screen.blit(text_surface, (dialog_box_rect.x + 20, dialog_box_rect.y + 20))
        btn_rect = pygame.Rect(dialog_box_rect.right - 120, dialog_box_rect.bottom - 40, 100, 30)
        pygame.draw.rect(self.screen, (200, 200, 255), btn_rect, border_radius=8)
        pygame.draw.rect(self.screen, (0, 0, 0), btn_rect, 2, border_radius=8)
        btn_font = pygame.font.SysFont("arial", 18)
        btn_text = btn_font.render("Avançar", True, (0, 0, 0))
        self.screen.blit(btn_text, (btn_rect.x + 18, btn_rect.y + 5))
        self.npc_dialog_btn_rect = btn_rect

g = Game()
g.new()
g.intro_screen()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()