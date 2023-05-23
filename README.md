Description from Professor Tacla's github:

# VictimSim
A simulator for testing search algorithms in rescue scenarios.
The simulator is for the course on Artificial Intelligence at UTFPR, Curitiba.
VictimSim simulates catastrophic scenarios in a simple GUI: a 2D grid where artificial agents search for victims and save them.

Some features of the simulator:
- allows one or more agents, each agent has its own color configurable by the config files (in data folder)
- detects colision of the agents with the walls and with the end of the grid (BUMPED)
- controls the scheduling of each agent by its state: ACTIVE, IDLE, TERMINATED or DEAD (only ACTIVE agents can execute actions)
- controls the executing time giving for each agent - once the time is expired, the agent dies.

The rescuer.py and explorer.py as provided in the packet as examples of use of the  main functionnalities of the simulator.
The Explorer walks randomly in the environment while the Rescuer has a stored plan. The execution is sequential. 
When the explorer finishes the task of locating and reading the vital signals of victims, it calls the Rescuer agent to start
the rescue task.


## What was done?

The project consisted on the implementation of methods that would allow the agents rescuer and explorer to walk around the map with
a concept in mind.

### Explorer

The explorer didn't have any kind of information before the execution, so he needed to figure everything out by itself, store
everything that was discovered, read the victims' vital signs and return to base. After that, the agent would send everything that
was discovered to the rescuer.

To make this happen, the participants decided to use the DFS-Online search method. Similar to the regular DFS method, but making
sure that it would be possible to make the movement. The results were stored in the dictionary, with each key being a tuple
having the content being the result of the movement. Another thing that was made was to store the victims position and their
vital signs
in another dictionary. 

Once the agent has returned to the base, everything is sent to the rescuer


### Rescuer

The rescuer had has preview information the map discovered by the explorer, with possible positions, walls, and grid limitations
and also had the victims positions.

- #### Who to save first?
With all of this in mind, the agent used a cluster concept, where each victim would be scanned on their around looking for
another victims as well. The clusters with higher values of gravity would be prioritised and everything would be stored in a
gravity descendent order

- #### Path construction
The rescuer agent used the A* method to create the optimal path to the first victim to be saved, then the second, then the third
and the process repeats until the last victim. On the last victim, it is constructed the optimal path to the base.

- #### Heuristic
To make the estimation accurate, it was used the diagonal distance heuristic, because the agent has the possibility to move in
all 8 directions of the grid.


It is important to inform that the rescuer does not return to base while all the victims are safe, and the explorer return is 
by backtracking. Which results in a higher chance of agents death occur.
