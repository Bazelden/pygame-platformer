# sprites.py
import pygame
import random
from config import WHITE, BLUE, YELLOW, RED, TILE_SIZE, BULLET_SPEED, ENEMY_SPEED

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.velocity_x = 0
        self.velocity_y = 0
        self.jumping = False
        self.gravity = 0.8
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.direction = 1  # 1 for right, -1 for left
        self.shoot_cooldown = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.direction = -1
        if keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.direction = 1
        if keys[pygame.K_SPACE] and not self.jumping:
            self.jump()

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.velocity_y = -15

    def apply_gravity(self):
        self.velocity_y += self.gravity

    def update(self, platforms):
        self.handle_input()
        self.apply_gravity()

        # Horizontal movement
        self.rect.x += self.velocity_x
        self.check_collisions(platforms, 'horizontal')

        # Vertical movement
        self.rect.y += self.velocity_y
        self.check_collisions(platforms, 'vertical')

        # Screen boundary check
        self.rect.x = max(0, min(self.screen_width - self.rect.width, self.rect.x))

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def check_collisions(self, platforms, direction):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if direction == 'horizontal':
                    if self.velocity_x > 0:  # Moving right
                        self.rect.right = platform.rect.left
                    elif self.velocity_x < 0:  # Moving left
                        self.rect.left = platform.rect.right
                    self.velocity_x = 0
                elif direction == 'vertical':
                    if self.velocity_y > 0:  # Falling
                        self.rect.bottom = platform.rect.top
                        self.jumping = False
                    elif self.velocity_y < 0:  # Jumping
                        self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20  # Set a cooldown of 20 frames
            return Bullet(self.rect.centerx, self.rect.centery, self.direction)
        return None

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# New class for the bullet sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface([10, 5])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.direction = direction
        self.speed = BULLET_SPEED

    def update(self, platforms):
        self.rect.x += self.speed * self.direction
        
        # Check for collisions with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.kill()  # Remove the bullet if it hits a platform
                break

# New class for the eneme sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = ENEMY_SPEED
        self.direction = 1  # 1 for right, -1 for left
        self.velocity_y = 0
        self.steps = 0
        self.gravity = 0.8
        self.max_steps = 4 * TILE_SIZE  # 4 tiles worth of movement

    def apply_gravity(self):
        self.velocity_y += self.gravity

    def update(self, platforms):
        self.apply_gravity() # Taken from player logic - not working

        # Horizontal movement
        self.rect.x += self.speed * self.direction
        self.steps += abs(self.speed)

        # Screen boundary check
        self.rect.x = max(0, min(800 - self.rect.width, self.rect.x))

        # Change direction after moving max_steps
        if self.steps >= self.max_steps:
            self.direction *= -1
            self.steps = 0

    def check_bullet_collision(self, bullets):
        for bullet in bullets:
            if self.rect.colliderect(bullet.rect):
                self.kill()
                bullet.kill()  
                return True
        return False