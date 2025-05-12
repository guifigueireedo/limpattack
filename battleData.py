from config import *

class EnemyBattle: #classe que representa um inimigo na batalha
    def __init__(self, nome, hp, ataques): #inicializa o inimigo com nome, hp e ataques
        self.nome = nome
        self.hp = hp
        self.ataques = ataques

    def ataque_aleatorio(self): #executa um ataque aleatorio com base na probabilidade de cada ataque
        from random import random
        for nome, dados in self.ataques.items():
            if random() <= dados["probabilidade"]:
                return nome, dados["dano"]
        return "Ataque Fraco", 3

class Item: #classe que representa um item que o jogador pode usar na batalha
    def __init__(self, nome, dano_base, eficacias): #inicializa o item com nome, dano base e eficacias
        self.nome = nome
        self.dano_base = dano_base
        self.eficacias = eficacias

    def calcular_dano(self, inimigo_nome): #calcula o dano com base na eficacia contra o inimigo
        return self.dano_base * self.eficacias.get(inimigo_nome, 0.2)

enemies = { #dicionario com todos os inimigos e seus respectivos ataques
    "Cárie": EnemyBattle("Cárie", 100, {
        "Dente Sujo": {"dano": 5, "probabilidade": 0.4},
        "Mau Hálito": {"dano": 10, "probabilidade": 0.3},
        "Dor e Inflamação": {"dano": 15, "probabilidade": 0.2},
        "Gengivite": {"dano": 25, "probabilidade": 0.1}
    }),
    "Mão Podre": EnemyBattle("Mão Suja", 80, {
        "Mãos Suja": {"dano": 5, "probabilidade": 0.5},
        "Germes": {"dano": 10, "probabilidade": 0.3},
        "Doenças da Pele": {"dano": 12, "probabilidade": 0.15},
        "Infecção": {"dano": 18, "probabilidade": 0.05}
    }),
    "Caspa no Cabelo": EnemyBattle("Caspa no Cabelo", 60, {
        "Caspa": {"dano": 4, "probabilidade": 0.5},
        "Coceira Intensa": {"dano": 8, "probabilidade": 0.3},
        "Queda de Cabelo": {"dano": 12, "probabilidade": 0.15},
        "Lesão no Couro Cabeludo": {"dano": 18, "probabilidade": 0.05}
    }),
    "Acne": EnemyBattle("Acne", 70, {
        "Cravo": {"dano": 6, "probabilidade": 0.4},
        "Espinha": {"dano": 9, "probabilidade": 0.35},
        "Inflamação": {"dano": 14, "probabilidade": 0.2},
        "Cisto": {"dano": 20, "probabilidade": 0.05}
    }),
    "Bactéria de Resfriado": EnemyBattle("Bactéria de Resfriado", 90, {
        "Espirro": {"dano": 5, "probabilidade": 0.4},
        "Nariz Entupido": {"dano": 10, "probabilidade": 0.3},
        "Tosse seca": {"dano": 15, "probabilidade": 0.2},
        "Febre": {"dano": 25, "probabilidade": 0.1}
    }),
    "Bactéria do Pé": EnemyBattle("Bactéria do Pé", 80, {
        "Fungo Pé Sujo": {"dano": 6, "probabilidade": 0.4},
        "Bicho de Oé": {"dano": 12, "probabilidade": 0.3},
        "Unha encravada": {"dano": 18, "probabilidade": 0.2},
        "Infecção Grave": {"dano": 30, "probabilidade": 0.1}
    }),
    "Gordura na Pele": EnemyBattle("Gordura na Pele", 70, {
        "Pele Oleosa": {"dano": 4, "probabilidade": 0.4},
        "Acúmulo de Sebo": {"dano": 8, "probabilidade": 0.3},
        "Obstrução dos Poros": {"dano": 12, "probabilidade": 0.2},
        "Acne com Sebo": {"dano": 18, "probabilidade": 0.1}
    })
}

itens = { #dicionario com todos os itens e suas eficacias contra os inimigos
    "Escova de Dente": Item("Escova de Dente", 15, {
        "Gordura na Pele": 0.5, "Caspa no Cabelo": 0.5,
        "Mão Suja": 0.5, "Acne": 0.5, "Bactéria de Resfriado": 1,
        "Cárie": 4, "Bactéria do Pé": 0.5
    }),
    "Pasta de Dente": Item("Pasta de Dente", 20, {
        "Gordura na Pele": 0.5, "Caspa no Cabelo": 0.5,
        "Mão Suja": 0.5, "Acne": 0.5, "Bactéria de Resfriado": 0.5,
        "Cárie": 4, "Bactéria do Pé": 0.5
    }),
    "Álcool 70%": Item("Álcool 70%", 25, {
        "Gordura na Pele": 1, "Caspa no Cabelo": 0.5,
        "Mão Suja": 4, "Acne": 0.5, "Bactéria de Resfriado": 2.5,
        "Cárie": 0.5, "Bactéria do Pé": 1.5
    }),
    "Sabão Líquido": Item("Sabão Líquido", 18, {
        "Gordura na Pele": 4, "Caspa no Cabelo": 1,
        "Mão Suja": 4, "Acne": 3, "Bactéria de Resfriado": 2.5,
        "Cárie": 0.5, "Bactéria do Pé": 2
    }),
    "Água Comum": Item("Água Comum", 10, {
        "Gordura na Pele": 1.5, "Caspa no Cabelo": 1,
        "Mão Suja": 2, "Acne": 1, "Bactéria de Resfriado": 0.5,
        "Cárie": 1, "Bactéria do Pé": 1
    }),
    "Escova para o Corpo": Item("Escova para o Corpo", 12, {
        "Gordura na Pele": 4, "Caspa no Cabelo": 0.5,
        "Mão Suja": 2, "Acne": 1, "Bactéria de Resfriado": 0.5,
        "Cárie": 0.5, "Bactéria do Pé": 2
    }),
    "Lenço Umidecido": Item("Lenço Umidecido", 8, {
        "Gordura na Pele": 1.5, "Caspa no Cabelo": 0.5,
        "Mão Suja": 3, "Acne": 1, "Bactéria de Resfriado": 3,
        "Cárie": 0.5, "Bactéria do Pé": 0.5
    }),
    "Shampoo": Item("Shampoo", 16, {
        "Gordura na Pele": 1.5, "Caspa no Cabelo": 4,
        "Mão Suja": 2, "Acne": 1, "Bactéria de Resfriado": 0.5,
        "Cárie": 0.5, "Bactéria do Pé": 1
    })
}

