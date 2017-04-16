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
    
        ambient = G.getAmbient()

        if self.player == "left":
        
            sgame = G.subgames[subgame]
            forecast = (0.5 * sgame.temperature) + sgame.leftStop

            newForecast = -math.inf
    
            options = G.subgames[subgame].leftOption

            for i in range(len(options)):
                t_new = options[i].temperature

                if options[i].rightStop - (0.5 * t_new) >= newForecast:
                    newForecast = options[i].rightStop - (0.5 * t_new)
                    opt = i
        
        else:
        
            sgame = G.subgames[subgame]
            forecast = sgame.rightStop - (0.5 * sgame.temperature)

            newForecast = math.inf
    
            options = G.subgames[subgame].rightOption

            for i in range(len(options)):
                t_new = options[i].temperature

                if options[i].leftStop + (0.5 * t_new) <= newForecast:
                    newForecast = options[i].leftStop + (0.5 * t_new)
                    opt = i

        return subgame, opt
