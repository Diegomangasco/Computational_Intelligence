Copyright **`(c)`** 2022 Diego Gasco `<diego.gasco99@gmail.com>`

# Set Covering problem

## Problem explanation
Given a number $N$ and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$, determine, if possible, $S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n})$, such that each number between $0$ and $N-1$ appears in at least one list, and that the total numbers of elements in all $L_{s_i}$ is minimum.

## Algorithm used
For solving this task I decided to adopt a Genetic Algorithm strategy.
I created a population with Individuals each one composed by a genome and a fitness: the first is a list of boolean that represents which sets from the initial list the individual is keeping, the second is an heuristic value calculated for ranking the population.
The fitness value takes in count how many elements a genome covers and how many repetitions are present in it. Then it rewards genomes that contain a solution to the problem.
The ideal optimal fitness is 2*N, where N is the size of the problem.
The idea behind the Genetic Algorithms is to create at each generation one new population, where the new individual added are the results of mutations and crossovers of the individual parents.
I chose an high randomly and low driven approach for this problem to simulate a real progression of generations in one biological species. The number on which the random approaches are based, derive from a trial and error approach that I adopted in the multiple trials that I've done. 
For the numbers that characterize the problem (the amount of individuals in a population, in an offspring, the number of generations, etc...), they can be modified for different trials and computation comfort.

## Sources
I based my solution on the search algorithm written by Professor Giovanni Squillero in the Computational Intelligence course. <br>
The link to the code shared to us during the lectures is: https://github.com/squillero/computational-intelligence/blob/master/2022-23/one-max.ipynb <br>
The solution was adapted for this specific problem. <br>

## Co-authors
I developed the code independently, but for some points about the algorithm or the Python language I compared my doubts with Amine Hamdi, a student enrolled in Computational Intelligence course.

## Results
I decided to operate with a population size of 10 individuals to speed up the beginning of the process and the filtering part at the end of each generation. <br>
Obviously the values of the parameters that I set are just the results of my trials, but it is possible that with other values the performances would be better. <br>
So be free to play with these numbers and let me know if some better solution can be found! ;) <br>

WARNING: This implementation is quite good for problems with a middle-higher number N, but it takes several time to finish if N > 600. So my suggestion is to NOT running with N > 600 (N = 600 is feasible) unless you have a lot of time! 
If you have any ideas to improve this time issue please inform me!

Performances:
* N = 5 (Generations=80, Offspring=150) &rarr; Find a solution in 4 steps; Total weight: 5; (bloat=0%)
* N = 10 (Generations=80, Offspring=150) &rarr; Find a solution in 3 steps; Total weight: 10; (bloat=0%)
* N = 20 (Generations=80, Offspring=150) &rarr; Find a solution in 4 steps; Total weight: 27; (bloat=35%)
* N = 50 (Generations=150, Offspring=100) &rarr; Find a solution in 5 steps; Total weight: 90; (bloat=80%) <br>
* N = 75 (Generations=250, Offspring=100) &rarr; Find a solution in 8 steps; Total weight: 176; (bloat=135%) <br>
* N = 100 (Generations=300, Offspring=150) &rarr; Find a solution in 8 steps; Total weight: 220; (bloat=120%) <br>
* N = 500 (Generations=300, Offspring=150) &rarr; Find a solution in 14 steps; Total weight: 2042; (bloat=308%) <br>
* N = 600 (Generations=500, Offspring=300) &rarr; Find a solution in 12 steps; Total weight: 2356; (bloat=293%) <br> 
