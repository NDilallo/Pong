from turtle import fillcolor, position
import pygame, sys
from settings import *
from player_class import *
from ball_class import *
from ai_class import *
from walls_class import *
import time

pygame.init()
vec = pygame.math.Vector2

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Constants all caps
        self.clock = pygame.time.Clock() #Clock for fps
        self.running = True
        self.state = 'start'
        self.player = Player(self, PLAYER_START_POS)
        self.ai = AI(self, AI_START_POS) 
        self.walls = Walls(self)
        self.ball = Ball(self)
        self.ai.giveBall(self.ball)
        self.horizontal_hitboxes = [] #Hitboxes oriented sideways ie top bottom walls
        self.horizontal_hitboxes.extend(self.walls.hitboxVert)
        self.vert_hitboxes = [self.player.hitbox, self.ai.hitbox]

        self.delay = False
        self.won = ''
        self.playerWins = 0

        self.winAmount = WIN_AMOUNT
        self.color = BLACK

        self.survivalMode = 'OFF'
        self.t0 = 0
        self.printTime = 0
        self.survivalRecord = 0.0

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'settings':
                self.settings_events()
                self.settings_update()
                self.settings_draw()
            elif self.state == 'playing Solo':
                self.playingSolo_events()
                self.playingSolo_update()
                self.playingSolo_draw()
            elif self.state == 'playing Survival':
                self.printTime = time.time() - self.t0
                self.playingSolo_events()
                self.playingSurvival_update()
                self.playingSurvival_draw()
            elif self.state == 'game over':
                self.game_over_events()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit() #Out of the game so quit
        sys.exit()

