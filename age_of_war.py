import pygame

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre de jeu
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Age of War Simplified")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Paramètres des bases et des unités
BASE_WIDTH, BASE_HEIGHT = 50, 100
UNIT_WIDTH, UNIT_HEIGHT = 20, 20
UNIT_SPEED = 2
DAMAGE_PER_SECOND = 10
FPS = 30

# Classe Base
class Base:
    def __init__(self, x, y, health, color):
        self.rect = pygame.Rect(x, y, BASE_WIDTH, BASE_HEIGHT)
        self.health = health
        self.max_health = health
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.rect(win, WHITE, self.rect, 2)  # Bordure blanche pour les bases

        # Dessiner la barre de vie
        health_bar_width = BASE_WIDTH
        health_ratio = self.health / self.max_health
        pygame.draw.rect(win, RED, (self.rect.x, self.rect.y - 10, health_bar_width, 5))
        pygame.draw.rect(win, GREEN, (self.rect.x, self.rect.y - 10, health_bar_width * health_ratio, 5))

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_destroyed(self):
        return self.health <= 0

# Classe Unité
class Unit:
    def __init__(self, x, y, target_base):
        self.rect = pygame.Rect(x, y, UNIT_WIDTH, UNIT_HEIGHT)
        self.target_base = target_base
        self.active = False
        self.attacking = False
        self.attack_timer = 0

    def move(self):
        if self.active and not self.attacking:
            if self.rect.right < self.target_base.rect.left:  # Assurer que l'unité se dirige vers la base
                self.rect.x += UNIT_SPEED
            else:
                self.attacking = True  # Commencer l'attaque une fois qu'elle atteint la base

    def attack(self):
        if self.attacking:
            # Infliger des dégâts à la base chaque seconde
            self.attack_timer += 1
            if self.attack_timer >= FPS:
                self.target_base.take_damage(DAMAGE_PER_SECOND)
                self.attack_timer = 0

    def draw(self, win):
        pygame.draw.rect(win, RED, self.rect)

# Initialisation des bases
player_base = Base(50, HEIGHT - BASE_HEIGHT, 100, BLUE)
enemy_base = Base(WIDTH - 100, HEIGHT - BASE_HEIGHT, 100, RED)

# Initialisation des unités (inactive au départ)
units = [Unit(100, HEIGHT - UNIT_HEIGHT - BASE_HEIGHT, enemy_base)]

# Boucle principale du jeu
def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Activer l'unité lorsque l'espace est pressé
                    for unit in units:
                        unit.active = True

        # Déplacement et attaque des unités
        for unit in units:
            unit.move()
            unit.attack()

        # Affichage des éléments
        WIN.fill(BLACK)
        player_base.draw(WIN)
        enemy_base.draw(WIN)

        for unit in units:
            unit.draw(WIN)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
