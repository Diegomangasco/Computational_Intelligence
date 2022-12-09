import random as rnd

class Agent(object):
    def __init__(self, alpha=0.15, random_factor=0.2):  # 80% explore, 20% exploit
        self._state_history = []  # state, reward
        self._alpha = alpha
        self._random_factor = random_factor
        self._G = {}

    def init_reward(self, state) -> None:
        self._G[state] = rnd.uniform(a=1.0, b=0.1)

    def choose_action(self, allowedStates) -> tuple:
        maxG = -10e15
        next_move = None
        randomN = rnd.random()
        if randomN < self._random_factor:
            # if random number below random factor, choose random action
            new_state, next_move = rnd.choice(allowedStates)
            if new_state not in self._G.keys():
                self.init_reward(new_state)
        else:
            # if exploiting, gather all possible actions and choose one with the highest G (reward)
            for state in allowedStates:
                new_state = state[0]
                if new_state not in self._G.keys():
                    self.init_reward(new_state)
                if self._G[new_state] >= maxG:
                    next_move = state[1]
                    maxG = self._G[new_state]
        return next_move

    def update_state_history(self, state, reward) -> None:
        self._state_history.append((state, reward))

    def learn(self) -> None:
        target = 0
        for prev, reward in reversed(self._state_history):
            self._G[tuple(prev)] = self._G[tuple(prev)] + self._alpha * (target - self._G[tuple(prev)])
            target += reward
        self._state_history = []
        self._random_factor -= 10e-5  # decrease random factor each episode of play
