import consts
import pygame
import random


class Point:
    """ Storing Point information """

    def __init__(self, x: int, y: int, move: str):
        self.x = x
        self.y = y
        self.move = move


class Life:
    """ Renders lifetime of the player """

    def __init__(self, initial_life: int = consts.INIT_LIFE):
        pygame.font.init()
        self.life = initial_life
        self.font = pygame.font.SysFont('Comic Sans MS', consts.FONT_SIZE)

    def update(self, collision_type: str):
        """
            Updates the lives left after a collision

            Note: Qix and Sparx have different damage levels!
        """
        if collision_type == 'Qix':
            self.life -= consts.QIX_DAMAGE
        else:
            self.life -= consts.SPARX_DAMAAGE

        return self.life <= 0

    def get_text(self):
        return self.font.render(f'Life: {self.life}', True, consts.FONT_COLOR)

    def get_coordinate(self):
        return consts.INIT_COOR


class Player:

    """
        Player Object that implements the logic of the
        player moving in the map.
    """

    def __init__(self):
        self.points = []
        self.x = (consts.MAP_WIDTH - consts.MARGIN) // 2
        self.y = consts.MAP_HEIGHT - consts.MARGIN
        self.claiming = False
        self.previous_direction = None
        self.life_force = 100

    def get_coordinate(self):
        return (self.x, self.y)

    def move(self, direction: str):
        """ Controls the movement of the player """
        if self.previous_direction != direction:
            self.previous_direction == direction

        if self.claiming:
            self.points.append(Point(self.x, self.y, direction))

        if direction == 'right':
            self._move_right()
        if direction == 'left':
            self._move_left()
        if direction == 'up':
            self._move_up()
        if direction == 'down':
            self._move_down()

    def _move_right(self):
        if self.x != consts.MAP_WIDTH - consts.MARGIN:
            self.x += consts.MOVE_DIM

    def _move_left(self):
        if self.x != consts.MARGIN:
            self.x -= consts.MOVE_DIM

    def _move_up(self):
        if self.y != consts.MARGIN:
            self.y -= consts.MOVE_DIM

    def _move_down(self):
        if self.y != consts.MAP_HEIGHT - consts.MARGIN:
            self.y += consts.MOVE_DIM


