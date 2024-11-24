class Target:
    def __init__(self, x, y, radius, disappearing=False, lifetime=2000):
        self.x = x
        self.y = y
        self.radius = radius
        self.disappearing = disappearing
        self.lifetime = lifetime
        self.creation_time = pygame.time.get_ticks()

    def draw(self):
        # Dibujar el objetivo en la pantalla
        if self.disappearing:
            color = YELLOW
        else:
            color = RED
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

    def check_hit(self, mouse_pos):
        # Verificar si el objetivo fue golpeado
        distance = math.hypot(mouse_pos[0] - self.x, mouse_pos[1] - self.y)
        return distance <= self.radius

    def should_disappear(self):
        # Verificar si el objetivo debe desaparecer
        if self.disappearing:
            return pygame.time.get_ticks() - self.creation_time > self.lifetime
        return False