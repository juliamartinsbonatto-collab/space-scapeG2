##############################################################
###             S P A C E  E S C A P E                     ###
##############################################################
###                   versao Alpha 0.3 ###
##############################################################
### Objetivo: desviar dos meteoros que caem.               ###
### Cada colisão tira uma vida. Sobreviva o máximo que     ###
### conseguir!                                             ###
##############################################################
### Prof. Filipo Novo Mor - github.com/ProfessorFilipo     ###
##############################################################

import pygame
import random
import os
import sys

# ----------------------------------------------------------
# INICIALIZAÇÃO GERAL E CONFIGURAÇÕES
# ----------------------------------------------------------
print("teste")
pygame.init()
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption(" Space Escape")

ASSETS = {
    "background": "frames.png",
    "player": "YODALEVEL1.png",
    "meteor": "meteoro-colorido1.png", # TIPO 1: -1 VIDA
    "meteor_strong": "meteoro-forte.png", # TIPO 2: -2 VIDAS
    "meteor_deadly": "meteoro-level3.png", # TIPO 3: -3 VIDAS
    "nave": "nave.png", # -2 VIDAS
    "sound_point": "game-bonus.mp3",
    "sound_hit": "buzzer.mp3",
    "music": "starwars-background-music.mp3",
    "game_over_sound": "game-over.mp3",
    "yoda_sad": "YODA-TRISTE.png"
}

WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
PURPLE = (150, 0, 150)
DARK_RED = (100, 0, 0)
LEVEL3_COLOR = (255, 0, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# FONTES
font = pygame.font.Font(None, 36)
start_font = pygame.font.SysFont("Arial Black", 40)
small_font = pygame.font.SysFont("Arial Black", 30)
win_font = pygame.font.SysFont("Arial Black", 45, bold=True)
final_font = pygame.font.SysFont("Arial Black", 25, bold=True)


# ----------------------------------------------------------
# FUNÇÕES DE UTILIDADE
# ----------------------------------------------------------

def load_image(filename, fallback_color, size=None):
    if os.path.exists(filename):
        img = pygame.image.load(filename).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    else:
        # Fallback para caso o arquivo não exista
        surf = pygame.Surface(size or (50, 50))
        surf.fill(fallback_color)
        return surf

def load_sound(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    return None

# ----------------------------------------------------------
# FUNÇÃO PRINCIPAL DO JOGO
# ----------------------------------------------------------

def start_game(level=1, current_score=0, current_lives=5):

    # ----------------------------------------------------------
    # REINÍCIO POR FASE
    # ----------------------------------------------------------

    lives = 5
    score = current_score
    tempo_limite = 30

    # Configurações dinâmicas por nível
    meteor_speed_mult = 1.0 + (level - 1) * 0.2
    nave_speed_mult = 1.0 + (level - 1) * 0.15

    base_meteor_speed = 5
    nave_speed = 1.5 * nave_speed_mult

    # Taxa de surgimento (Quanto menor o valor, mais rápido aparecem)
    # Nível 1: 60 (1 inimigo/segundo) | Nível 2: 40 | Nível 3: 30
    spawn_rate = max(30, 60 - (level - 1) * 20)
    spawn_counter = 0

    # Imagens e Sons
    background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
    # Meteoro Normal (-1 vida)
    meteor_img_normal = load_image(ASSETS["meteor"], RED, (70, 70))
    # Meteoro Forte (-2 vidas)
    # Meteoro Level 3 (-3 vidas)
    meteor_img_level3 = load_image(ASSETS["meteor_deadly"], LEVEL3_COLOR, (90, 90))

    nave_img = load_image(ASSETS["nave"], BLUE, (50, 50))
    player_nave_img = load_image("nave-player.png", WHITE, (80, 60))
    bullet_img = load_image("nave-tiro.png", WHITE, (20, 40))

    # Imagem de vitória
    yoda_win_img = load_image("YODA-WIN.png", GREEN, (150, 150))
    yoda_win_rect = yoda_win_img.get_rect()

    # Imagem de Game Over
    yoda_sad_img = load_image(ASSETS["yoda_sad"], RED, (150, 150))
    yoda_sad_rect = yoda_sad_img.get_rect()

    player_nave_rect = player_nave_img.get_rect(center=(WIDTH // 2, HEIGHT - 100))
    player_nave_speed = 6
    bullet_speed = 10
    can_shoot = True

    bullets = []

    # --- LISTAS DE OBSTÁCULOS ---
    nave_list = []
    meteor_list = []

    # ---------------------------------
    # PLAYER
    # ---------------------------------
    
    player_frames = []
    
    if level == 1:
        # NÍVEL 1:
        frame_names = ["YODA-LEVEL1-1.png", "YODA-LEVEL1-2.png"]
    elif level == 2:
        # NÍVEL 2:
        frame_names = ["YODA-LEVEL2-1.png", "YODA-LEVEL2.png"]
    elif level >= 3:
        # NÍVEL 3+:
        frame_names = ["YODA-LEVEL3-1.png", "YODA-LEVEL3.png"]

    # 2. Carregar os frames
    for name in frame_names:
        full_path = os.path.join("YODA-PNG", name)
        try:
            img = load_image(full_path, GREEN, (80, 60))
            player_frames.append(img)
        except pygame.error:
            # se a imagem não for encontrada
            print(f"Erro ao carregar imagem: {full_path}.")
            player_frames.append(load_image(None, GREEN, (80, 60)))


    player_index = 0
    player_anim_speed = 15
    player_anim_counter = 0
    # Inicializa posição do Yoda abaixo da nave
    player_rect = player_frames[0].get_rect(center=(player_nave_rect.centerx, player_nave_rect.bottom + 10))
    player_speed = 7

    # Estados
    running = True
    venceu = False

    # FUNDO ANIMADO
    frames = []
    for i in range(1, 25):
        try:
            img = pygame.image.load(f"frames/frame{i}.png").convert()
            img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            frames.append(img)
        except pygame.error:
            frames.append(pygame.Surface((WIDTH, HEIGHT)))
            frames[-1].fill((0, 0, 0))

    background_index = 0
    background_speed = 10
    frame_counter = 0

    # IMAGENS DE GAME OVER
    gameover_frames = []
    for i in range(1, 6):
        try:
            img = pygame.image.load(f"gameover/gameover{i}.png").convert()
            img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            gameover_frames.append(img)
        except pygame.error:
            gameover_frames.append(pygame.Surface((WIDTH, HEIGHT)))
            gameover_frames[-1].fill((50, 0, 0))

    # Sons
    sound_point = load_sound(ASSETS["sound_point"])
    sound_hit = load_sound(ASSETS["sound_hit"])

    if os.path.exists(ASSETS["music"]):
        pygame.mixer.music.load(ASSETS["music"])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    # CRONÔMETRO
    tempo_inicio = pygame.time.get_ticks()

    def spawn_enemy():
        
        # Inimigos possíveis no nível atual
        enemy_choices = [1]
        
        if level >= 2:
            enemy_choices.extend([1] * 3 + [2])
        
        if level >= 3:
            enemy_choices.extend([1] * 2 + [3])

        # Seleciona o tipo de inimigo
        enemy_type = random.choice(enemy_choices)
        
        # Meteoro Tipo 1: -1 Vida
        if enemy_type == 1:
            size = 70
            x = random.randint(0, WIDTH - size)
            y = random.randint(-150, -40)
            meteor_list.append({
                'rect': pygame.Rect(x, y, size, size),
                'type': 1,
                'img': meteor_img_normal,
                'speed_mult': meteor_speed_mult
            })
        
        # Nave Inimiga: -2 Vidas
        elif enemy_type == 2 and level >= 2:
            size = 50
            x = random.randint(0, WIDTH - size)
            y = random.randint(-300, -80)
            nave_list.append(pygame.Rect(x, y, size, size))

        # Meteoro Tipo 3: -3 Vidas
        elif enemy_type == 3 and level >= 3:
            size = 90
            x = random.randint(0, WIDTH - size)
            y = random.randint(-500, -100)
            meteor_list.append({
                'rect': pygame.Rect(x, y, size, size),
                'type': 3,
                'img': meteor_img_level3,
                'speed_mult': meteor_speed_mult
            })


    # ----------------------------------------------------------
    # LOOP PRINCIPAL DO JOGO
    # ----------------------------------------------------------
    while running:
        clock.tick(FPS)

        # --- CALCULO DO TEMPO ---
        tempo_passado = (pygame.time.get_ticks() - tempo_inicio) / 1000
        tempo_restante = max(0, tempo_limite - tempo_passado)

        # Condição de VITÓRIA/FINAL
        if tempo_restante <= 0 and lives > 0:
            venceu = True
            running = False

        # --- CONTROLE DINÂMICO ---
        if running: # Somente gera inimigos se o jogo estiver rodando
            spawn_counter += 1
            if spawn_counter >= spawn_rate:
                spawn_enemy()
                spawn_counter = 0


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # -----------------------------------------------
            # TIRO
            # -----------------------------------------------
            if event.type == pygame.KEYDOWN:
                # Espaço dispara os tiros
                if event.key == pygame.K_SPACE and can_shoot:
                    
                    # 1. TIRO DA NAVE
                    bullet_nave = bullet_img.get_rect(
                        center=(player_nave_rect.centerx, player_nave_rect.top) 
                    )
                    bullets.append(bullet_nave)
                    
                    # 2. TIRO DO YODA
                    bullet_yoda = bullet_img.get_rect(
                        center=(player_rect.centerx, player_rect.top) 
                    )
                    bullets.append(bullet_yoda)

                    can_shoot = False

            if event.type == pygame.KEYUP:
                # O espaço solto permite novo tiro
                if event.key == pygame.K_SPACE:
                    can_shoot = True
            # -----------------------------------------------

        # Renderização do fundo e animação do Yoda
        frame_counter += 1
        if frame_counter >= background_speed:
            frame_counter = 0
            background_index = (background_index + 1) % len(frames)
        screen.blit(frames[background_index], (0, 0))

        player_anim_counter += 1
        if player_anim_counter >= player_anim_speed:
            player_anim_counter = 0
            player_index = (player_index + 1) % len(player_frames)

        screen.blit(player_frames[player_index], player_rect)
        screen.blit(player_nave_img, player_nave_rect)

        # MOVIMENTOS
        keys = pygame.key.get_pressed()

        # MOVIMENTO DA NAVE (W, A, S, D)
        # Horizontal
        if keys[pygame.K_a] and player_nave_rect.left > 0:
            player_nave_rect.x -= player_nave_speed
        if keys[pygame.K_d] and player_nave_rect.right < WIDTH:
            player_nave_rect.x += player_nave_speed

        # Vertical
        if keys[pygame.K_w] and player_nave_rect.top > 0:
            player_nave_rect.y -= player_nave_speed
        if keys[pygame.K_s] and player_nave_rect.bottom < HEIGHT:
            player_nave_rect.y += player_nave_speed

        # MOVIMENTO DO YODA (SETAS)
        # Horizontal
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed

        # Vertical
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect.y += player_speed


        # ---------------------------------------------
        # ATUALIZAÇÕES E COLISÕES
        # ---------------------------------------------

        # Movimento dos Tiros
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Meteoros - Colisão e Reposicionamento
        for meteor_data in meteor_list:
            meteor_rect = meteor_data['rect']
            meteor_type = meteor_data['type']
            speed_mult = meteor_data.get('speed_mult', 1.0)

            # Movimento
            meteor_rect.y += base_meteor_speed * speed_mult

            if meteor_rect.y > HEIGHT:
                # Reposicionamento (Saiu da tela)
                meteor_list.remove(meteor_data)
                score += 1 # Pontuação por desviar
                if sound_point:
                    sound_point.play()
                break

            # Colisão: Meteoros colidindo com a NAVE (usando player_nave_rect)
            # OU colidindo com o YODA (usando player_rect)
            if meteor_rect.colliderect(player_nave_rect) or meteor_rect.colliderect(player_rect):
                # Lógica de dano pelos tipos de meteoros
                if meteor_type == 1:
                    lives -= 1 # Meteoro Normal (-1 vida)
                elif meteor_type == 3:
                    lives -= 3 # Meteoro Level 3 (-3 vidas)
                
                # Remove o meteoro após a colisão
                meteor_list.remove(meteor_data)

                if sound_hit and lives > 0:
                    sound_hit.play()
                if lives <= 0:
                    running = False
                break

        # Naves Inimigas - Colisão e Reposicionamento
        for nave in nave_list:
            nave.y += nave_speed

            if nave.y > HEIGHT:
                # Remove a nave que saiu da tela
                nave_list.remove(nave)
                break # Sai do loop para evitar erros com a remoção

            # Colisão: Naves inimigas colidindo com a NAVE ou com o YODA
            if nave.colliderect(player_nave_rect) or nave.colliderect(player_rect):
                score -= 5
                lives -= 2 # NAVE TIRA 2 VIDAS
                nave_list.remove(nave)
                if sound_hit:
                    sound_hit.play()
                if lives <= 0:
                    running = False
                break

        # Colisões Tiros
        meteor_to_remove = []
        bullet_to_remove = []

        # Tiros acertando Naves
        for bullet in bullets[:]:
            for nave in nave_list[:]:
                if bullet.colliderect(nave):
                    if bullet not in bullet_to_remove:
                        bullet_to_remove.append(bullet)
                    nave_list.remove(nave)
                    score += 10
                    break

        # Tiros acertando Meteoros
        for bullet in bullets[:]:
            for meteor_data in meteor_list[:]:
                if bullet.colliderect(meteor_data['rect']):
                    if bullet not in bullet_to_remove:
                        bullet_to_remove.append(bullet)

                    if meteor_data not in meteor_to_remove:
                        meteor_to_remove.append(meteor_data)
                        score += 5
                    break

        for bullet in bullet_to_remove:
            if bullet in bullets:
                bullets.remove(bullet)

        for meteor_data in meteor_to_remove:
            if meteor_data in meteor_list:
                meteor_list.remove(meteor_data)

        # DESENHAR OBJETOS
        for meteor_data in meteor_list:
            screen.blit(meteor_data['img'], meteor_data['rect'])

        for nave in nave_list:
            screen.blit(nave_img, nave)

        for bullet in bullets:
            screen.blit(bullet_img, bullet)

        # HUD
        text = font.render(f"Nível: {level} | Pontos: {score} | Vidas: {lives}", True, WHITE)
        screen.blit(text, (10, 10))

        timer_text = font.render(f"Tempo: {tempo_restante:.1f}s", True, WHITE)
        screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))

        pygame.display.flip()

    # FIM DO LOOP PRINCIPAL
    pygame.mixer.music.stop()

    # ----------------------------------------------------------
    # TELAS DE FIM DE JOGO (VITÓRIA / DERROTA)
    # ----------------------------------------------------------

    if venceu:
        # TELA DE VITÓRIA/FINAL

        # Se for o último nível
        if level >= 3:
            # TELA DE VITÓRIA FINAL DO JOGO
            win_message = "FIM DE JOGO! VOCÊ SALVOU A GALÁXIA!"
            next_level_action = False
            # Mensagem de ação final
            action_text = "Pressione ESPAÇO para Tentar de Novo (Nível 1)"
            next_level_start = 1
        else:
            # TELA DE VITÓRIA INTERMEDIÁRIA
            win_message = f"NÍVEL {level} CONCLUÍDO!"
            next_level_action = True
            # Mensagem para o próximo nível
            action_text = f"Click ESPAÇO para a FASE {level + 1}"
            next_level_start = level + 1

        win_sound = load_sound(ASSETS["sound_point"])
        if win_sound:
            win_sound.set_volume(1.0)
            win_sound.play()

        waiting = True

        # Posições fixas para a tela de vitória
        yoda_win_rect.center = (WIDTH // 2, HEIGHT // 2 - 20) 

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                        # Retorna para reiniciar Nível 1 ou avançar
                        return True, (score if next_level_action else 0), 5, next_level_start
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            screen.fill(BLACK)

            screen.blit(yoda_win_img, yoda_win_rect)

            you_win_text = win_font.render("YOU WIN", True, WHITE)
            screen.blit(you_win_text, (WIDTH//2 - you_win_text.get_width()//2, 350))

            # Mensagem de Próximo Nível/Reinício
            msg_proximo = small_font.render(action_text, True, WHITE)
            screen.blit(msg_proximo, (WIDTH//2 - msg_proximo.get_width()//2, 450))

            # Placar Final
            final_score = final_font.render(f"Pontos: {score} | Vidas Restantes: {lives}", True, WHITE)
            screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2, 530))

            pygame.display.flip()
            clock.tick(FPS)

    else:
        # TELA DE GAME OVER
        gameover_sound = load_sound(ASSETS["game_over_sound"])
        if gameover_sound:
            gameover_sound.set_volume(1.0)
            gameover_sound.play()

        go_index = 0
        go_speed = 20
        go_counter = 0

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

            go_counter += 1
            if go_counter >= go_speed:
                go_counter = 0
                go_index = (go_index + 1) % len(gameover_frames)

            screen.blit(gameover_frames[go_index], (0, 0))

            # --- Imagem do Yoda Triste ---
            yoda_sad_rect.center = (WIDTH // 2, HEIGHT // 2 - 100)
            screen.blit(yoda_sad_img, yoda_sad_rect)

            final_score_text = final_font.render(f"Score Final: {score}", True, WHITE)
            screen.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, yoda_sad_rect.bottom + 50))

            instrucao = final_font.render("Pressione ESPAÇO para Tentar Novamente", True, WHITE)
            screen.blit(instrucao, (WIDTH//2 - instrucao.get_width()//2, yoda_sad_rect.bottom + 120))

            pygame.display.flip()
            clock.tick(FPS)

        # Retorna os valores para reiniciar o Nível 1
        return True, 0, 5, 1


# ----------------------------------------------------------
# FUNÇÃO DA TELA INICIAL
# ----------------------------------------------------------

def show_start_screen():
    menu_state = "menu"
    baby_yoda_img = load_image("YODA-INICIO.png", WHITE, (220, 180))
    baby_yoda_rect = baby_yoda_img.get_rect(center=(WIDTH//2, 230))

    while menu_state != "jogar":
        screen.fill((0, 0, 0))

        if menu_state == "menu":
            # textos
            title = start_font.render("SPACE ESCAPE", True, WHITE)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 70))
            screen.blit(baby_yoda_img, baby_yoda_rect)

           # --- Botões ---
            btn_start = pygame.Rect(WIDTH//2 - 130, 420, 260, 50)
            btn_instr = pygame.Rect(WIDTH//2 - 130, 530, 260, 50)

            pygame.draw.rect(screen, (0, 0, 0), btn_start)
            pygame.draw.rect(screen, (0, 0, 0), btn_instr)
            pygame.draw.rect(screen, WHITE, btn_instr, 3)

            txt_start = small_font.render("Click Space To Start", True, WHITE)
            txt_start_rect = txt_start.get_rect(center=btn_start.center)
            screen.blit(txt_start, txt_start_rect)

            txt_instr = small_font.render("Instructions", True, WHITE)
            txt_instr_rect = txt_instr.get_rect(center=btn_instr.center)
            screen.blit(txt_instr, txt_instr_rect)


        # TELA DE INSTRUÇÕES
        elif menu_state == "instrucoes":
            screen.fill((0, 0, 20))

            titulo = start_font.render("INSTRUÇÕES", True, YELLOW)
            screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 50))

            instrucoes = [
                "Nave: Use W/S/A/D para mover a nave", 
                "Yoda: Use ↑/↓/←/→ para mover o Yoda",
                "Pressione ESPAÇO para TIRO DUPLO",
                "Sobreviva o tempo limite para avançar de nível"
            ]

            y = 180
            for linha in instrucoes:
                texto = small_font.render(linha, True, WHITE)
                screen.blit(texto, (WIDTH//2 - texto.get_width()//2, y))
                y += 50

            # Botão voltar
            btn_voltar = pygame.Rect(WIDTH//2 - 130, 500, 260, 50)
            pygame.draw.rect(screen, (0, 0, 20), btn_voltar)
            pygame.draw.rect(screen, WHITE, btn_voltar, 3)
            txt_voltar = small_font.render("Back", True, WHITE)
            txt_voltar_rect = txt_voltar.get_rect(center=btn_voltar.center)
            screen.blit(txt_voltar, txt_voltar_rect)


        pygame.display.update()

        # eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if menu_state == "menu":
                    if btn_start.collidepoint(pos):
                        menu_state = "jogar"
                    if btn_instr.collidepoint(pos):
                        menu_state = "instrucoes"
                elif menu_state == "instrucoes":
                    if btn_voltar.collidepoint(pos):
                        menu_state = "menu"

            # tecla espaço inicia o jogo direto
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if menu_state == "menu":
                        menu_state = "jogar"

    # Retorna os valores iniciais do jogo para começar o loop principal
    return True, 0, 5, 1

# ----------------------------------------------------------
# LOOP DE GERENCIAMENTO DE FASES
# ----------------------------------------------------------

if __name__ == "__main__":

    # Mostrar a tela inicial e obter os valores de início
    next_level, current_score, current_lives, current_level = show_start_screen()

    # O loop principal
    while next_level:
        # Chama a função do jogo e recebe o estado de volta
        next_level, current_score, current_lives, current_level = start_game(
            level=current_level,
            current_score=current_score,
            current_lives=current_lives
        )

    pygame.quit()
    sys.exit()