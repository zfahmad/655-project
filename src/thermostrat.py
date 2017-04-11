import position as pos
import game as g
import random as rnd
import game_creator as gc
import math

class Thermostrat():
    def __init__(self, player):
        self.player = player

    def chooseOption(self, G):
    
        numSubgames = len(G.subgames)
        
        maxWidth = -1
        ambient = G.getAmbient()
#        print(ambient)

        for i in range(numSubgames):
            if G.subgames[i].widthAtT(ambient) > maxWidth:
                subgame = i
                maxWidth = G.subgames[i].widthAtT(ambient)

        options = getattr(G.subgames[subgame], self.player + "Option")
        opt = rnd.randint(0, len(options) - 1)
#        opt = 0

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

#def test():
#    G1 = gc.game_creator([[[[50, [[51], [47]]], [12, [[14], [11]]]]], [[[8, [[15], [4]]], [0, [[4], [0]]]]]])
#    G2 = gc.game_creator([[[[58, [[67], [52]]], [23, [[29], [18]]]]], [[[8, [[10], [5]]], [0, [[6], [-6]]]]]])
#
#    G = g.Game([G1, G2])
#
#    player = Thermostrat("left")
#    print(player.chooseOption(G))
#
#test()
