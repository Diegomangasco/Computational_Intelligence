Copyright **`(c)`** 2022 Diego Gasco `<diego.gasco99@gmail.com>`

# Nim game

## Problem explanation

Write agents able to play Nim, with an arbitrary number of rows and an upper bound "k" on the number of objects that can be removed in a turn (a.k.a., subtraction game). <br>

Nim is a mathematical game of strategy in which two players take turns removing (or "nimming") objects from distinct heaps or piles (rows in my implementation). On each turn, a player must remove at least one object, and may remove any number of objects provided they all come from the same heap or pile. Depending on the version being played, the goal of the game is either to avoid taking the last object or to take the last object (in our case the goal is to take the last object).

## Code organization

I prepared my solutions with two files: one jupyter notebook file for the games, and one python file for all the tasks required. <br>
In the lib.py file I made one class for each player with useful attributes and methods. Each class has the method "play", that is used in the lab3.ipynb file for playing the games. <br>
The Genetic Algorithm System has one method, "evolve", that permits to train the model against a random player, before starting the real game (it is invoked just before the game). <br>

## Random player

The Random player simply plays with random moves between the possible ones.

## Task3.1: An agent using fixed rules based on nim-sum (i.e., an expert system)

For the first task, reading on internet, I decided to implement an Expert System that plays following the nim-sum rule. <br>
This latter says that a nim game can be win if at each turn, the player remove a certain quantity of pieces, such that the XOR operation between all the remaining rows is not equal to zero (unstable state). So the goal is to leave the table in an unstable state to the other player.
With this method we are sure to win every game, with the exception of a game played against another ExpertSystem (in this case the win depends on which player starts the game). <br>
The Expert System uses the first possible move that can bring in an unstable state. I there isn't a valid move, it choses a random one. <br> 

## Task3.2: An agent using evolved rules

For this task I decided to implement a Genetic Algorithm that is trained before a game such that a system could play by following some specific strategies. <br>
In details, this system has some hardcoded strategies that have been parametrized. The goal of the GA approach is to find the best set of parameters with some games against a Random player. <br>
Each individual is made with a genome (the parameters for the strategies) and a fitness function, that is updated after the games against the Random player (fitness=victories/total). <br>
My decision to train the GA with a Random Player everytime is that following this strategy, the GA System would probably more ready to beat against a lot of strategies (not against the nim-sum obviously) since it is trained a lot of time against a random one, that can be dummy or smart depending on the time and the moves. <br>
The set of parameters with the best fitness is taken and used for the game.

## Task3.3: An agent using minmax

The MinMax System follows the classical tree-based approach of the MinMax. Each node of the tree is a move done by MinMax System or by the opponent and the descent is recursive until one of the two player reaches the end. <br>
Due to huge dimension reasons, I had to limit the depth of the tree to obtain results in an acceptable amount of time. <br>
The recursive function evaluate all possible moves in each level and return an evaluation based on nim-sum strategy (-1 or 1 respectively for bad or good situation of MinMax System). <br>
With this method I'm trying to maximize the movements that can bring to a victory for the MinMax System and to minimize the movements that can bring to a victory for the opponent system. <br>
Another improvement that I've made is the row control at the beginning of each MinMax function call. It basically controls if in the state we are reaching, there are more than one row, if the assertion is false, the move that the System has to make is to remove all the remaining elements from the row. This control is useful both in limited-depth cases and in normal ones.    

## Task3.4: An agent using reinforcement learning

For the Reinforcement Learning System I based my solution on the one that Andrea Calabrese showed us in classroom. <br>
Obviously I adapted it to a two player game and for the Nim game itself. There are multiple runs in the games against the opponent, and in each one the RL System should learn better the moves to take. <br>
I defined the state as the combination of the move and the number of pieces that are still in the game (how many pieces the state is far from the victory?). <br>
The states are initialized with a reward that is randomly choose and updated everytime. <br>
The RL Agent is in another file for managing reasons. <br>

## Conclusions after trials

I made some trials game, but feel free to add some others and see the results! <br>
The Systems that I created seems to work well, but surely they can be improved in some ways, like adding some strategies or tuning parameters. <br>
By the way, the best Systems are surely the Expert an the MinMax ones, because they use the nim-sum rules that always brings to a win. But in some other games it can be not so simple to hardcode an optimal rule like that. So is important to think about other strategies. In this context the other approaches (RL, GA and MinMax with another evaluation rule) are useful to train an intelligent system that can beat another one.