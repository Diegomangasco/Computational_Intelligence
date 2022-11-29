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


class GeneticAlgorithmSystem:
    def __init__(self) -> None:
        self._nMoves = 0
        self._moves = []

    def printSolution(self) -> None:
        logging.info(f" Genetic Algorithm system won, moves have been: {self._moves}; total: {self._nMoves}")

    def verify_nim_sum(self, ply: tuple, nim: Nim) -> bool:
        nim.nimming_remove(ply[0], ply[1])
        valid = nim.verify_state()
        nim.nimming_add(ply[0], ply[1])
        return valid

    def strategies(self, nim: Nim) -> dict:
        str = dict()
        possible = [(r, o) for r, c in enumerate(nim._rows) for o in range(1, c + 1)]
        possible_nim_sum = [x for x in possible if self.verify_nim_sum(x, nim) == True]
        str['nim_sum'] = random.choice(possible_nim_sum) if possible_nim_sum else random.choice(possible)
        str['random'] = random.choice(possible)
        str['max_from_lowest'] = max(possible, key=lambda m: (-m[0], m[1]))
        str['min_from_lowest'] = max(possible, key=lambda m: (-m[0], -m[1]))
        str['max_from_highest'] = max(possible, key=lambda m: (m[0], m[1]))
        str['min_from_highest'] = max(possible, key=lambda m: (m[0], -m[1]))
        possible_longest = max((x for x in enumerate(nim._rows)), key=lambda y: y[1])[0]
        possible_shortest = min((x for x in enumerate(nim._rows) if x[1] > 0), key=lambda y: y[1])[0]
        str['longest_row'] = random.choice([x for x in possible if x[0] == possible_longest])
        str['shortest_row'] = random.choice([x for x in possible if x[0] == possible_shortest])
        return str

    def choose_strategy(self, nim: Nim, prob: list) -> tuple:
        p = random.random()
        if p <= prob[0]:
            return self.strategies(nim)['random']
        if p > prob[0] and p <= prob[1]:
            return random.choice([self.strategies(nim)['max_from_lowest'], self.strategies(nim)['max_from_highest']])
        if p > prob[1] and p <= prob[2]:
            return random.choice([self.strategies(nim)['min_from_lowest'], self.strategies(nim)['min_from_highest']])
        if p > prob[2] and p <= prob[3]:
            return random.choice([self.strategies(nim)['longest_row'], self.strategies(nim)['shortest_row']])
        if p > prob[3]:
            return self.strategies(nim)['nim_sum']

    def calculate_fitness(self):
        pass

    def play(self, nim: Nim):
        ply = self.choose_strategy(nim, [.2, .3, .4, .5])
        nim.nimming_remove(ply[0], ply[1])
        self._nMoves += 1
        self._moves.append(f"{ply[1]} items from row {ply[0]}")


class MinMaxSystem:
    def __init__(self) -> None:
        self._nMoves = 0
        self._moves = []
        self._max_depth = 4

    def printSolution(self) -> None:
        logging.info(f" MinMax system won, moves have been: {self._moves}; total: {self._nMoves}")

    def minmax(self, nim: Nim, player: bool, step: int):
        possible = [(r, o) for r, c in enumerate(nim._rows) for o in range(1, c + 1)]
        # True player is the MinMax system, False player is the other player
        if not possible:
            if player:
                # No win -> the other player arrives with the table empty
                return (None, -1)
            else:
                # Win -> the MinMax system arrives with the table empty
                return (None, 1)
        if step == self._max_depth:
            # Evaluate secure and unsecure configurations
            if player and nim.verify_state():
                return(None, -1)
            elif player and not nim.verify_state():
                return(None, 1)
            elif not player and nim.verify_state():
                return(None, 1)
            else:
                return(None, -1)
        evaluations = list()
        for ply in possible:
            nim.nimming_remove(ply[0], ply[1])
            # Recursive call
            _, val = self.minmax(nim, not player, step+1)
            nim.nimming_add(ply[0], ply[1])
            evaluations.append((ply, val))
        # Return the lightweight solution trough the found ones
        return max(evaluations, key=lambda x: x[1])

    def play(self, nim: Nim):
        best_ply, _ = self.minmax(nim, player=True, step=1)
        nim.nimming_remove(best_ply[0], best_ply[1])
        self._nMoves += 1
        self._moves.append(f"{best_ply[1]} items from row {best_ply[0]}")
