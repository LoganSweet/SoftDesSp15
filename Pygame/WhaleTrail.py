"""Whale Trail """

import pygame
import random
import time
import numpy as np
import cv2, sys

cap = cv2.VideoCapture(0)
def take_snapshot(delay=2):
    cap.set(3, 420) 
    cap.set(4, 420)
    take_picture = False;
    t0, filenum = 0, 1

while True:
    val, frame = cap.read()
    cv2.imshow("video", frame)          
    key = cv2.waitKey(30)
    cv2.imwrite(str('you') + ".jpg", frame)         # saves the photo as you.jpg
    break
    take_snapshot()                                 # takes a still image 

class DrawableSurface():
    """ A class that wraps a pygame.Surface and a pygame.Rect """
    def __init__(self, surface, rect):
        """ Initializes the drawable surface """
        self.surface = surface
        self.rect = rect

class Whale(object):
    """ the state of the whale player in the game"""
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = 75                             # sets the speed of scrolling
        self.vel_y = 0                              # initially isn't moving up & down
        self.image = pygame.image.load('whale.png')  # loads image of whale
        
    def get_bound(self):
        return self.get_drawables()[0].rect        

    def get_drawables(self):                        # fits the image to the game window size
        w,h = self.image.get_size()           
        return [DrawableSurface(self.image, self.image.get_rect().move(self.pos_x, self.pos_y))]

    def update(self,delta_t): 
        """ Determines position of the whale """

        self.pos_x += self.vel_x*delta_t             # x moves at constant velocity
        self.pos_y += self.vel_y*delta_t             # position increases faster when velocity is higher
        self.vel_y += delta_t*200                    # gravity

    #whale "flops" to go up 
    def flop(self): 
        self.vel_y -= 100

class EvilCloud():
    """ this class defines the obstacles that the whale cna hit """
    def __init__(self, pos_x, screen_height):
        self.pos_x = pos_x                                                          # starts at pos x 
        self.pos_y_bottom = random.randint(100, screen_height-100)
        self.pos_y_top = self.pos_y_bottom - 500                                    # determines the opening size of the clouds
        self.screen_height = screen_height 
        self.cloud1 = pygame.image.load('cloud1.png')
        self.cloud2 = pygame.image.load('cloud2.png')
        w,h = self.cloud1.get_size()
        self.cloud1 = pygame.transform.scale(self.cloud1, (int(w*0.5),int(h*0.5)))  # rescales images
        w,h = self.cloud2.get_size()
        self.cloud2 = pygame.transform.scale(self.cloud2, (int(w*0.5),int(h*0.5)))  # flips the clouds to be symmestrical ove the x axis
        self.cloud1_flipped = pygame.transform.flip(self.cloud1, False, True)

    def get_drawables(self):
        """ Get the drawables that constitute a cloud obstacle """
        drawables = []
        r = pygame.Rect(self.pos_x,                                                 # Creates the cloud obstacles
                        self.pos_y_bottom,
                        self.cloud1.get_rect().width,
                        self.cloud1.get_rect().height)
        drawables.append(DrawableSurface(self.cloud1,r))
        r = r.move(0,self.cloud1.get_rect().height)                                 # move the clouds down to create the thing we are drawing
        while r.top <= self.screen_height:
            drawables.append(DrawableSurface(self.cloud2,r))                        # add the top cloud
            r = r.move(0,self.cloud2.get_rect().height)
        r = pygame.Rect(self.pos_x,
                        self.pos_y_top,
                        self.cloud1_flipped.get_rect().width,
                        self.cloud1_flipped.get_rect().height)
        drawables.append(DrawableSurface(self.cloud1_flipped,r))

        while r.top > -self.cloud2.get_rect().height:
            r = r.move(0,-self.cloud2.get_rect().height)
            drawables.append(DrawableSurface(self.cloud2,r))
        return drawables

    def collided_with(self, entity_rect):                                           # determines if the whale has collided with anything
        """ Returns true if and only if the input rectangle entity_rect
            has collided with the obstacle """
        drawables = self.get_drawables()
        rectangles = []
        for d in drawables:
            rectangles.append(d.rect)
        return entity_rect.collidelist(rectangles) != -1

