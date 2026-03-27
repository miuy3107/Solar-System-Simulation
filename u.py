from vpython import *
import random 
from abc import ABC, abstractmethod

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
G = 6.67e-11       # gravitational constant
SCALE = 1/AU       
C = 3e8            # m/s    

class Body(ABC):
    def __init__(self, name, position=[0,0,0], velocity=[0,0,0], acceleration=[0,0,0], mass=1, radius=0.05, color=color.white):
        self.name = name 

        if isinstance(position, vector):     #check input
            self.position = position
        else:
            self.position = vector(*position)

        self.velocity = vector(*velocity)         # velocity [m/s]
        self.acceleration = vector(*acceleration) # acceleration [m/s^2]
        self.mass = mass                          # mass [kg] 
        self.radius = radius                      # radius [km]
        self.color = color                        # color
        
        # 3D visual object
        self.visual = sphere(
            pos=self.position * SCALE,
            radius=radius,
            color=color,
            make_trail=True,
        )

    def update_visual(self):
        if self.visual:
            self.visual.pos = self.position * SCALE

    @abstractmethod
    def body_type(self):
        pass

class Star(Body):
    def body_type(self):
        return "Star"

class Planet(Body):
    def body_type(self):
        return "Planet"

class Meteor(Body): 
    def body_type(self):
        return "Meteor"

class BlackHole(Body):
    def __init__(self, name, position, mass):
        super().__init__(name, position, [0,0,0], [0,0,0], mass=mass, radius=0, color=color.black)
        self.radius = (2*G*self.mass)/C**2  #schwarzchild radius 
        self.visual.emissive = False

   

# Convert hex color to RGB vector to easily customize colors
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return vector(
        int(hex_color[0:2],16)/255,       # Red
        int(hex_color[2:4],16)/255,       # Green
        int(hex_color[4:6],16)/255        # Blue
    )

# Instantiate the objects (NOTICE: Sun is now a Star!)
Sun = Star("Sun", [0, 0, 0], [0, 0, 0], [0, 0, 0], mass=1.989e30, radius=0.2, color=color.yellow) 
Sun.visual.emissive = True
local_light(pos=Sun.position * SCALE, color=color.white)

Mercury = Planet("Mercury", [0.39*AU,0,0.01*AU], [0,47.4*KM,0], [0,0,0], mass=3.30e23, radius=0.0007, color=hex_to_rgb("#B3CCDB"))
Venus   = Planet("Venus", [0.72*AU,0,-0.015*AU], [0,35.0*KM,0], [0,0,0], mass=4.87e24, radius=0.00174, color=hex_to_rgb("#F77E40"))
Earth   = Planet("Earth", [1.00*AU,0,0.02*AU], [0,29.8*KM,0], [0,0,0], mass=5.97e24, radius=0.00183, color=hex_to_rgb("#5789E0"))
Mars    = Planet("Mars", [1.52*AU,0,-0.01*AU], [0,24.1*KM,0], [0,0,0], mass=6.42e23, radius=0.00097, color=hex_to_rgb("#D2574B"))
Jupiter = Planet("Jupiter", [5.20*AU,0,0.03*AU], [0,13.1*KM,0], [0,0,0], mass=1.898e27, radius=0.02010, color=hex_to_rgb("#B88D7F"))
Saturn  = Planet("Saturn", [9.58*AU,0,-0.025*AU], [0,9.7*KM,0], [0,0,0], mass=5.683e26, radius=0.01674, color=hex_to_rgb("#875B4A"))
Uranus  = Planet("Uranus", [19.22*AU,0,0.015*AU], [0,6.8*KM,0], [0,0,0], mass=8.681e25, radius=0.00729, color=hex_to_rgb("#9BE4EE"))
Neptune = Planet("Neptune", [30.05*AU,0,-0.02*AU], [0,5.4*KM,0], [0,0,0], mass=1.024e26, radius=0.00708, color=hex_to_rgb("#5573E7"))
Pluto   = Planet("Pluto", [39.48*AU,0,0.01*AU], [0,4.7*KM,0], [0,0,0], mass=1.309e22, radius=0.00034, color=hex_to_rgb("#C3C4BB"))

