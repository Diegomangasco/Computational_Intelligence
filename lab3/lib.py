import logging
import random
from functools import reduce
from typing import Callable

logging.getLogger().setLevel(logging.INFO)

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i*2+1 for i in range(num_rows)]
        self._k = k

    def nimming_remove(self, row: int, num_objects: int) -> None:
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects < self._k
        self._rows[row] -= num_objects
    
    def nimming_add(self, row: int, num_objects: int) -> None:
        self._rows[row] += num_objects

    def goal(self) -> bool:
        # Check if someone has won
        return sum(self._rows) == 0

    def verify_state(self) -> bool:
    # Verify of the new game state is useful for the player with the nim sum rule
        xor = reduce(lambda a, b: a ^ b, self._rows)
        if xor == 0:
            return True
        else:
            return False


class RandomPlayer:
    def __init__(self) -> None:
        self._moves = []
        self._nMoves = 0
    
    def play(self, nim: Nim) -> None:
        # Chose a random row and a random number of pieces
        x = random.randint(0, len(nim._rows)-1)
        while nim._rows[x] == 0:
            x = random.randint(0, len(nim._rows)-1)
        y = random.randint(1, nim._rows[x])
        # Update the attributes
        self._nMoves += 1
        self._moves.append(f"{y} items from row {x}")
        nim.nimming_remove(x, y)
        
    def printSolution(self) -> None:
        logging.info(f" Random player won, moves have been: {self._moves}; total: {self._nMoves}")


class ExpertSystem:
    def __init__(self) -> None:
        self._nMoves = 0
        self._moves = []

    def printSolution(self) -> None:
        logging.info(f" Expert system won, moves have been: {self._moves}; total: {self._nMoves}")
    
    def play(self, nim: Nim) -> None:
        possible = [(r, o) for r, c in enumerate(nim._rows) for o in range(1, c + 1)]
        for ply in possible:
            nim.nimming_remove(ply[0], ply[1])
            valid = nim.verify_state()
            if valid:
                break
            else:
                nim.nimming_add(ply[0], ply[1])

        if not valid:
            ply = random.choice(possible)
            nim.nimming_remove(ply[0], ply[1])
            
        self._nMoves += 1
        self._moves.append(f"{ply[1]} items from row {ply[0]}")


class GeneticAlgorithm:
    def __init__(self) -> None:
        self._nMoves = 0
        self._moves = []

    def printSolution(self) -> None:
        logging.info(f" Expert system won, moves have been: {self._moves}; total: {self._nMoves}")

    def cook_status(self, nim: Nim) -> None:
        cooked = dict()
        cooked['possible_moves'] = [(r, o) for r, c in enumerate(nim._rows) for o in range(1, c + 1) if nim._k is None or o <= nim._k]
        cooked['active_rows_number'] = sum(r > 0 for r in nim._rows)
        cooked['shortest_row'] = min((x for x in enumerate(nim._rows) if x[1] > 0), key= lambda y: y[1])[0]
        cooked['longest_row'] = max((x for x in enumerate(nim._rows) if x[1] > 0), key= lambda y: y[1])[0]
        cooked['nim_status'] = nim.verify_state()
        return cooked

    def make_strategy(self, genome: dict) -> Callable:
        def evolvable(nim: Nim) -> tuple:
            data = self.cook_status(nim)
            if random.random() < genome['p']:
                ply = (data['shortest_row'], random.randint(1, nim._rows[data['shortest_row']]))
            else:
                ply = (data['longest_row'], random.randint(1, nim._rows[data['longest_row']]))
            
            return ply
        return evolvable

    def evaluate_strategy():
        pass

    def play():
        pass


class MinMaxSystem:
    def __init__(self) -> None:
        self._nMoves = 0
        self._moves = []

    def printSolution(self) -> None:
        logging.info(f" MinMax system won, moves have been: {self._moves}; total: {self._nMoves}")

    def minmax(self, nim: Nim, player: bool, step: int):
        possible = [(r, o) for r, c in enumerate(nim._rows) for o in range(1, c + 1)]
        # True player is the MinMax system, False player is the other player
        if not possible:
            if player:
                # No win -> the other player arrives with the table empty
                return (None, -1, step)
            else:
                # Win -> the MinMax system arrives with the table empty
                return (None, 1, step)
        evaluations = list()
        for ply in possible:
            nim.nimming_remove(ply[0], ply[1])
            # Recursive call
            _, val, weight = self.minmax(nim, not player, step+1)
            if val == 1 and step != 0:
                # Found a good path, return it
                nim.nimming_add(ply[0], ply[1])
                return (ply, val, weight)
            elif val == 1 and step == 0:
                # Found a good path, save it
                nim.nimming_add(ply[0], ply[1])
                evaluations.append((ply, val, weight))
            else:
                nim.nimming_add(ply[0], ply[1])
                evaluations.append((ply, val, weight))
        # Return the lightweight solution trough the found ones
        return max(evaluations, key=lambda x: -x[2])

    def play(self, nim: Nim):
        best_ply, _, _ = self.minmax(nim, player=True, step=0)
        nim.nimming_remove(best_ply[0], best_ply[1])
        self._nMoves += 1
        self._moves.append(f"{best_ply[1]} items from row {best_ply[0]}")
