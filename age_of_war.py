import pygame
import time

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
YELLOW = (255, 255, 0)

# Paramètres des bases et des unités
BASE_WIDTH, BASE_HEIGHT = 50, 100
UNIT_WIDTH, UNIT_HEIGHT = 20, 20
UNIT_SPEED = 2
DAMAGE_PER_SECOND = 5
FPS = 30
UNIT_HEALTH = 50
TOWER_DAMAGE = 5
TOWER_RANGE = WIDTH // 4  # Un quart de la distance totale
COOLDOWN_TIME = 2  # Cooldown de 2 secondes entre chaque invocation d'unité

# Classe Base
class Base:
    def __init__(self, x, y, health, color, is_enemy=False):
        self.rect = pygame.Rect(x, y, BASE_WIDTH, BASE_HEIGHT)
        self.health = health
        self.max_health = health
        self.color = color
        self.is_enemy = is_enemy

    def draw(self, win):
        # Dessiner la zone d'attaque
        center_x = self.rect.centerx
        center_y = self.rect.centery
        pygame.draw.circle(win, YELLOW, (center_x, center_y), TOWER_RANGE, 1)

        # Dessiner la base
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

    def attack_units(self, units):
        if self.is_destroyed():
            return  # Ne pas attaquer si la tour est détruite

        # Trouver la première unité dans la portée de la tour
        for unit in units:
            distance_to_unit = self.rect.centerx - unit.rect.centerx
            if self.is_enemy and abs(distance_to_unit) <= TOWER_RANGE:
                unit.take_damage(TOWER_DAMAGE / FPS)
                break  # Attaquer seulement une unité à la fois

# Classe Unité
class Unit:
    def __init__(self, x, y, target_base):
        self.rect = pygame.Rect(x, y, UNIT_WIDTH, UNIT_HEIGHT)
        self.target_base = target_base
        self.active = True
        self.attacking = False
        self.attack_timer = 0
        self.health = UNIT_HEALTH
        self.max_health = UNIT_HEALTH

    def move(self, units):
        if self.active and not self.attacking:
            # Vérifier la collision avec d'autres unités
            next_rect = self.rect.copy()
            next_rect.x += UNIT_SPEED
            collision = any(next_rect.colliderect(unit.rect) for unit in units if unit is not self)

            if not collision and self.rect.right < self.target_base.rect.left:
                self.rect.x += UNIT_SPEED
            else:
                if self.rect.right >= self.target_base.rect.left:
                    self.attacking = True  # Commencer l'attaque une fois qu'elle atteint la base

    def attack(self):
        if self.attacking:
            # Infliger des dégâts à la base chaque seconde
            self.attack_timer += 1
            if self.attack_timer >= FPS:
                self.target_base.take_damage(DAMAGE_PER_SECOND)
                self.attack_timer = 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.active = False
            self.rect.x = -100  # Retire l'unité de l'écran (elle est détruite)

    def draw(self, win):
        if self.active:
            pygame.draw.rect(win, RED, self.rect)
            
            # Dessiner la barre de vie de l'unité
            health_bar_width = UNIT_WIDTH
            health_ratio = self.health / self.max_health
            pygame.draw.rect(win, RED, (self.rect.x, self.rect.y - 10, health_bar_width, 3))
            pygame.draw.rect(win, GREEN, (self.rect.x, self.rect.y - 10, health_bar_width * health_ratio, 3))

# Initialisation des bases
player_base = Base(50, HEIGHT - BASE_HEIGHT, 100, BLUE)
enemy_base = Base(WIDTH - 100, HEIGHT - BASE_HEIGHT, 100, RED, is_enemy=True)

# Initialisation des unités
units = []  # La liste des unités est initialisée ici

# Variable pour le cooldown d'invocation
last_invocation_time = 0

# Boucle principale du jeu
def main():
    global units, last_invocation_time  # Déclarer la liste 'units' et le temps d'invocation comme variables globales
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_time = time.time()
                    if current_time - last_invocation_time >= COOLDOWN_TIME:
                        # Ajouter une nouvelle unité lorsque l'espace est pressé et que le cooldown est terminé
                        new_unit = Unit(100, HEIGHT - UNIT_HEIGHT - BASE_HEIGHT, enemy_base)
                        units.append(new_unit)
                        last_invocation_time = current_time

        # Déplacement et attaque des unités
        for unit in units:
            unit.move(units)
            unit.attack()

        # Les tours attaquent les unités à portée
        enemy_base.attack_units(units)

        # Retirer les unités mortes
        units = [unit for unit in units if unit.active]

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
