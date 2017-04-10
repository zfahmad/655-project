import math
import numpy as np
import thermograph as thm


class Position():
    def __init__(self, leftOption=None, rightOption=None, leftStop=0, rightStop=0):
        self.leftOption = leftOption
        self.rightOption = rightOption
        self.leftStop = leftStop
        self.rightStop = rightStop
        self.mean = 0
        self.temperature = 0
        self.thermoPoints = []
        self.calcLeftStop()
        self.calcRightStop()
        self.calcTemp()
    

    def calcLeftStop(self):
        if not self.leftOption:
            return self.leftStop
        else:
            leftStop = -math.inf
            for option in self.leftOption:
                foundStop = option.calcRightStop()
                if foundStop > leftStop:
                    leftStop = foundStop
            self.leftStop = leftStop
            return leftStop


    def calcRightStop(self):
        if not self.rightOption:
            return self.rightStop
        else:
            rightStop = math.inf
            for option in self.rightOption:
                foundStop = option.calcLeftStop()
                if foundStop < rightStop:
                    rightStop = foundStop
            self.rightStop = rightStop
            return rightStop

            
    def posDef(self):
        if not self.leftOption:
            return self.leftStop
        else:
    
            left = []
            right = []

            for option in self.leftOption:
                left.append(option.posDef())
            
            for option in self.rightOption:
                right.append(option.posDef())
            return [left, right]


    def rWallAtT(self, t):
        rVal = list(self.thermoPoints[:, 2])
        rT = list(self.thermoPoints[: , 3])
        
        if t >= rT[-1]:
            return rVal[-1]
        elif t in rT:
            return rVal[rT.index(t)]
        else:
            ub = len(rT)
            lb = 0
            
            for i in range(len(rT)):
                if rT[i] < t:
                    lb = i
                    ub = i + 1
            
            if rVal[ub] == rVal[lb]:
                return rVal[ub]
            else:
                return rVal[lb] + (t - rT[lb])
                

    def lWallAtT(self, t):
        lVal = list(self.thermoPoints[:, 0])
        lT = list(self.thermoPoints[: , 1])
        
        if t >= lT[-1]:
            return lVal[-1]
        elif t in lT:
            return lVal[lT.index(t)]
        else:
            ub = 0
            lb = len(lT)
            
            for i in range(len(lT)):
                if lT[i] < t:
                    lb = i
                    ub = i + 1
            
            if lVal[ub] == lVal[lb]:
                return lVal[ub]
            else:
                return lVal[lb] - (t - lT[lb])


    def widthAtT(self, t):
        return self.lWallAtT(t) - self.rWallAtT(t)


    def calcTemp(self, depth=0):
        if not self.leftOption:
            if self.leftStop <= 0:
                self.temperature = 1
            else:
                self.temperature = -1
            self.mean = self.leftStop
            
            self.thermoPoints = [[self.leftStop, self.rightStop, self.mean, self.temperature]]
            return [[self.leftStop, self.rightStop, self.mean, self.temperature]]
        else:
            leftStops = []
            rightStops = []
            
            for option in self.leftOption:
                l = option.calcTemp(depth=1)
                leftStops += [[l[0][1]] + [l[0][2]] + [l[0][3]]]
            
            leftWall = np.array(leftStops)
            idx = np.argsort(leftWall[:, 0])
            leftWall = leftWall[idx]

            for option in self.rightOption:
                r = option.calcTemp(depth=1)
                rightStops += [[r[0][0]] + [r[0][2]] + [r[0][3]]]

            rightWall = np.array(rightStops)
            idx = np.argsort(rightWall[:, 0])
            rightWall = rightWall[idx]
            
#            print(leftWall)
#            print(rightWall)

            i = np.size(leftWall, axis=0) - 1
            j = 0
            vert = 0
            diag = 1

            lTraj = [leftWall[i][0], 0, leftWall[i][1], 1]
            rTraj = [rightWall[j][0], 0, rightWall[j][1], 1]
            
            if leftWall[i][0] < leftWall[i][1]:# and lTraj[1] < leftWall[i][2]:
                lTraj[3] = 0
            if rightWall[j][0] > rightWall[j][1]:# and rTraj[1] > rightWall[j][2]:
                rTraj[3] = 0
            
            leftPlot = ([[lTraj[0], lTraj[1]]])
            rightPlot = ([[rTraj[0], rTraj[1]]])
            
