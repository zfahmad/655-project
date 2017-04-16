import position as pos
import pickle
import game_creator as gc
import play
import randBot as rbot
import hotstrat as hot
import thermostrat as therm
import kibitz as kib
import guru
import game as g

# Experimental stats

NUM_GAMES = 100
NUM_SUB = 5
TRIALS = 1

# Definition of bots

leftKib = kib.Kibitz("left")
rightKib = kib.Kibitz("right")

leftHot = hot.Hotstrat("left")
rightHot = hot.Hotstrat("right")

leftTherm = therm.Thermostrat("left")
rightTherm = therm.Thermostrat("right")

leftRand = rbot.RandomBot("left")
rightRand = rbot.RandomBot("right")

leftGuru = guru.Guru("left")
rightGuru = guru.Guru("right")

# Experiments

total = 0

for _ in range(TRIALS):
    
    input = open('games.in', "rb")
    
    for m in range(NUM_GAMES):
        game = []
        
        for s in range(NUM_SUB):
            line = pickle.load(input)
            game.append(gc.game_creator(line))
        
        G = g.Game(game)

        P = play.Play(G, leftTherm, rightGuru)
        P.play()
        total += P.score
        
        print("Loaded game: ", m)

    input.close()

print("Total Score: ", total / TRIALS)
print("Successfully loaded and ended all games.")
