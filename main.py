# Python imports
import random

# Library imports
import pygame

# pymunk imports
import pymunk
import pymunk.pygame_util


class BouncyBalls(object):
    def __init__(self) -> None:
        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, 900.0)

        # Physics
        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1

        # pygame
        pygame.init()
        self._screen = pygame.display.set_mode((607.5, 1080))
        self._clock = pygame.time.Clock()

        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Static barrier walls (lines) that the balls bounce off of
        self.add_object()

        self._running = True

    def run(self) -> None:
        """
        The main loop of the game.
        :return: None
        """
        # Main loop
        while self._running:
            # Progress time forward
            for x in range(self._physics_steps_per_frame):
                self._space.step(self._dt)

            self._process_events()
            self.clear_screen()
            self.draw_objects()
            pygame.display.flip()
            # Delay fixed time between frames
            self._clock.tick(60)
            pygame.display.set_caption("fps: " + str(self._clock.get_fps()))

    def add_object(self) -> None:
        """
        Create the ball and the static objects.
        :return: None
        """
        static_body = self._space.static_body
        static_lines = [
            pymunk.Segment(static_body, (0.0, 1080), (607.5, 1080), 0.0),
            pymunk.Segment(static_body, (0.0, 0.0), (0.0, 1080), 0.0),
            pymunk.Segment(static_body, (0.0, 1080), (607.5, 1080), 0.0),
            pymunk.Segment(static_body, (607.5, 1080), (607.5, 0.0), 0.0)
        ]
        self.create_ball()
        for line in static_lines:
            line.elasticity = 0.9
            line.friction = 0.9
        self._space.add(*static_lines)

    def _process_events(self) -> None:
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

    def create_ball(self) -> None:
        """
        Create a ball.
        :return:
        """
        mass = 10
        radius = 50
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        x = random.randint(115, 350)
        body.position = x, 200
        body.velocity = 200, -100
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.975
        shape.friction = 0.5

        self._space.add(body, shape)

    def clear_screen(self) -> None:
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill(pygame.Color("white"))

    def draw_objects(self) -> None:
        """
        Draw the objects.
        :return: None
        """
        self._space.debug_draw(self._draw_options)


def main():
    game = BouncyBalls()
    game.run()


if __name__ == "__main__":
    main()
