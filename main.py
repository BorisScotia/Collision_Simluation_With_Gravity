#Boris Sergienko
#Grade 12 Physics Final Collision Simulator
#January 2023

import pygame
import pymunk
import random


#Renders display
pygame.init()
display = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Elastic and Ineleastic Simulation')
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 100


#Loads font
font = pygame.font.SysFont('Arial',15,bold=True)


def convert_coordinates(point):
    return int(point[0]), int(600 - point[1])

#Creates a Ball classs
class Ball():
    def __init__(self, x, y, color, velocity, mass):
        self.color = color
        self.body = pymunk.Body()
        self.body.position = x, y
        self.body.velocity = velocity
        self.body.mass = mass
        self.shape = pymunk.Circle(self.body, 15)
        self.shape.density = 1
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

#Draws the ball and makes sure balls don't leave border
    def draw(self):
        pos = self.body.position
        pygame.draw.circle(display, self.color, convert_coordinates(pos), 15)
        if pos[0] >= 595 or pos[0] <= 10:
            self.body.velocity *= -1
        if pos[1] >= 595 or pos[1] <= 10:
            self.body.velocity *= -1

#Generates random location

a = []

for num in range(6):
    b = random.randint(10, 590)
    a.append(b)


#Main game loop
def game():

#Makes 3 balls
    ball_1 = Ball(a[0], a[1], (255, 0, 0), (250, 400), 10)
    ball_2 = Ball(a[2], a[3], (0, 255, 0), (350, 400), 50)
    ball_3 = Ball(a[4], a[5], (0, 0, 255), (150, 350), 100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            #Adds Gravity
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    if space.gravity == (0,0):
                        space.gravity = (0,-981)
                    else:
                        space.gravity = (0,0)

        #Render's Balls
        display.fill((255, 255, 255))
        ball_1.shape.elasticity = 0.5
        ball_2.shape.elasticity = 0.3
        ball_3.shape.elasticity = 1
        ball_1.draw()
        ball_2.draw()
        ball_3.draw()

        #------- Fonts------#
        text_red = font.render(f'Red ball velocity:{round(ball_1.body.velocity[0])}, {round(ball_1.body.velocity[1])} '
                               f'Elasticity = {ball_1.shape.elasticity * 100}%', True, (0,0,0))
        textrect = text_red.get_rect()
        textrect.center = ((420, 20))

        text_green = font.render(f'Green ball velocity:{round(ball_2.body.velocity[0])},{round(ball_2.body.velocity[1])} '
                                 f'Elasticity = {ball_2.shape.elasticity * 100}%', True, (0, 0, 0))
        textrect1 = text_green.get_rect()
        textrect1.center = ((420, 40))

        text_blue = font.render(f'Blue ball velocity:{round(ball_3.body.velocity[0])},{round(ball_3.body.velocity[1])} '
                                f'Elasticity = {ball_3.shape.elasticity * 100}%', True, (0, 0, 0))

        textrect2 = text_blue.get_rect()
        textrect2.center = ((420, 60))

        #Gravity text
        if space.gravity == (0, 0):
            text_gravity = font.render("Gravity: OFF", True, (0, 0, 0))
            text_grav_rect = text_gravity.get_rect()
            text_grav_rect.center = ((200, 50))
            display.blit(text_gravity, text_grav_rect)
        else:
            text_gravity = font.render("Gravity: ON", True, (0, 0, 0))
            text_grav_rect = text_gravity.get_rect()
            text_grav_rect.center = ((200, 50))
            display.blit(text_gravity, text_grav_rect)


        #Displays mass and velocities
        display.blit(text_red, textrect)
        display.blit(text_green, textrect1)
        display.blit(text_blue, textrect2)

        pygame.display.update()
        clock.tick(FPS)
        space.step(1 / FPS)


if __name__ == "__main__":
    game()

pygame.quit()

'''
LIMITATIONS
Mass doesn't affect Ek
Doesn't account for Elastic Equations Vf1 = (m1-m2/m1+m2)*vi1
and Vf2 = (2m/m1+m2)*vi1
Sometimes ball goes off screen if it lands in the corners
'''




















