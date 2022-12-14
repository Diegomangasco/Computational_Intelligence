import logging
import random
from functools import reduce
from RLAgent import Agent
from copy import deepcopy
import matplotlib.pyplot as plt

logging.getLogger().setLevel(logging.INFO)

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i*2+1 for i in range(num_rows)]
        self._k = k
        self._nElements = sum(self._rows)

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
        # Verify of the new game state is useful for the player with the nim-sum rule
        xor = reduce(lambda a, b: a ^ b, self._rows)
        if xor == 0:
            return True
        else:
            return False


class RandomPlayer:
    def __init__(self) -> None:
        self._moves = []
        self._nMoves = 0
    
    def play(self, nim: Nim, trial=0) -> None:
        # Chose a random row and a random number of pieces
        x = random.randint(0, len(nim._rows)-1)
        while nim._rows[x] == 0:
            x = random.randint(0, len(nim._rows)-1)
        y = random.randint(1, nim._rows[x])
        # Update the attributes
        if trial == 0:
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
        self._generations = 50
        self._population_size = 10
        self._genome_length = 6
        self._offspring_size = 100

    def printSolution(self) -> None:
        logging.info(f" Genetic Algorithm system won, moves have been: {self._moves}; total: {self._nMoves}")

    def strategies(self, nim: Nim, parameters: list()) -> dict:
        str = dict()
        x = parameters[0]
        y = parameters[1]
        z = parameters[2]
        possible = [(r, o) for r, c in enumerate(nim._rows) for o in range(1, c + 1)]
        flag = False
        # z is a particular parameter and requires an ad hoc initialization
        for p in possible:
            if p[0] == z:
                # If the row associated with parameter z is still alive
                flag = True
                break
        if flag == False:
            # Choose another row
            z = random.choice(possible)[0]
        possible_z = [p for p in possible if p[0] == z]
        str = {
            'x_elements_from_longest': (max(possible, key=lambda i: i[1])[0], 
            x if x<=max(possible, key=lambda i: i[1])[1] else max(possible, key=lambda i: i[1])[1]),
            'y_elements_from_smaller': (min(possible, key=lambda i: i[1])[0], 
            y if y<=min(possible, key=lambda i: i[1])[1] else min(possible, key=lambda i: i[1])[1]),
            'all_elements_from_row_z': (z, max(possible_z, key=lambda i: i[1])[1])
        }
        return str

    def mutation(self, selected, nim: Nim) -> list:
        # Random mutation of all the parameters
        selected[0] = random.randint(1, len(nim._rows))
        selected[1] = random.randint(1, len(nim._rows))
        selected[2] = random.randint(0, len(nim._rows))
        return selected

    def game(self, nim: Nim, total_games, player2, parameters: list) -> int:
        # Game simulations with a Random player
        play = random.choice([1, 2])
        win = 0
        par = []
        for i in range(0, total_games):
            table = Nim(len(nim._rows))
            while table.goal() != True:
                if play == 1:
                    r = self.strategies(table, parameters)
                    strategy = random.choice(list(r.values()))
                    table.nimming_remove(strategy[0], strategy[1])
                    play = 2
                else:
                    player2.play(table, trial=1)
                    play = 1
            if play == 2:
                win += 1
        return win

    def evolution(self, nim: Nim, player) -> tuple:
        # Randomic initilization of population
        population = [list() for _ in range(self._population_size)]
        for p in population:
            p.append(random.randint(1, len(nim._rows)))
            p.append(random.randint(1, len(nim._rows)))
            p.append(random.randint(0, len(nim._rows)))
            p.append(0.0)
        total_games = 20
        # Loop over generations
        for generation in range(self._generations):
            offspring = list()
            for i in range(self._offspring_size):
                # Select a gene
                selected = random.choice(population)
                if random.random() < 0.7:
                    # Mutation
                    selected = self.mutation(selected[0:3], nim)
                # Game simulation with a certain set of parameters
                win = self.game(nim, total_games, player, selected[0:3])
                new_fitness = win/total_games
                offspring.append([selected[0], selected[1], selected[2], new_fitness])
            population += offspring
            population = sorted(population, key=lambda i: i[3], reverse=True)[:self._population_size]
        return population[0][0:3]

    def play(self, nim: Nim, parameters: list) -> None:
        ply = random.choice(list(self.strategies(nim, parameters).values()))
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

    def minmax(self, nim: Nim, player: bool, step: int) -> tuple:
        possible = [(r, o) for r, c in enumerate(nim._rows) for o in range(1, c + 1)]
        alive_rows = []
        if player:
            for p in possible:
                if p[0] not in alive_rows:
                    alive_rows.append(p[0])
            if len(alive_rows) == 1:
                # Is there one row only?
                # A bit improvement for MinMax strategy: take all the elements from the remaining row
                nim.nimming_remove(max(possible, key=lambda x: x[1])[0], max(possible, key=lambda x: x[1])[1])
                _, val = self.minmax(nim, not player, step+1)
                nim.nimming_add(max(possible, key=lambda x: x[1])[0], max(possible, key=lambda x: x[1])[1])
                return(max(possible, key=lambda x: x[1]), val)
        # True player is the MinMax system, False player is the other player
        if not possible:
            if player:
                # No win -> the other player arrives with the table empty
                return (None, -1)
            else:
                # Win -> the MinMax system arrives with the table empty
                return (None, 1) 
        if step == self._max_depth:
            # Evaluate secure and insecure configurations when the tree exploration reaches the max depth
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
            # Restore the previous situation
            nim.nimming_add(ply[0], ply[1])
            evaluations.append((ply, val))
        if player:
            return max(evaluations, key=lambda x: x[1])
        else:
            return min(evaluations, key=lambda x: x[1])

    def play(self, nim: Nim) -> None:
        best_ply, _ = self.minmax(nim, player=True, step=1)
        nim.nimming_remove(best_ply[0], best_ply[1])
        self._nMoves += 1
        self._moves.append(f"{best_ply[1]} items from row {best_ply[0]}")


