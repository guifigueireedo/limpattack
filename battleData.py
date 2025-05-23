from config import *
import random

class EnemyBattle:
    def __init__(self, nome, hp, ataques):
        self.nome = nome
        self.hp = hp
        self.ataques = ataques

    def ataque_aleatorio(self):
        from random import random
        for nome, dados in self.ataques.items():
            if random() <= dados["probabilidade"]:
                return nome, dados["dano"]
        return "Ataque Fraco", 3

class Item:
    def __init__(self, nome, dano_base, eficacias):
        self.nome = nome
        self.dano_base = dano_base
        self.eficacias = eficacias

    def calcular_dano(self, inimigo_nome):
        return self.dano_base * self.eficacias.get(inimigo_nome, 0.2)

class ItemCura:
    def __init__(self, nome, cura, raridade):
        self.nome = nome
        self.cura = cura
        self.raridade = raridade

def selecionar_ataques_eficazes_e_aleatorios(enemy_name):
    todos_itens = list(itens.values())
    eficazes = sorted(
        todos_itens,
        key=lambda item: item.eficacias.get(enemy_name, 0),
        reverse=True
    )
    melhores = eficazes[:2]
    restantes = [item for item in todos_itens if item not in melhores]
    aleatorios = random.sample(restantes, 2) if len(restantes) >= 2 else restantes
    return melhores + aleatorios

enemies = {
    "Cárie": EnemyBattle("Cárie", 100, {
        "Dente Sujo": {"dano": 5, "probabilidade": 0.4},
        "Mau Hálito": {"dano": 10, "probabilidade": 0.3},
        "Dor e Inflamação": {"dano": 15, "probabilidade": 0.2},
        "Gengivite": {"dano": 18, "probabilidade": 0.1}
    }),
    "Mão Podre": EnemyBattle("Mão Podre", 80, {
        "Mãos Suja": {"dano": 5, "probabilidade": 0.5},
        "Germes": {"dano": 10, "probabilidade": 0.3},
        "Doenças da Pele": {"dano": 12, "probabilidade": 0.15},
        "Infecção": {"dano": 25, "probabilidade": 0.05}
    }),
    "Caspa no Cabelo": EnemyBattle("Caspa no Cabelo", 70, {
        "Caspa": {"dano": 4, "probabilidade": 0.5},
        "Coceira Intensa": {"dano": 8, "probabilidade": 0.3},
        "Queda de Cabelo": {"dano": 12, "probabilidade": 0.15},
        "Lesão no Couro Cabeludo": {"dano": 25, "probabilidade": 0.05}
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
        "Tosse Seca": {"dano": 15, "probabilidade": 0.2},
        "Febre": {"dano": 25, "probabilidade": 0.1}
    }),
    "Bactéria do Pé": EnemyBattle("Bactéria do Pé", 80, {
        "Fungo Pé Sujo": {"dano": 6, "probabilidade": 0.4},
        "Bicho de Oé": {"dano": 12, "probabilidade": 0.3},
        "Unha Encravada": {"dano": 18, "probabilidade": 0.2},
        "Infecção Grave": {"dano": 30, "probabilidade": 0.1}
    }),
    "Gordura na Pele": EnemyBattle("Gordura na Pele", 70, {
        "Pele Oleosa": {"dano": 4, "probabilidade": 0.4},
        "Acúmulo de Sebo": {"dano": 8, "probabilidade": 0.3},
        "Obstrução dos Poros": {"dano": 12, "probabilidade": 0.2},
        "Acne com Sebo": {"dano": 18, "probabilidade": 0.1}
    })
}

# boss = {
#     "Rei Mundiça": EnemyBattle("Rei Mundiça", 200, {
#         "Ataque Poderoso": {"dano": 20, "probabilidade": 0.4},
#         "Grito de Guerra": {"dano": 30, "probabilidade": 0.3},
#         "Destruição Total": {"dano": 50, "probabilidade": 0.2},
#         "Fúria do Rei": {"dano": 70, "probabilidade": 0.1}
#     })
# }

