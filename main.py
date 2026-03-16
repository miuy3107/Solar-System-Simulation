AU = 1.496e11      # meters
KM = 1000          # meters

class Body:
    def __init__(self, name, x, y, vx, vy, ax = 0, ay = 0, mass = 1):
        self.name = name 
        #position [m]
        self.x = x
        self.y = y
        #velocity [m/s]
        self.vx = vx
        self.vy = vy
        #acceleration [m/s^2]
        self.ax = ax
        self.ay = ay
        #mass [kg] 
        self.mass = mass

class Planet(Body):
    pass 
class Meteor(Body): 
    pass 

Sun = Body("Sun",0, 0, 0, 0, mass = 1.989e30) 
#the unit of position is in [AU] so it needs to be multiplied by AU to be [m], similarly with velocity 
Mercury = Planet("Mercury",0.39*AU,0,0,47.4*KM,mass=3.30e23)
Venus   = Planet("Venus",0.72*AU,0,0,35.0*KM,mass=4.87e24)
Earth   = Planet("Earth",1.00*AU,0,0,29.8*KM,mass=5.97e24)
Mars    = Planet("Mars",1.52*AU,0,0,24.1*KM,mass=6.42e23)
Jupiter = Planet("Jupiter",5.20*AU,0,0,13.1*KM,mass=1.898e27)
Saturn  = Planet("Saturn",9.58*AU,0,0,9.7*KM,mass=5.683e26)
Uranus  = Planet("Uranus",19.22*AU,0,0,6.8*KM,mass=8.681e25)
Neptune = Planet("Neptune",30.05*AU,0,0,5.4*KM,mass=1.024e26)
Pluto   = Planet("Pluto",39.48*AU,0,0,4.7*KM,mass=1.309e22)

planets = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto]
bodies = [Sun] + planets
