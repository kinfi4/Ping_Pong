import pygame as pg

from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self, screen, basic_font, timer_font, accent_color, bg_color):
        # Drawing the game objects
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        # Updating the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update(screen, bg_color, timer_font)
        self.reset_ball()
        self.draw_score(screen, basic_font, accent_color)

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= SCREEN_WIDTH:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self, screen, basic_font, accent_color):
        player_score = basic_font.render(str(self.player_score), True, accent_color)
        opponent_score = basic_font.render(str(self.opponent_score), True, accent_color)

        player_score_rect = player_score.get_rect(midleft=(SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT // 2))
        opponent_score_rect = opponent_score.get_rect(midright=(SCREEN_WIDTH / 2 - 40, SCREEN_HEIGHT // 2))
        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)
