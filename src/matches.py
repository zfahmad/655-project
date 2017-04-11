import position as pos
import pickle
import game_creator as gc
import play
import randBot as rbot
import hotstrat as hot
import thermostrat as therm
import kibitz as kib
import game as g


NUM_GAMES = 100
NUM_SUB = 5

input = open('games.in', "rb")

total = 0

leftKib = kib.Kibitz("left")
rightKib = kib.Kibitz("right")

leftHot = hot.Hotstrat("left")
rightHot = hot.Hotstrat("right")

leftTherm = therm.Thermostrat("left")
rightTherm = therm.Thermostrat("right")

leftRand = rbot.RandomBot("left")
rightRand = rbot.RandomBot("right")

for m in range(NUM_GAMES):
    game = []

    
    for s in range(NUM_SUB):
        line = pickle.load(input)
#        print(line)
        game.append(gc.game_creator(line))
    
    G = g.Game(game)

    P = play.Play(G, leftHot, rightRand)
    P.play()
    total += P.score
        
    print("Loaded game: ", m)
print("Total Score: ", total)
print("Successfully loaded and ended all games.")

input.close()
