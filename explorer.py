## EXPLORER AGENT
### @Author: Tacla, UTFPR
### It walks randomly in the environment looking for victims.

import sys
import os
import random
from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod


class Explorer(AbstractAgent):

    result = {}
    untried = {}
    unbacktracked = {}
    #antAction = None
    action = None
    #inverter valor das tuplas na vertical, pois o grid sobe quando y é negativo
    directions = {'U':(0,-1), 'UR':(1,-1), 'R':(1,0), 'DR':(1,1), 'D':(0,1), 'DL':(-1, 1), 'L':(-1,0), 'UL':(-1, -1)}
    actions = ['U', 'UR', 'R', 'DR', 'D', 'DL', 'L', 'UL']

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

    """def dfs_Online(self):

        #Movement variables
        dx = 0
        dy = 0
        movement
        newMovement
       
        self.untried [(self.x,self.y)] = self.actions #First iteration is out of the loop

       # if goal-test(s') then return stop

        while(self.untried != None or self.unbacktracked != None):
            if (self.x,self.y) not in self.untried:
                self.untried[(self.x,self.y)] = self.actions
            if self.antAction is not None:
                if (self.x,self.y) in self.result: #If the position was already tested then there is nothing to be done, so we'll just pass by
                    pass
                else:
                    movement = self.directions[self.actions] #Priority based direction
                    dx = movement[0]
                    dy = movement[1]
                    self.result[(self.x+dx,self.y+dy)] = self.body.walk(dx,dy)
                    self.unbacktracked[(self.x,self.y)] = self.antAction
            if self.untried[(self.x,self.y)] is None:
                if self.unbacktracked[(self.x,self.y)] is None:
                    return
                else:
                    newMovement = self.unbacktracked[(self.x,self.y)]
                    self.action = newMovement.pop(0)
            else:
                newMovement = self.unbacktracked[(self.x, self.y)]
                self.action = newMovement.pop(0)
            #self.antState = newState
            self.x = self.x
            self.y = self.y
        
        return"""
    
    def deliberate(self) -> bool:
        """ The agent chooses the next action. The simulator calls this
        method at each cycle. Must be implemented in every agent"""

        # No more actions, time almost ended
        if self.rtime < 10.0: 
            # time to wake up the rescuer
            # pass the walls and the victims (here, they're empty)
            print(f"{self.NAME} I believe I've remaining time of {self.rtime:.1f}")
            self.resc.go_save_victims([],[])
            return False
        
        # Movement variables
        dx = 0
        dy = 0
        movimento = 0

        # First iteration is out of the loop
        self.untried[(self.x, self.y)] = self.actions.copy()


        if (self.x, self.y) not in self.untried:
            self.untried[(self.x, self.y)] = self.actions.copy()
        if self.action is not None:
            # If the position was already tested then there is nothing to be done, so we'll just pass by
            if (self.x, self.y) in self.result:
                pass
            else:
                # Priority based direction
                movement = self.directions[self.action]
                dx = movement[0]
                dy = movement[1]
                movimento = self.body.walk(dx,dy)
                self.result[(self.x+dx,self.y+dy)] = movimento
                self.unbacktracked[(self.x,self.y)] = self.action
        if self.untried[(self.x, self.y)] is None:
            if self.unbacktracked[(self.x, self.y)] is None:
                return
            else:
                self.action = self.unbacktracked[(self.x, self.y)].pop(0)
        else:
            if len(self.untried[(self.x, self.y)]) > 0:
                self.action = self.untried[(self.x, self.y)].pop(0)
        # self.antState = newState
        if movimento == PhysAgent.EXECUTED:
            self.x = self.x + dx
            self.y = self.y + dy
        else:
            walls = 1
        
        #self.dfs_Online(self)
        
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

