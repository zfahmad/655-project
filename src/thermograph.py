import matplotlib.pyplot as plt
import numpy as np

def thermograph(thermoPoints):
    lPoints = thermoPoints[:, :2]
    lPoints = np.flip(lPoints, axis=0)
    
    rPoints = thermoPoints[:, 2:]
    
    plt.grid()
    
    plt.xlim(lPoints[-1,0] + 1, rPoints[0,0] - 1)
    plt.ylim(-1, lPoints[0,1] + 1)
    
    plt.xlabel("Value")
    plt.ylabel("Temperature")
    
    plt.axhline(0, color="black", alpha=0.5)
    plt.axvline(0, color="black", alpha=0.5)
    
    plt.plot(lPoints[:, 0], lPoints[:, 1], color="Blue", lw=2, alpha=0.8)
    plt.plot(rPoints[:, 0], rPoints[:, 1], color="Green", lw=2, alpha=0.8)
    plt.arrow(lPoints[0,0], lPoints[0,1], 0, 0.5, head_length=.25, head_width=0.15, color="Red", lw=2, alpha=0.8)
    
    plt.show()


def compThermograph(l, r, t, amb):
    lPoints = l

    rPoints = r
    
    plt.grid()
    
    plt.xlim(lPoints[-1] + 1, rPoints[0] - 1)
    plt.ylim(-1, t[-1] + 1)
    
    plt.xlabel("Stop")
    plt.ylabel(r"Temperature ($t$)")
    
    plt.axhline(0, color="black", alpha=0.5)
    plt.axvline(0, color="black", alpha=0.5)
    plt.axhline(amb, color="purple", alpha=0.7, ls="--", lw=2)
    
    plt.plot(lPoints, t, color="Blue", lw=2, alpha=0.8)
    plt.plot(rPoints, t, color="Green", lw=2, alpha=0.8)
    plt.arrow(lPoints[-1], t[-1], 0, 0.5, head_length=.25, head_width=0.15, color="Red", lw=2, alpha=0.8)
    
    plt.show()


def line(thermoPoints):
    plt.grid()
    
    x = thermoPoints[0][0]
    y = thermoPoints[0][3]
    
    
    plt.xlim(thermoPoints[0][0] + 1, thermoPoints[0][0] - 1)
    if y < 0:
        plt.ylim(-1.25, .25)
    else:
        plt.ylim(-.25, 1.25)
    
    plt.xlabel("Value")
    plt.ylabel("Temperature")
    
    plt.axhline(0, color="black", alpha=0.5)
    plt.axvline(0, color="black", alpha=0.5)
    
#    print(thermoPoints)

    if y > 0:
        plt.arrow(x, 0, 0, y - 0.2, head_length=0.2, head_width=0.1, color="Red", lw=2, alpha=0.8)
    else:
        plt.arrow(x, 0, 0, y + 0.2, head_length=0.2, head_width=0.1, color="Red", lw=2, alpha=0.8)
    
    plt.show()