enemy_spritesheets = {
    "Cárie": "img/carie_spritesheet.png",
    "Mão Podre": "img/mao_podre_spritesheet.png",
    "Caspa no Cabelo": "img/caspa_spritesheet.png",
    "Acne": "img/acne_spritesheet.png",
    "Bactéria de Resfriado": "img/resfriado_spritesheet.png",
    "Bactéria do Pé": "img/pe_spritesheet.png",
    "Gordura na Pele": "img/gordura_spritesheet.png"
}

enemy_animations = {
    "Cárie": [(0, 0), (64, 0), (128, 0), (192, 0), (256, 0), (320, 0),
              (0, 64), (64, 64), (128, 64), (192, 64), (256, 64), (320, 64),
              (0, 128), (64, 128), (128, 128), (192, 128), (256, 128), (320, 128),
              (0, 192), (64, 192), (128, 192), (192, 192), (256, 192), (320, 192),
              (0, 256), (64, 256), (128, 256), (192, 256), (256, 256), (320, 256),
              (0, 320), (64, 320), (128, 320), (192, 320), (256, 320), (320, 320),],
    "Mão Podre": [(0, 0), (64, 0), (128, 0), (192, 0), (256, 0), (320, 0),
              (0, 64), (64, 64), (128, 64), (192, 64), (256, 64), (320, 64),
              (0, 128), (64, 128), (128, 128), (192, 128), (256, 128), (320, 128),
              (0, 192), (64, 192), (128, 192), (192, 192), (256, 192), (320, 192),
              (0, 256), (64, 256), (128, 256), (192, 256), (256, 256), (320, 256),
              (0, 320), (64, 320), (128, 320), (192, 320), (256, 320), (320, 320),],
    "Caspa no Cabelo": [(0, 0), (64, 0), (128, 0), (192, 0), (256, 0), (320, 0),
              (0, 64), (64, 64), (128, 64), (192, 64), (256, 64), (320, 64),
              (0, 128), (64, 128), (128, 128), (192, 128), (256, 128), (320, 128),
              (0, 192), (64, 192), (128, 192), (192, 192), (256, 192), (320, 192),
              (0, 256), (64, 256), (128, 256), (192, 256), (256, 256), (320, 256),
              (0, 320), (64, 320), (128, 320), (192, 320), (256, 320), (320, 320),],
    "Acne": [(0, 0), (64, 0), (128, 0), (192, 0), (256, 0), (320, 0),
              (0, 64), (64, 64), (128, 64), (192, 64), (256, 64), (320, 64),
              (0, 128), (64, 128), (128, 128), (192, 128), (256, 128), (320, 128),
              (0, 192), (64, 192), (128, 192), (192, 192), (256, 192), (320, 192),
              (0, 256), (64, 256), (128, 256), (192, 256), (256, 256), (320, 256),
              (0, 320), (64, 320), (128, 320), (192, 320), (256, 320), (320, 320),],
    "Bactéria de Resfriado": [(0, 0), (64, 0), (128, 0), (192, 0), (256, 0), (320, 0),
              (0, 64), (64, 64), (128, 64), (192, 64), (256, 64), (320, 64),
              (0, 128), (64, 128), (128, 128), (192, 128), (256, 128), (320, 128),
              (0, 192), (64, 192), (128, 192), (192, 192), (256, 192), (320, 192),
              (0, 256), (64, 256), (128, 256), (192, 256), (256, 256), (320, 256),
              (0, 320), (64, 320), (128, 320), (192, 320), (256, 320), (320, 320),],
    "Bactéria do Pé": [(0, 0), (64, 0), (128, 0), (192, 0), (256, 0), (320, 0),
              (0, 64), (64, 64), (128, 64), (192, 64), (256, 64), (320, 64),
              (0, 128), (64, 128), (128, 128), (192, 128), (256, 128), (320, 128),
              (0, 192), (64, 192), (128, 192), (192, 192), (256, 192), (320, 192),
              (0, 256), (64, 256), (128, 256), (192, 256), (256, 256), (320, 256),
              (0, 320), (64, 320), (128, 320), (192, 320), (256, 320), (320, 320),],
    "Gordura na Pele": [(0, 0), (64, 0), (128, 0), (192, 0), (256, 0), (320, 0),
              (0, 64), (64, 64), (128, 64), (192, 64), (256, 64), (320, 64),
              (0, 128), (64, 128), (128, 128), (192, 128), (256, 128), (320, 128),
              (0, 192), (64, 192), (128, 192), (192, 192), (256, 192), (320, 192),
              (0, 256), (64, 256), (128, 256), (192, 256), (256, 256), (320, 256),
              (0, 320), (64, 320), (128, 320), (192, 320), (256, 320), (320, 320),]
}
