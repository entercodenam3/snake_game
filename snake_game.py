
import pygame
from pygame.locals import *
import time
import random

size = 40

class Apple:
    
    def __init__(self,back_screen):
        self.back_screen = back_screen
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x = size*3
        self.y = size*3
    
    def draw(self):
        self.back_screen.blit(self.apple,(self.x,self.y))
        pygame.display.flip()  

    def move(self):
        self.x = random.randint(0,15)*size
        self.y = random.randint(0,15)*size  


class Snake:
    
    def __init__(self,back_screen,length):
        self.length = length
        self.back_screen = back_screen
        self.block = pygame.image.load("resources/pixel.png").convert()
        self.x = [size]*length
        self.y = [size]*length
        self.direction = 'right'
    
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    
    def draw(self):
        for i in range(self.length):
            self.back_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()
    
    def move_left(self):
        self.direction = 'left'
    
    def move_right(self):
        self.direction = 'right'
    
    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'
    
    def walk(self):

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


class Game:
    
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000,700))
        pygame.mixer.init()
        self.play_background_music()
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)

    
    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
    
    def play_background_music(self):
        pygame.mixer.music.load("resources/forest_sounds.mp3")
        pygame.mixer.music.play()

    def render_background(self):
        bg = pygame.image.load("resources/forestbg.jpg")
        self.surface.blit(bg,(0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()


        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            sound = pygame.mixer.Sound("resources/ding.mp3")
            pygame.mixer.Sound.play(sound)
            self.apple.move()
            self.snake.increase_length()
        
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                sound = pygame.mixer.Sound("resources/sheep_baaing.mp3")
                pygame.mixer.Sound.play(sound)
                raise "Game Over"

    
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(850,10)) 
    
    
    def show_game_over(self):
        self.render_background()
        
        font = pygame.font.SysFont('impact', 30)
        line1 = font.render("OOPS! You blew it, NOOB!", True, (255, 106, 0))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"Your score is {self.snake.length}", True, (247, 0, 16))
        self.surface.blit(line2, (210, 350))
        line3 = font.render("Press ENTER to play again. To exit press Escape!", True, (255, 106, 0))
        self.surface.blit(line3, (200, 400))     
        pygame.display.flip() 
        
        pygame.mixer.music.pause()
    
 
    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    
                    if not pause:
                        
                        if event.key == K_UP:
                            self.snake.move_up()
                        
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
        
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)
 


if __name__=="__main__":
    game = Game()
    game.run()




