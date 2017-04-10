import position as pos
import math
import numpy as np
import thermograph as thm
import game_creator as gc


class Game():
    def __init__(self, subgames):
        self.subgames = subgames
        l, r, t = self.compoundTherm()
        self.leftWall = l
        self.rightWall = r
        self.turnPoints = t


    def compoundTherm(self):
        turnPoints = np.array([])
        lWall = np.array([])
        rWall = np.array([])
        
        for game in self.subgames:
            turnPoints = np.append(turnPoints, game.thermoPoints[:, -1])
        
        turnPoints = np.unique(turnPoints)
        
        print(turnPoints)

        for temp in turnPoints:
            rs = 0
            ls = 0
            width = 0
            
            
            for game in self.subgames:
                rs += game.rWallAtT(temp)
                
                if game.widthAtT(temp) >= width:
                    width = game.widthAtT(temp)
            
            rWall = np.append(rWall, rs)
            ls = rs + width
            lWall = np.append(lWall, ls)

        return lWall, rWall, turnPoints
        
    
    def getAmbient(self):
        return self.turnPoints[np.argmax(self.leftWall)]


    def plotTherm(self):
        thm.compThermograph(self.leftWall, self.rightWall, self.turnPoints)



def test():
    G1 = gc.game_creator([[[[50, [[51], [47]]], [12, [[14], [11]]]]], [[[8, [[15], [4]]], [0, [[4], [0]]]]]])
    G2 = gc.game_creator([[[[58, [[67], [52]]], [23, [[29], [18]]]]], [[[8, [[10], [5]]], [0, [[6], [-6]]]]]])

    G = Game([G1, G2])
    print(G1.thermoPoints)
    print(G2.thermoPoints)
    G1.plotThermograph()
    G2.plotThermograph()
    G.compoundTherm()
    G.plotTherm()
    print(G.leftWall)
    print(G.getAmbient())

test()
