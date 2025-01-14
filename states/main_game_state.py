import pygame
import random
import math
import os 
import sys 

from scripts.settings import *
from scripts.asteroids import Asteroid
from scripts.player import Player
from scripts.buttons import Button
from states.game_over_state import GameOver
from states.base_state import BaseState
from scripts.bullet import Bullet
from scripts.enemy import Enemy

# THE MAIN GAME CLASS 
class InGame(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.screen = self.game.screen
        self.clock = pygame.time.Clock()
        self.button = Button()

        # Create sprites
        self.all_sprites = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.spaceships = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()  # Add group for enemy bullets
        self.player = Player()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.spaceships)

        # Spawn rates and counters
        self.spawn_rate_asteroids = 200
        self.spawn_rate_spaceships = random.randint(1000, 5000)
        self.spawn_counter_asteroids = 0
        self.spawn_counter_spaceships = 0
        self.paused = False

        # Initialize fonts
        self.font = pygame.font.Font(FONT1, 150)
        self.font1 = pygame.font.Font(FONT2, 80)
        self.font2 = pygame.font.Font(FONT3, 80)
        self.font3 = pygame.font.Font(FONT4, 80)
        self.font4 = pygame.font.Font(FONT4, 40)

    def check_collisions(self, player, asteroids, bullets, spaceships, enemy_bullets):
        for asteroid in asteroids:
            if player.rect.colliderect(asteroid.rect):
                self.game.state_manager.change_state("game_over")
        for spaceship in spaceships:
            if player.rect.colliderect(spaceship.rect):
                self.game.state_manager.change_state("game_over")
        
        # Check for bullet-asteroid collisions
        collisions = pygame.sprite.groupcollide(bullets, asteroids, True, True)
        for bullet, collided_asteroids in collisions.items():
            # Here you can handle additional logic like scoring or creating smaller asteroids
            pass
        collisions = pygame.sprite.groupcollide(bullets, spaceships, True, True)
        for bullet, collided_spaceships in collisions.items():
            # Here you can handle additional logic like scoring or creating smaller asteroids
            pass

        # Check for enemy bullet collisions with player
        if pygame.sprite.spritecollide(player, enemy_bullets, True):
            self.game.state_manager.change_state("game_over")

    def update(self, events):
        # Process input/events
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused

        if not self.paused:
            # Update all sprites except spaceships (Enemy)
            for sprite in self.all_sprites:
                if isinstance(sprite, Enemy):
                    bullet = sprite.update(self.player.rect.center)
                    if bullet:
                        self.all_sprites.add(bullet)
                        self.enemy_bullets.add(bullet)
                else:
                    sprite.update()

            # Spawn asteroids
            self.spawn_counter_asteroids += 1
            if self.spawn_counter_asteroids >= self.spawn_rate_asteroids:
                asteroid = Asteroid()
                self.all_sprites.add(asteroid)
                self.asteroids.add(asteroid)
                self.spawn_counter_asteroids = 0
                
            # Spawn spaceships
            self.spawn_counter_spaceships += 1
            if self.spawn_counter_spaceships >= self.spawn_rate_spaceships:
                spaceship = Enemy()
                self.all_sprites.add(spaceship)
                self.spaceships.add(spaceship)
                self.spawn_counter_spaceships = 0

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.player.rotate_left()
            if keys[pygame.K_d]:
                self.player.rotate_right()
            if keys[pygame.K_w]:
                self.player.accelerate()
            if keys[pygame.K_s]:
                self.player.decelerate()
            if keys[pygame.K_SPACE] and self.player.can_shoot():
                bullet = Bullet(self.player.rect.center, self.player.angle)
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)

            # Draw / render
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.check_collisions(self.player, self.asteroids, self.bullets, self.spaceships, self.enemy_bullets)

        else: 
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if self.resume_button.collidepoint(event.pos):
                        self.paused = False 
                    if self.restart_button.collidepoint(event.pos):
                        self.game.state_manager.change_state("game")
                    if self.options_button.collidepoint(event.pos):
                        print("Options Screen")
                    if self.quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            # DRAW THE TITLE SCREEN NAME
            pause_screen_text = self.font2.render("PAUSED", True, WHITE)
            self.screen.blit(pause_screen_text, (375, 200))
            self.resume_button = self.button.draw_button(self.screen, 100, 700, BUTTON_WIDTH, BUTTON_HEIGHT, "Resume", WHITE, self.font1, BLACK)
            self.restart_button = self.button.draw_button(self.screen, 400, 700, BUTTON_WIDTH, BUTTON_HEIGHT, "Restart", WHITE, self.font1, BLACK)
            self.options_button = self.button.draw_button(self.screen, 800, 700, BUTTON_WIDTH, BUTTON_HEIGHT, "Options", WHITE, self.font1, BLACK)
            self.quit_button = self.button.draw_button(self.screen, 1100, 700, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit", WHITE, self.font1, BLACK)

        pygame.display.update()
        self.clock.tick(FPS)
