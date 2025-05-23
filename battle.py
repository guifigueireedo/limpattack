import pygame
import random
from config import *

pygame.init()

WIDTH, HEIGHT = 640, 480

pygame.font.init()
font = pygame.font.SysFont("arial", 20)
dialog_font = pygame.font.SysFont("arial", 16)
small_button_font = pygame.font.SysFont("arial", 14)

def battle_screen(player_hp, player_max_hp, enemy, enemy_img, player_img, bg_img, itens_selecionados, main_game_over_func, inventario_cura):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("LimpAttack")
    clock = pygame.time.Clock()

    if not hasattr(enemy, "max_hp"):
        enemy.max_hp = enemy.hp
    if not hasattr(enemy, "damage_flash"):
        enemy.damage_flash = 0

    player_damage_flash = 0
    selected_move = 0
    message = "O que Nala fará?"
    battle_phase = 0
    current_item = None
    running = True
    phase_timer = 0
    phase_delay = 2500
    modo_cura = False

    def draw_text(text, x, y, font=font, color=BLACK):
        rendered = font.render(text, True, color)
        screen.blit(rendered, (x, y))

    def draw_hp_bar(name, x, y, hp, max_hp):
        bar_width = 150
        bar_height = 10
        hp_ratio = hp / max_hp if max_hp > 0 else 0
        pygame.draw.rect(screen, WHITE, (x - 8, y - 28, 170, 70))
        pygame.draw.rect(screen, BLACK, (x - 8, y - 28, 170, 70), 2)
        draw_text(name, x, y - 24)
        pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (x, y, bar_width * hp_ratio, bar_height))
        draw_text(f"HP: {int(hp)}/{int(max_hp)}", x, y + 14, font)

    def draw_dialog_box(message):
        box_width = 220
        box_height = 90
        box_x = 640 - box_width - 10
        box_y = 380
        pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), border_radius=8)
        pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height), 2)
        for i, line in enumerate(message.split('\n')):
            draw_text(line, box_x + 8, box_y + 8 + i * 18, dialog_font)

    def draw_attack_buttons(moves, mouse_pos):
        container_x = 10
        container_y = 380
        container_width = 390
        container_height = 90
        pygame.draw.rect(screen, WHITE, (container_x, container_y, container_width, container_height), border_radius=10)
        pygame.draw.rect(screen, BLACK, (container_x, container_y, container_width, container_height), 2)
        button_width = 180
        button_height = 30
        spacing_x = 10
        spacing_y = 10
        start_x = container_x + 8
        start_y = container_y + 8
        for i, move in enumerate(moves):
            col = i % 2
            row = i // 2
            x = start_x + col * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)
            button_rect = pygame.Rect(x, y, button_width, button_height)
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, LIGHT_ORANGE, button_rect, border_radius=8)
            else:
                pygame.draw.rect(screen, GRAY, button_rect, border_radius=8)
            pygame.draw.rect(screen, BLACK, button_rect, 2)
            draw_text(move.nome, button_rect.x + 8, button_rect.y + 6)

    def draw_cura_buttons(itens_cura, mouse_pos):
        inventario_dict = {}
        for item in itens_cura:
            if item.nome not in inventario_dict:
                inventario_dict[item.nome] = {"item": item, "quantidade": 1}
            else:
                inventario_dict[item.nome]["quantidade"] += 1
        itens_unicos = list(inventario_dict.values())

        container_x = 10
        container_y = 380
        container_width = 390
        container_height = 90
        pygame.draw.rect(screen, WHITE, (container_x, container_y, container_width, container_height), border_radius=10)
        pygame.draw.rect(screen, BLACK, (container_x, container_y, container_width, container_height), 2)
        button_width = 180
        button_height = 30
        spacing_x = 10
        spacing_y = 10
        start_x = container_x + 8
        start_y = container_y + 8
        for i, data in enumerate(itens_unicos):
            item = data["item"]
            quantidade = data["quantidade"]
            col = i % 2
            row = i // 2
            x = start_x + col * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)
            button_rect = pygame.Rect(x, y, button_width, button_height)
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, LIGHT_ORANGE, button_rect, border_radius=8)
            else:
                pygame.draw.rect(screen, GRAY, button_rect, border_radius=8)
            pygame.draw.rect(screen, BLACK, button_rect, 2)
            color = (0, 200, 255) if item.raridade == 1 else (0, 255, 100) if item.raridade == 2 else (255, 200, 0) if item.raridade == 3 else (255, 80, 80)
            pygame.draw.rect(screen, color, (button_rect.x + 4, button_rect.y + 4, 22, 22), border_radius=4)
            draw_text(f"{item.nome} (+{item.cura} HP)", button_rect.x + 32, button_rect.y + 6, small_button_font)
            draw_text(f"x{quantidade}", button_rect.x + button_width - 28, button_rect.y + 6, small_button_font)
            imagens = {
                "Curativo": "img/curativo.png",
                "Comprimido": "img/comprimido.png",
                "Pomada": "img/pomada.png",
                "Chá Natural": "img/cha.png"
            }
            img_path = imagens.get(item.nome, "img/curativo.png")
            try:
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (22, 22))
                screen.blit(img, (button_rect.x + 4, button_rect.y + 4))
            except Exception as e:
                pygame.draw.rect(screen, (255, 0, 0), (button_rect.x + 4, button_rect.y + 4, 22, 22), border_radius=4)

    def draw_toggle_cura_button(mouse_pos, modo_cura):
        btn_x = 410
        btn_y = 335
        btn_w = 130
        btn_h = 30
        btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        cor_btn = (180, 255, 180) if not modo_cura else (255, 220, 180)
        if btn_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, cor_btn, btn_rect, border_radius=10)
        else:
            pygame.draw.rect(screen, WHITE, btn_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, btn_rect, 2)
        texto = "Modo Cura" if not modo_cura else "Modo Ataque"
        draw_text(f"{texto}", btn_x + 10, btn_y + 5)

    def handle_button_click(mouse_pos, moves):
        nonlocal selected_move
        container_x = 10
        container_y = 380
        button_width = 180
        button_height = 30
        spacing_x = 10
        spacing_y = 10
        start_x = container_x + 8
        start_y = container_y + 8
        for i, move in enumerate(moves):
            col = i % 2
            row = i // 2
            x = start_x + col * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)
            button_rect = pygame.Rect(x, y, button_width, button_height)
            if button_rect.collidepoint(mouse_pos):
                selected_move = i
                return True
        return False

    def handle_cura_button_click(mouse_pos, itens_cura):
        inventario_dict = {}
        for item in itens_cura:
            if item.nome not in inventario_dict:
                inventario_dict[item.nome] = {"item": item, "quantidade": 1}
            else:
                inventario_dict[item.nome]["quantidade"] += 1
        itens_unicos = list(inventario_dict.values())

        container_x = 10
        container_y = 380
        button_width = 180
        button_height = 30
        spacing_x = 10
        spacing_y = 10
        start_x = container_x + 8
        start_y = container_y + 8
        for i, data in enumerate(itens_unicos):
            col = i % 2
            row = i // 2
            x = start_x + col * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)
            button_rect = pygame.Rect(x, y, button_width, button_height)
            if button_rect.collidepoint(mouse_pos):
                return data["item"].nome
        return None

    def fade_in():
        alpha = 255
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill(BLACK)
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        while alpha > 0:
            alpha -= 8
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(10)

    def fade_out():
        alpha = 0
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill(BLACK)
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        while alpha < 255:
            alpha += 8
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(10)

    def show_battle_intro(enemy_name, bg_img, player_img, enemy_img):
        intro_texts = [f"Um inimigo apareceu: {enemy_name}!", "Vamos Combater, Nala!"]
        for text in intro_texts:
            fade_text(text)
            pygame.time.delay(600)
        transition_to_battle(bg_img, player_img, enemy_img)

    def transition_to_battle(bg_img, player_img, enemy_img):
        for alpha in range(0, 256, 16):
            screen.fill(BLACK)
            temp_bg = bg_img.copy()
            temp_bg.set_alpha(alpha)
            screen.blit(temp_bg, (0, 0))
            temp_player = player_img.copy()
            temp_player.set_alpha(alpha)
            screen.blit(temp_player, (40, 260))
            temp_enemy = enemy_img.copy()
            temp_enemy.set_alpha(alpha)
            screen.blit(temp_enemy, (400, 120))
            draw_hp_bar("Nala", 40, 220, player_hp, player_max_hp)
            draw_hp_bar(enemy.nome, 420, 60, enemy.hp, enemy.max_hp)
            draw_dialog_box("A batalha vai começar!")
            pygame.display.flip()
            pygame.time.delay(20)

    def fade_text(text):
        font_intro = pygame.font.SysFont("arial", 32)
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill(BLACK)
        screen.fill(BLACK)
        pygame.display.flip()
        for alpha in range(0, 256, 16):
            screen.blit(fade_surface, (0, 0))
            fade_surface.set_alpha(alpha)
            draw_text_centered(text, font_intro, WHITE)
            pygame.display.flip()
            pygame.time.delay(10)
        pygame.time.delay(400)
        for alpha in range(255, -1, -16):
            screen.blit(fade_surface, (0, 0))
            fade_surface.set_alpha(alpha)
            draw_text_centered(text, font_intro, WHITE)
            pygame.display.flip()
            pygame.time.delay(10)

    def draw_text_centered(text, font, color):
        screen.fill(BLACK)
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(rendered, rect)

    def ataque_do_jogador(item_usado, inimigo):
        dano = int(item_usado.calcular_dano(inimigo.nome))
        inimigo.hp -= dano
        inimigo.hp = max(inimigo.hp, 0)
        if hasattr(inimigo, "damage_flash"):
            inimigo.damage_flash = 4
        else:
            setattr(inimigo, "damage_flash", 4)
        return dano

    def ataque_do_inimigo(inimigo):
        nonlocal player_hp, player_damage_flash
        atk_nome, atk_dano = inimigo.ataque_aleatorio()
        player_hp -= atk_dano
        player_hp = max(player_hp, 0)
        player_damage_flash = 4
        return atk_nome, atk_dano

    fade_in()
    show_battle_intro(enemy.nome, bg_img, player_img, enemy_img)

    while running:
        screen.blit(bg_img, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        now = pygame.time.get_ticks()

        if player_damage_flash % 2 == 1:
            tinted = player_img.copy()
            tinted.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(tinted, (40, 260))
        else:
            screen.blit(player_img, (110, 240))

        if getattr(enemy, "damage_flash", 0) % 2 == 1:
            tinted = enemy_img.copy()
            tinted.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(tinted, (410, 130))
        else:
            screen.blit(enemy_img, (400, 130))

        if player_damage_flash > 0:
            player_damage_flash -= 1
        if getattr(enemy, "damage_flash", 0) > 0:
            enemy.damage_flash -= 1

        draw_hp_bar("Nala", 60, 180, player_hp, player_max_hp)
        draw_hp_bar(enemy.nome, 420, 60, enemy.hp, enemy.max_hp)

        draw_dialog_box(message)
        if modo_cura:
            draw_cura_buttons(inventario_cura, mouse_pos)
        else:
            draw_attack_buttons(itens_selecionados, mouse_pos)
        draw_toggle_cura_button(mouse_pos, modo_cura)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "derrota"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                btn_x, btn_y, btn_w, btn_h = 410, 335, 130, 30
                if pygame.Rect(btn_x, btn_y, btn_w, btn_h).collidepoint(event.pos):
                    modo_cura = not modo_cura
                    continue
                if event.button == 1 and battle_phase == 0:
                    if not modo_cura:
                        if handle_button_click(event.pos, itens_selecionados):
                            current_item = itens_selecionados[selected_move]
                            message = f"Nala escolheu...\n{current_item.nome}!"
                            battle_phase = 1
                            phase_timer = now
                    else:
                        nome_item_clicado = handle_cura_button_click(event.pos, inventario_cura)
                        if nome_item_clicado:
                            for idx, item in enumerate(inventario_cura):
                                if item.nome == nome_item_clicado:
                                    cura = item.cura
                                    player_hp = min(player_hp + cura, player_max_hp)
                                    message = f"Nala usou {item.nome}!\nRecuperou {cura} de vida."
                                    inventario_cura.pop(idx)
                                    battle_phase = 2
                                    phase_timer = now
                                    break

        if battle_phase == 1 and now - phase_timer > phase_delay:
            dano = ataque_do_jogador(current_item, enemy)
            if dano >= enemy.hp + dano:
                eficiencia_msg = "Dano crítico! Muito bem!"
            elif dano >= 0.8 * enemy.max_hp:
                eficiencia_msg = "O ataque foi MUITO EFICIENTE!"
            elif dano >= 0.6 * enemy.max_hp:
                eficiencia_msg = "O ataque foi eficiente!"
            elif dano >= 0.4 * enemy.max_hp:
                eficiencia_msg = "O ataque foi bom..."
            elif dano <= 0.2 * enemy.max_hp:
                eficiencia_msg = "O ataque não foi eficiente..."
            else:
                eficiencia_msg = ""
            message = f"Nala usou...\n{current_item.nome}!\nCausou {dano} de dano.\n{eficiencia_msg}"
            battle_phase = 2
            phase_timer = now

        if battle_phase == 2 and now - phase_timer > phase_delay:
            if enemy.hp > 0:
                atk_nome, atk_dano = ataque_do_inimigo(enemy)
                message = f"{enemy.nome} usou...\n{atk_nome}!\nCausou {atk_dano} de dano."
            else:
                victory_messages = [
                    "Higiene é tudo!",
                    "A higiene venceu denovo!",
                    "Viva aos bons hábitos!",
                    "Nala venceu com muita higiene!",
                    "Bactérias não tem vez aqui!",
                    "Vitória brilhante e cheirosa!",
                    "Nada resiste à higiene!",
                    "Bons hábitos sempre vencem!",
                    "Continue com a higiene!",
                    "Mostrou quem manda na limpeza!"
                ]
                message = f"{enemy.nome} foi derrotado!\n{random.choice(victory_messages)}"
            battle_phase = 3
            phase_timer = now

        if battle_phase == 3 and now - phase_timer > phase_delay:
            if enemy.hp <= 0 or player_hp <= 0:
                fade_out()
                if player_hp <= 0:
                    main_game_over_func()
                    return "derrota"
                else:
                    return player_hp
            else:
                message = "O que Nala fará?"
                battle_phase = 0