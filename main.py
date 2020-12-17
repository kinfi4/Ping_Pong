import random
from time import sleep
import pygame as pg
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BALL_HEIGHT, BALL_WIDTH, PLAYER_WIDTH, PLAYER_HEIGHT, BALL_SPEED_X, \
    BALL_SPEED_Y, PLAYER_SPEED, OPPONENT_SPEED


def ball_animation():
    global ball_x_speed, ball_y_speed, ball_got_into_gates, player_score, opponent_score, score_time

    ball.x += ball_x_speed
    ball.y += ball_y_speed

    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_y_speed *= -1

    if ball.left <= 0:
        score_time = pg.time.get_ticks()
        player_score += 1

    if ball.right >= SCREEN_WIDTH:
        score_time = pg.time.get_ticks()
        opponent_score += 1

    if ball.colliderect(player) and ball_x_speed > 0:
        if abs(ball.right - player.left) < 10:
            ball_x_speed *= -1
        elif abs(ball.bottom - player.top) < 10:
            ball_y_speed *= -1
        elif abs(ball.top - player.bottom) < 10:
            ball_y_speed *= -1

    if ball.colliderect(opponent) and ball_x_speed < 0:
        if abs(ball.left - opponent.right) < 10:
            ball_x_speed *= -1
        elif abs(ball.bottom - opponent.top) < 10:
            ball_y_speed *= -1
        elif abs(ball.top - opponent.bottom) < 10:
            ball_y_speed *= -1


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0

    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT


def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0

    if opponent.bottom >= SCREEN_HEIGHT:
        opponent.bottom = SCREEN_HEIGHT


def ball_restart():
    global ball_x_speed, ball_y_speed, score_time

    current_time = pg.time.get_ticks()
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    if current_time - score_time < 700:
        number_three = score_font.render('3', False, light_grey)
        screen.blit(number_three, (SCREEN_WIDTH // 2 - 22, 50))

    if 700 < current_time - score_time < 1400:
        number_two = score_font.render('2', False, light_grey)
        screen.blit(number_two, (SCREEN_WIDTH // 2 - 22, 50))

    if 1400 < current_time - score_time < 2100:
        number_one = score_font.render('1', False, light_grey)
        screen.blit(number_one, (SCREEN_WIDTH // 2 - 22, 50))

    if current_time - score_time < 2100:
        ball_x_speed, ball_y_speed = 0, 0
    else:
        ball_x_speed = BALL_SPEED_X * random.choice((1, -1))
        ball_y_speed = BALL_SPEED_Y * random.choice((1, -1))
        score_time = None


pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player_score = 0
opponent_score = 0
game_font = pg.font.Font('freesansbold.ttf', 32)
score_font = pg.font.Font('freesansbold.ttf', 80)


if __name__ == '__main__':
    pg.display.set_caption('Ping Pong')
    ball = pg.Rect(SCREEN_WIDTH // 2 - BALL_WIDTH // 2, SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2, BALL_WIDTH, BALL_HEIGHT)
    player = pg.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
    opponent = pg.Rect(10, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)

    bg_color = pg.Color('grey12')
    light_grey = (200, 200, 200)

    player_speed = 0
    opponent_speed = OPPONENT_SPEED
    score_time = None
    ball_x_speed = BALL_SPEED_X
    ball_y_speed = BALL_SPEED_Y

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    player_speed += PLAYER_SPEED
                if event.key == pg.K_UP:
                    player_speed -= PLAYER_SPEED

            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN:
                    player_speed -= PLAYER_SPEED
                if event.key == pg.K_UP:
                    player_speed += PLAYER_SPEED

        player_animation()
        ball_animation()
        opponent_ai()

        screen.fill(bg_color)
        pg.draw.rect(screen, light_grey, player)
        pg.draw.rect(screen, light_grey, opponent)
        pg.draw.ellipse(screen, light_grey, ball)
        pg.draw.aaline(screen, light_grey, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        if score_time:
            ball_restart()
            player.center = (SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2)
            opponent.center = (10, SCREEN_HEIGHT // 2)

        player_text = game_font.render(f'{player_score}', False, light_grey)
        opponent_text = game_font.render(f'{opponent_score}', False, light_grey)

        screen.blit(player_text, (SCREEN_WIDTH // 2 + 16, SCREEN_HEIGHT // 2 - 16))
        screen.blit(opponent_text, (SCREEN_WIDTH // 2 - 32, SCREEN_HEIGHT // 2 - 16))

        pg.display.flip()

        clock.tick(60)
