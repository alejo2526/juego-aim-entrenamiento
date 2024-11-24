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
        self.targets = [target for target in self.targets if not target.should_disappear()]

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
            instruction_text = font.render("¡Cuidado! Los objetivos amarillos desaparecen", True, YELLOW)
            screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT - 50))

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
            self.time_left = max(30 - (pygame.time.get_ticks() - start_time) / 1000, 0)
            if self.time_left <= 0:
                self.game_state = "game_over"

            clock.tick(60)