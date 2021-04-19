import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 840, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Voando Alto")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

POZE_IDLE = pygame.image.load(os.path.join('Assets', 'idle.png'))
POZE_SHOOTING = pygame.image.load(os.path.join('Assets', 'shoot.png'))
RED_SPACESHIP_OLD = pygame.image.load(os.path.join('Assets', 'static.png'))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_OLD, (60, 60))

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.jpeg')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, yellow_health, poze_status):
    WIN.blit(SPACE, (0, 0))

    yellow_health_text = HEALTH_FONT.render("Pontos: " + str(yellow_health), 1, BLACK)
    WIN.blit(yellow_health_text, (10, 10))

    
    if poze_status == "idle":
        WIN.blit(POZE_IDLE, (yellow.x, yellow.y))
    elif poze_status == "shooting":
        WIN.blit(POZE_SHOOTING, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < 300:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, BLACK)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    poze_status = "idle"
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        red.x -= 5

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width + 20, yellow.y + yellow.height//2 + 10, 10, 5)
                    yellow_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                #BULLET_HIT_SOUND.play()

        winner_text = ""

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        if keys_pressed[pygame.K_SPACE]:
            poze_status = "shooting"
        else:
            poze_status = "idle"

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, yellow_health, poze_status)

    main()


if __name__ == "__main__":
    main()


##health:
#0,800
#0,2 2