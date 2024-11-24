import pygame
import sys
import random
import math

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Fuentes
font = pygame.font.Font(None, 36)

# Sonidos
hit_sound = pygame.mixer.Sound("pistol-shot-233473.wav")  # Asegúrate de tener este archivo de sonido

# Cambiar el cursor a una mira (crosshair)
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)