#            print("LW: ", leftWall)
#            print("RW: ", rightWall)
#            
#            print("LT: ", lTraj, lTraj[3])
#            print("RT: ", rTraj, rTraj[3])

            found = False

            while (i > 0 or j < np.size(rightWall, axis=0)) and not found:
#                print("LW: ", leftWall)
#                print("RW: ", rightWall)

                # Special cases
                
                if lTraj[0] < 0 and rTraj[0] > 0:
                    print("Special 1")
                    self.mean = 0
                    self.temperature = -1
                    self.thermoPoints = [[self.mean, self.mean, self.mean, self.temperature]]
                    return [[self.leftStop, self.rightStop, self.mean, self.temperature]]
                elif lTraj[0] == 0 and rTraj[0] > 1:
                    print("Special 2")
                    self.mean = 1
                    self.temperature = -1
                    self.thermoPoints = [[self.mean, self.mean, self.mean, self.temperature]]
                    return [[self.leftStop, self.rightStop, self.mean, self.temperature]]
                elif lTraj[0] < -1 and rTraj[0] == 0:
                    print("Special 3")
                    self.mean = -1
                    self.temperature = -1
                    self.thermoPoints = [[self.mean, self.mean, self.mean, self.temperature]]
                    return [[self.leftStop, self.rightStop, self.mean, self.temperature]]
                elif lTraj[0] < rTraj[0]:
                    print("Special 4")
                    choices = [lTraj[0], rTraj[0]]
                    ind = np.argmin(np.abs(choices))
                    if choices[ind] < 0:
                        choices[ind] -= 1
                    else:
                        choices[ind] += 1
                    self.mean = choices[ind]
                    self.temperature = -1
                    self.thermoPoints = [[self.mean, self.mean, self.mean, self.temperature]]
                    return [[self.leftStop, self.rightStop, self.mean, self.temperature]]


                # Normal shifting of trajectories
                
                if lTraj[3] and rTraj[3]:
                
                    # When both are diagonal
                    
                    midpoint = (lTraj[0] + rTraj[0]) / 2
                    rShift = midpoint - rTraj[0]
                    lShift = lTraj[0] - midpoint
                    
                    if i > 0:
                        if leftWall[i-1][0] > midpoint:
                            lShift = lTraj[0] - leftWall[i-1][0]
            
                    if j < np.size(rightWall, axis=0) - 1:
                        if rightWall[j+1][0] < midpoint:
                            rShift = rightWall[j+1][0] - rTraj[0]
                    
#                    print(midpoint, lShift, rShift)

                    if lShift < rShift:
                        lTraj[0] -= lShift
                        lTraj[1] += lShift
                    
                        rTraj[0] += lShift
                        rTraj[1] += lShift
                    
                        i -= 1
                        if i >= 0:
                            if lTraj[1] < leftWall[i][2]:
                                lTraj[3] = 0
                    
                        
                    elif rShift < lShift:
                        lTraj[0] -= rShift
                        lTraj[1] += rShift
                        
                        rTraj[0] += rShift
                        rTraj[1] += rShift
                        
                        j += 1
                        if j < np.size(rightWall, axis=0):
                            if rTraj[1] < rightWall[j][2]:
                                rTraj[3] = 0
                    
                    else:
                        lTraj[0] -= lShift
                        lTraj[1] += lShift
                        
                        rTraj[0] += rShift
                        rTraj[1] += rShift
                        
                        i -= 1
                        j += 1
                        
                        if not lTraj[0] == rTraj[0]:
                            if i >= 0:
                                if lTraj[1] < leftWall[i][2]:
                                    lTraj[3] = 0
                            if j < np.size(rightWall, axis=0):
                                if rTraj[1] < rightWall[j][2]:
                                    rTraj[3] = 0
                        else:
                            found = True
                                
                elif lTraj[3] and not rTraj[3]:
                
                    # When Right is Vertical
                
                    intersect = lTraj[0] - rTraj[0]
                    lShift = intersect
                
                    if i > 0:
                        if lTraj[0] - leftWall[i-1][0] < intersect:
                            lShift = lTraj[0] - leftWall[i-1][0]
                        else:
                            lShift = intersect
                    else:
                        lShift = intersect

                    rvShift = rightWall[j][2] - rTraj[1]
                    
