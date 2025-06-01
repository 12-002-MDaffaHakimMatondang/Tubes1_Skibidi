import random
from typing import Optional, List, Tuple
from math import sqrt

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position


class GameUtilities:

    
    @staticmethod
    def get_teleports(board: Board) -> list[Position]:

        teleport_gate = list()
        obj: GameObject
        for obj in board.game_objects:
            if (obj.type == "TeleportGameObject"):
                teleport_gate.append(obj.position)
        return teleport_gate

    @staticmethod
    def get_reset(board: Board) -> List[GameObject]:

        reset = list()
        obj: GameObject
        for obj in board.game_objects:
            if (obj.type == "DiamondButtonGameObject"):
                reset.append(obj)
        return reset


class MovementCalculator:

    
    @staticmethod
    def get_direction(curr: Position, dest: Position, teleports: List[Position]) -> Tuple[int, int]:

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        mn = float('inf')
        dest_tele = False

        # Destination is teleport
        for t in teleports:
            if (dest.x == t.x and dest.y == t.y):
                dest_tele = True

        if (dest_tele == False):
            print("Dont go to teleport!!!")
            _new = list()
            for i in range(len(directions)):
                get = True
                for t in teleports:
                    if ((curr.x + directions[i][0]) == t.x and (curr.y + directions[i][1]) == t.y):
                        get = False
                        break

                if (get):
                    _new.append(directions[i])

            directions = _new
        else:
            print("Go to teleport!!!")

        using = 0
        for i in range(len(directions)):
            new_x = curr.x + directions[i][0]
            new_y = curr.y + directions[i][1]

            euclidean = sqrt((new_x - dest.x)**2 + (new_y - dest.y)**2)
            if (mn > euclidean):
                using = i
                mn = euclidean

        return directions[using]

    @staticmethod
    def distance(obj1: Position, obj2: Position, teleports: List[Position]):

        pos_x = obj1.x
        pos_y = obj1.y

        min_distance = float('inf')

        # Masuk tanpa teleport
        distance = abs(obj2.x - pos_x) + \
            abs(obj2.y - pos_y)
        if (min_distance > distance):
            min_distance = distance

        # Masuk lewat teleport pertama
        distance_x = abs(teleports[0].x - pos_x) + \
            abs(teleports[1].x - obj2.x)
        distance_y = abs(teleports[0].y - pos_y) + \
            abs(teleports[1].y - obj2.y)
        distance = distance_x + distance_y
        if (min_distance > distance):
            min_distance = distance

        # Masuk lewat teleport Kedua
        distance_x = abs(teleports[1].x - pos_x) + \
            abs(teleports[0].x - obj2.x)
        distance_y = abs(teleports[1].y - pos_y) + \
            abs(teleports[0].y - obj2.y)
        distance = distance_x + distance_y
        if (min_distance > distance):
            min_distance = distance

        return min_distance


