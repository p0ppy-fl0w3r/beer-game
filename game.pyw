import sys
import random

import pygame


class Sprite:
    def __init__(self,image,game):
        self.image = image
        self.game = game
        self.position = [0,0]
        self.reset()

    def update(self):
        pass

    def draw(self):
        '''
        Draws the sprite on its current
        position
        '''
        self.game.surface.blit(self.image,self.position)

    def reset(self):
        pass

    def intersects_with(self,target):
        max_x = self.position[0]+self.image.get_width()-20
        max_y = self.position[1]+self.image.get_height()-20

        target_x = target.position[0]+target.image.get_width()-20
        target_y = target.position[1]+target.image.get_height()-20

        if max_x < target.position[0]:
            #The sprite is on the left and doesn't intersect
            return False
        if max_y < target.position[1]:
            #Down and doesn't intersect
            return False
        if self.position[0] > target_x:
            #Right
            return False
        if self.position[1] > target_y:
            #Up
            return False
        #The sprite intersects if we get here
        return True

class Male(Sprite):

    def reset(self):
        #Center the male on every reset
        self.position[0] = (self.game.width - self.image.get_width())/2
        self.position[1] = (self.game.height - self.image.get_height())/2
        #Make sure the male isn't moving
        self.movingUP = False
        self.movingDOWN = False
        self.movingLEFT = False
        self.movingRIGHT = False
        #set the speed of movement(move x and move y)
        self.speed = [5,5]

    def update(self):
        if self.movingUP:
            self.position[1] = self.position[1] - self.speed[0]
        if self.movingDOWN:
            self.position[1] = self.position[1] + self.speed[0]
        if self.movingLEFT:
            self.position[0] = self.position[0] - self.speed[1]
        if self.movingRIGHT:
            self.position[0] = self.position[0] + self.speed[1]


        #Clamp the man into the screen
        #Prevent the man from falling up or left
        if self.position[0] < 0:
            self.position[0] = 0
        if self.position[1] < 0:
            self.position[1] = 0
        #Prevent the man from falling down or right
        if self.position[0]+self.image.get_width() > self.game.width:
            self.position[0] = self.game.width - self.image.get_width()
        if self.position[1]+self.image.get_height() > self.game.height:
            self.position[1] = self.game.height - self.image.get_height()

    def startMovingUP(self):
        self.movingUP = True

    def stopMovingUP(self):
        self.movingUP = False

    def startMovingDOWN(self):
        self.movingDOWN = True
        
    def stopMovingDOWN(self):
        self.movingDOWN = False

    def startMovingLEFT(self):
        self.movingLEFT = True

    def stopMovingLEFT(self):
        self.movingLEFT = False

    def startMovingRIGHT(self):
        self.movingRIGHT = True

    def stopMovingRIGHT(self):
        self.movingRIGHT = False

class Beer(Sprite):

    def __init__(self,image,game,captured_sound):
        super().__init__(image,game)
        self.captured_sound = captured_sound
    
    def reset(self):
        self.position[0] = random.randint(0,self.game.width - self.image.get_width())
        self.position[1] = random.randint(0,self.game.height - self.image.get_height())

    def update(self):
        if self.intersects_with(game.male_sprite):
            self.captured_sound.play()
            self.reset()
            self.game.score += 1

class Female(Sprite):
    def __init__(self, image, game, entry_delay):
        super().__init__(image, game)
        self.entry_delay = entry_delay

    def update(self):

        self.entry_count = self.entry_count + 1
        if self.entry_count < self.entry_delay:
            return

        if game.male_sprite.position[0] > self.position[0]:
            self.x_speed =  self.x_speed + self.x_accel
        else:
            self.x_speed =  self.x_speed - self.x_accel
        self.x_speed = self.x_speed * self.friction_value
        self.position[0] = self.position[0] + self.x_speed

        
        if game.male_sprite.position[1] > self.position[1]:
            self.y_speed =  self.y_speed + self.y_accel
        else:
            self.y_speed =  self.y_speed - self.y_accel
        self.y_speed = self.y_speed * self.friction_value
        self.position[1] = self.position[1] + self.y_speed

        if self.intersects_with(game.male_sprite):
            game.end_game()

        
    def reset(self):
        self.entry_count = 0
        self.friction_value = 0.99
        self.x_accel = 0.2
        self.y_accel = 0.2
        self.x_speed = 0
        self.y_speed = 0
        self.position = [-100,-100]

