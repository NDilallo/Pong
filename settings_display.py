import pygame
from settings import *


class settingsDisplay():

    def __init__(self, game):
        self.game = game

    def clickCheck(self, mouse):
        #Back button
        if 10 <= mouse[0] <= 10+WINS_TEXT_SIZE*4 and 5 <= mouse[1] <= 5+WINS_TEXT_SIZE:
                    self.game.state = 'start'
        #Scores to win
        if WIDTH//4 <= mouse[0] <= WIDTH//4+MEDIUM_TEXT_SIZE and 60 <= mouse[1] <= 60+MEDIUM_TEXT_SIZE:
                    self.game.winAmount = 5
        if WIDTH//2 <= mouse[0] <= WIDTH//2+MEDIUM_TEXT_SIZE and 60 <= mouse[1] <= 60+MEDIUM_TEXT_SIZE:
                    self.game.winAmount = 7
        if WIDTH-(WIDTH//4) <= mouse[0] <= WIDTH-(WIDTH//4)+MEDIUM_TEXT_SIZE*2 and 60 <= mouse[1] <= 60+MEDIUM_TEXT_SIZE:
                    self.game.winAmount = 10
        #Ball Start Speed
        if WIDTH//4-50 <= mouse[0] <= WIDTH//4-50+MEDIUM_TEXT_SIZE*4 and 220 <= mouse[1] <= 220+MEDIUM_TEXT_SIZE:
                    self.game.ball.change_start_speed(2)
        if WIDTH//2-60 <= mouse[0] <= WIDTH//2-60+MEDIUM_TEXT_SIZE*5 and 220 <= mouse[1] <= 220+MEDIUM_TEXT_SIZE:
                    self.ball.change_start_speed(4)
        if WIDTH-(WIDTH//4)-20 <= mouse[0] <= WIDTH-(WIDTH//4)-20+MEDIUM_TEXT_SIZE*4 and 220 <= mouse[1] <= 220+MEDIUM_TEXT_SIZE:
                    self.game.ball.change_start_speed(10)
        #Ball Colors
        if WIDTH//8 + 175-50 <= mouse[0] <= WIDTH//8 + 175-50+SMALL_TEXT_SIZE*5 and 347 <= mouse[1] <= 347+SMALL_TEXT_SIZE:
            if self.game.color != WHITE:
                self.game.ball.change_color(WHITE)
        if WIDTH//8 + 275-50 <= mouse[0] <= WIDTH//8 + 275-50+SMALL_TEXT_SIZE*3 and 347 <= mouse[1] <= 347+SMALL_TEXT_SIZE:
            if self.game.color != RED:
                self.game.ball.change_color(RED)
        if WIDTH//8 + 375-50 <= mouse[0] <= WIDTH//8 + 375-50+SMALL_TEXT_SIZE*4 and 347 <= mouse[1] <= 347+SMALL_TEXT_SIZE:
            if self.game.color != BLUE:
                self.game.ball.change_color(BLUE)
        if WIDTH//8 + 475-50 <= mouse[0] <= WIDTH//8 + 475-50+SMALL_TEXT_SIZE*5 and 347 <= mouse[1] <= 347+SMALL_TEXT_SIZE:
            if self.game.color != GREEN:
                self.game.ball.change_color(GREEN)
        #Paddle Colors
        if WIDTH//8 + 175-50 <= mouse[0] <= WIDTH//8 + 175-50+SMALL_TEXT_SIZE*5 and 397 <= mouse[1] <= 397+SMALL_TEXT_SIZE:
            if self.game.color != WHITE:
                self.game.player.change_color(WHITE)
                self.game.ai.change_color(WHITE)
        if WIDTH//8 + 275-50 <= mouse[0] <= WIDTH//8 + 275-50+SMALL_TEXT_SIZE*3 and 397 <= mouse[1] <= 397+SMALL_TEXT_SIZE:
            if self.game.color != RED:
                self.game.player.change_color(RED)
                self.game.ai.change_color(RED)
        if WIDTH//8 + 375-50 <= mouse[0] <= WIDTH//8 + 375-50+SMALL_TEXT_SIZE*4 and 397 <= mouse[1] <= 397+SMALL_TEXT_SIZE:
            if self.game.color != BLUE:
                self.game.player.change_color(BLUE)
                self.game.ai.change_color(BLUE)
        if WIDTH//8 + 475-50 <= mouse[0] <= WIDTH//8 + 475-50+SMALL_TEXT_SIZE*5 and 397 <= mouse[1] <= 397+SMALL_TEXT_SIZE:
            if self.game.color != GREEN:
                self.game.player.change_color(GREEN)
                self.game.ai.change_color(GREEN)
        #Background Colors
        if WIDTH//8 + 175-50 <= mouse[0] <= WIDTH//8 + 175-50+SMALL_TEXT_SIZE*5 and 447 <= mouse[1] <= 447+SMALL_TEXT_SIZE:
            if self.game.ball.color != WHITE and self.game.player.color != WHITE:
                self.game.color = WHITE
                print('white')
        if WIDTH//8 + 275-50 <= mouse[0] <= WIDTH//8 + 275-50+SMALL_TEXT_SIZE*3 and 447 <= mouse[1] <= 447+SMALL_TEXT_SIZE:
            if self.game.ball.color != RED and self.game.player.color != RED:
                self.game.color = RED
                print('red')
        if WIDTH//8 + 375-50 <= mouse[0] <= WIDTH//8 + 375-50+SMALL_TEXT_SIZE*4 and 447 <= mouse[1] <= 447+SMALL_TEXT_SIZE:
            if self.game.ball.color != BLUE and self.game.player.color != BLUE:
                self.game.color = BLUE
                print('blue')
        if WIDTH//8 + 475-50 <= mouse[0] <= WIDTH//8 + 475-50+SMALL_TEXT_SIZE*5 and 447 <= mouse[1] <= 447+SMALL_TEXT_SIZE:
            if self.game.ball.color != GREEN and self.game.player.color != GREEN:
                self.game.color = GREEN
                print('green')
        if WIDTH//8 + 550-50 <= mouse[0] <= WIDTH//8 + 550-50+SMALL_TEXT_SIZE*5 and 447 <= mouse[1] <= 447+SMALL_TEXT_SIZE:
            self.game.color = BLACK
            print('black')
    

    def settings_update(self):
        pass
            

    def settings_draw(self):
        self.game.screen.fill(BLACK)
        self.game.draw_text(f'BACK', self.game.screen, [10,5], 
        WINS_TEXT_SIZE, (44, 167, 198), START_FONT)

        self.game.draw_text('SCORE TO WIN',self.game.screen, 
        [WIDTH//2, 20], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        scoreFlag = False
        if self.game.winAmount == 5:
            scoreFlag = True
        self.game.draw_text(f'5', self.game.screen, [WIDTH//4, 60], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT, rect=scoreFlag)
        scoreFlag = False
        if self.game.winAmount == 7:
            scoreFlag = True
        self.game.draw_text(f'7', self.game.screen, [WIDTH//2, 60], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT, rect=scoreFlag)
        scoreFlag = False
        if self.game.winAmount == 10:
            scoreFlag = True
        self.game.draw_text(f'10', self.game.screen, [WIDTH-(WIDTH//4), 60], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT, rect=scoreFlag)
        scoreFlag = False

        self.game.draw_text('BALL START SPEED',self.game.screen, 
        [WIDTH//2, 160], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        speedFlag = False
        if self.game.ball.horizontal_speed == 2:
            speedFlag = True
        self.game.draw_text(f'SLOW', self.game.screen, [WIDTH//4-50, 220], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT, rect = speedFlag)
        speedFlag = False
        if self.game.ball.horizontal_speed == 4:
            speedFlag = True
        self.game.draw_text(f'MEDIUM', self.game.screen, [WIDTH//2-60, 220], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT, rect=speedFlag)
        speedFlag = False
        if self.game.ball.horizontal_speed == 10:
            speedFlag = True
        self.game.draw_text(f'FAST', self.game.screen, [WIDTH-(WIDTH//4)-20, 220], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT, rect= speedFlag)
        speedFlag = False

        self.game.draw_text('COLOR SETTINGS',self.game.screen, 
        [WIDTH//2, 300], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)

        self.game.draw_text(f'BALL:', self.game.screen, [WIDTH//9-50, 340], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT)
        ballColorFlag = False
        if self.game.ball.color == WHITE:
            ballColorFlag = True
        self.game.draw_text(f'WHITE', self.game.screen, [WIDTH//8 + 175-50, 347], 
        SMALL_TEXT_SIZE, WHITE, START_FONT, rect=ballColorFlag)
        ballColorFlag = False
        if self.game.ball.color == RED:
            ballColorFlag = True
        self.game.draw_text(f'RED', self.game.screen, [WIDTH//8 + 275-50, 347], 
        SMALL_TEXT_SIZE, RED, START_FONT, rect=ballColorFlag)
        ballColorFlag = False
        if self.game.ball.color == BLUE:
            ballColorFlag = True
        self.game.draw_text(f'BLUE', self.game.screen, [WIDTH//8 + 375-50, 347], 
        SMALL_TEXT_SIZE, BLUE, START_FONT, rect=ballColorFlag)
        ballColorFlag = False
        if self.game.ball.color == GREEN:
            ballColorFlag = True
        self.game.draw_text(f'GREEN', self.game.screen, [WIDTH//8 + 475-50, 347], 
        SMALL_TEXT_SIZE, GREEN, START_FONT, rect=ballColorFlag)
        ballColorFlag = False

        self.game.draw_text(f'PADDLE:', self.game.screen, [WIDTH//9-50, 390], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT)
        paddleColorFlag = False
        if self.game.player.color == WHITE:
            paddleColorFlag = True
        self.game.draw_text(f'WHITE', self.game.screen, [WIDTH//8 + 175-50, 397], 
        SMALL_TEXT_SIZE, WHITE, START_FONT, rect= paddleColorFlag)
        paddleColorFlag = False
        if self.game.player.color == RED:
            paddleColorFlag = True
        self.game.draw_text(f'RED', self.game.screen, [WIDTH//8 + 275-50, 397], 
        SMALL_TEXT_SIZE, RED, START_FONT, rect= paddleColorFlag)
        paddleColorFlag = False
        if self.game.player.color == BLUE:
            paddleColorFlag = True
        self.game.draw_text(f'BLUE', self.game.screen, [WIDTH//8 + 375-50, 397], 
        SMALL_TEXT_SIZE, BLUE, START_FONT, rect= paddleColorFlag)
        paddleColorFlag = False
        if self.game.player.color == GREEN:
            paddleColorFlag = True
        self.game.draw_text(f'GREEN', self.game.screen, [WIDTH//8 + 475-50, 397], 
        SMALL_TEXT_SIZE, GREEN, START_FONT, rect= paddleColorFlag)
        paddleColorFlag = False

        self.game.draw_text(f'BACKGROUND:', self.game.screen, [WIDTH//9-50, 440], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT)
        backgroundColorFlag = False
        if self.game.color == WHITE:
            backgroundColorFlag = True
        self.game.draw_text(f'WHITE', self.game.screen, [WIDTH//8 + 175-50, 447], 
        SMALL_TEXT_SIZE, WHITE, START_FONT, rect= backgroundColorFlag)
        backgroundColorFlag = False
        if self.game.color == RED:
            backgroundColorFlag = True
        self.game.draw_text(f'RED', self.game.screen, [WIDTH//8 + 275-50, 447], 
        SMALL_TEXT_SIZE, RED, START_FONT, rect= backgroundColorFlag)
        backgroundColorFlag = False
        if self.game.color == BLUE:
            backgroundColorFlag = True
        self.game.draw_text(f'BLUE', self.game.screen, [WIDTH//8 + 375-50, 447], 
        SMALL_TEXT_SIZE, BLUE, START_FONT, rect= backgroundColorFlag)
        backgroundColorFlag = False
        if self.game.color == GREEN:
            backgroundColorFlag = True
        self.game.draw_text(f'GREEN', self.game.screen, [WIDTH//8 + 475-50, 447], 
        SMALL_TEXT_SIZE, GREEN, START_FONT, rect= backgroundColorFlag)
        backgroundColorFlag = False
        if self.game.color == BLACK:
            backgroundColorFlag = True
        self.game.draw_text(f'BLACK', self.game.screen, [WIDTH//8 + 550-50, 447], 
        SMALL_TEXT_SIZE, GRAY, START_FONT, rect= backgroundColorFlag)
        backgroundColorFlag = False

        pygame.display.update()