class SifuLogic(BaseLogic):

    
    def __init__(self) -> None:
        # Game state variables
        self.bot: GameObject = None
        self.board: Board = None
        self.goal: Position | None = None
        
        # Path finding variables
        self.route: List[Position] = []
        self.goal_evaluation: float = 0
        self.best_route: List[GameObject] = []
        
        # Game objects
        self.teleports: List[Position] = []
        self.reset: List[GameObject] = []
        self.other_bot: List[GameObject] = []
        self.diamonds: List[GameObject] = []
        self.allowed: List[Tuple[int, int]] = []

    def _initialize_game_state(self, board_bot: GameObject, board: Board) -> None:

        self.bot = board_bot
        self.board = board
        self.teleports = GameUtilities.get_teleports(self.board)
        self.reset = GameUtilities.get_reset(self.board)
        self.goal = None
        self.allowed = list(filter(lambda t: board.is_valid_move(
            self.bot.position, t[0], t[1]), [(0, 1), (1, 0), (0, -1), (-1, 0)]))
        self.route: List[GameObject] = list()
        self.goal_evaluation = float('-inf')
        self.best_route: List[GameObject] = list()
        self.other_bot: List[GameObject] = list(filter(lambda bot: bot.id !=
                                                       self.bot.id, board.bots))
        self.diamonds = board.diamonds

    def set_goal(self, goal: GameObject, force: bool):

        pos_x = self.bot.position.x
        pos_y = self.bot.position.y
        teleports = self.teleports
        props = goal.properties

        min_distance = float('inf')
        if (self.goal and not force):
            min_distance = abs(pos_x - self.goal.x) + \
                abs(pos_y - self.goal.y)

        # Masuk tanpa teleport
        distance = abs(goal.position.x - pos_x) + \
            abs(goal.position.y - pos_y)
        if (min_distance > distance):
            self.goal = Position(
                goal.position.y, goal.position.x)
            min_distance = distance

        # Masuk lewat teleport pertama
        distance_x = abs(teleports[0].x - pos_x) + \
            abs(teleports[1].x - goal.position.x)
        distance_y = abs(teleports[0].y - pos_y) + \
            abs(teleports[1].y - goal.position.y)
        distance = distance_x + distance_y
        if (min_distance > distance):
            self.goal = Position(
                teleports[0].y, teleports[0].x)
            min_distance = distance

        # Masuk lewat teleport Kedua
        distance_x = abs(teleports[1].x - pos_x) + \
            abs(teleports[0].x - goal.position.x)
        distance_y = abs(teleports[1].y - pos_y) + \
            abs(teleports[0].y - goal.position.y)
        distance = distance_x + distance_y
        if (min_distance > distance):
            self.goal = Position(
                teleports[1].y, teleports[1].x)
            min_distance = distance

    def search_optimal(self, max_diamond: int, position: Position, total_points, total_distance) -> None:

        if (total_distance >= 15):
            return

        if (max_diamond == 0 or 0 < total_distance < 15 or len(self.route) == len(self.diamonds)):

            last_goal_to_base = MovementCalculator.distance(
                self.route[len(self.route) - 1].position, self.bot.properties.base, self.teleports)

            evaluation = (total_points/(total_distance + last_goal_to_base))
            if (self.goal_evaluation < evaluation):
                self.best_route = self.route.copy()
                self.goal_evaluation = evaluation

                self.set_goal(self.route[0], False)

        diamonds = self.diamonds

        for d in diamonds:
            search = True

            # Don't go more deep using the same diamond
            for dias in self.route:
                if (dias.id == d.id):
                    search = False

            if (not search):
                continue

            # Don't check if our backpack is not capable
            if (d.properties.points > max_diamond):
                continue

            self.route.append(d)
            dist = MovementCalculator.distance(position, d.position, self.teleports)

            # If it is close to other bot, decrease points
            can = True
            for other in self.other_bot:
                if (MovementCalculator.distance(other.position, d.position, self.teleports) < dist):
                    can = False

            # Go more deep
            if (total_distance + dist <= 15):
                self.search_optimal(max_diamond - d.properties.points,
                                    d.position, total_points + d.properties.points - (0 if can else 0.3), total_distance + dist)

            self.route.pop()

    def _check_early_returns(self) -> Optional[Tuple[int, int]]:

        props = self.bot.properties
        
        # Early return - inventori penuh
        if (self.bot.properties.diamonds == self.bot.properties.inventory_size):
            self.set_goal(GameObject(9999, Position(
                props.base.y, props.base.x), "Base", None), True)
            return MovementCalculator.get_direction(self.bot.position, self.bot.properties.base, self.teleports)

        # Time is up! lets go home
        if (self.bot.properties.milliseconds_left/1000 - 2.5 < MovementCalculator.distance(self.bot.position, props.base, self.teleports)):
            print("TIME TO GO TO BASE!!!")
            self.set_goal(GameObject(9999, Position(
                props.base.y, props.base.x), "Base", None), True)
            return MovementCalculator.get_direction(self.bot.position,
                                 self.goal, self.teleports)
        
        return None

    def _handle_combat(self) -> Optional[Tuple[int, int]]:

        props = self.bot.properties
        
        # Kill other bot!
        for other in self.other_bot:
            if (abs(self.bot.position.x - other.position.x) + abs(self.bot.position.y - other.position.y) <= 1):
                if (props.milliseconds_left > other.properties.milliseconds_left):
                    continue
                return MovementCalculator.get_direction(self.bot.position, other.position, self.teleports)
        
        return None

    def _evaluate_reset_buttons(self) -> None:

        if (self.goal_evaluation > 0):
            for rstBtn in self.reset:
                d = MovementCalculator.distance(self.bot.position,
                             rstBtn.position, self.teleports)
                if (0.25/d > self.goal_evaluation):
                    self.goal_evaluation = 0.25/d
                    self.set_goal(rstBtn, True)

    def _finalize_goal(self) -> None:

        props = self.bot.properties
        
        # if goal is too bad just go home
        if (self.goal == None or (self.goal_evaluation <= 0.05 and len(self.other_bot) > 0)):
            self.set_goal(GameObject(9999, Position(
                props.base.y, props.base.x), "Base", None), True)

    def _handle_safety_check(self, delta_x: int, delta_y: int) -> Tuple[int, int]:

        props = self.bot.properties
        next_position = Position(
            self.bot.position.x + delta_x, self.bot.position.y + delta_y)

        # is it safe to go there?
        for other in self.other_bot:
            # check if it is safe, otherwise menjauh
            if (abs(next_position.x - other.position.x) + abs(next_position.y - other.position.y) <= 1 and other.properties.milliseconds_left < props.milliseconds_left):
                go_away = list(
                    filter(lambda t: (abs(self.bot.position.x + t[0] - other.position.x) + abs(self.bot.position.y - other.position.y) >= 2), self.allowed))
                delta_x, delta_y = random.choice(go_away)
                print("GO AWAY!!!")
                break
        
        return delta_x, delta_y

    def _debug_print(self) -> None:
 
        print("bot position:", self.bot.position)
        print(self.goal_evaluation)
        print("goal: ", self.goal)
        print("with route: ")
        for obj in self.best_route:
            print(obj.position)
        print(self.teleports)
        print("==========")
        
        print("Bot position is:", self.bot.position)
        print("It's goal is:", self.goal)
        print("With goal evaluation:", self.goal_evaluation)
        print("\n\nWith route:")
        for obj in self.best_route:
            print(obj.position)

        print("max_depth: ", len(self.best_route))
        print("with route: ")

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int]:

        # Inisialisasi state game
        self._initialize_game_state(board_bot, board)
        
        # Cek kondisi early return
        early_return = self._check_early_returns()
        if early_return:
            return early_return
        
        # Handle combat
        combat_move = self._handle_combat()
        if combat_move:
            return combat_move

        # Cari rute optimal
        props = self.bot.properties
        self.search_optimal(props.inventory_size -
                            props.diamonds, self.bot.position, 0, 0)

        self._debug_print()

        # Evaluasi reset buttons
        self._evaluate_reset_buttons()

        # Finalisasi goal
        self._finalize_goal()

        # Jika sudah sampai goal, gerak random
        if (self.bot.position.x == self.goal.x and self.bot.position.y == self.goal.y):
            print(self.allowed)
            return random.choice(self.allowed)

        # Tentukan arah gerak
        delta_x, delta_y = MovementCalculator.get_direction(
            self.bot.position, self.goal, self.teleports)
        
        # Safety check
        delta_x, delta_y = self._handle_safety_check(delta_x, delta_y)

        return MovementCalculator.get_direction(self.bot.position, self.goal, self.teleports)