itens = {
    "Escova de Dente": Item("Escova de Dente", 12, {
        "Cárie": 4, "Mão Podre": 0.5, "Caspa no Cabelo": 0.2, "Acne": 0.2,
        "Bactéria de Resfriado": 0.2, "Bactéria do Pé": 0.2, "Gordura na Pele": 0.2
    }),
    "Pasta de Dente": Item("Pasta de Dente", 10, {
        "Cárie": 4, "Mão Podre": 0.5, "Caspa no Cabelo": 0.2, "Acne": 0.2,
        "Bactéria de Resfriado": 0.2, "Bactéria do Pé": 0.2, "Gordura na Pele": 0.2
    }),
    "Álcool 70%": Item("Álcool 70%", 15, {
        "Mão Podre": 4, "Bactéria de Resfriado": 3, "Cárie": 0.2, "Caspa no Cabelo": 0.2,
        "Acne": 0.5, "Bactéria do Pé": 1, "Gordura na Pele": 0.5
    }),
    "Sabão Líquido": Item("Sabão Líquido", 14, {
        "Mão Podre": 4, "Gordura na Pele": 4, "Cárie": 0.2, "Caspa no Cabelo": 0.5,
        "Acne": 1, "Bactéria de Resfriado": 1, "Bactéria do Pé": 1
    }),
    "Bucha": Item("Bucha", 10, {
        "Gordura na Pele": 4, "Acne": 4, "Cárie": 0.2, "Caspa no Cabelo": 0.5,
        "Mão Podre": 1, "Bactéria de Resfriado": 1, "Bactéria do Pé": 1
    }),
    "Sabonete": Item("Sabonete", 12, {
        "Gordura na Pele": 4, "Bactéria do Pé": 4, "Cárie": 0.2, "Caspa no Cabelo": 0.5,
        "Mão Podre": 4, "Acne": 1, "Bactéria de Resfriado": 2
    }),
    "Shampoo": Item("Shampoo", 10, {
        "Caspa no Cabelo": 4, "Gordura na Pele": 2, "Cárie": 0.2, "Mão Podre": 0.5,
        "Acne": 0.5, "Bactéria de Resfriado": 0.2, "Bactéria do Pé": 0.2
    }),
    "Condicionador": Item("Condicionador", 8, {
        "Caspa no Cabelo": 4, "Gordura na Pele": 1.5, "Cárie": 0.2, "Mão Podre": 0.5,
        "Acne": 0.5, "Bactéria de Resfriado": 0.2, "Bactéria do Pé": 0.2
    }),
    "Sabonete Facial": Item("Sabonete Facial", 10, {
        "Acne": 4, "Gordura na Pele": 2, "Cárie": 0.2, "Caspa no Cabelo": 0.5,
        "Mão Podre": 2, "Bactéria de Resfriado": 0.2, "Bactéria do Pé": 0.2
    }),
    "Lenço Umidecido": Item("Lenço Umidecido", 8, {
        "Acne": 4, "Bactéria de Resfriado": 2, "Cárie": 0.2, "Caspa no Cabelo": 0.5,
        "Mão Podre": 1, "Gordura na Pele": 1, "Bactéria do Pé": 0.5
    }),
    "Talco": Item("Talco", 10, {
        "Bactéria do Pé": 4, "Gordura na Pele": 1.5, "Cárie": 0.2, "Caspa no Cabelo": 0.2,
        "Mão Podre": 0.5, "Acne": 0.5, "Bactéria de Resfriado": 0.2
    }),
    "Nulo": Item("Nulo", 0, {
        "Cárie": 0, "Mão Podre": 0, "Caspa no Cabelo": 0, "Acne": 0,
        "Bactéria de Resfriado": 0, "Bactéria do Pé": 0, "Gordura na Pele": 0
    })
}

itens_cura = [
    ItemCura("Curativo", 15, 1),
    ItemCura("Pomada", 30, 2),
    ItemCura("Xarope", 60, 3),
    ItemCura("Chá Natural", 100, 4)
]

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
"Mão Podre": [(0, 0), (64, 0), (128, 0), (192, 0),
              (0, 64), (64, 64), (128, 64), (192, 64),
              (0, 128), (64, 128), (128, 128), (192, 128),
              (0, 192),],
"Caspa no Cabelo": [(0, 0), (64, 0), (128, 0), (192, 0), (256, 0), (320, 0),
              (0, 64), (64, 64), (128, 64), (192, 64), (256, 64), (320, 64),
              (0, 128), (64, 128), (128, 128), (192, 128), (256, 128), (320, 128),
              (0, 192), (64, 192), (128, 192), (192, 192), (256, 192), (320, 192),
              (0, 256), (64, 256), (128, 256), (192, 256), (256, 256), (320, 256),
              (0, 320), (64, 320), (128, 320), (192, 320), (256, 320),],
"Acne": [(0, 0), (64, 0), (128, 0), (192, 0), (256, 0), (320, 0),
              (0, 64), (64, 64), (128, 64), (192, 64), (256, 64), (320, 64),
              (0, 128), (64, 128), (128, 128), (192, 128), (256, 128), (320, 128),
              (0, 192), (64, 192), (128, 192), (192, 192), (256, 192), (320, 192),
              (0, 256), (64, 256), (128, 256), (192, 256), (256, 256), (320, 256),
              (0, 320), (64, 320), (128, 320), (192, 320), (256, 320),],
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
              (0, 320), (64, 320), (128, 320),],
"Gordura na Pele": [(0, 0), (64, 0), (128, 0), (192, 0),
              (0, 64), (64, 64), (128, 64), (192, 64),
              (0, 128), (64, 128), (128, 128), (192, 128),
              (0, 192),]
}
