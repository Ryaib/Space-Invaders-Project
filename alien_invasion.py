import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from ufo import UFO


def run_game():

    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))

    pygame.display.set_caption("Alien Invasion")

    play_button = Button(ai_settings, screen, "PLAY")
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)
    ufo = UFO(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    enemy_bullets = Group()

    # Create the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)
    ai_settings.alien_number = 0
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets, ufo)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets, ufo)
            gf.update_ufo(ai_settings, ufo)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, enemy_bullets, ufo)


run_game()
