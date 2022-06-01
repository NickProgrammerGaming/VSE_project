import pygame
from sys import exit

#topki

def spawn_squares():
    row_count = 3
    blocks_count = 20
    s_x_pos = 5
    s_y_pos = 5
    for row in range(0, row_count):
        for block in range(0, blocks_count):
            square_rect = pygame.rect.Rect(s_x_pos, s_y_pos, 48, 48)
            squares_list.append(square_rect)
            s_x_pos += 64
        s_y_pos += 64
        s_x_pos = 5
    global spawned
    spawned = True


def draw_squares():
    for square in squares_list:
        pygame.draw.rect(screen, "White", square)


tolerance = 10


def check_collisions():
    global y_ball_speed, x_ball_speed, restart_screen, gameplay, spawned

    if ball_rect.left <= 0 or ball_rect.right >= s_width:
        x_ball_speed *= -1
    if ball_rect.top <= 0:
        y_ball_speed *= -1

    if ball_rect.colliderect(platform_rect):
        if abs(platform_rect.top - ball_rect.bottom) < tolerance:
            y_ball_speed *= -1
        if abs(platform_rect.right - ball_rect.left) < tolerance:
            x_ball_speed *= -1
        if abs(platform_rect.left - ball_rect.right) < tolerance:
            x_ball_speed *= -1
    for square in squares_list:
        if ball_rect.colliderect(square):
            if abs(square.top - ball_rect.bottom) < tolerance:
                y_ball_speed *= -1
            if abs(square.bottom - ball_rect.top) < tolerance:
                y_ball_speed *= -1
            if abs(square.right - ball_rect.left) < tolerance:
                x_ball_speed *= -1
            if abs(square.left - ball_rect.right) < tolerance:
                x_ball_speed *= -1
            squares_list.remove(square)
    if ball_rect.y >= s_height:
        restart_screen = True
        gameplay = False


def restart_game():
    squares_list.clear()
    global spawned, gameplay, x_ball, y_ball
    spawned = False
    gameplay = True
    x_ball = s_width / 2
    y_ball = s_height / 2
    platform_rect.center = (s_width/2, 650)


pygame.init()
s_width = 1280
s_height = 720
screen = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Bonk")

clock = pygame.time.Clock()

platform_rect = pygame.Rect(0, 0, 200, 30)
platform_rect.center = (s_width/2, 650)

ball_surf = pygame.image.load("Graphics/ball.png").convert_alpha()

platform_move_speed = 10

x_ball = s_width/2
y_ball = s_height/2

ball_rect = ball_surf.get_rect(center=(x_ball, y_ball))

x_ball_speed = 5
y_ball_speed = 7

squares_list = []

spawned = False

start_screen = True
gameplay = False
restart_screen = False
won = False

transfer = pygame.USEREVENT + 1
pygame.time.set_timer(transfer, 5000)

start_screen_surf = pygame.image.load("Graphics/Start_Screen.png")
start_screen_rect = start_screen_surf.get_rect(topleft=(0, 0))

restart_screen_surf = pygame.image.load("Graphics/Lose_Screen.png")
restart_screen_rect = restart_screen_surf.get_rect(topleft=(0, 0))

win_screen_surf = pygame.image.load("Graphics/Win_Screen.png")
win_screen_rect = win_screen_surf.get_rect(topleft=(0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(1)
        if won and event.type == transfer:
            won = False
            start_screen = True

    p_input = pygame.key.get_pressed()

    if start_screen:
        screen.blit(start_screen_surf, start_screen_rect)
        if p_input[pygame.K_SPACE]:
            restart_game()
            start_screen = False

    if restart_screen:
        screen.blit(restart_screen_surf, restart_screen_rect)
        if p_input[pygame.K_SPACE]:
            restart_game()
            restart_screen = False

    if won:
        screen.blit(win_screen_surf, win_screen_rect)


    if gameplay:
        if not spawned:
            spawn_squares()

        screen.fill("Black")

        if p_input[pygame.K_a]:
            platform_rect.x -= platform_move_speed
        if p_input[pygame.K_d]:
            platform_rect.x += platform_move_speed

        if platform_rect.right <= 0:
            platform_rect.left = s_width
        elif platform_rect.left >= s_width:
            platform_rect.right = 0

        x_ball -= x_ball_speed
        y_ball += y_ball_speed

        ball_rect.x = x_ball
        ball_rect.y = y_ball

        check_collisions()

        draw_squares()

        if len(squares_list) <= 0:
            won = True
            gameplay = False

        pygame.draw.rect(screen, "White", platform_rect)
        screen.blit(ball_surf, ball_rect)
        pygame.display.flip()

    pygame.display.update()
    clock.tick(60)





