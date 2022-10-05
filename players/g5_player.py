import os
import pickle
import numpy as np
import sympy
import logging
from typing import Tuple


class Player:
    def __init__(self, rng: np.random.Generator, logger: logging.Logger, total_days: int, spawn_days: int,
                 player_idx: int, spawn_point: sympy.geometry.Point2D, min_dim: int, max_dim: int, precomp_dir: str) \
            -> None:
        """Initialise the player with given skill.

            Args:
                rng (np.random.Generator): numpy random number generator, use this for same player behavior across run
                logger (logging.Logger): logger use this like logger.info("message")
                total_days (int): total number of days, the game is played
                spawn_days (int): number of days after which new units spawn
                player_idx (int): index used to identify the player among the four possible players
                spawn_point (sympy.geometry.Point2D): Homebase of the player
                min_dim (int): Minimum boundary of the square map
                max_dim (int): Maximum boundary of the square map
                precomp_dir (str): Directory path to store/load pre-computation
        """

        # precomp_path = os.path.join(precomp_dir, "{}.pkl".format(map_path))

        # # precompute check
        # if os.path.isfile(precomp_path):
        #     # Getting back the objects:
        #     with open(precomp_path, "rb") as f:
        #         self.obj0, self.obj1, self.obj2 = pickle.load(f)
        # else:
        #     # Compute objects to store
        #     self.obj0, self.obj1, self.obj2 = _

        #     # Dump the objects
        #     with open(precomp_path, 'wb') as f:
        #         pickle.dump([self.obj0, self.obj1, self.obj2], f)

        self.rng = rng
        self.logger = logger
        self.player_idx = player_idx

    def play(self, unit_id, unit_pos, map_states, current_scores, total_scores) -> [tuple[float, float]]:
        """Function which based on current game state returns the distance and angle of each unit active on the board

                Args:
                    unit_id (list(list(str))): contains the ids of each player's units (unit_id[player_idx][x])
                    unit_pos (list(list(float))): contains the position of each unit currently present on the map
                                                    (unit_pos[player_idx][x])
                    map_states (list(list(int)): contains the state of each cell, using the x, y coordinate system
                                                    (map_states[x][y])
                    current_scores (list(int)): contains the number of cells currently occupied by each player
                                                    (current_scores[player_idx])
                    total_scores (list(int)): contains the cumulative scores up until the current day
                                                    (total_scores[player_idx]

                Returns:
                    List[Tuple[float, float]]: Return a list of tuples consisting of distance and angle in radians to
                                                move each unit of the player
                """

        moves = []
        if self.player_idx == 0:
            angles = [0, np.pi / 4, np.pi / 2]
            unit_at_homebase = len(unit_id[self.player_idx]) % 3 # 2
            for i in range(len(unit_id[self.player_idx])-unit_at_homebase): # i = 0,1,2
                distance = 1
                angle = angles[i % 3]
                moves.append((distance, angle))

            for i in range(unit_at_homebase):
                moves.append((0,0))
        elif self.player_idx == 1:
            angles = [- np.pi / 4, - np.pi / 2, 0]
            for i in range(len(unit_id[self.player_idx])):
                distance = 1
                angle = angles[i % 3]
                moves.append((distance, angle))
        elif self.player_idx == 2:
            anglesEvenLayer = [- np.pi / 2, -3 * np.pi / 4, - np.pi]
            anglesOddLayer = [ -5 * np.pi / 8, -7 * np.pi / 8]
            n = len(unit_id[self.player_idx])
            r = n % 5
            for i in range(n-r):
                if i % 5 <= 2:
                    distance = 1
                    angle = anglesEvenLayer[i % 5]
                    moves.append((distance, angle))
                else:
                    # i % 5 > 2
                    distance = 1
                    angle = anglesOddLayer[(i % 5) - 3]
                    moves.append((distance, angle))
            if r == 1:
                moves.append((0, 0))
            elif r == 2:
                moves.append((0, 0))
                moves.append((0, 0))
            elif r == 3:
                distance = 1
                for j in range(3):
                    angle = anglesEvenLayer[j]
                    moves.append((distance, angle))
            elif r == 4:
                distance = 1
                for j in range(3):
                    angle = anglesEvenLayer[j]
                    moves.append((distance, angle))
                moves.append((0, 0))
        else:
            for i in range(len(unit_id[self.player_idx])):
                moves.append((0, 0))

        return moves
