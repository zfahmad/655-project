import position as pos
import game as g
import random as rnd
import game_creator as gc
import math

class Kibitz():
    def __init__(self, player):
        self.player = player
        self.tax = math.inf

    def chooseOption(self, G):
    
        numSubgames = len(G.subgames)
        maxTemp = -math.inf
        
        for i in range(numSubgames):

            if G.subgames[i].temperature >= maxTemp:
                subgame = i
                maxTemp = G.subgames[i].temperature
    
        if self.tax >= maxTemp:
            self.tax = maxTemp
        
        sgame = G.subgames[subgame]
        options = getattr(sgame, self.player + "Option")

        if self.player == "left":
        
            forecast = (0.5 * self.tax) + sgame.leftStop
            diff = -math.inf

            for i in range(len(options)):
                t_new = options[i].temperature
                newForecast = options[i].rightStop - (0.5 * t_new)

                if newForecast - forecast >= diff:
                    diff = newForecast - forecast
                    opt = i
        
        else:
        
            forecast = sgame.rightStop - (0.5 * self.tax)
            diff = -math.inf

            for i in range(len(options)):
                t_new = options[i].temperature
                newForecast = options[i].leftStop + (0.5 * t_new)

                if forecast - newForecast >= diff:
                    diff = forecast - newForecast
                    opt = i

        return subgame, opt
