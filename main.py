import pygame
from config import *
from sprites import *
import sys
from battleData import itens, enemies
import random

pygame.display.set_caption("LimpAttack") #define o titulo da janela do jogo

mapas = [tilemap1, tilemap2, tilemap3, tilemap4, tilemap5, tilemap6] #lista com os mapas disponiveis do jogo
mapa_atual_index = 0 #indice do mapa atual
mapa_atual = mapas[mapa_atual_index] #referencia para o mapa atual com base no indice
mapas_visitados = [False] * len(mapas) #marca quais mapas ja foram visitados

class Game: #classe principal que gerencia o estado geral do jogo
    def __init__(self): #inicializa o jogo, carrega spritesheets e define variaveis iniciais
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain1.png')
        self.enemy_spritesheet = Spritesheet('img/enemy1.png')
        self.tree_spritesheet = Spritesheet('img/tree_Mid.png')

        self.in_battle = False
        self.battle_started = False
        self.battle_enemy = None
        self.fox_hp = 100
        self.battle_turn = "fox"
        #variaveis que controlam o estado da batalha

        self.inimigos_aviso_exibido = False
        self.trocando_mapa = False

    def handle_battle(self): #logica principal da batalha por turnos entre jogador e inimigo
        enemy_name = random.choice(list(enemies.keys())) #escolhe inimigo aleatorio para a batalha
        enemy = enemies[enemy_name]
        current_enemy_hp = enemy.hp
        print(f"\n⚔️ BATALHA CONTRA {enemy.nome.upper()} COMEÇOU!")

        while self.in_battle: #laco principal da batalha enquanto ela estiver ativa
            print(f"\n🦊 HP da Raposa: {self.fox_hp:.0f} | 👾 HP do {enemy.nome}: {current_enemy_hp:.0f}")

            if self.battle_turn == "fox": #turno do jogador para escolher item e causar dano
                print("É o seu turno! Escolha um item:")
                for i, item in enumerate(itens.keys()):
                    print(f"[{i+1}] {item}")

                try:
                    escolha = int(input(">> ")) - 1
                    item_nome = list(itens.keys())[escolha]
                    item = itens[item_nome]
                    dano = item.calcular_dano(enemy.nome)
                    current_enemy_hp -= dano
                    print(f"🧼 Você usou {item_nome}! Dano causado: {dano:.0f}")
                except:
                    print("❌ Escolha inválida.")
                    continue

                if current_enemy_hp <= 0:
                    print(f"✅ {enemy.nome} foi derrotado!")
                    self.in_battle = False
                    self.battle_started = False
                    self.battle_enemy.kill()
                    fases[mapa_atual_index] = False
                    break
                else:
                    self.battle_turn = "enemy"

            elif self.battle_turn == "enemy": #turno do inimigo para atacar
                ataque_nome, dano = enemy.ataque_aleatorio()
                self.fox_hp -= dano
                print(f"💢 {enemy.nome} usou '{ataque_nome}'! Dano recebido: {dano:.0f}")
                if self.fox_hp <= 0:
                    print("💀 A raposa foi derrotada... FIM DE JOGO")
                    self.in_battle = False
                    self.battle_started = False
                    break
                self.battle_turn = "fox"

    def new(self): #inicia novo jogo e cria os grupos de sprites
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemy = pygame.sprite.LayeredUpdates()
        self.portals = pygame.sprite.LayeredUpdates()

        self.createTiledmap()

    def createTiledmap(self): #percorre o mapa atual e instancia os objetos baseados nos simbolos
        for i, row in enumerate(mapa_atual): #verifica o tipo de objeto para criar (ex: jogador, inimigo, arvore etc.)
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    if mapa_atual_index == 0 and not mapas_visitados[mapa_atual_index]:
                        self.player = Player(self, 15, 20)
                    else:
                        self.player = Player(self, j, i)
                if column == "E" and fases[mapa_atual_index]:
                    enemy = Enemy(self, j, i)
                if column == "t":
                    Tree1(self, j, i)
                if column == "T":
                    Tree2(self, j, i)
                if column == "M":
                    Tree3(self, j, i)
                if column == "p":
                    ClosedPortal(self, j, i)      
                if column == "p" and len(self.enemy) == 0:
                    Portal(self, j, i)

        mapas_visitados[mapa_atual_index] = True

    def verificar_portal(self): #verifica se o jogador pode usar o portal para trocar de mapa
        if len(self.enemy) > 0: #impede troca de mapa se ainda houver inimigos
            if not self.inimigos_aviso_exibido:
                print("Ainda há inimigos no mapa! Derrote-os antes de sair.")
                self.inimigos_aviso_exibido = True
            return False

        self.inimigos_aviso_exibido = False

        for portal in self.portals: #verifica colisao com algum portal
            if self.player.rect.colliderect(portal.rect):
                if not self.trocando_mapa:
                    self.trocando_mapa = True
                    if portal.rect.centerx < self.player.rect.centerx:
                        print("🔄 Tentando trocar para o mapa anterior...")
                        self.trocar_mapa("anterior")
                    else:
                        print("🔄 Tentando trocar para o próximo mapa...")
                        self.trocar_mapa("proximo")
                return True

        self.trocando_mapa = False #garante que a troca ocorra apenas uma vez por colisao
        return False
 
    def events(self): #trata eventos do pygame como fechar a janela
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self): #atualiza todos os sprites e verifica eventos como abertura de portal
        self.all_sprites.update()
        
        if len(self.enemy) == 0: #se todos inimigos foram derrotados, substitui portal fechado por aberto
            for sprite in self.blocks:
                if isinstance(sprite, ClosedPortal):
                    sprite.kill()
                    Portal(self, sprite.rect.x // TILESIZE, sprite.rect.y // TILESIZE)
        
        if self.verificar_portal(): #checa se jogador entrou no portal
            print("🔄 Jogador colidiu com um portal.")

    def trocar_mapa(self, direcao="proximo"): #muda o mapa atual com base na direcao escolhida
        global mapa_atual_index, mapa_atual

        if direcao == "proximo": #verifica se pode ir para o proximo mapa
            if mapa_atual_index < len(mapas) - 1:
                mapa_atual_index += 1
            else:
                print("⚠️ Já está no último mapa. Não é possível avançar.")
                return
        elif direcao == "anterior": #verifica se pode voltar para o mapa anterior
            if mapa_atual_index > 0:
                mapa_atual_index -= 1
            else:
                print("⚠️ Já está no primeiro mapa. Não é possível voltar.")
                return

        mapa_atual = mapas[mapa_atual_index]

        print(f"🔄 Mudando para o mapa {mapa_atual_index + 1}")

        self.new() #recarrega o jogo com o novo mapa

    def draw(self): #desenha os sprites e atualiza a tela
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()
    
    def main(self): #loop principal do jogo enquanto estiver jogando
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False
    
    def game_over(self):
        pass
    
    def intro_screen(self):
        pass

g = Game() #cria instancia do jogo
g.new()
g.intro_screen()
while g.running: #executa o jogo enquanto estiver rodando
    g.main()
    g.game_over()
pygame.quit()
sys.exit()