import pygame
from target import Target
from constants import *
import random


class Game:
    def __init__(self):
        self.targets = []
        self.score = 0
        self.level = 1
        self.time_left = 30
        self.game_state = "enter_name"
        self.high_scores = {}
        self.player_name = ""

    def generate_target(self):
        # Generar un nuevo objetivo con posición y tamaño aleatorios
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        radius = max(10, 30 - self.level * 2)

        # Hacer que los objetivos desaparezcan en niveles múltiplos de 3
        disappearing = self.level % 3 == 0
        lifetime = random.randint(1000, 3000) if disappearing else 2000

        self.targets.append(Target(x, y, radius, disappearing, lifetime))

    def update(self):
        # Actualizar el estado del juego
        if len(self.targets) < 3 + self.level:
            self.generate_target()

        # Eliminar objetivos que deben desaparecer
        self.targets = [
            target for target in self.targets if not target.should_disappear()]

    def draw(self):
        # Dibujar todos los elementos del juego
        screen.fill(BLACK)
        for target in self.targets:
            target.draw()

        # Mostrar información del juego en pantalla
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        time_text = font.render(f"Time: {int(self.time_left)}", True, WHITE)
        name_text = font.render(f"Player: {self.player_name}", True, WHITE)

        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(time_text, (WIDTH - 150, 10))
        screen.blit(name_text, (WIDTH - 300, 50))

        # Mostrar instrucciones para niveles con objetivos que desaparecen
        if self.level % 3 == 0:
            instruction_text = font.render(
                "¡Cuidado! Los objetivos amarillos desaparecen", True, YELLOW)
            screen.blit(instruction_text, (WIDTH // 2 -
                        instruction_text.get_width() // 2, HEIGHT - 50))

    def check_hit(self, mouse_pos):
        # Verificar si se ha golpeado algún objetivo
        for target in self.targets[:]:
            if target.check_hit(mouse_pos):
                self.targets.remove(target)
                self.score += 10 * self.level
                hit_sound.play()
                if self.score % 100 == 0:
                    self.level += 1
                return True
        return False

    def run(self):
        # Bucle principal del juego
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while self.game_state == "playing":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Botón izquierdo del ratón
                        self.check_hit(pygame.mouse.get_pos())

            self.update()
            self.draw()
            pygame.display.flip()

            # Actualizar el tiempo restante
            self.time_left = max(
                30 - (pygame.time.get_ticks() - start_time) / 1000, 0)
            if self.time_left <= 0:
                self.game_state = "game_over"

            clock.tick(60)

    def show_menu(self):
        # Mostrar el menú principal
        screen.fill(BLACK)
        title_text = font.render("Aim Trainer", True, WHITE)
        start_text = font.render("Click to Start", True, WHITE)
        high_score_text = font.render(
            f"High Score: {self.get_high_score()}", True, WHITE)

        screen.blit(title_text, (WIDTH // 2 -
                    title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(start_text, (WIDTH // 2 -
                    start_text.get_width() // 2, HEIGHT // 2))
        screen.blit(high_score_text, (WIDTH // 2 -
                    high_score_text.get_width() // 2, HEIGHT * 2 // 3))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    self.game_state = "playing"
                    self.score = 0
                    self.level = 1
                    self.time_left = 30
                    self.targets = []

    def show_game_over(self):
        # Mostrar la pantalla de fin de juego
        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = font.render("Click to Restart", True, WHITE)

        screen.blit(game_over_text, (WIDTH // 2 -
                    game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 -
                    score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 -
                    restart_text.get_width() // 2, HEIGHT * 2 // 3))

        # Actualizar la puntuación más alta si es necesario
        if self.score > self.get_high_score():
            self.high_scores[self.player_name] = self.score

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    self.game_state = "enter_name"

    def enter_name(self):
        # Pantalla para ingresar el nombre del jugador
        screen.fill(BLACK)
        title_text = font.render("Enter Your Name", True, WHITE)
        name_text = font.render(self.player_name, True, WHITE)
        instruction_text = font.render("Press Enter when done", True, WHITE)

        screen.blit(title_text, (WIDTH // 2 -
                    title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(name_text, (WIDTH // 2 -
                    name_text.get_width() // 2, HEIGHT // 2))
        screen.blit(instruction_text, (WIDTH // 2 -
                    instruction_text.get_width() // 2, HEIGHT * 2 // 3))

        pygame.display.flip()

        entering = True
        while entering:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.player_name:
                            entering = False
                            self.game_state = "menu"
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        self.player_name += event.unicode

            screen.fill(BLACK)
            screen.blit(title_text, (WIDTH // 2 -
                        title_text.get_width() // 2, HEIGHT // 3))
            name_text = font.render(self.player_name, True, WHITE)
            screen.blit(name_text, (WIDTH // 2 -
                        name_text.get_width() // 2, HEIGHT // 2))
            screen.blit(instruction_text, (WIDTH // 2 -
                        instruction_text.get_width() // 2, HEIGHT * 2 // 3))
            pygame.display.flip()

    def get_high_score(self):
        # Obtener la puntuación más alta
        if not self.high_scores:
            return 0
        return max(self.high_scores.values())
