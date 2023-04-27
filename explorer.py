## EXPLORER AGENT
### @Author: Tacla, UTFPR
### It walks randomly in the environment looking for victims.

import sys
import os
import random
import time
import heapq
from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod


class Explorer(AbstractAgent):

    result = {}
    untried = {}
    unbacktracked = {}
    plan = []
    victims = {}
    action = None
    directions = {'U':(0,-1), 'UR':(1,-1), 'R':(1,0), 'DR':(1,1), 'D':(0,1), 'DL':(-1, 1), 'L':(-1,0), 'UL':(-1, -1), 'END': (0,0)}
    actions = ['U', 'UR', 'R', 'DR', 'D', 'DL', 'L', 'UL', 'END'] #Clockwork movement pattern

    """
        +x = direita
        -x = esquerda
        +y = baixo
        -y = cima
    """

    def __init__(self, env, config_file, resc):
        """ Construtor do agente random on-line
        @param env referencia o ambiente
        @config_file: the absolute path to the explorer's config file
        @param resc referencia o rescuer para poder acorda-lo
        """

        super().__init__(env, config_file)
        
        # Specific initialization for the rescuer
        self.resc = resc           # reference to the rescuer agent
        self.rtime = self.TLIM     # remaining time to explore
        self.x = 0
        self.y = 0
        self.last_x = 0
        self.last_y = 0
        self.plan_made= 0
        self.retornando = 0
        self.terminou = 0

    def neighbors(self, position):
        x, y = position
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1), (x-1, y-1), (x+1, y+1), (x-1, y+1), (x+1, y-1)]
        valid_neighbors = []
        for neighbor in neighbors:
            if neighbor in self.result and self.result[neighbor] == PhysAgent.EXECUTED:
                valid_neighbors.append(neighbor)

        return valid_neighbors
    
    def distance(self, position, neighbor):
        x1, y1 = position
        x2, y2 = neighbor
        dx, dy = abs(x1 - x2), abs(y1 - y2)
        if dx == dy:
            return 1.5
        else:
            return 1

    def heuristic(self, position, goal):
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])
    
    def A_Star(self, start, goal, neighbors, distance, heuristic):
        #Inicializa o set de explorados, a fila de prioridade e o dicionario contendo o pai de cada posicao
        explored = set()
        queue = [(self.heuristic(start, goal), start)]
        parent = {start: None}

        while queue:
            #Recebe a posicao com o menor custo estimado
            _, current = heapq.heappop(queue)

            #Se estamos no objetivo, o caminho e reconstruido e retornado
            if current == goal:
                path = []
                while current:
                    if current in parent and parent[current]:
                        dx = current[0] - parent[current][0]
                        dy = current[1] - parent[current][1]
                        path.append((dx, dy))
                        current = parent[current]
                    else:
                        break
                return path[::-1] #Inverte a lista para que o caminho seja retornado do inicio para o objetivo
            
            #Marca a posicao atual como explorada
            explored.add(current)

            #Explora os vizinhos da posicao atual
            for neighbor in self.neighbors(current):
                #Calcula a distancia de movimento
                cost = self.distance(current, neighbor)

                #Calcula o total estimado para alcancar o objetivo atraves do vizinho atual
                estimated_cost = cost + self.heuristic(neighbor, goal)

                #Verifica se o vizinho nao foi explorado e nao esta na fila
                if neighbor not in explored and neighbor not in (node[1] for node in queue):
                    heapq.heappush(queue, (estimated_cost, neighbor))
                    parent[neighbor] = current

                #Se um caminho melhor foi encontrado, atualizar a prioridade e o pai
                elif any(neighbor == node[1] for node in queue) and estimated_cost < next(node for node in queue if node[1] == neighbor)[0]:
                    index = next(i for i, node in enumerate(queue) if node[1] == neighbor)
                    queue[index] = (estimated_cost, neighbor)
                    heapq.heapify(queue)
                    parent[neighbor] = current
        
        #Se chega aqui, entao nao existe caminho
        return None
        
        
    def voltaBase(self, position, goal):

        if self.plan_made == 0:

            self.plan_made = 1
        
            path = self.A_Star(position, goal, self.neighbors, self.distance, self.heuristic)

            if path is not None:
                for i in path:
                    self.plan.append(i) 
        
        else:

            if self.plan == []:  # empty list, no more actions to do
                return False
            
            # Takes the first action of the plan (walk action) and removes it from the plan
            dx, dy = self.plan.pop(0)

            # Walk - just one step per deliberation
            self.body.walk(dx, dy)



    def dfs_Online(self):

        """
            Implementacao do metodo de busca do DFS Online, com tabelas que colocam os resultados de movimento e os locais onde estao as
            paredes e as vitimas para informar o socorrista. Os slides do professor no moodle possuem o pseudo codigo usado como base
            para a implementacao a seguir
        """

        # Movement variables
        dx = 0
        dy = 0
        movimento = 0
        voltou = 0

        if (self.x, self.y) not in self.untried:
            self.untried[(self.x, self.y)] = self.actions.copy()

        if self.action is not None and self.action != 'END':
            movement = self.directions[self.action]
            dx = movement[0]
            dy = movement[1]
            # If the position was already tested then there is nothing to be done, so we'll just pass by
            if (self.x+dx, self.y+dy) not in self.result:
                # Priority based direction
                movimento = self.body.walk(dx,dy)
                self.result[(self.x+dx,self.y+dy)] = movimento

        if self.untried[(self.x,self.y)] == []:
            if self.unbacktracked == {}:
                self.terminou = 1
                last_dx = self.last_x - self.x
                last_dy = self.last_y - self.y
                self.body.walk(last_dx,last_dy)
                return
            
            else:
                voltou = 1
                last_dx = self.last_x - self.x
                last_dy = self.last_y - self.y
                self.body.walk(last_dx,last_dy)
                self.x = self.last_x
                self.y = self.last_y

                if self.heuristic((self.x,self.y), (0,0)) >= self.rtime - 10:
                    self.retornando = 1

                lastMov = self.unbacktracked.popitem()
                self.last_x = lastMov[1][0]
                self.last_y = lastMov[1][1]


        else:
            if len(self.untried[(self.x, self.y)]) > 0 and movimento != PhysAgent.EXECUTED:
                self.action = self.untried[(self.x, self.y)].pop(0)
            else:
                self.action = None

        if movimento == PhysAgent.EXECUTED and voltou != 1:
            self.last_x = self.x
            self.last_y = self.y
            self.x = self.x + dx
            self.y = self.y + dy
            self.unbacktracked[(self.x,self.y)] = (self.last_x,self.last_y)

            if self.heuristic((self.x,self.y), (0,0)) >= self.rtime - 10:
                    self.retornando = 1

            seq = self.body.check_for_victim()

            if seq >= 0:
                vs = self.body.read_vital_signals(seq)
                #self.rtime -= self.COST_READ
                self.victims[(self.x,self.y)] = vs
                # print("exp: read vital signals of " + str(seq))
                # print(vs)

        return
    
    def deliberate(self) -> bool:
        """ The agent chooses the next action. The simulator calls this
        method at each cycle. Must be implemented in every agent"""

        # No more actions, time almost ended
        if self.rtime < 10.0: 
            # time to wake up the rescuer
            # pass the walls and the victims (here, they're empty)
            print(f"{self.NAME} I believe I've remaining time of {self.rtime:.1f}")
            self.resc.go_save_victims(self.result,self.victims)
            return False
        
        if self.retornando == 1:    #Returned to base through function
            # Takes the first action of the plan (walk action) and removes it from the plan
            self.voltaBase((self.x,self.y), (0,0))

            if self.plan == []:
                self.resc.go_save_victims(self.result,self.victims)
                return False
        
        else:                       #Walked through the whole grid and returned to base through backtracking
            if self.terminou == 0: 
                self.dfs_Online()

            else:
                self.resc.go_save_victims(self.result,self.victims)
                return False
        
        ##Professor's code##
        
        """dx = random.choice([-1, 0, 1])

        if dx == 0:
           dy = random.choice([-1, 1])
        else:
           dy = random.choice([-1, 0, 1])
        
        # Moves the body to another position
        result = self.body.walk(dx, dy)

        # Update remaining time
        if dx != 0 and dy != 0:
            self.rtime -= self.COST_DIAG
        else:
            self.rtime -= self.COST_LINE

        # Test the result of the walk action
        if result == PhysAgent.BUMPED:
            walls = 1  # build the map- to do
            # print(self.name() + ": wall or grid limit reached")

        if result == PhysAgent.EXECUTED:
            # check for victim returns -1 if there is no victim or the sequential
            # the sequential number of a found victim
            seq = self.body.check_for_victim()
            if seq >= 0:
                vs = self.body.read_vital_signals(seq)
                self.rtime -= self.COST_READ
                # print("exp: read vital signals of " + str(seq))
                # print(vs)"""
                
        return True

