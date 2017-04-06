import position as pos
import pickle
import game_creator as gc


NUM_GAMES = 100
NUM_SUB = 5

input = open("games.in", "rb")

for m in range(NUM_GAMES):
    game = []
    
    for s in range(NUM_SUB):
        line = pickle.load(input)
#        print(line)
        game.append(gc.game_creator(line))
    print("Loaded game: ", m)
print("Successfully loaded and ended all games.")

input.close()
