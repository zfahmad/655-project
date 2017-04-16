import position as pos
import game as g
import random as rnd
import game_creator as gc
import math

class Hotstrat():
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

        options = getattr(G.subgames[subgame], self.player + "Option")
        opt = rnd.randint(0, len(options) - 1)

        if self.player == "left":
            l_t = G.subgames[subgame].lWallAtT(ambient)
            
            leastDiff = math.inf
        
            for i in range(len(options)):
                r_t = options[i].rWallAtT(ambient)
                
                if abs((r_t - ambient) - (l_t)) < leastDiff:
                    opt = i
                    leastDiff = abs((r_t - ambient) - (l_t))
                
        else:
            r_t = G.subgames[subgame].rWallAtT(ambient)
            
            leastDiff = math.inf
            
            for i in range(len(options)):
                l_t = options[i].lWallAtT(ambient)
                
                if abs((l_t + ambient) - (r_t)) < leastDiff:
                    opt = i
                    leastDiff = abs((l_t + ambient) - (r_t))
        

        return subgame, opt