class WhaleView():
    """ The view of the Whale Trail"""
    def __init__(self, model, width, height):
        """ Initialize the view for Whale Trail.  The input model
            is necessary to find the position of relevant objects to draw. """
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))                      # to retrieve width and height use screen.get_size()
        self.screen_boundaries = pygame.Rect(0 ,0, width, height)                   # screen boundaries
        self.model = model

        self.image = pygame.image.load('you.jpg')                                   # loads captured image from suprise webcam shot
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(2.4*w), int(1.8*h)))   # scales captured image to game window size 

    def draw(self):
        """ Redraw the full game window """
        self.screen.blit(self.image, (0,0))                                          # sets surprise image to background image
        self.drawables = self.model.get_drawables()                                  # get the new drawables
        screen_position = self.screen_boundaries.move(self.model.whale.pos_x,0)      # move the screen boundaries to coincide with the player's x coordinate
        for d in self.drawables:
            """ the coordinates of the drawables are defined relative to an origin
                placed in the upper left corner of the beginning of the level.  In
                order to render them within the current screen boundaries, we need
                to shift them over based on the screen's position. """
            rect = d.rect.move(-screen_position.x, -screen_position.y)                # 
            self.screen.blit(d.surface, rect)
        pygame.display.update()

class WhaleTrailController():
    def __init__(self, model):
        self.model = model
        self.space_pressed = False

    def process_events(self):
        """ process keyboard events.  This must be called periodically
            in order for the controller to have any effect on the game """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print event.key
                if event.key == 32:
                    self.model.whale.flop()

class WhaleModel(object):
    """ Represents the game state of our Whale Trail clone """
    
    def __init__(self, width, height):
        """ Initialize the flappy model """
        self.width = width
        self.height = height
        self.whale = Whale(0,250)   # initial position of whale   
        self.obstacles = []
        for i in range (100): 
            self.obstacles.append(EvilCloud((i+1)*500, height))

    def get_drawables(self):
        """ Return a list of DrawableSurfaces for the model """
        drawables = self.whale.get_drawables()
        for obstacle in self.obstacles:
            drawables += obstacle.get_drawables()
        return drawables

    def is_dead(self):
        """ Return True if the player is dead (for instance) the player
            has collided with an obstacle, and false otherwise """
        #TODO: modify this if the player becomes more complicated
        player_rect = self.whale.get_bound()

        for obstacle in self.obstacles:
            #if the whale hits an obstacle, it dies
            if obstacle.collided_with(player_rect):
                return True
        return False
 
    def update(self, delta_t):                              
        """ Updates the model and its constituent parts """
        self.whale.update(delta_t)

class WhaleTrail():
    """ The main Whale class that allows the game to run using all classes """
    def __init__(self):
        """ Initialize the whale trail game.  Use Whale.run to
            start the game """ 
        #determines game window size
        self.model = WhaleModel(1600, 900)
        self.view = WhaleView(self.model, 1600, 900)
        self.controller = WhaleTrailController(self.model)

    def run(self):
        """ the main loop: loops until the whale dies """
        #captures beginning time
        last_update_time = time.time()

        while not(self.model.is_dead()):
            # redraw the level
            self.view.draw()
            # check for key presses
            self.controller.process_events()
            # compute delta_t so we know how much to update various
            # positions in in the model.update function.
            delta_t = time.time() - last_update_time
            # update the model (basically runs the physics of the game)
            self.model.update(delta_t)
            # store the last update time so we can calculate the next delta_t
            last_update_time = time.time()

if __name__ == '__main__':
    trail = WhaleTrail()
    trail.run()