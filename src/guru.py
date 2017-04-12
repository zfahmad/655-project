import position as pos
import game as g
import random as rnd
import game_creator as gc
import math

class Guru():
    def __init__(self, player):
        self.player = player

    def chooseOption(self, G):
    
        numSubgames = len(G.subgames)

        if self.player == "left":
            diff = -math.inf
            
            for i in range(numSubgames):
                sgame = G.subgames[i]
                forecast = sgame.leftStop - (0.5 * sgame.temperature)
    
                options = sgame.leftOption

                for j in range(len(options)):
                
                    t_new = options[j].temperature
                    newForecast = options[j].rightStop# + (0.5 * t_new)
                    
                    if newForecast - forecast >= diff:
                        diff = newForecast - forecast
                        opt = j
                        subgame = i
        
        else:
            diff = -math.inf
            
            for i in range(numSubgames):
                sgame = G.subgames[i]
                forecast = sgame.rightStop + (0.5 * sgame.temperature)
    
                options = sgame.rightOption

                for j in range(len(options)):
                
                    t_new = options[j].temperature
                    newForecast = options[j].leftStop# - (0.5 * t_new)
                    
                    if forecast - newForecast >= diff:
                        diff = forecast - newForecast
                        opt = j
                        subgame = i

        return subgame, opt
