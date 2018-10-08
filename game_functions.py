import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien, Alien2, Alien3
from bullet import EnemyBullet
import random


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets, ufo):
    enemy_bullets.update()
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets, ufo)


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                fire_bullet(ai_settings, screen, ship, bullets)
            elif event.key == pygame.K_q:
                sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        pygame.mixer.music.load('sound/laser.ogg')
        pygame.mixer.music.play(0)


def check_keyup_events(event, ship):
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False


def create_fleet(ai_settings, screen, ship, aliens):
    # Create a full fleet
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    # Create the fleet of aliens.

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            if row_number == 0:
                alien_type = 3
            elif 0 < row_number <= 2:
                alien_type = 2
            else:
                alien_type = 0

            create_alien(ai_settings, screen, aliens, alien_number, row_number, alien_type)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number, alien_type):
    # Create an alien and place it in the row.
    if alien_type == 2:
        alien = Alien2(ai_settings, screen)
    elif alien_type == 3:
        alien = Alien3(ai_settings, screen)
    else:
        alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.alien_number = ai_settings.alien_number
    ai_settings.alien_number += 1
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets, ufo):
    # Check if the fleet is at an edge and then update the positions of all aliens in the fleet

    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    enemy_fire(ai_settings, screen, aliens, enemy_bullets)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, ufo)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, ufo)


def enemy_fire(ai_settings, screen, aliens, enemy_bullets):
    current = pygame.time.get_ticks()
    rng = random.randint(0, 45)
    if (current - ai_settings.last_tick) > ai_settings.tickrate:
        ai_settings.last_tick = current
        for alien in aliens.sprites():
            if alien.alien_number == rng:
                pygame.mixer.music.load('sound/enemy.wav')
                pygame.mixer.music.play(0)
                new_bullet = EnemyBullet(ai_settings, screen, alien)
                enemy_bullets.add(new_bullet)


def update_ufo(ai_settings, ufo):
    current = pygame.time.get_ticks()
    if (current - ai_settings.ufo_tick) > 10000 and not ufo.UFO_SPAWN:
        ai_settings.ufo_tick = pygame.time.get_ticks()
        ufo.UFO_SPAWN = True
        print('UFO HAS SPAWNED!')
    if ufo.UFO_SPAWN:
        ufo.update()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, enemy_bullets, ufo):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for bullet in enemy_bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    ufo.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            if alien.check_edges():
                change_fleet_direction(ai_settings, aliens)
                break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_destroyed(ai_settings, screen, stats, sb, ship, aliens, bullets, ufo):
    pygame.mixer.music.load('sound/death.wav')
    pygame.mixer.music.play(0)
    ship.destroy_ship()
    ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, ufo)


def ufo_reset(ufo):
    ufo.destroyed = False
    ufo.UFO_SPAWN = False
    ufo.x = -100
    ufo.update()


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets, ufo):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    dead = pygame.sprite.spritecollide(ship, enemy_bullets, True)
    ufo_score = pygame.sprite.spritecollide(ufo, bullets, True)
    if ufo_score:
        ufo.destroyed = True
        ufo.rect.x = -100
        print('Ufo HIT')
        pygame.mixer.music.load('sound/kill.ogg')
        pygame.mixer.music.play(0)
    if dead:
        ship_destroyed(ai_settings, screen, stats, sb, ship, aliens, bullets, ufo)

    if collisions:
        for aliens in collisions.values():
            ai_settings.tickrate -= 11
            stats.score += ai_settings.alien_points * len(aliens)
            pygame.mixer.music.load('sound/kill.ogg')
            pygame.mixer.music.play(0)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        ai_settings.tickrate = 500
        ai_settings.alien_number = 0
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, ufo):
    # Decrement ships
    ufo_reset(ufo)
    ai_settings.alien_number = 0
    ai_settings.tickrate = 500
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # Pause
        sleep(0.5)
    else:
        stats.game_active = False


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, ufo):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, ufo)
            break


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True
        # Reset the Scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
