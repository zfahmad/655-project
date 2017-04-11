import position as pos
import game as g
import random as rnd
import game_creator as gc

class RandomBot():
    def __init__(self, player):
        self.player = player

    def chooseOption(self, G):
    
        numSubgames = len(G.subgames)
#        print(numSubgames)
        subgame = rnd.randint(0, numSubgames - 1)

        options = getattr(G.subgames[subgame], self.player + "Option")
#        print(len(options))
        opt = rnd.randint(0, len(options) - 1)

        return subgame, opt

def test():
    G1 = gc.game_creator([[[[50, [[51], [47]]], [12, [[14], [11]]]]], [[[8, [[15], [4]]], [0, [[4], [0]]]]]])
    G2 = gc.game_creator([[[[58, [[67], [52]]], [23, [[29], [18]]]]], [[[8, [[10], [5]]], [0, [[6], [-6]]]]]])

    G = g.Game([G1, G2])

    player = RandomBot("left")
    print(player.chooseOption(G))

#test()
