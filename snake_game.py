import pygame
from pygame.locals import *
import time
import random

size = 40

# This class has all functions related to Apple
class Apple:
    
    # Initialization of 'Apple' 
    def __init__(self,back_screen):
        self.back_screen = back_screen
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x = size*3
        self.y = size*3
    
    # To make apple appear on screen at specific coordinates
    def draw(self):
        self.back_screen.blit(self.apple,(self.x,self.y))
        pygame.display.flip()  

    # To move the apple after it has been consumed
    def move(self):
        self.x = random.randint(0,15)*size
        self.y = random.randint(0,15)*size  

# This class has all function related to Snake
class Snake:
    
    # Initialization of 'Snake'
    def __init__(self,back_screen,length):
        self.length = length
        self.back_screen = back_screen
        self.block = pygame.image.load("resources/pixel.png").convert()
        self.x = [size]*length
        self.y = [size]*length
        self.direction = 'right'
    
    # Increases the length of the snake after each apple is consumed
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    # Used for replication of snake ,i.e., addition of blocks of snake
    def draw(self):
        for i in range(self.length):
            self.back_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()
    
    # The next 4 functions are responsible for all direction changes
    def left(self):
        self.direction = 'left'
    
    def right(self):
        self.direction = 'right'
    
    def up(self):
        self.direction = 'up'

    def down(self):
        self.direction = 'down'
    
    # Movement function for blocks following the first block 
    def move(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size
        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size
        self.draw()

# This is the main class responsible for the functioning of the game
class Game:
    
    # Initialization of 'Game' 
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000,700))
        pygame.mixer.init()
        self.play_background_music()
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
    
    # Detects whether snake has collided with the apple
    def check_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
    
    # Plays background music during the game
    def play_background_music(self):
        pygame.mixer.music.load("resources/forest_sounds.mp3")
        pygame.mixer.music.play()

    # Renders the background for the game
    def render_background(self):
        bg = pygame.image.load("resources/forestbg.jpg")
        self.surface.blit(bg,(0,0))

    # It is the main game function
    def play(self):
        self.render_background()
        self.snake.move()
        self.apple.draw()
        self.show_current_score()
        pygame.display.flip()
    


        if self.check_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.apple.move()
            self.snake.increase_length()
        
        for i in range(3,self.snake.length):
            if self.check_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                sound = pygame.mixer.Sound("resources/sheep_baaing.mp3")
                pygame.mixer.Sound.play(sound)
                raise "Game Over"

    # Displays the score in-game
    def show_current_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(850,10)) 
    
    # Responsible for showing the game over message
    def game_over(self):
        self.render_background()
        
        font = pygame.font.SysFont('impact', 30)
        line1 = font.render("OOPS! You blew it, NOOB!", True, (255, 106, 0))
        self.surface.blit(line1, (100, 200))
        line = font.render(f"SCORE : {self.snake.length}", True, (247, 0, 16))
        self.surface.blit(line, (100, 300))
        line2 = font.render("Press ESC to exit the game!", True, (255, 106, 0))
        self.surface.blit(line2, (100, 350))     
        pygame.display.flip() 
        
        pygame.mixer.music.pause()
    
    # Main run function of the whole game
    def run_game(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    
                    if not pause:
                        if event.type == K_RETURN:
                            self.reset()
                        if event.key == K_UP:
                            self.snake.up()
                        
                        if event.key == K_DOWN:
                            self.snake.down()
                        
                        if event.key == K_LEFT:
                            self.snake.left()
                        
                        if event.key == K_RIGHT:
                            self.snake.right()

                elif event.type == QUIT:
                    running = False
        
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                pause = True

            time.sleep(0.2)

if __name__=="__main__":
    game = Game()
    game.run_game()