class Enemy:
    """ Manages the obstacles within the game """
    class _Qix:
        """ Implementing the logic for Qix Object. """

        def __init__(self):
            self.x, self.y = self._random_position()
            self.prev_move_x = None
            self.prev_move_y = None
            self.prev_move = None

        def _random_position(self):
            """ Generates a random position for qix """
            range_x = consts.MARGIN // consts.MOVE_DIM
            range_y = (consts.MAP_WIDTH - consts.MARGIN) // consts.MOVE_DIM

            x = random.randrange(range_x, range_y) * consts.MOVE_DIM
            y = random.randrange(range_x, range_y) * consts.MOVE_DIM
            print("Inital Qix: ", x, y)
            return x, y

        def get_coordinate(self):
            return (self.x, self.y)

        def next_move(self):
            self._possible_moves()

            self.prev_move = random.choice(self.moves)

            if self.prev_move == 'down':
                self._move_down()
            if self.prev_move == 'up':
                self._move_up()
            if self.prev_move == 'left':
                self._move_left()
            if self.prev_move == 'right':
                self._move_right()

            if self.prev_move == 'down' or self.prev_move == 'up':
                self.prev_move_y = self.prev_move
            if self.prev_move == 'left' or self.prev_move == 'right':
                self.prev_move_x = self.prev_move

        def _possible_moves(self):
            # Getting all the possible
            moves = []

            if self.x != consts.MARGIN: moves.append('left')
            if self.x != consts.MAP_WIDTH - consts.MARGIN: moves.append('right')
            if self.y != consts.MAP_HEIGHT  - consts.MARGIN: moves.append('down')
            if self.y != consts.MARGIN: moves.append('up')
            
            # Optimize the randomness
            if random.randrange(0, 10) > 1:
                if "up" in moves and "down" in moves and len(moves) > 2:
                    if self.prev_move_y == "down": moves.remove("up")
                    if self.prev_move_y == "up": moves.remove("down")
                
                if "right" in moves and "left" in moves and len(moves) > 2:
                    if self.prev_move_x == "right": moves.remove("left")
                    elif self.prev_move_x == "left": moves.remove("right")

            self.moves = moves
            # print(self.moves, self.prev_move)
            

        def _move_right(self):
            if self.x != consts.MAP_WIDTH - consts.MARGIN:
                self.x += consts.MOVE_DIM

        def _move_left(self):
            if self.x != consts.MARGIN:
                self.x -= consts.MOVE_DIM

        def _move_up(self):
            if self.y != consts.MARGIN:
                self.y -= consts.MOVE_DIM

        def _move_down(self):
            if self.y != consts.MAP_HEIGHT - consts.MARGIN:
                self.y += consts.MOVE_DIM

    class _Sparx:
        """ Implementing the logic for Sparx Object. """

        def __init__(self):
            self.move = None  # up, down, left, right of the grid
            self.x, self.y, self.orientation = self._random_position()
            print(self.x, self.y, self.orientation)

        def get_coordinate(self) -> (int, int):
            return self.x, self.y

        def get_orientation(self):
            return self.orientation

        def _random_position(self)-> (int, int):
            """ Return random positions for sparx """
            fix_x = [consts.MARGIN, consts.MAP_WIDTH - consts.MARGIN]
            fix_y = [consts.MARGIN, consts.MAP_HEIGHT - consts.MARGIN]

            range_x = consts.MARGIN // consts.MOVE_DIM
            range_y = (consts.MAP_WIDTH - consts.MARGIN) // consts.MOVE_DIM

            # 0: Vertical
            if random.choice([0, 1]) == 0:
                x = random.choice(fix_x)
                y = random.randrange(range_x, range_y) * consts.MOVE_DIM
                return x, y, 'vertical'
            else:
                x = random.randrange(range_x, range_y) * consts.MOVE_DIM
                y = random.choice(fix_y)
                return x, y, 'horizontal'

        def next_move(self):
            # Check to see the orientation should change
            self._check_orientation()
            
            if self.orientation == 'horizontal':
                if self.x == consts.MARGIN: self.move = 'left'
                else:
                    self.move = random.choice(['right', 'left'])
            else:
                if self.y == consts.MARGIN:  # to set initial direction
                    self.move = 'up'
                else:
                    self.move = random.choice(['down', 'up'])
            
            print(self.move)

            if self.move == 'down':
                self._move_down()
            if self.move == 'up':
                self._move_up()
            if self.move == 'left':
                self._move_left()
            if self.move == 'right':
                self._move_right()
        
        def _check_orientation(self):
            if self.orientation == 'vertical':
                if self.y == consts.MARGIN or self.y == consts.MAP_HEIGHT - consts.MARGIN:
                    self.orientation = 'horizontal'
            else:
                if self.x == consts.MARGIN or self.x == consts.MAP_HEIGHT - consts.MARGIN:
                    self.orientation = 'vertical'

        def _move_right(self):
            if self.x != consts.MAP_WIDTH - consts.MARGIN:
                self.x += consts.MOVE_DIM

        def _move_left(self):
            if self.x != consts.MARGIN:
                self.x -= consts.MOVE_DIM

        def _move_up(self):
            if self.y != consts.MARGIN:
                self.y -= consts.MOVE_DIM

        def _move_down(self):
            if self.y != consts.MAP_HEIGHT - consts.MARGIN:
                self.y += consts.MOVE_DIM

    def __init__(self):
        self.quixes = []
        self.sparxes = []
        self.init = True

    def _add_sparx(self):
        self.sparxes.append(Enemy._Sparx())

    def _add_qix(self):
        self.quixes.append(Enemy._Qix())

    def update(self):
        if self.init:
            self._add_qix()
            self._add_sparx()
            self.init = False

        self._fetch_next_moves()

    def _fetch_next_moves(self):
        for sparx in self.sparxes:
            sparx.next_move()

        for quix in self.quixes:
            quix.next_move()


