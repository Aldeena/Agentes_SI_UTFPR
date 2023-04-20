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


## Classe que define o Agente Rescuer com um plano fixo
class Rescuer(AbstractAgent):
    walls = {}
    victims = {}
    neighbors = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    dictCluster = {}
    posCluster = {}
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

        
    
    def go_save_victims(self, walls, victims):
        """ The explorer sends the map containing the walls and
        victims' location. The rescuer becomes ACTIVE. From now,
        the deliberate method is called by the environment"""
        self.body.set_state(PhysAgent.ACTIVE)

        self.walls = walls
        self.victims = victims

        #Monta o mapa descoberto
        self.min_dx = 0
        self.min_dy = 0
        self.max_dx = 0
        self.max_dy = 0

        #Organizar o que foi descoberto pelo explorador
        for p in walls:
            if p[0] < self.min_dx:
                self.min_dx = p[0] + 1
            elif p[0] > self.max_dx:
                self.max_dx = p[0] - 1

            if p[1] < self.min_dy:
                self.min_dy = p[1] + 1
            elif p[1] > self.max_dy:
                self.max_dy = p[1] - 1

        for p in victims.keys():
            if p[0] < self.min_dx:
                self.min_dx = p[0]
            elif p[0] > self.max_dx:
                self.max_dx = p[0]

            if p[1] < self.min_dy:
                self.min_dy = p[1]
            elif p[1] > self.max_dy:
                self.max_dy = p[1]

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
            path = self.AStar(tile, victim)
            
            tileAux = tile
            for i in path:
                self.plan.append(i)

                tileAux = (tileAux[0]+i[0], tileAux[1]+i[1])
                #if tileAux in self.dictCluster.keys():
                #    del self.dictCluster[tileAux]
            
            tile = victim



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
            for neighbor in self.neighbors:
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
    
    def salvaCluster(self):

            victim = self.dictCluster.keys()[0]
            x = victim[0]
            y = victim[1]

            for neighbor in self.neighbors:
                dx = neighbor[0]
                dy = neighbor[1]
                if (x+dx, y+dy) in self.victims:
                    result = self.body.walk(dx, dy)
                    if result == PhysAgent.EXECUTED:
                        # check if there is a victim at the current position
                        seq = self.body.check_for_victim()
                        if seq >= 0:
                            res = self.body.first_aid(seq) # True when rescued           
                            if res == True:
                                del self.victims[(x+dx, y+dy)]
                                result = self.body.walk(x-dx,y-dy)

    
    def distManhattan(self, source, goal):
        return ((abs(source[0]) + (abs(goal[0]))) + (abs(source[1]) + (abs(goal[1]))))

    def AStar(self, tile, victim):
        
        possibilidades = {}
        visitados = {}

        possibilidades[tile] = {'G':0, 'H':self.distManhattan(tile, victim)}

        while True:
            road = None
            F = 99999
            for i in possibilidades.keys():
                if (possibilidades[i]['G'] + possibilidades[i]['H']) < F:
                    F = possibilidades[i]['G'] + possibilidades[i]['H']
                    road = i

            if not road:
                break

            visitados[road] = possibilidades[road]
            del possibilidades[road]
            if road == victim:
                break

            movimentos = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
            for mov in movimentos:
                nextMov = (road[0] + mov[0], road[1] + mov[1])
                if nextMov in visitados.keys() or nextMov in self.walls or nextMov[0] < self.min_dx or nextMov[0] > self.max_dx or nextMov[1] < self.min_dy or nextMov[1] > self.max_dy:
                    continue

                if nextMov not in possibilidades.keys():
                    possibilidades[nextMov] = {'G':visitados[road]['G']+1, 'H':self.distManhattan(nextMov,victim),'pai':road}
                elif (visitados[road]['G']+1) < possibilidades[nextMov]['G']:
                    possibilidades[nextMov]['G'] = visitados[road]['G']+1
                    possibilidades[nextMov]['pai'] = road

        #Criar o caminho a ser percorrido pelo agente
        if not road:
            return False
        
        atual = victim
        path = []

        while not atual == tile:
            passo = (atual[0] - visitados[atual]['pai'][0], atual[1] - visitados[atual]['pai'][1])
            path.append(passo)
            atual = visitados[atual]['pai']
        return list(reversed(path))

    """def bfsplan(self, source, victims):
        rows, cols = len(matrix), len(matrix[0])
        visited = [[False] * cols for  in range(rows)]
        parents = [[None] * cols for _ in range(rows)]
        queue = deque([(source[0], source[1])])
        visited[source[0]][source[1]] = True

        for victim in victims:
            visited[victim[0]][victim[1]] = True

        while queue:
            x, y = queue.popleft()

            if (x, y) in victims:
                path = []
                while (x, y) != source:
                    path.append((x, y))
                    x, y = parents[x][y]
                path.append((x, y))
                path.reverse()
                return path

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy

                if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and matrix[nx][ny] != 0:
                    visited[nx][ny] = True
                    parents[nx][ny] = (x, y)
                    queue.append((nx, ny))

        return None"""
        
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

        print(self.dictCluster)
        print(self.posCluster)

        # Rescue the victim at the current position
        if result == PhysAgent.EXECUTED:
            # check if there is a victim at the current position
            seq = self.body.check_for_victim()
            if seq >= 0:
                res = self.body.first_aid(seq) # True when rescued           
                if res == True:
                   self.salvaCluster()

        return True

