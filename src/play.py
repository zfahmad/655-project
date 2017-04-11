import position as pos
import game as g
import random as rnd
import randBot as rbot
import game_creator as gc


class Play():

    def __init__(self, G, left, right):
        self.game = G
        self.left = left
        self.right = right
        self.current = "left"
        self.score = 0
        

    def switchPlayer(self):
        if self.current == "left":
            self.current = "right"
        else:
            self.current = "left"


    def play(self):
        end = False

        while not end:
            player = getattr(self, self.current)
            subgame, option = player.chooseOption(self.game)
            self.score += self.game.transition(subgame, option, self.current)
            self.switchPlayer()
            end = self.game.isOver()


#def test():
#    G1 = gc.game_creator([[[[50, [[51], [47]]], [12, [[14], [11]]]]], [[[8, [[15], [4]]], [0, [[4], [0]]]]]])
#    G2 = gc.game_creator([[[[58, [[67], [52]]], [23, [[29], [18]]]]], [[[8, [[10], [5]]], [0, [[6], [-6]]]]]])
#    G3 = gc.game_creator([[[[40, [[61], [62]]], [13, [[21], [18]]]]], [[[8, [[10], [-5]]], [0, [[6], [-5]]]]]])
#
#    G = g.Game([G1, G2, G3])
#
#    bot1 = rbot.RandomBot("left")
#    bot2 = rbot.RandomBot("right")
#
#    P = Play(G, bot1, bot2)
#    P.play()
#    print(P.score)
#
##test()
