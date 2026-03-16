from vpython import *
<<<<<<< HEAD
import random 

=======
>>>>>>> 2093dbf4b0cacac91ce13adfec566d866e5a8b37
AU = 1.496e11      # meters
KM = 1000          # meters
G = 6.67e-11       #( gravitational constant ) 
class Body:
<<<<<<< HEAD
    def __init__(self, name, x, y, z, vx, vy, vz, ax = 0, ay = 0, az = 0, mass = 1):
=======
    def __init__(self, name, x, y, z, vx, vy, vz, ax = 0, ay = 0, mass = 1):
>>>>>>> 2093dbf4b0cacac91ce13adfec566d866e5a8b37
        self.name = name 
        #position [m]
        self.x = x
        self.y = y
        self.z = z
        #velocity [m/s]
        self.vx = vx
        self.vy = vy
        self.vz = vz
        #acceleration [m/s^2]
        self.ax = ax
        self.ay = ay
        self.az = az 
        #mass [kg] 
        self.mass = mass

class Planet(Body):
    pass 
class Meteor(Body): 
    pass 

Sun = Body("Sun",0, 0, 0, 0, 0, 0, mass = 1.989e30) 
#the unit of position is in [AU] so it needs to be multiplied by AU to be [m], similarly with velocity 
Mercury = Planet("Mercury",0.39*AU,0,0,47.4*KM,0,mass=3.30e23)
Venus   = Planet("Venus",0.72*AU,0,0,35.0*KM,0,mass=4.87e24)
Earth   = Planet("Earth",1.00*AU,0,0,29.8*KM,0,mass=5.97e24)
Mars    = Planet("Mars",1.52*AU,0,0,24.1*KM,0,mass=6.42e23)
Jupiter = Planet("Jupiter",5.20*AU,0,0,13.1*KM,0,mass=1.898e27)
Saturn  = Planet("Saturn",9.58*AU,0,0,9.7*KM,0,mass=5.683e26)
Uranus  = Planet("Uranus",19.22*AU,0,0,6.8*KM,0,mass=8.681e25)
Neptune = Planet("Neptune",30.05*AU,0,0,5.4*KM,0,mass=1.024e26)
Pluto   = Planet("Pluto",39.48*AU,0,0,4.7*KM,0,mass=1.309e22)

planets = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto]
bodies = [Sun] + planets

<<<<<<< HEAD
=======
sun = sphere(pos=vector(0,0,0), radius=AU/10, color=color.yellow)
mercury = sphere(pos=vector(0.39*AU, 0, 0), radius=AU/40, color=color.gray(0.5), make_trail=True)
mercury.v = vector(0, 47.4*KM, 0)
venus = sphere(pos=vector(0.72*AU, 0, 0), radius=AU/40, color=color.orange, make_trail=True)
venus.v = vector(0, 35.0*KM, 0)
earth = sphere(pos=vector(1.00*AU, 0, 0), radius=AU/40, color=color.blue, make_trail=True)
earth.v = vector(0, 29.8*KM, 0)
mars = sphere(pos=vector(1.52*AU, 0, 0), radius=AU/40, color=color.red, make_trail=True) #light streak when object move 
mars.v = vector(0, 24.1*KM, 0)
jupiter = sphere(pos=vector(5.20*AU, 0, 0), radius=AU/25, color=color.cyan, make_trail=True)
jupiter.v = vector(0, 13.1*KM, 0)
saturn = sphere(pos=vector(9.58*AU, 0, 0), radius=AU/30, color=color.white, make_trail=True)
saturn.v = vector(0, 9.7*KM, 0)
uranus = sphere(pos=vector(19.22*AU, 0, 0), radius=AU/35, color=color.green, make_trail=True)
uranus.v = vector(0, 6.8*KM, 0)
neptune = sphere(pos=vector(30.05*AU, 0, 0), radius=AU/35, color=color.blue, make_trail=True)
neptune.v = vector(0, 5.4*KM, 0)
pluto = sphere(pos=vector(39.48*AU, 0, 0), radius=AU/50, color=color.gray(0.7), make_trail=True)
pluto.v = vector(0, 4.7*KM, 0)
>>>>>>> 2093dbf4b0cacac91ce13adfec566d866e5a8b37
t = 0
dt = 3600 * 24 
while t < 365 * 24 * 3600 * 250: # Run for 250 Earth years to see Pluto move
    rate(100) 
    
    for p in planets:
        r_vec = p.pos - sun.pos                           # Distance vector from the Sun to the Planet
        p.a = -G * sun.mass * norm(r_vec) / mag(r_vec)**2 # acceleration: a = -G * M_sun * r_hat / r^2
        p.v = p.v + p.a * dt                              # Updatd velocity: v2 = v1 + a * dt
        p.pos = p.pos + p.v * dt                          # Updated position
    t = t + dt