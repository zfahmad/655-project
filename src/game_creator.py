import position as pos
import numpy as np

def game_creator(state):
    if type(state) == int:
        return pos.Position(leftStop=state, rightStop=state)

    else:
        left = state[0]
        right = state[1]
        
        leftOpts = []
        for opt in left:
            leftOpts.append(game_creator(opt))

        rightOpts = []
        for opt in right:
            rightOpts.append(game_creator(opt))

        return pos.Position(leftOption=leftOpts, rightOption=rightOpts)


#def test():
#    a = game_creator([[[[50, [[50], [46]]], [38, [[42], [30]]]]], [[[1, [[3], [1]]], [0, [[7], [-4]]]]]])
#    a.plotThermograph()
#    print(a.mean, a.temperature)
#
#test()