#                    if rvShift == 0:
#                        rTraj[3] = 1
#                        break

                    if rvShift < lShift:
                        rTraj[1] += rvShift
                        
                        lTraj[0] -= rvShift
                        lTraj[1] += rvShift
                        
                        rTraj[3] = 1
                        
                    elif lShift < rvShift:
                        lTraj[0] -= lShift
                        lTraj[1] += lShift
                        
                        rTraj[1] += lShift
                        
                        i -= 1

                        if i >= 0:
                            if lTraj[1] < leftWall[i][2]:
                                lTraj[3] = 0
                                
                    else:
                        rTraj[1] += rvShift
                        
                        lTraj[0] -= rvShift
                        lTraj[1] += rvShift
                        
                        if not lTraj[0] == rTraj[0]:
                            i -= 1
                            if lTraj[1] < leftWall[i][2]:
                                lTraj[3] = 0
                            rTraj[3] = 1
                        else:
                            found = True

                elif not lTraj[3] and rTraj[3]:
#                    print("VD")

                    # When Left is Vertical
            
                    intersect = lTraj[0] - rTraj[0]
                    rShift = intersect
                
                    if j < np.size(rightWall, axis=0) - 1:
                        if rightWall[j+1][0] - rTraj[0] < intersect:
                            rShift = rightWall[j+1][0] - rTraj[0]
                        else:
                            rShift = intersect
                    else:
                        rShift = intersect

                    lvShift = leftWall[i][2] - lTraj[1]

#                    if lvShift <= 0:
#                        lTraj[3] = 1
#                        break

#                    print("Shifts: ", lvShift, rShift)

                    if lvShift < rShift:
                        lTraj[1] += lvShift
                        
                        rTraj[0] += lvShift
                        rTraj[1] += lvShift
                        
                        lTraj[3] = 1
                        
                    elif rShift < lvShift:
                        rTraj[0] += rShift
                        rTraj[1] += rShift
                        
                        lTraj[1] += rShift
                        
                        j += 1

                        if j <= np.size(rightWall, axis=0) - 1:
                            if rTraj[1] < rightWall[j][2]:
                                rTraj[3] = 0
                                
                    else:
                        lTraj[1] += lvShift
                        
                        rTraj[0] += lvShift
                        rTraj[1] += lvShift
                        
                        if not lTraj[0] == rTraj[0]:
                            j += 1
                            if rTraj[1] < rightWall[j][2]:
                                rTraj[3] = 0
                            lTraj[3] = 1
                        else:
                            found = True
                
                elif not lTraj[3] and not rTraj[3]:
                
                    # When both are Vertical
                
                    lvShift = leftWall[i][2] - lTraj[1]
                    rvShift = rightWall[j][2] - rTraj[1]
                    
                    if lvShift < rvShift:
                        lTraj[1] += lvShift
                        rTraj[1] += lvShift
                        lTraj[3] = 1
                    elif rvShift < lvShift:
                        lTraj[1] += rvShift
                        rTraj[1] += rvShift
                        rTraj[3] = 1
                    else:
                        lTraj[1] += lvShift
                        rTraj[1] += rvShift
                        rTraj[3] = 1
                        lTraj[3] = 1
                

                leftPlot = np.vstack((leftPlot, [[lTraj[0], lTraj[1]]]))
#                print("L: ", lTraj)
#                print("R: ", rTraj)
                rightPlot = np.vstack((rightPlot, [[rTraj[0], rTraj[1]]]))
                
                if lTraj[0] == rTraj[0]:
                    found = True

            self.mean = lTraj[0]
            self.temperature = lTraj[1]
            self.thermoPoints = np.hstack((leftPlot, rightPlot))
            
            
            return [[self.leftStop, self.rightStop, self.mean, self.temperature]]
    

    def plotThermograph(self):
        if np.size(self.thermoPoints, axis=0) == 1:
            thm.line(self.thermoPoints)
        else:
            thm.thermograph(self.thermoPoints)


