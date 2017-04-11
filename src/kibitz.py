import position as pos
import game as g
import random as rnd
import game_creator as gc
import math

class Kibitz():
    def __init__(self, player):
        self.player = player

    def chooseOption(self, G):
    
        numSubgames = len(G.subgames)
        maxTemp = -1
        
        for i in range(numSubgames):

            if G.subgames[i].temperature >= maxTemp:
                subgame = i
                maxTemp = G.subgames[i].temperature

        if self.player == "left":
        
            maxForecast = -math.inf
            
            for i in range(numSubgames):
                sgame = G.subgames[i]
                if  (0.5 * maxTemp) + sgame.leftStop >= maxForecast:
                    subgame = i
                    maxForecast = (0.5 * maxTemp) + sgame.leftStop
    
            newForecast = -math.inf
    
            options = G.subgames[subgame].leftOption

            for i in range(len(options)):
                t_new = options[i].temperature

                if options[i].rightStop - (0.5 * t_new) >= newForecast:
                    newForecast = options[i].rightStop - (0.5 * t_new)
                    opt = i
        
        else:
        
            minForecast = math.inf
            
            for i in range(numSubgames):
                sgame = G.subgames[i]
                if sgame.rightStop - (0.5 * maxTemp) <= minForecast:
                    subgame = i
                    minForecast = sgame.rightStop - (0.5 * maxTemp)
    
            newForecast = math.inf
    
            options = G.subgames[subgame].rightOption

            for i in range(len(options)):
            
                t_new = options[i].temperature

                if options[i].leftStop + (0.5 * t_new) <= newForecast:
                    newForecast = options[i].leftStop + (0.5 * t_new)
                    opt = i

        return subgame, opt