class RLSystem:
    def __init__(self, nim: Nim) -> None:
        self._wins = []
        self._epochs = []
        self._nim_steps = 0
        self._nim = nim
        self._robot = Agent(alpha=0.1, random_factor=0.4)
        self._robot_state = tuple(deepcopy(nim._rows))

    def printSolution(self, n: int) -> None:
        logging.info(f" RL system total wins: {n}")

    def get_state_and_reward(self) -> tuple:
        # If at end give 0 reward
        # If not at end give -1 reward
        return deepcopy(self._nim._rows), -1 * int(not self._nim.goal())

    def allowed_states(self) -> list:
        # A state is defined by the pieces in the rows
        possible = [(r, o) for r, c in enumerate(self._robot_state) for o in range(1, c + 1)]
        states = [list(deepcopy(self._robot_state)) for _ in possible]
        ret = []
        for i, s in enumerate(states):
            s[possible[i][0]] -= possible[i][1]
            ret.append((tuple(s), possible[i]))
        return ret

    def play(self, player, parameters=None) -> None:
        rows = len(self._nim._rows)
        number_win = 0
        number_win_local = 0
        for i in range(5000):
            win = random.choice([1, 2])
            while not self._nim.goal():
                if win == 1:
                    state, _ = self.get_state_and_reward()  # Get the current state
                    self._robot_state = deepcopy(state)
                    # Choose an action (explore or exploit)
                    action = self._robot.choose_action(self.allowed_states())
                    self._nim.nimming_remove(action[0], action[1])  # Update the nim according to the action
                    self._robot_state = deepcopy(self._nim._rows)
                    self._nim_steps += 1
                    state, reward = self.get_state_and_reward()  # Get the new state and reward
                    # Update the robot memory with state and reward
                    self._robot.update_state_history(state, reward)
                    win = 2
                else:
                    # Other player
                    if parameters:
                        player.play(self._nim, parameters)
                    else:
                        player.play(self._nim)
                    win = 1
            if win == 2: 
                # Robot win
                number_win += 1
                number_win_local += 1
            self._robot.learn()  # Robot should learn after every episode
            # Get a history of number of steps taken to plot later
            if i % 50 == 0:
                print(f"{i}: {number_win}")
                self._wins.append(number_win_local)
                self._epochs.append(i)
                number_win_local = 0
            self._nim = Nim(rows)  # Reinitialize the game
            self._nim_steps = 0
            self._robot_state = deepcopy(self._nim._rows)
        self.printSolution(number_win)
        plt.semilogy(self._epochs, self._wins, "b")
        plt.show()
