import pygame
import random

pygame.init()


sw = 800
sh = 600
screen = pygame.display.set_mode((sw,sh))

player = pygame.image.load('./Ship_1.png')
enemy = pygame.image.load('./Ship_3.png')
gameover = pygame.image.load('./gameover.png')
pos = player.get_rect(center=(sw//2, sh//2))
player_speed = 5
bullet_speed = 10
enemy_speed = 7
star_speed = 3

bullets = []
enemies = []
stars = []
score = 0

#health bar properties
player_health = 100
max_health = 100
health_bar_length = 200
health_bar_height = 20
health_bar_color = (0,255,0)



clock = pygame.time.Clock()



# spawn a bullet
def spawn_bullet():
    bullet = pygame.Rect(pos.centerx -2, pos.top, 4, 10)
    bullets.append(bullet)

# spawn an enemy
def spawn_enemy():
    enemy_rect = enemy.get_rect(center=(random.randint(0, sw), 0))
    enemies.append(enemy_rect)

# spawn a star
def spawn_star():
    star_rect = pygame.Rect(random.randint(0, sw), 0, 2, 2)  
    stars.append(star_rect)


spawn_enemy_timer = 0
enemy_spawn_interval = 60
star_spawn_timer = 0
star_spawn_interval = 10

# draw the health bar 
def draw_health_bar():
    health_bar_width = (player_health / max_health) * health_bar_length
    health_bar_rect = pygame.Rect(10, 10, health_bar_width, health_bar_height)
    background_rect = pygame.Rect(10, 10, health_bar_length, health_bar_height)
    pygame.draw.rect(screen, (255, 0, 0), background_rect)
    pygame.draw.rect(screen, health_bar_color, health_bar_rect)

# draw the score
def draw_score():
    font = pygame.font.Font(None, 30)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect()
    score_rect.topright = (sw - 30, 15)
    screen.blit(score_text, score_rect)

# Main 
game_active = True
running = True
while running:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  
                    spawn_bullet()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                player_health = max_health
                pos = player.get_rect(center=(sw//2, sh//2))
                enemies.clear()
                bullets.clear()
                score = 0
    for star in stars:
        star.y += star_speed
        pygame.draw.rect(screen, (255, 255, 255), star)

    star_spawn_timer += clock.get_rawtime()
    if star_spawn_timer >= star_spawn_interval:
        spawn_star()
        star_spawn_timer = 0

    if game_active:
        screen.blit(player,pos)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            pos.y = max(pos.y - player_speed, 0)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            pos.y = min(pos.y + player_speed, sh - pos.height)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            pos.x = max(pos.x - player_speed, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            pos.x = min(pos.x + player_speed, sw - pos.width)


        for bullet in bullets:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)


        spawn_enemy_timer += clock.get_rawtime()
        if spawn_enemy_timer >= enemy_spawn_interval:
            spawn_enemy()
            spawn_enemy_timer = 0

        for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 255), bullet)

        for enemy_rect in enemies:
            enemy_rect.y += enemy_speed
            screen.blit(enemy, enemy_rect)

        for enemy_rect in enemies[:]:
            for bullet in bullets[:]:
                if enemy_rect.colliderect(bullet):
                    enemies.remove(enemy_rect)
                    bullets.remove(bullet)
                    print("Enemy Killed!")
                    score += 1

        for enemy_rect in enemies[:]:
            if enemy_rect.colliderect(pos):
                enemies.remove(enemy_rect)
                player_health -= 10
                print("-10 hp")
                if player_health <= 0:
                    print("Game Over")
                    game_active=False

                    
        draw_health_bar()
        draw_score()
    else:
        screen.blit(gameover, (sw//2 - gameover.get_width()//2, sh//2.5 - gameover.get_height()//2))
        font = pygame.font.Font(None, 30)
        text = font.render("Press Spacebar to Replay", True, (255, 255, 255))
        text_rect = text.get_rect(center=(sw // 2, sh // 2 + 100))
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()