########################### HELPER FUNCTIONS ###################################

    def draw_text(self, words, screen, pos, size, color, font_name, centered=False, rect=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if centered==True:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

        if rect==True:
            pygame.draw.rect(self.screen, WHITE, (pos[0]-text_size[0]/4, 
            pos[1]-text_size[1]/4, text_size[0]+text_size[0]/2, text_size[1]+text_size[1]/2), 2) #x, y, rectWidth, rectHeight
        
########################### INTRO FUNCTIONS ####################################
    
    def start_events(self):
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.running = False #If we click quit, exit program
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: #Press spacebar and game starts
                if self.survivalMode == 'OFF':
                    self.state = 'playing Solo'
                else:
                    self.state = 'playing Survival'
                    self.t0 = time.time()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH//2-60 <= mouse[0] <= WIDTH//2+60 and HEIGHT//2+135 <= mouse[1] <= HEIGHT//2+160:
                    self.state = 'settings'
                if WIDTH-125 <= mouse[0] <= WIDTH-125+WINS_TEXT_SIZE*13 and 0 <= mouse[1] <= WINS_TEXT_SIZE:
                    if self.survivalMode == 'ON':
                        self.survivalMode = 'OFF'
                    else:
                        self.survivalMode = 'ON'
    
    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PONG', self.screen, [WIDTH//2, HEIGHT-330], 
        PONG_TITLE_SIZE, WHITE, PONG_TEXT_FONT, centered=True, rect=True)
        self.draw_text('PUSH SPACEBAR TO BEGIN',self.screen, 
        [WIDTH//2, HEIGHT//2+50], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text(f'WINS: {self.playerWins}', self.screen, [4,0], 
        WINS_TEXT_SIZE, (44, 167, 198), START_FONT)
        self.draw_text(f'Survival Record: {round(self.survivalRecord, 2)}', self.screen, [4,20], 
        WINS_TEXT_SIZE, (44, 167, 198), START_FONT)
        self.draw_text(f'Survival: {self.survivalMode}', self.screen, [WIDTH-125,0], 
        WINS_TEXT_SIZE, (44, 167, 198), START_FONT)

        pygame.draw.rect(self.screen, WHITE, (WIDTH//2-60, HEIGHT//2+135,120,25))
        self.draw_text('SETTINGS', self.screen, [WIDTH//2, HEIGHT//2+150], 
        SETTINGS_TEXT_SIZE, RED, PONG_TEXT_FONT, centered=True)

        pygame.display.update()

############################# PLAYING SOLO FUNCTIONS ###############################

    def playingSolo_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False #If we click quit, exit program
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                            self.player.move(vec(0,-4))
                    if event.key == pygame.K_DOWN:
                            self.player.move(vec(0,4))
                    if event.key == pygame.K_ESCAPE:
                        self.reset()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.player.move(vec(0,0))

    
    def playingSolo_update(self):
        self.player.update()
        self.ball.update()
        self.ai.update()

        if pygame.Rect.colliderect(self.ball.hitbox, self.player.hitbox):
            self.ball.reflect('player', self.player)
        elif pygame.Rect.colliderect(self.ball.hitbox, self.ai.hitbox):
            self.ball.reflect('player', self.ai)
        elif pygame.Rect.colliderect(self.ball.hitbox, self.walls.hitboxVert[0]) or pygame.Rect.colliderect(self.ball.hitbox, self.walls.hitboxVert[1]):
            self.ball.reflect('wall', self.walls)
    
        self.delay = self.ball.scoreCheck()
        if self.delay[0] == True:
            self.incrementScore(self.delay[1])
            self.won = self.winCheck()
            if self.won == '':
                self.respawnDelay()


    def playingSolo_draw(self):
        self.screen.fill(self.color)
        spawn_height = HEIGHT
        while spawn_height >= 10:
            pygame.draw.rect(self.screen, WHITE, [WIDTH/2-5, spawn_height-15, 10, 10])
            spawn_height -= 20
        self.player.draw()
        self.ball.draw()
        self.ai.draw()
        self.walls.draw()
        self.draw_text(str(self.player.score), self.screen, [WIDTH-WIDTH//4,10], 
        SCORE_TEXT_SIZE, (44, 167, 198), START_FONT)
        self.draw_text(str(self.ai.score), self.screen, [WIDTH//4,10], 
        SCORE_TEXT_SIZE, (44, 167, 198), START_FONT)
        
        if self.won != '':
            if self.won == 'ai':
                self.draw_text('YOU LOSE', self.screen, [WIDTH//2, HEIGHT-330], 
                PONG_TITLE_SIZE, RED, PONG_TEXT_FONT, centered=True)
            else:
                self.draw_text('YOU WIN!', self.screen, [WIDTH//2, HEIGHT-330], 
                PONG_TITLE_SIZE, RED, PONG_TEXT_FONT, centered=True)
                self.playerWins += 1
            self.draw_text('PUSH SPACEBAR TO EXIT',self.screen, 
            [WIDTH//2, HEIGHT//2+50], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        pygame.display.update()

    
    def incrementScore(self, scorer):
        if scorer == 'player':
            self.player.score += 1
        else:
            self.ai.score += 1
    
    def winCheck(self):
        if self.player.score == self.winAmount:
            self.state = 'game over'
            return 'player'
        elif self.ai.score == self.winAmount:
            self.state = 'game over'
            return 'ai'
        return ''


########################## Playing Survival Functions #######################################

    def playingSurvival_update(self):
        self.player.update()
        self.ball.update()
        self.ai.update()

        if pygame.Rect.colliderect(self.ball.hitbox, self.player.hitbox):
            self.ball.reflect('player', self.player)
        elif pygame.Rect.colliderect(self.ball.hitbox, self.ai.hitbox):
            self.ball.reflect('player', self.ai)
        elif pygame.Rect.colliderect(self.ball.hitbox, self.walls.hitboxVert[0]) or pygame.Rect.colliderect(self.ball.hitbox, self.walls.hitboxVert[1]):
            self.ball.reflect('wall', self.walls)

        self.delay = self.ball.scoreCheck()
        if self.delay[1] == 'ai':
            self.state = 'game over'
        if self.delay[1] == 'player':
            self.respawnDelay()

    def playingSurvival_draw(self):
        self.screen.fill(self.color)
        self.draw_text(f'TIME: {round(self.printTime, 2)}', self.screen, [4,0], 
        WINS_TEXT_SIZE, (44, 167, 198), START_FONT)
        spawn_height = HEIGHT
        while spawn_height >= 10:
            pygame.draw.rect(self.screen, WHITE, [WIDTH/2-5, spawn_height-15, 10, 10])
            spawn_height -= 20
        self.player.draw()
        self.ball.draw()
        self.ai.draw()
        self.walls.draw()

        if self.state == 'game over':
            self.draw_text('GAME OVER', self.screen, [WIDTH//2, HEIGHT-330], 
            PONG_TITLE_SIZE, RED, PONG_TEXT_FONT, centered=True)
            self.draw_text('PUSH SPACEBAR TO EXIT',self.screen, 
            [WIDTH//2, HEIGHT//2+50], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
            if self.printTime > self.survivalRecord:
                self.survivalRecord = self.printTime
        pygame.display.update()


######################## BALL RESPAWN FUNCTION ###########################################

    def respawnDelay(self):
            time_delay = pygame.time.get_ticks() + BALL_RESPAWN_DELAY
            if self.ball.pos[0] > WIDTH:
                self.ball.pos[0] -= WIDTH/2
                self.ball.pos[1] -= self.ball.pos[1]-HEIGHT/2
            elif self.ball.pos[0] < 0:
                self.ball.pos[0] += WIDTH/2
                self.ball.pos[1] -= self.ball.pos[1]-HEIGHT/2
            self.ball.vert_speed += -self.ball.vert_speed
            self.ball.horizontal_speed = 0
            while pygame.time.get_ticks() < time_delay:
                if self.survivalMode == 'OFF':
                    self.playingSolo_events()
                    self.playingSolo_update()
                    self.playingSolo_draw()
                else:
                    self.playingSolo_events()
                    self.playingSurvival_update()
                    self.playingSurvival_draw()
                    self.printTime = time.time() - self.t0
                self.clock.tick(FPS)
            self.delay = False
            self.ball.respawn()


######################## GAME OVER FUNCTIONS ###########################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: #Press spacebar and game starts
                self.reset()
    
    def reset(self):
        self.delay = False
        self.state = 'start'
        self.player.__init__(self, PLAYER_START_POS)
        self.ai.score = 0
        self.won = ''
        if self.ball.pos[0] >= WIDTH//2:
            self.ball.pos[0] -= self.ball.pos[0]-WIDTH//2
            self.ball.pos[1] -= self.ball.pos[1]-HEIGHT/2
        elif self.ball.pos[0] < WIDTH//2:
            self.ball.pos[0] += (WIDTH/2)-self.ball.pos[0]
            self.ball.pos[1] -= self.ball.pos[1]-HEIGHT/2
        self.ball.hidden = False
        self.ball.vert_speed += -self.ball.vert_speed
        self.ball.horizontal_speed = BALL_START_SPEED

######################### SETTINGS FUNCTIONS ###################################


    def settings_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False #If we click quit, exit program
            mouse = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clickCheck(mouse)

    def clickCheck(self, mouse):
        #Back button
        if 10 <= mouse[0] <= 10+WINS_TEXT_SIZE*4 and 5 <= mouse[1] <= 5+WINS_TEXT_SIZE:
                    self.state = 'start'
        #Scores to win
        if WIDTH//4 <= mouse[0] <= WIDTH//4+MEDIUM_TEXT_SIZE and 60 <= mouse[1] <= 60+MEDIUM_TEXT_SIZE:
                    self.winAmount = 5
        if WIDTH//2 <= mouse[0] <= WIDTH//2+MEDIUM_TEXT_SIZE and 60 <= mouse[1] <= 60+MEDIUM_TEXT_SIZE:
                    self.winAmount = 7
        if WIDTH-(WIDTH//4) <= mouse[0] <= WIDTH-(WIDTH//4)+MEDIUM_TEXT_SIZE*2 and 60 <= mouse[1] <= 60+MEDIUM_TEXT_SIZE:
                    self.winAmount = 10
        #Ball Start Speed
        if WIDTH//4-50 <= mouse[0] <= WIDTH//4-50+MEDIUM_TEXT_SIZE*4 and 220 <= mouse[1] <= 220+MEDIUM_TEXT_SIZE:
                    self.ball.change_start_speed(2)
        if WIDTH//2-60 <= mouse[0] <= WIDTH//2-60+MEDIUM_TEXT_SIZE*5 and 220 <= mouse[1] <= 220+MEDIUM_TEXT_SIZE:
                    self.ball.change_start_speed(4)
        if WIDTH-(WIDTH//4)-20 <= mouse[0] <= WIDTH-(WIDTH//4)-20+MEDIUM_TEXT_SIZE*4 and 220 <= mouse[1] <= 220+MEDIUM_TEXT_SIZE:
                    self.ball.change_start_speed(10)
        #Ball Colors
        if WIDTH//8 + 175-50 <= mouse[0] <= WIDTH//8 + 175-50+SMALL_TEXT_SIZE*5 and 347 <= mouse[1] <= 347+SMALL_TEXT_SIZE:
            if self.color != WHITE:
                self.ball.change_color(WHITE)
        if WIDTH//8 + 275-50 <= mouse[0] <= WIDTH//8 + 275-50+SMALL_TEXT_SIZE*3 and 347 <= mouse[1] <= 347+SMALL_TEXT_SIZE:
            if self.color != RED:
                self.ball.change_color(RED)
        if WIDTH//8 + 375-50 <= mouse[0] <= WIDTH//8 + 375-50+SMALL_TEXT_SIZE*4 and 347 <= mouse[1] <= 347+SMALL_TEXT_SIZE:
            if self.color != BLUE:
                self.ball.change_color(BLUE)
        if WIDTH//8 + 475-50 <= mouse[0] <= WIDTH//8 + 475-50+SMALL_TEXT_SIZE*5 and 347 <= mouse[1] <= 347+SMALL_TEXT_SIZE:
            if self.color != GREEN:
                self.ball.change_color(GREEN)
        #Paddle Colors
        if WIDTH//8 + 175-50 <= mouse[0] <= WIDTH//8 + 175-50+SMALL_TEXT_SIZE*5 and 397 <= mouse[1] <= 397+SMALL_TEXT_SIZE:
            if self.color != WHITE:
                self.player.change_color(WHITE)
                self.ai.change_color(WHITE)
        if WIDTH//8 + 275-50 <= mouse[0] <= WIDTH//8 + 275-50+SMALL_TEXT_SIZE*3 and 397 <= mouse[1] <= 397+SMALL_TEXT_SIZE:
            if self.color != RED:
                self.player.change_color(RED)
                self.ai.change_color(RED)
        if WIDTH//8 + 375-50 <= mouse[0] <= WIDTH//8 + 375-50+SMALL_TEXT_SIZE*4 and 397 <= mouse[1] <= 397+SMALL_TEXT_SIZE:
            if self.color != BLUE:
                self.player.change_color(BLUE)
                self.ai.change_color(BLUE)
        if WIDTH//8 + 475-50 <= mouse[0] <= WIDTH//8 + 475-50+SMALL_TEXT_SIZE*5 and 397 <= mouse[1] <= 397+SMALL_TEXT_SIZE:
            if self.color != GREEN:
                self.player.change_color(GREEN)
                self.ai.change_color(GREEN)
        #Background Colors
        if WIDTH//8 + 175-50 <= mouse[0] <= WIDTH//8 + 175-50+SMALL_TEXT_SIZE*5 and 447 <= mouse[1] <= 447+SMALL_TEXT_SIZE:
            if self.ball.color != WHITE and self.player.color != WHITE:
                self.color = WHITE
        if WIDTH//8 + 275-50 <= mouse[0] <= WIDTH//8 + 275-50+SMALL_TEXT_SIZE*3 and 447 <= mouse[1] <= 447+SMALL_TEXT_SIZE:
            if self.ball.color != RED and self.player.color != RED:
                self.color = RED
        if WIDTH//8 + 375-50 <= mouse[0] <= WIDTH//8 + 375-50+SMALL_TEXT_SIZE*4 and 447 <= mouse[1] <= 447+SMALL_TEXT_SIZE:
            if self.ball.color != BLUE and self.player.color != BLUE:
                self.color = BLUE
        if WIDTH//8 + 475-50 <= mouse[0] <= WIDTH//8 + 475-50+SMALL_TEXT_SIZE*5 and 447 <= mouse[1] <= 447+SMALL_TEXT_SIZE:
            if self.ball.color != GREEN and self.player.color != GREEN:
                self.color = GREEN
        if WIDTH//8 + 550-50 <= mouse[0] <= WIDTH//8 + 550-50+SMALL_TEXT_SIZE*5 and 447 <= mouse[1] <= 447+SMALL_TEXT_SIZE:
            self.color = BLACK
    

    def settings_update(self):
        pass
            

    def settings_draw(self):
        self.screen.fill(BLACK)
        self.draw_text(f'BACK', self.screen, [10,5], 
        WINS_TEXT_SIZE, (44, 167, 198), START_FONT)

        self.draw_text('SCORE TO WIN',self.screen, 
        [WIDTH//2, 20], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        scoreFlag = False
        if self.winAmount == 5:
            scoreFlag = True
        self.draw_text(f'5', self.screen, [WIDTH//4, 60], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT, rect=scoreFlag)
        scoreFlag = False
        if self.winAmount == 7:
            scoreFlag = True
        self.draw_text(f'7', self.screen, [WIDTH//2, 60], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT, rect=scoreFlag)
        scoreFlag = False
        if self.winAmount == 10:
            scoreFlag = True
        self.draw_text(f'10', self.screen, [WIDTH-(WIDTH//4), 60], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT, rect=scoreFlag)
        scoreFlag = False

        self.draw_text('BALL START SPEED',self.screen, 
        [WIDTH//2, 160], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        speedFlag = False
        if self.ball.horizontal_speed == 2:
            speedFlag = True
        self.draw_text(f'SLOW', self.screen, [WIDTH//4-50, 220], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT, rect = speedFlag)
        speedFlag = False
        if self.ball.horizontal_speed == 4:
            speedFlag = True
        self.draw_text(f'MEDIUM', self.screen, [WIDTH//2-60, 220], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT, rect=speedFlag)
        speedFlag = False
        if self.ball.horizontal_speed == 10:
            speedFlag = True
        self.draw_text(f'FAST', self.screen, [WIDTH-(WIDTH//4)-20, 220], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT, rect= speedFlag)
        speedFlag = False

        self.draw_text('COLOR SETTINGS',self.screen, 
        [WIDTH//2, 300], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)

        self.draw_text(f'BALL:', self.screen, [WIDTH//9-50, 340], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT)
        ballColorFlag = False
        if self.ball.color == WHITE:
            ballColorFlag = True
        self.draw_text(f'WHITE', self.screen, [WIDTH//8 + 175-50, 347], 
        SMALL_TEXT_SIZE, WHITE, START_FONT, rect=ballColorFlag)
        ballColorFlag = False
        if self.ball.color == RED:
            ballColorFlag = True
        self.draw_text(f'RED', self.screen, [WIDTH//8 + 275-50, 347], 
        SMALL_TEXT_SIZE, RED, START_FONT, rect=ballColorFlag)
        ballColorFlag = False
        if self.ball.color == BLUE:
            ballColorFlag = True
        self.draw_text(f'BLUE', self.screen, [WIDTH//8 + 375-50, 347], 
        SMALL_TEXT_SIZE, BLUE, START_FONT, rect=ballColorFlag)
        ballColorFlag = False
        if self.ball.color == GREEN:
            ballColorFlag = True
        self.draw_text(f'GREEN', self.screen, [WIDTH//8 + 475-50, 347], 
        SMALL_TEXT_SIZE, GREEN, START_FONT, rect=ballColorFlag)
        ballColorFlag = False

        self.draw_text(f'PADDLE:', self.screen, [WIDTH//9-50, 390], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT)
        paddleColorFlag = False
        if self.player.color == WHITE:
            paddleColorFlag = True
        self.draw_text(f'WHITE', self.screen, [WIDTH//8 + 175-50, 397], 
        SMALL_TEXT_SIZE, WHITE, START_FONT, rect= paddleColorFlag)
        paddleColorFlag = False
        if self.player.color == RED:
            paddleColorFlag = True
        self.draw_text(f'RED', self.screen, [WIDTH//8 + 275-50, 397], 
        SMALL_TEXT_SIZE, RED, START_FONT, rect= paddleColorFlag)
        paddleColorFlag = False
        if self.player.color == BLUE:
            paddleColorFlag = True
        self.draw_text(f'BLUE', self.screen, [WIDTH//8 + 375-50, 397], 
        SMALL_TEXT_SIZE, BLUE, START_FONT, rect= paddleColorFlag)
        paddleColorFlag = False
        if self.player.color == GREEN:
            paddleColorFlag = True
        self.draw_text(f'GREEN', self.screen, [WIDTH//8 + 475-50, 397], 
        SMALL_TEXT_SIZE, GREEN, START_FONT, rect= paddleColorFlag)
        paddleColorFlag = False

        self.draw_text(f'BACKGROUND:', self.screen, [WIDTH//9-50, 440], 
        MEDIUM_TEXT_SIZE, (44, 167, 198), START_FONT)
        backgroundColorFlag = False
        if self.color == WHITE:
            backgroundColorFlag = True
        self.draw_text(f'WHITE', self.screen, [WIDTH//8 + 175-50, 447], 
        SMALL_TEXT_SIZE, WHITE, START_FONT, rect= backgroundColorFlag)
        backgroundColorFlag = False
        if self.color == RED:
            backgroundColorFlag = True
        self.draw_text(f'RED', self.screen, [WIDTH//8 + 275-50, 447], 
        SMALL_TEXT_SIZE, RED, START_FONT, rect= backgroundColorFlag)
        backgroundColorFlag = False
        if self.color == BLUE:
            backgroundColorFlag = True
        self.draw_text(f'BLUE', self.screen, [WIDTH//8 + 375-50, 447], 
        SMALL_TEXT_SIZE, BLUE, START_FONT, rect= backgroundColorFlag)
        backgroundColorFlag = False
        if self.color == GREEN:
            backgroundColorFlag = True
        self.draw_text(f'GREEN', self.screen, [WIDTH//8 + 475-50, 447], 
        SMALL_TEXT_SIZE, GREEN, START_FONT, rect= backgroundColorFlag)
        backgroundColorFlag = False
        if self.color == BLACK:
            backgroundColorFlag = True
        self.draw_text(f'BLACK', self.screen, [WIDTH//8 + 550-50, 447], 
        SMALL_TEXT_SIZE, GRAY, START_FONT, rect= backgroundColorFlag)
        backgroundColorFlag = False

        pygame.display.update()

        