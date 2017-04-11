import position as pos
import math
import numpy as np
import thermograph as thm
import game_creator as gc


class Game():
    def __init__(self, subgames):
        self.subgames = subgames
        self.compoundTherm()


    def compoundTherm(self):
        turnPoints = np.array([])
        lWall = np.array([])
        rWall = np.array([])
        
        for game in self.subgames:
#            print(game.thermoPoints)
            if np.size(game.thermoPoints, axis=0) == 1:
                turnPoints = np.append(turnPoints, game.thermoPoints[0][-1])
            else:
                turnPoints = np.append(turnPoints, game.thermoPoints[:, -1])
        
        turnPoints = np.unique(turnPoints)
        
#        print(turnPoints)

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
        
        self.leftWall = lWall
        self.rightWall = rWall
        self.turnPoints = turnPoints

        return lWall, rWall, turnPoints
        
    
    def getAmbient(self):
#        print(np.argmax(self.leftWall))
        return self.turnPoints[np.argmax(self.leftWall)]


    def plotTherm(self):
        thm.compThermograph(self.leftWall, self.rightWall, self.turnPoints)


    def isOver(self):
        if len(self.subgames) == 0:
            return True
        else:
            return False


    def transition(self, subgameNum, optionNum, player):
        subgame = self.subgames[subgameNum]

        options = getattr(subgame, player + "Option")
        nextState = options[optionNum]
        
        if nextState.leftOption == None:
            self.subgames.pop(subgameNum)
            scoreInc = nextState.leftStop
        else:
            self.subgames[subgameNum] = nextState
            scoreInc =  0

        self.compoundTherm()
        return scoreInc



def test():
    G1 = gc.game_creator([[[[50, [[51], [47]]], [12, [[14], [11]]]]], [[[8, [[15], [4]]], [5, [[4], [0]]]]]])
    G2 = gc.game_creator([[[[58, [[67], [52]]], [23, [[29], [18]]]]], [[[8, [[10], [5]]], [0, [[6], [-6]]]]]])

    G = Game([G1, G2])
    
    print(G.subgames[0].posDef())
#    print(G.subgames[1].posDef())
#    print(G1.thermoPoints)
#    print(G2.thermoPoints)
#    G1.plotThermograph()
#    G2.plotThermograph()
#    G.compoundTherm()
#    G.plotTherm()
#    print(G.leftWall)
#    print(G.getAmbient())
    G.transition(0, 0, "right")
    print(G.subgames[0].posDef())

    print(G.transition(0, 0, "right"))
    print(G.subgames[0].posDef())

#test()