planets = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto]
bodies = [Sun] + planets

# ========================================= INTERACTIVE FEATURE ==========================================================

planet_facts = {
    "Sun": "Temperature: 5778 K\nFun fact: Contains 99.86% of the Solar System's mass",
    "Mercury": "Moons: 0\nFun fact: A day is longer than a year (176 vs 88 Earth days)",
    "Venus": "Moons: 0\nFun fact: Rotates backwards and is hotter than Mercury",
    "Earth": "Moons: 1\nFun fact: The only known planet with life",
    "Mars": "Moons: 2\nFun fact: Home to Olympus Mons, the largest volcano",
    "Jupiter": "Moons: 95\nFun fact: Great Red Spot storm has lasted over 300 years",
    "Saturn": "Famous for its complex and beautiful ring system.",
    "Uranus": "An ice giant that rotates on its side.",
    "Neptune": "The farthest known planet from the Sun.",
    "Pluto": "A famous dwarf planet in the Kuiper belt.",
}

info_board = label(visible=False, xoffset=60, yoffset=50, space=30, height=25, border=4, font='sans')

def on_mouse_click(evt):
    click_pos = evt.pos 
    click_dist = mag(click_pos) 
    
    closest_body = None
    min_diff = float('inf')
    
    for b in bodies:
        body_dist = mag(b.visual.pos) 
        diff = abs(click_dist - body_dist)
        
        if diff < min_diff:
            min_diff = diff
            closest_body = b
            
    if min_diff < 0.3: 
        if closest_body.name in planet_facts:
            new_text = f"{closest_body.name}\nType: {closest_body.body_type()}\n{planet_facts[closest_body.name]}"
            
            if info_board.visible and info_board.text == new_text:
                info_board.visible = False
            else:
                info_board.text = new_text
                info_board.visible = True  
    else:
        info_board.visible = False     

scene.bind('mousedown', on_mouse_click)

# ========================================= BLACK HOLE ==========================================================

black_hole = None
is_black_hole = False

def toggle_black_hole(b):
    global Sun, black_hole, is_black_hole, bodies

    if not is_black_hole:
        Sun.visual.visible = False
        black_hole = BlackHole("BlackHole", Sun.position, Sun.mass*10)
        bodies[0] = black_hole
        is_black_hole = True
    else:
        if black_hole:
            black_hole.visual.visible = False
        Sun.visual.visible = True
        local_light(pos=Sun.position * SCALE, color=color.white)
        bodies[0] = Sun
        is_black_hole = False
    
def key_input(evt):
    if evt.key.lower() == 'b':
        toggle_black_hole(None)

scene.bind('keydown', key_input)

# ========================================= MAIN LOOP ==========================================================

def compute_acceleration(p, bodies, G):
    total_acc = vector(0, 0, 0)
    for other in bodies:
        if p is other:
            continue
        r_vec = p.position - other.position
        dist = mag(r_vec)
        if dist < 1e-5:
            continue
        total_acc += -G * other.mass * r_vec / dist**3   
        
    # THIS RETURN STATEMENT IS CRITICAL! If this is missing or indented wrong, it causes the NoneType error!
    return total_acc


t = 0
dt = 3600 * 24 

while t < 365 * 24 * 3600 * 250:
    rate(50)
    
    for p in bodies:
        p.acceleration = compute_acceleration(p, bodies, G)

    for p in bodies:
        p.position += p.velocity * dt + 0.5 * p.acceleration * dt**2

    new_acc_list = []
    for p in bodies:
        new_acc_list.append(compute_acceleration(p, bodies, G))

    for i, p in enumerate(bodies):
        p.velocity += 0.5 * (p.acceleration + new_acc_list[i]) * dt

    for i, p in enumerate(bodies):
        p.acceleration = new_acc_list[i]

    for p in bodies:
        p.update_visual()

    t += dt