class Map:
    """ Main map that renders everything within here """

    def __init__(self, height: int = consts.MAP_HEIGHT, width: int = consts.MAP_WIDTH):
        self.width = width
        self.height = height

        # Initialize the pygame module
        pygame.init()

        self.life = Life()

        # Set the properties of the Display
        self.gameDisplay = pygame.display.set_mode((self.height, self.width))
        self.gameDisplay.fill(consts.BG_COLOR)

        # Setting the caption
        pygame.display.set_caption('QIX')

        self.player = Player()

        self.enemy = Enemy()

    def render(self):
        """ Renders the graphics """

        self.gameDisplay.fill(consts.BG_COLOR)

        # Draw the borders
        self._draw_borders()

        # Draw the player and the claimed areas
        self._draw_player()
        self._draw_clamied_areas()

        self.enemy.update()
        self._render_enemy()

        # Write the life text
        # Note: This should be rendered at the end to overwrite anything else!
        self.gameDisplay.blit(self.life.get_text(), self.life.get_coordinate())

    def _render_enemy(self):
        """ Renders the graphics for enemy objects. """
        for sparx in self.enemy.sparxes:
            self._draw_sparx(sparx)

        for quix in self.enemy.quixes:
            self._draw_qix(quix)

    def _draw_sparx(self, sparx: Enemy._Sparx, color=consts.SPARX_COLOR):
        x, y = sparx.get_coordinate()
        
        pygame.draw.polygon(self.gameDisplay,
                            color,
                            [(x, y), (x + consts.SPARX_DIM, y + consts.SPARX_DIM),
                             (x, y + 2 * consts.SPARX_DIM), (x - consts.SPARX_DIM, y + consts.SPARX_DIM)])

    def _draw_qix(self, quix: Enemy._Qix, color=consts.QIX_COLOR):
        x, y = quix.get_coordinate()

        pygame.draw.polygon(self.gameDisplay,
                            consts.QIX_COLOR,
                            [(x, y), (x + consts.QIX_DIM, y + consts.QIX_DIM),
                             (x, y + 2 * consts.QIX_DIM), (x - consts.QIX_DIM, y + consts.QIX_DIM)])

    def _draw_clamied_areas(self):
        pass

    def _draw_player(self):
        """ Draws the player """
        pygame.draw.circle(self.gameDisplay,
                           consts.PLAYER_COLOR,
                           self.player.get_coordinate(),
                           consts.PLAYER_RADIUS)

    def _draw_borders(self, margin: int = consts.MARGIN, color: (int, int, int) = consts.BORDER_COLOR):
        """ Draws the border for the QIX game """
        # Upper Horizontal Line
        pygame.draw.line(self.gameDisplay, color,
                         (margin, margin), (self.width - margin, margin))

        # Lower Horizontal Line
        pygame.draw.line(self.gameDisplay, color, (margin, self.height -
                                                   margin), (self.width - margin, self.height - margin))
        # Left Vertical Line
        pygame.draw.line(self.gameDisplay, color,
                         (margin, margin), (margin, self.height - margin))
        # Right Vertical Line
        pygame.draw.line(self.gameDisplay, color, (self.width - margin,
                                                   margin), (self.width - margin, self.height - margin))
    def remove_alpha(self, pixel):
        """removes last element in 4 element color tuple"""
        temp_list = list(pixel)
        temp_list.pop()
        RGB = tuple(temp_list)
        return RGB

    def check_movement(self,direction):
        """checks if player is able to move in a certain direction if claiming is False"""
        if(direction=="right"):
            if(map.remove_alpha(map.gameDisplay.get_at((map.player.x + 10, map.player.y))) == consts.BORDER_COLOR):
                return True
            else:
                return False
        if(direction=="left"):
            if (map.remove_alpha(map.gameDisplay.get_at((map.player.x - 11, map.player.y))) == consts.BORDER_COLOR):
                return True
            else:
                if((map.player.x,map.player.y)==(30,400) or (map.player.x,map.player.y)==(30,20)):
                    return True
                else:
                    return False
        if(direction =="up"):
            if (map.remove_alpha(map.gameDisplay.get_at((map.player.x, map.player.y-11))) == consts.BORDER_COLOR):
                return True
            else:
                if ((map.player.x, map.player.y) == (20, 30) or (map.player.x,map.player.y)==(400,30)):
                    return True
                else:
                    return False
                return False
        if(direction =="down"):
            if (map.remove_alpha(map.gameDisplay.get_at((map.player.x, map.player.y + 10))) == consts.BORDER_COLOR):
                return True
            else:
                return False


def run():

    # Initialization
    clock = pygame.time.Clock()
    PAUSE = False
    map = Map()
    map.render()
    
    while True:
        for event in pygame.event.get():
    
            # Quitting the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
            if event.type == pygame.KEYDOWN:
    
                # Starting to claim territory
                if event.key == pygame.K_SPACE:
                    map.player.claiming = not map.player.claiming
    
                # Pausing
                if event.key == pygame.K_p:
                    PAUSE = True
    
                # Moving manually
                if event.key == pygame.K_RIGHT:
                    #movements are restricted to moving along border if player is not claiming
                    if (map.player.claiming == False and map.check_movement("right")):
                        map.player.move(direction="right")
                    elif (map.player.claiming):
                        map.player.move(direction="right")
    
                if event.key == pygame.K_LEFT:
                    if (map.player.claiming == False and map.check_movement("left")):
                        map.player.move(direction="left")
                    elif (map.player.claiming):
                        map.player.move(direction="left")
    
                if event.key == pygame.K_UP:
                    if (map.player.claiming == False and map.check_movement("up")):
                        map.player.move(direction="up")
                    elif (map.player.claiming):
                        map.player.move(direction="up")
    
                if event.key == pygame.K_DOWN:
                    if (map.player.claiming == False and map.check_movement("down")):
                        map.player.move(direction="down")
                    elif (map.player.claiming):
                        map.player.move(direction="down")
    
        # If the game is not paused then render the graphics
        if not PAUSE:
            map.render()
        
        pygame.display.update()
        clock.tick(consts.FPS)