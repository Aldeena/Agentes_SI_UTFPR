## EXPLORER AGENT
### @Author: Tacla, UTFPR
### It walks randomly in the environment looking for victims.

import sys
import os
import random
import time
from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod


class Explorer(AbstractAgent):

    result = {}
    untried = {}
    unbacktracked = {}
    walls = {}
    victims = {}
    action = None
    directions = {'U':(0,-1), 'UR':(1,-1), 'R':(1,0), 'DR':(1,1), 'D':(0,1), 'DL':(-1, 1), 'L':(-1,0), 'UL':(-1, -1)}
    #actions = ['U', 'UR', 'R', 'DR', 'D', 'DL', 'L', 'UL'] #Clockwork movement pattern
    actions = ['U', 'R', 'D', 'L', 'UR', 'DR', 'UL', 'DL'] #New movement pattern, more efficient

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
        self.manhattanDist = 0
        self.retornando = 0
        self.terminou = 0
        #self.passos = 0

    def voltaBase(self): #Function responsible to make the agent return to base prioritizing the minimum cost possible. Brute force decisions
        """
            A ideia eh que o agente consiga voltar a base priorizando o menor custo, o que em um caso médio, seria priorizando a diagonal
            ao invés de um movimento em um eixo seguido de um movimento em outro eixo. Contudo, mesmo que movimentos no sentido oposto 
            ao objetivonao sejam bem vistos para a solução final, eles podem devem ser considerados caso o robo nao estejan encaixotado 
            em um canto do grid cercado por paredes
        """
        
                

        if self.x < 0: #Left
            if self.y < 0: #Up
                movimentos = ['UR', 'R', 'U', 'DR', 'UL', 'D', 'L', 'DL']

                for i in movimentos:
                    dx = self.directions[i][0]
                    dy = self.directions[i][1]
                    passo = self.body.walk(self.x+dx, self.y+dy)
                    if passo == PhysAgent.EXECUTED:
                        self.x = self.x + dx
                        self.y = self.y + dy
                        if dx != 0 and dy != 0:
                            self.rtime -= self.COST_DIAG
                        else:
                            self.rtime -= self.COST_LINE
                        
                        return
                
                print("Agent is in a dead end and can't move anymore! Agent will be killed!")
                return
            
            elif self.y > 0: #Down
                movimentos = ['DR', 'R', 'D', 'UR', 'DL', 'U', 'L', 'UL']

                for i in movimentos:
                    dx = self.directions[i][0]
                    dy = self.directions[i][1]
                    passo = self.body.walk(self.x+dx, self.y+dy)
                    if passo == PhysAgent.EXECUTED:
                        self.x = self.x + dx
                        self.y = self.y + dy
                        if dx != 0 and dy != 0:
                            self.rtime -= self.COST_DIAG
                        else:
                            self.rtime -= self.COST_LINE
                        
                        return
                
                print("Agent is in a dead end and can't move anymore! Agent will be killed!")
                return
            
            else: #y=0
                movimentos = ['R', 'UR', 'DR', 'U', 'D', 'DL', 'UL', 'L']

                for i in movimentos:
                    dx = self.directions[i][0]
                    dy = self.directions[i][1]
                    passo = self.body.walk(self.x+dx, self.y+dy)
                    if passo == PhysAgent.EXECUTED:
                        self.x = self.x + dx
                        self.y = self.y + dy
                        if dx != 0 and dy != 0:
                            self.rtime -= self.COST_DIAG
                        else:
                            self.rtime -= self.COST_LINE
                        
                        return
                
                print("Agent is in a dead end and can't move anymore! Agent will be killed!")
                return
            
        elif self.x > 0: #Right
            if self.y < 0: #Up
                movimentos = ['DL', 'L', 'D', 'UL', 'DR', 'U', 'R', 'UR']

                for i in movimentos:
                    dx = self.directions[i][0]
                    dy = self.directions[i][1]
                    passo = self.body.walk(self.x+dx, self.y+dy)
                    if passo == PhysAgent.EXECUTED:
                        self.x = self.x + dx
                        self.y = self.y + dy
                        if dx != 0 and dy != 0:
                            self.rtime -= self.COST_DIAG
                        else:
                            self.rtime -= self.COST_LINE
                        
                        return
                
                print("Agent is in a dead end and can't move anymore! Agent will be killed!")
                return
            
            elif self.y > 0: #Down
                movimentos = ['UL', 'L', 'U', 'DL', 'UR', 'D', 'R', 'DR']

                for i in movimentos:
                    dx = self.directions[i][0]
                    dy = self.directions[i][1]
                    passo = self.body.walk(self.x+dx, self.y+dy)
                    if passo == PhysAgent.EXECUTED:
                        self.x = self.x + dx
                        self.y = self.y + dy
                        if dx != 0 and dy != 0:
                            self.rtime -= self.COST_DIAG
                        else:
                            self.rtime -= self.COST_LINE
                        
                        return
                
                print("Agent is in a dead end and can't move anymore! Agent will be killed!")
                return
            
            else: #y=0
                movimentos = ['L', 'UL', 'DL', 'U', 'D', 'DR', 'UR', 'R']

                for i in movimentos:
                    dx = self.directions[i][0]
                    dy = self.directions[i][1]
                    passo = self.body.walk(self.x+dx, self.y+dy)
                    if passo == PhysAgent.EXECUTED:
                        self.x = self.x + dx
                        self.y = self.y + dy
                        if dx != 0 and dy != 0:
                            self.rtime -= self.COST_DIAG
                        else:
                            self.rtime -= self.COST_LINE
                        
                        return
                
                print("Agent is in a dead end and can't move anymore! Agent will be killed!")
                return
                
        else: #x=0
            if self.y < 0: #Up
                movimentos = ['D', 'DL', 'DR', 'L', 'R', 'UL', 'UR', 'U']

                for i in movimentos:
                    dy = self.directions[i][1]
                    dx = self.directions[i][0]
                    passo = self.body.walk(self.x+dx, self.y+dy)
                    if passo == PhysAgent.EXECUTED:
                        self.x = self.x + dx
                        self.y = self.y + dy
                        if dx != 0 and dy != 0:
                            self.rtime -= self.COST_DIAG
                        else:
                            self.rtime -= self.COST_LINE
                        
                        return
                
                print("Agent is in a dead end and can't move anymore! Agent will be killed!")
                return
            
            elif self.y > 0: #Down
                movimentos = ['U', 'UL', 'UR', 'L', 'R', 'DL', 'DR', 'D']

                for i in movimentos:
                    dx = self.directions[i][0]
                    dy = self.directions[i][1]
                    passo = self.body.walk(self.x+dx, self.y+dy)
                    if passo == PhysAgent.EXECUTED:
                        self.x = self.x + dx
                        self.y = self.y + dy
                        if dx != 0 and dy != 0:
                            self.rtime -= self.COST_DIAG
                        else:
                            self.rtime -= self.COST_LINE
                        
                        return
                
                print("Agent is in a dead end and can't move anymore! Agent will be killed!")
                return
            
            else: #y=0
                print("Agent already base! Time to summon the rescuer")
                return


    def dfs_Online(self):

        """
            Implementacao do metodo de busca do DFS Online, com tabelas que colocam os resultados de movimento e os locais onde estao as
            paredes e as vitimas para informar o socorrista. Os slides do professor no moodle possuem o pseudo codigo usado como base
            para a implementacao a seguir
        """

        # Movement variables
        dx = 0
        dy = 0
        movimento = -1
        voltou = 0

        if (self.x, self.y) not in self.untried:
            self.untried[(self.x, self.y)] = self.actions.copy()
        if self.action is not None:
            movement = self.directions[self.action]
            dx = movement[0]
            dy = movement[1]
            # If the position was already tested then there is nothing to be done, so we'll just pass by
            if (self.x+dx, self.y+dy) not in self.result:
                # Priority based direction
                movimento = self.body.walk(dx,dy)
                if dx != 0 and dy != 0:
                    self.rtime -= self.COST_DIAG
                else:
                    self.rtime -= self.COST_LINE
                #self.passos += 1
                self.result[(self.x+dx,self.y+dy)] = movimento
                self.unbacktracked[(self.x,self.y)] = (self.last_x,self.last_y)
        if self.untried[(self.x,self.y)] == []:
            if self.unbacktracked == {}:
                self.resc.go_save_victims([], [])
                self.terminou = 1
                return
            else:
                voltou = 1
                #print("last_x: ", self.last_x, " last_y: ", self.last_y)
                last_dx = self.last_x - self.x
                last_dy = self.last_y - self.y
                self.body.walk(last_dx,last_dy)
                if dx != 0 and dy != 0:
                    self.rtime -= self.COST_DIAG
                else:
                    self.rtime -= self.COST_LINE
                #self.passos += 1
                self.x = self.last_x
                self.y = self.last_y
                self.manhattanDist = abs(self.last_x) + abs(self.last_y)
                if self.manhattanDist >= self.rtime:
                    self.retornando = 1
                print("Manhattan Dist: ", self.manhattanDist)
                print("Tempo: ", self.rtime)
                print("Retornando: ", self.retornando)
                #time.sleep(0.1)
                #if (self.x == 0 and self.y == 0) and ((0,0) not in self.unbacktracked):
                    #self.resc.go_save_victims([], [])
                    #self.terminou = 1
                    #return
                lastMov = self.unbacktracked.popitem()
                self.last_x = lastMov[1][0]
                self.last_y = lastMov[1][1]
                #self.x = self.x + dx
                #self.y = self.y + dy
        else:
            if len(self.untried[(self.x, self.y)]) > 0 and movimento == PhysAgent.BUMPED:
                self.action = self.untried[(self.x, self.y)].pop(0)
            else:
                self.action = None

        if movimento == PhysAgent.EXECUTED and voltou != 1:
            self.last_x = self.x
            self.last_y = self.y
            self.x = self.x + dx
            self.y = self.y + dy
            self.manhattanDist = abs(self.last_x) + abs(self.last_y)
            if self.manhattanDist >= self.rtime:
                    self.retornando = 1
            print("Manhattan Dist: ", self.manhattanDist)
            print("Tempo: ", self.rtime)
            print("Retornando: ", self.retornando)
            seq = self.body.check_for_victim()
            if seq >= 0:
                vs = self.body.read_vital_signals(seq)
                self.rtime -= self.COST_READ
                print("exp: read vital signals of " + str(seq))
                print(vs)
            #time.sleep(0.1)
        else:
            walls = 1

        return
    
    def deliberate(self) -> bool:
        """ The agent chooses the next action. The simulator calls this
        method at each cycle. Must be implemented in every agent"""

        """# No more actions, time almost ended
        if self.rtime < 10.0: 
            # time to wake up the rescuer
            # pass the walls and the victims (here, they're empty)
            print(f"{self.NAME} I believe I've remaining time of {self.rtime:.1f}")
            self.resc.go_save_victims([],[])
            return False"""
        
        if self.retornando == 1:    #Returned to base through function
            if self.x != 0 or self.y != 0:
                self.voltaBase()
                time.sleep(0.2)
            else:
                return False
        else:                       #Walked through the whole grid and returned to base through backtracking
            if self.terminou == 0: 
                self.dfs_Online()
                time.sleep(0.2)
            else:
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

