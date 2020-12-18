import random
from time import sleep
import pygame as pg
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BALL_HEIGHT, BALL_WIDTH, PLAYER_WIDTH, PLAYER_HEIGHT, BALL_SPEED_X, \
    BALL_SPEED_Y, PLAYER_SPEED, OPPONENT_SPEED

from models import Ball, Player, Opponent
from controller import GameManager


pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


bg_color = pg.Color('#2F373F')
accent_color = (27, 35, 43)
player_score = 0
opponent_score = 0
game_font = pg.font.Font('freesansbold.ttf', 32)
timer_font = pg.font.Font('freesansbold.ttf', 80)

middle_strip = pg.Rect(SCREEN_WIDTH/2 - 2, 0, 4, SCREEN_HEIGHT)


if __name__ == '__main__':
    pg.display.set_caption('Ping Pong')
    player = Player('img/Paddle.png', SCREEN_WIDTH - 20, SCREEN_HEIGHT//2, 5)
    opponent = Opponent('img/Paddle.png', 20, SCREEN_HEIGHT//2, 5)
    paddle_group = pg.sprite.Group()
    paddle_group.add(player)
    paddle_group.add(opponent)

    ball = Ball('img/Ball.png', SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 4, 4, paddle_group)
    ball_sprite = pg.sprite.GroupSingle()
    ball_sprite.add(ball)

    game_manager = GameManager(ball_sprite, paddle_group)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    player.movement -= player.speed
                if event.key == pg.K_DOWN:
                    player.movement += player.speed
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    player.movement += player.speed
                if event.key == pg.K_DOWN:
                    player.movement -= player.speed

        screen.fill(bg_color)
        pg.draw.rect(screen, accent_color, middle_strip)

        # Run the game
        game_manager.run_game(screen, game_font, timer_font, accent_color, bg_color)

        # Rendering
        pg.display.flip()
        clock.tick(120)