class BeerGame:

    def display_message(self,message,y_pos,color,font):
        shadow = font.render(message, True, (0,0,0))
        text = font.render(message, True, color)
        text_position = [self.width/2 - text.get_width()/2, y_pos]
        self.surface.blit(shadow, text_position)
        text_position[0] += 2
        text_position[1] += 2
        self.surface.blit(text, text_position)

    def draw_game(self):
        for sprite in self.sprites:
            sprite.draw()
        status = 'Score: ' + str(game.score)
        self.display_message(status, 0,(227, 193, 79),self.font)

    def start_game(self):
        for sprite in self.sprites:
            sprite.reset()
        self.game_running = True
        self.score=0

    def end_game(self):
        self.game_running = False
        if self.score > self.top_score:
            self.top_score = self.score

    def update_start(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif e.key == pygame.K_g:
                    self.start_game()

    def update_game(self):
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif e.key == pygame.K_UP:
                    self.male_sprite.startMovingUP()
                elif e.key == pygame.K_DOWN:
                    self.male_sprite.startMovingDOWN()
                elif e.key == pygame.K_LEFT:
                    self.male_sprite.startMovingLEFT()
                elif e.key == pygame.K_RIGHT:
                    self.male_sprite.startMovingRIGHT()
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_UP:
                    self.male_sprite.stopMovingUP()
                elif e.key == pygame.K_DOWN:
                    self.male_sprite.stopMovingDOWN()
                if e.key == pygame.K_LEFT:
                    self.male_sprite.stopMovingLEFT()
                elif e.key == pygame.K_RIGHT:
                    self.male_sprite.stopMovingRIGHT()
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for sprite in self.sprites:
            sprite.update()
        
        
    def draw_start(self):
        color = (227, 193, 79)
        r_up = pygame.font.Font('ROUNDAP.otf',60)
        self.start_background_sprite.draw()
        self.display_message(message='Top Score: ' + str(self.top_score),y_pos=0,color=color,font = self.font)
        self.display_message(message='Welcome to Beer Game', y_pos=150,color=(100,100,100),font = r_up)
        self.display_message(message='Steer the male to', y_pos=250,color=color,font = self.font)
        self.display_message(message='drink some beer', y_pos=300,color=color,font = self.font)
        self.display_message(message='BEWARE OF THE WIFE!!', y_pos=350,color=color,font = self.font)
        self.display_message(message='Arrow keys to move', y_pos=450,color=color,font = self.font)
        self.display_message(message='Press G to play', y_pos=500,color=color,font = self.font)
        self.display_message(message='Press Escape to exit', y_pos=550,color=color,font = self.font)

    def play_game(self):

        if pygame.init()[1] != 0:
            print('pygame not installed properly.')
            return

        self.width = 800
        self.height = 600
        self.size = (self.width,self.height)

        self.font = pygame.font.Font('BebasNeue-Regular.ttf', 45)

        start_background_image = pygame.image.load('start_background.jpg')
        self.start_background_sprite = Sprite(image=start_background_image,
                                              game=self)

        self.surface = pygame.display.set_mode(self.size)
        self.background_img = pygame.image.load('background.jpg')
        self.male_img = pygame.image.load('male.gif')
        self.beer_img = pygame.image.load('beer.png')
        self.burp_sound = pygame.mixer.Sound('burp.wav')
        self.female_img = pygame.image.load('female.png')

        self.background_sprite = Sprite(self.background_img,self)
        self.male_sprite = Male(self.male_img,self)
        self.sprites = []

        self.sprites.append(self.background_sprite)
        
        for _ in range(20):
            beer_sprite = Beer(self.beer_img,self,self.burp_sound)
            self.sprites.append(beer_sprite)
        

        self.sprites.append(self.male_sprite)

        
        for entry_delay in range(0,3000,300):
            female_sprite = Female(image=self.female_img,
                                        game=self,
                                        entry_delay=entry_delay )
            self.sprites.append(female_sprite)


        clock = pygame.time.Clock()

        self.score = 0
        self.top_score = 0
        self.end_game()

        self.game_active = True

        while self.game_active:
            clock.tick(60)
            if self.game_running:
                self.update_game()
                self.draw_game()
            else:
                self.update_start()
                self.draw_start()
            pygame.display.flip()


game = BeerGame()
game.play_game()