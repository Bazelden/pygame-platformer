# main.py
import pygame
from sprites import Player, Platform, Bullet, Enemy
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, TILEMAP, TILE_SIZE, FPS

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Platformer")

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create platforms based on the tilemap
for row_index, row in enumerate(TILEMAP):
    for col_index, tile in enumerate(row):
        if tile == 1:
            platform = Platform(col_index * TILE_SIZE, row_index * TILE_SIZE)
            all_sprites.add(platform)
            platforms.add(platform)
        elif tile == 2:  # Assuming '2' represents an enemy in the TILEMAP
            enemy = Enemy(col_index * TILE_SIZE, row_index * TILE_SIZE)
            all_sprites.add(enemy)
            enemies.add(enemy)

# Create the player
player = Player(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH, SCREEN_HEIGHT)
all_sprites.add(player)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                new_bullet = player.shoot()
                if new_bullet:
                    bullets.add(new_bullet)
                    all_sprites.add(new_bullet)

    # Update
    player.update(platforms)
    bullets.update(platforms)
    enemies.update(platforms)

    # Remove bullets that have gone off-screen
    for bullet in bullets.copy():
        if bullet.rect.right < 0 or bullet.rect.left > SCREEN_WIDTH:
            bullet.kill()

    for enemy in enemies.copy():
        if enemy.check_bullet_collision(bullets):
            # Potential future game logic here like scores, etc.
            pass

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()