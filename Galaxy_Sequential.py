# Kobe Luna
# Nbody Project

from tkinter import *
import numpy as np
import random #not needed but can use
import math #sqrt
import time
start = time.time()

root = Tk()
root.wm_title("Galaxy")

#animation widget for X and Y plane
canvas = Canvas(root, width=700, height=700, bg="black")
canvas.grid(row=0, column=0)

G = 0.5 #gravitational constant fg=g(m1,m2/r^2)
Nbodies=[]

class Body:
    #initialization
    def __init__(self, Mass, Px, Py, V):
        self.Mass = Mass #mass
        self.Px=Px #position x
        self.Py=Py #position y
        self.P=np.array([self.Px, self.Py], dtype=float) #array of x and y position from above ^^
        self.V = np.array(V, dtype=float) #velocity array
        self.Logx=[] #list of x coordinates over time
        self.Logy=[] #list of y coordinates over time
        self.R=(self.Mass/3.14)**(1/3) # 3D density (spheres)

#force of gravity
    def FG(self, otherM):
        # DV=change in velocity
        if self == otherM:
            self.DV = np.array([0,0], dtype=float) #if measuring against itself nothing changes
        else:
            self.Dist = math.sqrt((self.P[0]-otherM.P[0])**2 + (self.P[1]-otherM.P[1])**2) #distance between 2 objects
            self.DV=np.array([0,0], dtype=float)
            if self.Dist == 0: #if distance = 0 then change in velocity = 0, keeps from dividing by 0
                self.DV=0
            else:
                #force
                self.F = (-G * self.Mass * otherM.Mass / self.Dist**2) * (self.P - otherM.P) / self.Dist
                self.DV = self.F / self.Mass #force/mass
                if self.Dist < self.R + otherM.R+5: #if objects overlap, rebounding force happens
                    self.DV *= -0.5
        self.V += self.DV #velocity = total velocity

        #borders of the animation, objects bounce off of the borders to keep in the frame
        if self.P[0] < 10 + self.R:
            self.V[0] *= -0.9
            self.P[0] += 1
        if self.P[0] > 690 - self.R:
            self.V[0] *= 0.9
            self.P[0] -= 1
        if self.P[1] < 10 + self.R:
            self.V[1] *= -0.9
            self.P[1] += 1
        if self.P[1] > 690 - self.R:
            self.V[1] *= -0.9
            self.P[1] -= 1

N = 500
#random parameters for mass, x, y, velocity
for i in range(0, N):
    Nbodies.append(Body(random.randrange(200,600), random.randrange(50,650), random.randrange(50,650),[(random.randrange(-15,15)/30), (random.randrange(-15,15)/30)]))

T = 0 #timer
Tx = True

# N body animation loop
while Tx == True:
    T+=1
    canvas.delete('all')

    for Body1 in Nbodies:
        for Body2 in Nbodies:
            Body1.FG(Body2)
        Body1.P += Body1.V #velocity added to position
        #border bouncing
        if Body1.P[1] < 5:
            Body1.V[1] *= -0.5
        if Body1.P[1] > 695:
            Body1.V[1] *= -0.5
        if Body1.P[0] < 5:
            Body1.V[0] *= -0.9
        if Body1.P[0] > 695:
            Body1.V[0] *= -0.9
        canvas.create_oval(Body1.P[0] - Body1.R, Body1.P[1] - Body1.R, Body1.P[0] + Body1.R, Body1.P[1] + Body1.R, fill = 'red')
    
    canvas.update() #create frame and update loop/frame
    end = time.time()
    print("runtime of the program is: ", end - start)

    if T == 1000: #turns off animation loop after 1000 seconds
        Tx = False
mainloop()