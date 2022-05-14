from email.mime import base
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
        self.ball_size = BALL_SIZE
        self.ai.giveBall(self.ball)

        self.delay = False
        self.won = ''
        self.playerWins = 0

        self.winAmount = WIN_AMOUNT
        self.color = BLACK

        self.survivalMode = 'OFF'
        self.t0 = 0
        self.printTime = 0
        self.survivalRecord = 0.0

        self.draw_error = False

    def run(self):
        first = True
        while self.running:
            if self.state == 'start':
                first = True
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
            elif self.state == 'playing Chaos':
                self.playing_chaos_settings_draw()
                settings = self.playing_chaos_settings_events()
            elif self.state == 'playing Chaos Game':
                if first:
                    balls = self.create_balls(settings[0])
                    first = False
                    self.winAmount = int(settings[1])
                    self.color = (20,130,210)
                self.playingChaos_events()
                self.playingChaos_update(balls)
                self.playingChaos_draw(balls)
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
                if WIDTH//2-50 <= mouse[0] <= WIDTH//2+50 and HEIGHT//2+180 <= mouse[1] <= HEIGHT//2+205:
                    self.state = 'playing Chaos'
    
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
        pygame.draw.rect(self.screen, RED, (WIDTH//2-50, HEIGHT//2+180,100,25))
        self.draw_text('CHAOS', self.screen, [WIDTH//2, HEIGHT//2+195], 
        SETTINGS_TEXT_SIZE, WHITE, PONG_TEXT_FONT, centered=True)

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
        if self.color != WHITE:
            dashes = WHITE
        else:
            dashes = GRAY
        while spawn_height >= 10:
            pygame.draw.rect(self.screen, dashes, [WIDTH/2-5, spawn_height-15, 10, 10])
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
        if self.player.score >= self.winAmount:
            self.state = 'game over'
            return 'player'
        elif self.ai.score >= self.winAmount:
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
        if self.color != WHITE:
            dashes = WHITE
        else:
            dashes = GRAY
        while spawn_height >= 10:
            pygame.draw.rect(self.screen, dashes, [WIDTH/2-5, spawn_height-15, 10, 10])
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

######################## PLAYING CHAOS SETTINGS FUNCTIONS #########################################

    def playing_chaos_settings_events(self):

        base_font = pygame.font.Font(None, 32)
        waiting = True
        color_active = pygame.Color('lightskyblue3')
        color_passive = pygame.Color('gray15')

        user_text_balls = ''
        active_balls = False
        input_rect_balls = pygame.Rect(WIDTH//4+150, HEIGHT//3-16, 140, 32)
        color_balls = color_passive

        user_text_winScore = ''
        active_winScore = False
        input_rect_winScore = pygame.Rect(WIDTH//4+150, HEIGHT-HEIGHT//3-16, 140, 32)
        color_winScore = color_passive

        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() #If we click quit, exit program
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect_balls.collidepoint(event.pos):
                        active_balls = True
                    else:
                        active_balls = False
                    if input_rect_winScore.collidepoint(event.pos):
                        active_winScore = True
                    else:
                        active_winScore = False
                    mouse = pygame.mouse.get_pos()
                    if (WIDTH//2-10)-MEDIUM_TEXT_SIZE*2.5 <= mouse[0] <= (WIDTH//2-10)+MEDIUM_TEXT_SIZE*2.5 and HEIGHT//2-MEDIUM_TEXT_SIZE <= mouse[1] <= HEIGHT//2+MEDIUM_TEXT_SIZE:
                        self.ball_size = 10
                    if (WIDTH-WIDTH//3)-MEDIUM_TEXT_SIZE*1.5 <= mouse[0] <= (WIDTH-WIDTH//3)+MEDIUM_TEXT_SIZE*1.5 and HEIGHT//2-MEDIUM_TEXT_SIZE <= mouse[1] <= HEIGHT//2+MEDIUM_TEXT_SIZE:
                        self.ball_size = 25
                    if (WIDTH-WIDTH//6)-MEDIUM_TEXT_SIZE*2.5 <= mouse[0] <= (WIDTH-WIDTH//6)+MEDIUM_TEXT_SIZE*2.5 and HEIGHT//2-MEDIUM_TEXT_SIZE <= mouse[1] <= HEIGHT//2+MEDIUM_TEXT_SIZE:
                        self.ball_size = 50
                    
  
                if event.type == pygame.KEYDOWN:
                    if active_balls == True:
                        # Check for backspace
                        if event.key == pygame.K_BACKSPACE:
                            # get text input from 0 to -1 i.e. end.
                            user_text_balls = user_text_balls[:-1]
                        # Unicode standard is used for string
                        # formation
                        else:
                            user_text_balls += event.unicode

                    if active_winScore == True:
                        if event.key == pygame.K_BACKSPACE:
                            user_text_winScore = user_text_winScore[:-1]
                        else:
                            user_text_winScore += event.unicode

            self.screen.fill((0,0,0))

            if active_balls:
                color_balls = color_active
            else:
                color_balls = color_passive
            if active_winScore:
                color_winScore = color_active
            else:
                color_winScore = color_passive
            
            pygame.draw.rect(self.screen, color_balls, input_rect_balls, 2)
            text_surface = base_font.render(user_text_balls, True, (255, 255, 255))
            self.screen.blit(text_surface, (input_rect_balls.x+5, input_rect_balls.y+5))
            input_rect_balls.w = max(100, text_surface.get_width()+10)

            pygame.draw.rect(self.screen, color_winScore, input_rect_winScore, 2)
            text_surface = base_font.render(user_text_winScore, True, (255, 255, 255))
            self.screen.blit(text_surface, (input_rect_winScore.x+5, input_rect_winScore.y+5))
            input_rect_winScore.w = max(100, text_surface.get_width()+10)

            self.playing_chaos_settings_update()
            waiting = self.playing_chaos_settings_draw(user_text_balls, user_text_winScore)

            # self.clock.tick(FPS)

        if self.state == 'playing Chaos Game':
            return (user_text_balls, user_text_winScore)


    def playing_chaos_settings_update(self):
        pass

    def playing_chaos_settings_draw(self, numBalls=0, scoreVal=0):
        if self.draw_error:
            self.draw_text('Number of Balls and Win Score must be a valid number greater than 0', self.screen, [WIDTH//2, HEIGHT-35], 
            MEDIUM_TEXT_SIZE, RED, PONG_TEXT_FONT, centered=True)
        
        self.draw_text('CHAOS', self.screen, [WIDTH//2, HEIGHT//3//2-10], 
            PONG_TITLE_SIZE, RED, VIDEO_GAME_FONT, centered=True)
        self.draw_text('NUMBER OF BALLS:', self.screen, [WIDTH//4, HEIGHT//3], 
            LARGE_TEXT_SIZE, BLUE, SETTINGS_TEXT_FONT, centered=True)
        self.draw_text('BALL SIZE:', self.screen, [WIDTH//4, HEIGHT//2],
            LARGE_TEXT_SIZE, BLUE, SETTINGS_TEXT_FONT, centered=True)
        self.draw_text('Score To Win:', self.screen, [WIDTH//4, HEIGHT-HEIGHT//3],
            LARGE_TEXT_SIZE, BLUE, SETTINGS_TEXT_FONT, centered=True)
        
        small, med, large = False, False, False
        if self.ball_size == 10:
            small = True
        elif self.ball_size == 25:
            med = True
        else:
            large = True
        self.draw_text(f'SMALL', self.screen, [WIDTH//2-10, HEIGHT//2], 
        MEDIUM_TEXT_SIZE, WHITE, START_FONT, centered=True, rect = small)
        self.draw_text(f'MED', self.screen, [WIDTH-WIDTH//3, HEIGHT//2], 
        MEDIUM_TEXT_SIZE, WHITE, START_FONT, centered=True, rect=med)
        self.draw_text(f'LARGE', self.screen, [WIDTH-WIDTH//6, HEIGHT//2], 
        MEDIUM_TEXT_SIZE, WHITE, START_FONT, centered=True, rect=large)

        start_rect = pygame.Rect(WIDTH//2-70, HEIGHT-HEIGHT//5, 140, 32)
        pygame.draw.rect(self.screen, GREEN, start_rect, 0)
        base_font = pygame.font.Font(None, 32)
        user_text_balls = 'START'
        text_surface = base_font.render(user_text_balls, True, WHITE)
        self.screen.blit(text_surface, (start_rect.center[0]-35, start_rect.center[1]-8))

        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        try:
                            numBalls = int(numBalls)
                            scoreVal = int(scoreVal)
                        except:
                            numBalls, scoreVal = -1, -1
                        if numBalls <= 0 or scoreVal <= 0:
                            self.draw_error = True
                        else:
                            self.state = 'playing Chaos Game'
                            return False
        
        pygame.display.update()
        return True

######################## PLAYING CHAOS FUNCTIONS #########################################

    def playingChaos_events(self):
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

    def playingChaos_update(self, balls):
        self.player.update()

        for ball in balls:
            ball.update()
            if pygame.Rect.colliderect(ball.hitbox, self.player.hitbox):
                ball.reflect('player', self.player)
            elif pygame.Rect.colliderect(ball.hitbox, self.ai.hitbox):
                ball.reflect('player', self.ai)
            elif pygame.Rect.colliderect(ball.hitbox, self.walls.hitboxVert[0]) or pygame.Rect.colliderect(ball.hitbox, self.walls.hitboxVert[1]):
                ball.reflect('wall', self.walls)
    
            self.delay = ball.scoreCheck()
            if self.delay[0] == True:
                self.incrementScore(self.delay[1])
                self.won = self.winCheck()
                if self.won == '':
                    ball.respawn()
            ball.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        colors = [random.randint(1, 9) * random.randrange(-1, 2, 2), random.randint(1, 9) * random.randrange(-1, 2, 2), random.randint(1, 9) * random.randrange(-1, 2, 2)]
        for i in range(3):
            if self.color[i]+colors[i] >= 255:
                colors[i] *= -1
            if self.color[i]+colors[i] <= 0:
                colors[i] *= - 1
        self.color = (self.color[0]+colors[0], self.color[1]+colors[1], self.color[2]+colors[2])
        self.ai.update()


    def playingChaos_draw(self, balls):
        self.screen.fill(self.color)
        spawn_height = HEIGHT
        if self.color != WHITE:
            dashes = WHITE
        else:
            dashes = GRAY
        while spawn_height >= 10:
            pygame.draw.rect(self.screen, dashes, [WIDTH/2-5, spawn_height-15, 10, 10])
            spawn_height -= 20
        self.player.draw()
        for ball in balls:
            ball.draw()
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

######################## BALLS ######################################################

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
    
    def create_balls(self, num):
        balls = []
        for i in range(int(num)):
            balls.append(Ball(self))

            balls[i].pos = [random.randint(WIDTH//6, WIDTH-WIDTH//6), random.randint(20, HEIGHT-20)]
            balls[i].dir_horizontal = random.randrange(-1, 2, 2)
            balls[i].hitbox = pygame.Rect(balls[i].pos[0]-balls[i].size, balls[i].pos[1]-balls[i].size, balls[i].size*2, balls[i].size*2)
            balls[i].size = self.ball_size
            balls[i].horizontal_speed = random.randint(2, 10)
            balls[i].speedSave = balls[i].horizontal_speed

            self.ai.giveBall(balls[i])
        return balls


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
        oldColor = self.player.color
        self.player.__init__(self, PLAYER_START_POS)
        self.player.color = oldColor
        self.ai.score = 0
        self.ai.ballPos = [self.ball]
        self.won = ''
        # self.winAmount = WIN_AMOUNT
        if self.ball.pos[0] >= WIDTH//2:
            self.ball.pos[0] -= self.ball.pos[0]-WIDTH//2
            self.ball.pos[1] -= self.ball.pos[1]-HEIGHT/2
        elif self.ball.pos[0] < WIDTH//2:
            self.ball.pos[0] += (WIDTH/2)-self.ball.pos[0]
            self.ball.pos[1] -= self.ball.pos[1]-HEIGHT/2
        self.ball.hidden = False
        self.ball.vert_speed += -self.ball.vert_speed
        self.ball.horizontal_speed = self.ball.speedSave

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

        