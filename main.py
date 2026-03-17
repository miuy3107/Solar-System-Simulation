from vpython import *
import random 


# ========================================= BACKGROUND ==========================================================

scene = canvas(title="Solar System Simulation", width=1280, height=720, center=vector(0,0,0), background=color.black)

NUM_STARS = 200

for _ in range(NUM_STARS):
    x = random.uniform(-50, 50)
    y = random.uniform(-50, 50)
    z = random.uniform(-50, 50)

    sphere(
        pos=vector(x, y, z),
        radius=random.uniform(0.001, 0.1),
        color=color.white,
        emissive=True  # self-glowed 
    )

# ========================================= SOLAR SYSTEM ==========================================================
AU = 1.496e11      # meters
KM = 1000          # meters
G = 6.67e-11       # (gravitational constant) 
SCALE = 1/AU        

class Body:
    def __init__(self, name, position = [0,0,0], velocity = [0,0,0], acceleration = [0,0,0], mass = 1, radius = 0.05, color = color.white):
        self.name = name 
        # position [m]
        self.position = vector(*position)
        # velocity [m/s]
        self.velocity = vector(*velocity)
        # acceleration [m/s^2]
        self.acceleration = vector(*acceleration)  
        # mass [kg] 
        self.mass = mass
        # radius [km]
        self.radius = radius
        # color
        self.color = color
        # visual
        self.visual = sphere(
            pos=self.position * SCALE,
            radius=radius,
            color=color,
            make_trail=True,
        )

    def update_visual(self):
        if self.visual:
            self.visual.pos = self.position * SCALE
class Planet(Body):
    pass 
class Meteor(Body): 
    pass 

# convert color to rgb to easily customize 
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return vector(
        int(hex_color[0:2],16)/255,       # first 2 characters related to "r"
        int(hex_color[2:4],16)/255,       # next 2 characters related to "g"
        int(hex_color[4:6],16)/255        # last 2 characters related to "b"
    )

Sun = Body("Sun",[0, 0, 0], [0, 0, 0], mass = 1.989e30,radius=0.2,color=color.yellow) 
Sun.visual.emissive = True
local_light(pos=Sun.position * SCALE, color=color.white)

# the unit of position is in [AU] so it needs to be multiplied by AU to be [m], similarly with velocity 
# the position vector need to be perpendicular to the velocity vector ==> the planet won't fly away from the Solar system 
# position at x while velocity at y 
Mercury = Planet("Mercury",[0.39*AU,0,0.01*AU],[0,47.4*KM,0],mass=3.30e23,radius=0.0007,color=hex_to_rgb("#B3CCDB"))
Venus   = Planet("Venus",[0.72*AU,0,-0.015*AU],[0,35.0*KM,0],mass=4.87e24,radius=0.00174,color=hex_to_rgb("#F77E40"))
Earth   = Planet("Earth",[1.00*AU,0,0.02*AU],[0,29.8*KM,0],mass=5.97e24,radius=0.00183,color=hex_to_rgb("#5789E0"))
Mars    = Planet("Mars",[1.52*AU,0,-0.01*AU],[0,24.1*KM,0],mass=6.42e23,radius=0.00097,color=hex_to_rgb("#D2574B"))
Jupiter = Planet("Jupiter",[5.20*AU,0,0.03*AU],[0,13.1*KM,0],mass=1.898e27,radius=0.02010,color=hex_to_rgb("#B88D7F"))
Saturn  = Planet("Saturn",[9.58*AU,0,-0.025*AU],[0,9.7*KM,0],mass=5.683e26,radius=0.01674,color=hex_to_rgb("#875B4A"))
Uranus  = Planet("Uranus",[19.22*AU,0,0.015*AU],[0,6.8*KM,0],mass=8.681e25,radius=0.00729,color=hex_to_rgb("#9BE4EE"))
Neptune = Planet("Neptune",[30.05*AU,0,-0.02*AU],[0,5.4*KM,0],mass=1.024e26,radius=0.00708,color=hex_to_rgb("#5573E7"))
Pluto   = Planet("Pluto",[39.48*AU,0,0.01*AU],[0,4.7*KM,0],mass=1.309e22,radius=0.00034,color=hex_to_rgb("#C3C4BB"))
Meteor1 = Meteor("Meteor1",[1.5*AU, 0.3*AU, 0],[-15000, -5000, 0],1e12,radius=0.03,color=color.white)

planets = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto]
bodies = [Sun] + planets + [Meteor1] 

t = 0
dt = 3600 * 24 
while t < 365 * 24 * 3600 * 250: # Run for 250 Earth years to see Pluto move
    rate(50) 
    
    for p in planets:
        r_vec = p.position - Sun.position                           # Distance vector from the Sun to the Planet
        p.acceleration = -G * Sun.mass * norm(r_vec) / mag(r_vec)**2 # acceleration: a = -G * M_sun * r_hat / r^2
        p.velocity = p.velocity + p.acceleration * dt                              # Updatd velocity: v2 = v1 + a * dt
        p.position = p.position + p.velocity * dt                          # Updated position
        p.update_visual()
    t = t + dt           # Updated time 





    # ========================================= METEOR FEATURE ==========================================================
