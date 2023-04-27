##  RESCUER AGENT
### @Author: Tacla (UTFPR)
### Demo of use of VictimSim

import os
import random
from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod
from collections import deque
from node import Node
import heapq
import time
import math


## Classe que define o Agente Rescuer com um plano fixo
class Rescuer(AbstractAgent):
    victims = {}
    mapa = {}
    neighbors_list = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    dictCluster = {}
    def __init__(self, env, config_file):
        """ 
        @param env: a reference to an instance of the environment class
        @param config_file: the absolute path to the agent's config file"""

        super().__init__(env, config_file)

        # Specific initialization for the rescuer
        self.plan = []              # a list of planned actions
        self.rtime = self.TLIM      # for controlling the remaining time
        
        # Starts in IDLE state.
        # It changes to ACTIVE when the map arrives
        self.x = 0
        self.y = 0
        self.body.set_state(PhysAgent.IDLE)

        
    
    def go_save_victims(self, mapa, victims):
        """ The explorer sends the map containing the walls and
        victims' location. The rescuer becomes ACTIVE. From now,
        the deliberate method is called by the environment"""
        self.body.set_state(PhysAgent.ACTIVE)

        self.mapa = mapa
        self.victims = victims

        self.calculaCluster()

        # planning
        self.__planner()

        
    
    def __planner(self):
        """ A private method that calculates the walk actions to rescue the
        victims. Further actions may be necessary and should be added in the
        deliberata method"""

        # This is a off-line trajectory plan, each element of the list is
        # a pair dx, dy that do the agent walk in the x-axis and/or y-axis
        #self.plan.append((-1,1))
        #self.plan.append((0,1))
        #self.plan.append((1,1))
        #self.plan.append((1,0))
        #self.plan.append((1,-1))
        #self.plan.append((0,-1))
        #self.plan.append((1,1))
        #self.plan.append((-1,0))
        #self.plan.append((-1,-1))
        #self.plan.append((-1,-1))

        tile = (0,0)
        for victim in self.dictCluster.keys():
            path = self.A_Star(tile, victim, self.neighbors, self.distance, self.heuristic)
            
            tileAux = tile
            for i in path:
                self.plan.append(i)

                tileAux = (tileAux[0]+i[0], tileAux[1]+i[1])
                #if tileAux in self.dictCluster.keys():
                #    del self.dictCluster[tileAux]
            
            tile = victim
        

        #Construir caminho da última vítima até a base
        path = self.A_Star(tile, (0,0), self.neighbors, self.distance, self.heuristic)

        for i in path:
            self.plan.append(i)

            tileAux = (tileAux[0]+i[0], tileAux[1]+i[1])

        #print (self.plan)


    def calculaCluster(self):

        for victim in self.victims:
            if int(self.victims[victim][7]) == 1:
                cluster = int(self.victims[victim][7]) * 6
            elif int(self.victims[victim][7]) == 2:
                cluster = int(self.victims[victim][7]) * 3

            elif int(self.victims[victim][7]) == 3:
                cluster = int(self.victims[victim][7]) * 2

            else:
                cluster = int(self.victims[victim][7]) * 1

            x = victim[0]
            y = victim[1]
            for neighbor in self.neighbors_list:
                dx = neighbor[0]
                dy = neighbor[1]
                if (x+dx, y+dy) in self.victims:
                    if int(self.victims[victim][7]) == 1:
                        cluster = cluster + int(self.victims[victim][7]) * 6
                    elif int(self.victims[victim][7]) == 2:
                        cluster = cluster + int(self.victims[victim][7]) * 3

                    elif int(self.victims[victim][7]) == 3:
                        cluster = cluster + int(self.victims[victim][7]) * 2

                    else:
                        cluster = cluster + int(self.victims[victim][7]) * 1
            
            self.dictCluster[(x,y)] = cluster
    
        #Acabou o cao

        dictClusterOrdenado = sorted(self.dictCluster.items(), key=lambda x:x[1], reverse = True)
        self.dictCluster = dict(dictClusterOrdenado)

        return

    
    def neighbors(self, position):
        x, y = position
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1), (x-1, y-1), (x+1, y+1), (x-1, y+1), (x+1, y-1)]
        valid_neighbors = []
        for neighbor in neighbors:
            if neighbor in self.mapa and self.mapa[neighbor] == PhysAgent.EXECUTED:
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
        dx = abs(position[0] - goal[0])
        dy = abs(position[1] - goal[1])
        diagonal_moves = min(dx, dy)
        linear_moves = max(dx, dy) - diagonal_moves
        return linear_moves + diagonal_moves * 1.5
    
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
        
    def deliberate(self) -> bool:
        """ This is the choice of the next action. The simulator calls this
        method at each reasonning cycle if the agent is ACTIVE.
        Must be implemented in every agent
        @return True: there's one or more actions to do
        @return False: there's no more action to do """

        # No more actions to do
        if self.plan == []:  # empty list, no more actions to do
            return False

        # Takes the first action of the plan (walk action) and removes it from the plan
        dx, dy = self.plan.pop(0)

        # Walk - just one step per deliberation
        result = self.body.walk(dx, dy)

        self.x += dx
        self.y += dy

        # Rescue the victim at the current position
        if result == PhysAgent.EXECUTED:
            # check if there is a victim at the current position
            seq = self.body.check_for_victim()
            if seq >= 0:
                res = self.body.first_aid(seq) # True when rescued   

        return True

