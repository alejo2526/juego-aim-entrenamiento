class Game(Game):  # Continuing the Game class
    def show_menu(self):
        # Mostrar el menú principal
        screen.fill(BLACK)
        title_text = font.render("Aim Trainer", True, WHITE)
        start_text = font.render("Click to Start", True, WHITE)
        high_score_text = font.render(f"High Score: {self.get_high_score()}", True, WHITE)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT * 2 // 3))

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

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT * 2 // 3))

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

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT * 2 // 3))

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
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
            name_text = font.render(self.player_name, True, WHITE)
            screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2))
            screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT * 2 // 3))
            pygame.display.flip()

    def get_high_score(self):
        # Obtener la puntuación más alta
        if not self.high_scores:
            return 0
        return max(self.high_scores.values())