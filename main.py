#Boris Sergienko
#January 18th 2023

import pygame
import pymunk

class CollisionSimulation:
    def __init__(self):
        # Initialize Pygame and Pymunk
        pygame.init()
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0) # set gravity value

        # Set the screen size
        self.size = (700, 500)
        self.screen = pygame.display.set_mode(self.size)

        # Set the title of the window
        pygame.display.set_caption("Elastic Collision Simulation with Gravity")
        
            # Create two circles for the objects
        self.object1_mass = 2.0
        self.object2_mass = 3.0
        self.object1_radius = 50
        self.object2_radius = 30
        self.object1_pos = (150, 250)
        self.object2_pos = (550, 250)
        self.object1_body = pymunk.Body(self.object1_mass, pymunk.inf)
        self.object2_body = pymunk.Body(self.object2_mass, pymunk.inf)
        self.object1_shape = pymunk.Circle(self.object1_body, self.object1_radius)
        self.object2_shape = pymunk.Circle(self.object2_body, self.object2_radius)
        self.object1_body.position = self.object1_pos
        self.object2_body.position = self.object2_pos

        # Create a slider for controlling the mass of the objects
        self.slider_rect = pygame.Rect(50, 400, 600, 50)
        self.slider_color = (0, 0, 255)
        self.slider_mass = 0.5

        # Create a variable for controlling the initial velocities
        self.object1_body.velocity = Vector(3.0, 2.0)
        self.object2_body.velocity = Vector(-2.0, 4.0)

        # Create a start button
        self.start_button_rect = pygame.Rect(250, 450, 200, 50)
        self.start_button_color = (255, 255, 255)
        self.start_button_text = "Start"

        # Create a text box for displaying the current velocities
        self.velocity_text_box = pygame.Rect(450, 50, 200, 50)
        self.velocity_text_color = (0, 0, 0)
        self.velocity_text_font = pygame.font.Font(None, 32)

        # Create a flag for controlling the start and stop of the simulation
        self.simulation_running = False

        # Add objects to the space
        self.space.add(self.object1_body, self.object1_shape)
        self.space.add(self.object2_body, self.object2_shape)

        # Set collision handler
        self.collision_handler = self.space.add_collision_handler(0, 0)
        self.collision_handler.data["surface"] = self.screen
        self.collision_handler.post_solve = self.collision_post_solve

    def collision_post_solve(arbiter, space, data):
        """This function is called after a collision is resolved."""
        # Get the bodies involved in the collision
        body1, body2 = arbiter.shapes[0].body, arbiter.shapes[1].body

        # Get the velocities of the bodies before the collision
        v1 = body1.velocity
        v2 = body2.velocity

        # Get the masses of the bodies
        m1 = body1.mass
        m2 = body2.mass

        # Calculate the new velocities of the bodies after the collision
        v1_prime = (v1 * (m1 - m2) + (2 * m2 * v2)) / (m1 + m2)
        v2_prime = (v2 * (m2 - m1) + (2 * m1 * v1)) / (m1 + m2)

        # Set the new velocities
        body1.velocity = v1_prime
        body2.velocity = v2_prime

    def run(self):
        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw the circles, slider, start button, and text box on the screen
            self.screen.fill((255, 255, 255))
            pygame.draw.circle(self.screen, (255, 0, 0), self.object1_body.position, self.object1_radius)
            pygame.draw.circle(self.screen, (0, 255, 0), self.object2_body.position, self.object2_radius)
            pygame.draw.rect(self.screen, self.slider_color, self.slider_rect)
            pygame.draw.rect(self.screen, self.start_button_color, self.start_button_rect)
            pygame.draw.rect(self.screen, self.velocity_text_color, self.velocity_text_box)

            # Handle user input for controlling the mass and initial velocities
            mouse_pos = pygame.mouse.get_pos()
            if self.slider_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    self.slider_mass = (mouse_pos[0] - self.slider_rect.left) / self.slider_rect.width
            self.object1_mass = self.slider_mass
            self.object2_mass = 1 - self.slider_mass

            # Handle user input for the start button
            if self.start_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    self.simulation_running = not self.simulation_running

            # Run the simulation if the start button is pressed
            if self.simulation_running:
                self.space.step(1/50.0)  # step the space by 1/50 sec

            # Display the current velocities in the text box
            velocity_text = self.velocity_text_font.render("Velocity 1: {} m/s Velocity 2: {} m/s".format(self.object1_body.velocity, self.object2_body.velocity), True, self.velocity_text_color)
            self.screen.blit(velocity_text, (self.velocity_text_box.x, self.velocity_text_box.y))

            pygame.display.flip()

        # Exit Pygame
        pygame.quit()

if __name__ == "__main__":
    simulation = CollisionSimulation()
    simulation.run()
