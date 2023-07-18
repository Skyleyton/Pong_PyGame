import constantes
import pygame
from sys import exit

"""TODO :
    Implémenter un système de dash + cooldown pour les raquettes (ça peut être fun).
"""

# Menu pause
def menu_pause():
    pause_surface = font.render("Press Space", False, "BLACK")
    pause_rect = pause_surface.get_rect(center = (constantes.WIDTH // 2, constantes.HEIGHT // 2))
    ecran.blit(pause_surface, pause_rect)

# Menu score
def display_score_player():
    score_surface = font.render(f"Score : {player_score}", False, "BLACK")
    score_rect = score_surface.get_rect(center = ((constantes.WIDTH // 2) // 2, 20))
    ecran.blit(score_surface, score_rect)

def display_score_ia():
    score_surface = font.render(f"Score : {ia_score}", False, "BLACK")
    score_rect = score_surface.get_rect(center = ((constantes.WIDTH // 2) + (constantes.WIDTH // 4), 20))
    ecran.blit(score_surface, score_rect)

# Affichage des FPS
def show_fps():
    fps_font = pygame.font.Font("../font/Pixeltype.ttf", 40)
    fps_surface = fps_font.render(f"FPS: {int(clock.get_fps())}", False, "BLACK")
    fps_rect = fps_surface.get_rect(center = (constantes.WIDTH // 2, 20))
    ecran.blit(fps_surface, fps_rect)

# Initialisation
pygame.init()
pygame.display.set_caption("Pong")

ecran = pygame.display.set_mode((constantes.WIDTH, constantes.HEIGHT))
clock = pygame.time.Clock() # Clock object

# État du jeu
game_active = True

font = pygame.font.Font("../font/Pixeltype.ttf", 50)

# La raquette du joueur
player_surface = pygame.Surface((0, 0))
player_rect = pygame.Rect((0, constantes.HEIGHT // 2), (10, 70))
player_speed = 0
player_score = 0

# La raquette de l'IA
ia_surface = pygame.Surface((0, 0))
ia_rect = pygame.Rect((constantes.WIDTH - 10, constantes.HEIGHT // 2), (10, 70))
ia_speed = 0
ia_score = 0

# La balle
ball_surface = pygame.Surface((constantes.WIDTH // 2, constantes.HEIGHT // 2))
ball_rect = pygame.Rect((constantes.WIDTH // 2, constantes.HEIGHT // 2), (10, 10))
ball_y_speed = 6
ball_x_speed = 6


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Pour mettre le jeu en pause
                    game_active = False
                if event.key == pygame.K_s:
                    player_speed += 10
                if event.key == pygame.K_z:
                    player_speed -= 10
                """ Pour l'autre joueur
                if event.key == pygame.K_UP:
                    ia_speed -= 10
                if event.key == pygame.K_DOWN:
                    ia_speed += 10
                """

            if event.type == pygame.KEYUP: # Pour annuler le KEYDOWN, du coup on annule la vitesse
                if event.key == pygame.K_s:
                    player_speed -= 10
                if event.key == pygame.K_z:
                    player_speed += 10
                """ Pour l'autre joueur
                if event.key == pygame.K_UP:
                    ia_speed += 10
                if event.key == pygame.K_DOWN:
                    ia_speed -= 10
                """

        else: # Pour reprendre le jeu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True

    if game_active:
        player_rect.y += player_speed

        ecran.fill("LIGHTBLUE")

        pygame.draw.rect(ecran, "BLACK", player_rect)
        pygame.draw.rect(ecran, "BLACK", ia_rect)
        pygame.draw.ellipse(ecran, "RED", ball_rect)

        # Ligne de séparation d'écran
        pygame.draw.aaline(ecran, "DARKGREY", (constantes.WIDTH // 2, 0), (constantes.WIDTH // 2, constantes.HEIGHT))

        ecran.blit(player_surface, player_rect)
        ecran.blit(ia_surface, ia_rect)

        ball_rect.x += ball_x_speed
        ball_rect.y += ball_y_speed

        # Pour pas que les raquettes dépassent l'écran
        if player_rect.top <= 0:
            player_rect.top = 0
        if player_rect.bottom >= constantes.HEIGHT:
            player_rect.bottom = constantes.HEIGHT

        if ia_rect.top <= 0:
            ia_rect.top = 0
        if ia_rect.bottom >= constantes.HEIGHT:
            ia_rect.bottom = constantes.HEIGHT

        # Rebond de la balle
        if ball_rect.top <= 0 or ball_rect.bottom >= constantes.HEIGHT:
            ball_y_speed *= -1
        if ball_rect.left <= 0:
            ball_rect = pygame.Rect((constantes.WIDTH // 2, constantes.HEIGHT // 2), (10, 10))
            ia_score += 1
        if ball_rect.right >= constantes.WIDTH:
            ball_rect = pygame.Rect((constantes.WIDTH // 2, constantes.HEIGHT // 2), (10, 10))
            player_score += 1

        # Collision balle contre raquettes
        if ball_rect.colliderect(player_rect) or ball_rect.colliderect(ia_rect):
            ball_x_speed *= -1
        
        # IA de l'adversaire (L'IA c'est une fraude, elle est basé sur la position de la balle)
        if ball_rect.y < ia_rect.y:
            ia_speed = 6
            ia_rect.y -= ia_speed
        if ball_rect.y > ia_rect.y:
            ia_speed = 6
            ia_rect.y += ia_speed

        # Affichage des scores et des FPS
        display_score_player()
        display_score_ia()
        show_fps()

        # Continuer menu de pause + IA pour l'adversaire

    else:
        ecran.fill("WHITE")
        menu_pause()
    
    
    # Dessine nos éléments
    # Mets à jour tout le contenu (l'écran)
    pygame.display.update()

    clock.tick(constantes.FPS_MAX) # Maximum de 60fps
