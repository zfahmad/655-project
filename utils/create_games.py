import pickle

f = open("./test_input.in", "r")
o = open("./test_games.in", "wb")

for line in f:
#    print(line)
    if not line == "\n":
        pos = []
        options = line.strip('\n').split('||')
        for i in options:
            opt = []
            i = i.replace("{", "")
            i = i.replace("}", "")
            i = i.replace("|", ",")
            l = i.split(",")
            pos.append([[[int(l[0]), [[int(l[1])], [int(l[2])]]], [int(l[3]), [[int(l[4])], [int(l[5])]]]]])
        pickle.dump(pos, o)
    
f.close()
o.close()
