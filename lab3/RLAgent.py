import random as rnd

ACTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}


class Agent(object):
    def __init__(self, states, alpha=0.15, random_factor=0.2):  # 80% explore, 20% exploit
        self._state_history = [((0, 0), 0)]  # state, reward
        self._alpha = alpha
        self._random_factor = random_factor
        self._G = {}
        self.init_reward(states)

    def init_reward(self, states) -> None:
        for action in states:
            self._G[(action[0], action[1])] = rnd.uniform(a=1.0, b=0.1)

    def choose_action(self, allowedMoves) -> tuple:
        maxG = -10e15
        next_move = None
        randomN = rnd.random()
        if randomN < self._random_factor:
            # if random number below random factor, choose random action
            next_move = rnd.choice(allowedMoves)
        else:
            # if exploiting, gather all possible actions and choose one with the highest G (reward)
            for action in allowedMoves:
                new_state = action[0]
                if self._G[new_state] >= maxG:
                    next_move = action
                    maxG = self._G[new_state]
        return next_move

    def update_state_history(self, state, reward) -> None:
        self._state_history.append((state, reward))

    def learn(self) -> None:
        target = 0
        for prev, reward in reversed(self._state_history):
            self._G[prev[0]] = self._G[prev[0]] + self._alpha * (target - self._G[prev[0]])
            target += reward
        self._state_history = []
        self._random_factor -= 10e-5  # decrease random factor each episode of play
