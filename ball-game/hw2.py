import pygame
import sys
import random

min_value = 300 # min value to stop
# arranging random seed
random_seed_param = random.randint(150,300) # randomizing the seed to randomizing the initial position of the balls
random.seed(random_seed_param)


# this class is storing ball speed, screen and some functionalities
class Ball:
    def __init__(self, ball_direction, screen) -> None:
        self.ball_direction = ball_direction # direction of movement
        self.screen = screen
        self.ball_img = pygame.image.load(self.screen.image) # loading the ball image into pygame
        self.ball_rect = self.get_ball_rect()

    # this gets ball's rect 
    def get_ball_rect(self):
        # initial position of the ball image in the screen
        pos = [random.random() * self.screen.width * 0.5, random.random() * self.screen.height * 0.5]
        scale = random.randrange(-30, 30) 
        ball_rect = self.ball_img.get_rect().inflate(scale, scale) # arrange size of the ball randomly
        ball_rect = pygame.Rect(pos[0], pos[1], ball_rect.width, ball_rect.height) # arranging position with ball's fields
        return ball_rect

    # this gets ball's image with respect to ball's rect
    def get_ball_image(self):
        ball_img = pygame.transform.scale(self.ball_img, (self.ball_rect.width, self.ball_rect.height))
        return ball_img

    # this functions updates the balls direction when it bounces from edge
    def update(self):
        # moving the ball in x,y direction 
        self.ball_rect = self.ball_rect.move([self.ball_direction[0], self.ball_direction[1]])

        # Check if the ball is at the top or bottom of the screen
        if self.ball_rect.top <= 0 or self.ball_rect.bottom >= self.screen.height:
            self.ball_direction[1] = -self.ball_direction[1] #change y direction of ball movement

        # Check if the ball is at the left or right of the screen
        if self.ball_rect.left <= 0 or self.ball_rect.right >= self.screen.width:
            self.ball_direction[0] = -self.ball_direction[0] #change x direction of ball movement

# this class for storing width, height, image and background color
class Screen:
    def __init__(self, width, height, image, background_color) -> None:
        self.width = width
        self.height = height
        self.image = image
        self.background_color = background_color

# this class moves the balls in the pygame's screen
# it takes a ball list that contains balls
class Game:
    def __init__(self, balls) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.total_time_after_move = 0
        self.inter_move_time = 150 # initial fpms of the ball(frame per millisecond): it moves a frame as this value
        self.balls_list = balls
        # this arranges the screen of game's width and height (because all balls have the same screen size, any of the ball of is ok)
        self.screen = pygame.display.set_mode((self.balls_list[0].screen.width, self.balls_list[0].screen.height))

    # this runs the game 
    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN: # check if user clicks key up or down
                    
                    if event.key == pygame.K_DOWN: # check if user clicks key down
                        self.inter_move_time += 5 # increase move time to move the balls slowly
                        
                        if self.inter_move_time >= min_value:  # to stop the ball when it becomes min_value (slowest)
                            self.inter_move_time = 1000000 # it stops the ball (actually not stopping but ball will move each frame in 1000s)
                            
                    if event.key == pygame.K_UP: # check if user clicks key up
                        
                        if self.inter_move_time == 1000000:  # if it is stopped before, balls will move again
                            self.inter_move_time = min_value
                            
                        self.inter_move_time -= 5 # decrease the fpms to move the balls faster

                        if self.inter_move_time <= 5:  # to prevent bug when it becomes 0 (fastest)
                            self.inter_move_time = 5

            self.total_time_after_move += self.clock.get_time()
            if self.total_time_after_move < self.inter_move_time: # tick the clock while its smaller than total_time_after_move
                self.clock.tick()
                continue # continue to while without make total_time_after_move, 0 again in this way it moves smoothly instead of pixel by pixel
            
            
            # else it makes total_time_after_move 0 
            self.total_time_after_move = 0

            for ball in self.balls_list:  # to implement all balls in game
                ball.update() # arrange the balls position (change the direction if it bounces)

            # Fill the screen and blit each ball after all balls have been updated
            # if we don't do that, we would see the previous ball's position, however now we fill entire screen as a background color
            self.screen.fill(self.balls_list[0].screen.background_color) # set background's color
            for ball in self.balls_list:
                #draws the pixels of the screen with respect to balls image an position in the current screen
                self.screen.blit(ball.get_ball_image(), ball.ball_rect) 

            pygame.display.flip() #it updates the frames with respect to new screen.

            self.clock.tick() 

def main():
    
    image = "ball.gif"
    pygame.init()
    # arranging the screen size, image and background color
    my_screen = Screen(720, 360, image, (125, 125, 125))

    balls = [] # balls list
    for i in range(3):
        # Randomize the directions
        ball_direction = [random.randrange(2, 32), random.randint(2, 12)]  
        balls.append(Ball(ball_direction, my_screen)) # add the ball into balls list
        
    # arrange the game with balls list
    game = Game(balls)
     # run the game
    game.run()

if __name__ == "__main__":
    main()
