import pygame
from target import Target
from constants import *
import random

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.hit_sound = pygame.mixer.Sound("hit.wav")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        
        self.targets = []
        self.score = 0
        self.level = 1
        self.time_left = 30
        self.game_state = "enter_name"
        self.high_scores = {}
        self.player_name = ""

    def generate_target(self):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        radius = max(10, 30 - self.level * 2)
        disappearing = self.level % 3 == 0
        lifetime = random.randint(1000, 3000) if disappearing else 2000
        self.targets.append(Target(x, y, radius, disappearing, lifetime))

    def update(self):
        if len(self.targets) < 3 + self.level:
            self.generate_target()
        self.targets = [target for target in self.targets if not target.should_disappear()]

    def draw(self):
        self.screen.fill(BLACK)
        for target in self.targets:
            target.draw(self.screen)
        
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        time_text = self.font.render(f"Time: {int(self.time_left)}", True, WHITE)
        name_text = self.font.render(f"Player: {self.player_name}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
        self.screen.blit(time_text, (WIDTH - 150, 10))
        self.screen.blit(name_text, (WIDTH - 300, 50))

        if self.level % 3 == 0:
            instruction_text = self.font.render("¡Cuidado! Los objetivos amarillos desaparecen", True, YELLOW)
            self.screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT - 50))

    def check_hit(self, mouse_pos):
        for target in self.targets[:]:
            if target.check_hit(mouse_pos):
                self.targets.remove(target)
                self.score += 10 * self.level
                self.hit_sound.play()
                if self.score % 100 == 0:
                    self.level += 1
                return True
        return False

    def run(self):
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while self.game_state == "playing":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.check_hit(pygame.mouse.get_pos())

            self.update()
            self.draw()
            pygame.display.flip()

            self.time_left = max(30 - (pygame.time.get_ticks() - start_time) / 1000, 0)
            if self.time_left <= 0:
                self.game_state = "game_over"

            clock.tick(60)

    def show_menu(self):
        self.screen.fill(BLACK)
        title_text = self.font.render("Aim Trainer", True, WHITE)
        start_text = self.font.render("Click to Start", True, WHITE)
        high_score_text = self.font.render(f"High Score: {self.get_high_score()}", True, WHITE)

        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        self.screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        self.screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT * 2 // 3))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    self.game_state = "playing"
                    self.score = 0
                    self.level = 1
                    self.time_left = 30
                    self.targets = []

    def show_game_over(self):
        self.screen.fill(BLACK)
        game_over_text = self.font.render("Game Over", True, WHITE)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Click to Restart", True, WHITE)

        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT * 2 // 3))

        if self.score > self.get_high_score():
            self.high_scores[self.player_name] = self.score

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    self.game_state = "enter_name"

    def enter_name(self):
        self.screen.fill(BLACK)
        title_text = self.font.render("Enter Your Name", True, WHITE)
        name_text = self.font.render(self.player_name, True, WHITE)
        instruction_text = self.font.render("Press Enter when done", True, WHITE)

        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        self.screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2))
        self.screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT * 2 // 3))

        pygame.display.flip()

        entering = True
        while entering:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.player_name:
                            entering = False
                            self.game_state = "menu"
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        self.player_name += event.unicode
            
            self.screen.fill(BLACK)
            self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
            name_text = self.font.render(self.player_name, True, WHITE)
            self.screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2))
            self.screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT * 2 // 3))
            pygame.display.flip()

    def get_high_score(self):
        if not self.high_scores:
            return 0
        return max(self.high_scores.values())