def testStop():
    f = Position(leftStop=6, rightStop=6)
    g = Position(leftStop=1, rightStop=1)
    b = Position(leftOption=[f], rightOption=[g])
    
    h = Position(leftStop=4, rightStop=4)
    
    j = Position(leftStop=2, rightStop=2)
    k = Position(leftStop=-3, rightStop=-3)
    i = Position(leftOption=[j], rightOption=[k])
    
    l = Position(leftStop=2, rightStop=2)
    m = Position(leftStop=-4, rightStop=-4)
    
    c = Position(leftOption=[h], rightOption=[i])
    
    d = Position(leftStop=-3, rightStop=-3)
    
    e = Position(leftOption=[l], rightOption=[m])
    
    a = Position(leftOption=[b, c], rightOption=[d, e])

    print(a.mean, a.temperature)
    
    a.plotThermograph()
    print(a.posDef())
#    b.plotThermograph()
#    c.plotThermograph()
#    d.plotThermograph()
#    e.plotThermograph()
#    f.plotThermograph()
#    g.plotThermograph()
#    h.plotThermograph()
#    i.plotThermograph()
#    j.plotThermograph()
#    k.plotThermograph()
#    l.plotThermograph()
#    m.plotThermograph()

def testStop2():
    a = Position(leftStop=2, rightStop=2)
    b = Position(leftStop=4, rightStop=4)
    c = Position(leftStop=1, rightStop=1)
    d = Position(leftStop=-1, rightStop=-1)
    e = Position(leftStop=-2, rightStop=-2)
    f = Position(leftOption=[b], rightOption=[c])
    g = Position(leftOption=[d], rightOption=[e])
    h = Position(leftOption=[a, f], rightOption=[g])

    f.plotThermograph()
    h.plotThermograph()

def testData():
    a = Position(leftStop=50, rightStop=50)
    
    b = Position(leftStop=51, rightStop=51)
    c = Position(leftStop=47, rightStop=47)

    d = Position(leftStop=12, rightStop=12)

    e = Position(leftStop=14, rightStop=14)
    f = Position(leftStop=11, rightStop=11)


    g = Position(leftStop=8, rightStop=8)

    h = Position(leftStop=15, rightStop=15)
    i = Position(leftStop=4, rightStop=4)

    j = Position(leftStop=0, rightStop=0)

    k = Position(leftStop=4, rightStop=4)
    l = Position(leftStop=0, rightStop=0)


    m = Position(leftOption=[b], rightOption=[c])

    n = Position(leftOption=[e], rightOption=[f])

    o = Position(leftOption=[h], rightOption=[i])

    p = Position(leftOption=[k], rightOption=[l])

    q = Position(leftOption=[a, m], rightOption=[d, n])

    r = Position(leftOption=[g, o], rightOption=[j, p])

    s = Position(leftOption=[q], rightOption=[r])

    s.plotThermograph()
    print(s.mean, s.temperature)
    print(s.posDef())

def testData2():
    a = Position(leftStop=49, rightStop=49)
    
    b = Position(leftStop=57, rightStop=57)
    c = Position(leftStop=49, rightStop=49)

    d = Position(leftStop=46, rightStop=46)

    e = Position(leftStop=47, rightStop=47)
    f = Position(leftStop=46, rightStop=46)


    g = Position(leftStop=18, rightStop=18)
#    g.plotThermograph()

    h = Position(leftStop=18, rightStop=18)
    i = Position(leftStop=15, rightStop=15)

    j = Position(leftStop=0, rightStop=0)
#    j.plotThermograph()

    k = Position(leftStop=7, rightStop=7)
    l = Position(leftStop=-4, rightStop=-4)


    m = Position(leftOption=[b], rightOption=[c])
#    m.plotThermograph()

    n = Position(leftOption=[e], rightOption=[f])
#    n.plotThermograph()

    o = Position(leftOption=[h], rightOption=[i])
#    o.plotThermograph()

    p = Position(leftOption=[k], rightOption=[l])
#    p.plotThermograph()

    q = Position(leftOption=[a, m], rightOption=[d, n])
#    q.plotThermograph()

    r = Position(leftOption=[g, o], rightOption=[j, p])
#    r.plotThermograph()

    s = Position(leftOption=[q], rightOption=[r])
#    s.plotThermograph()

#    s.plotThermograph()
    print(s.mean, s.temperature)
    print(s.thermoPoints)
    print(s.rWallAtT(13))
    print(s.lWallAtT(13))
    print(s.widthAtT(13))


#testData2()
