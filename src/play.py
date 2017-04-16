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

