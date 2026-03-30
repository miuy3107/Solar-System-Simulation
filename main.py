from vpython import *
from abc import ABC, abstractmethod
import random 

# ============================================= BACKGROUND ==========================================================

scene = canvas(title="Solar System Simulation", width=1280, height=720, center=vector(0,0,0), background=color.black)

NUM_STARS = 1000

for _ in range(NUM_STARS):
    x = random.uniform(-100, 100)
    y = random.uniform(-100, 100)
    z = random.uniform(-100, 100)

    sphere(
        pos=vector(x, y, z),
        radius=random.uniform(0.001, 0.1),
        color=color.white,
        emissive=True  # self-glowed 
    )

# ============================================== SOLAR SYSTEM ==========================================================
AU = 1.496e11      # meters
KM = 1000          # meters
G = 6.67e-11       # gravitational constant
SCALE = 1/AU       
C = 3e8            # m/s    

class Body(ABC):
    def __init__(self, name, texture, position=[0,0,0], velocity=[0,0,0], acceleration=[0,0,0], mass=1, radius=0.05):
        self.name = name 

        # Check input for position
        if isinstance(position, vector):     
            self.position = position
        else:
            self.position = vector(*position)

        # Check input for velocity
        if isinstance(velocity, vector):
            self.velocity = velocity
        else:
            self.velocity = vector(*velocity)         

        # Check input for acceleration
        if isinstance(acceleration, vector):
            self.acceleration = acceleration
        else:
            self.acceleration = vector(*acceleration) 

        self.mass = mass                          
        self.radius = radius                      
        self.texture = texture            

        
        # 3D visual object
        self.visual = sphere(
            pos=self.position * SCALE,
            radius=radius,
            texture=self.texture,
            make_trail=True,
            trail_color = color.white
        )
    
    def update_visual(self):
        if self.visual:
            self.visual.pos = self.position * SCALE

    def body_type(self):
        pass 
    
class Star(Body):
    def body_type(self):
        return "Star" 
    
class Meteor(Body): 
    def body_type(self):
        return "Meteor"

class Planet(Body):
    def __init__(self, name, texture, position, velocity, acceleration, mass, radius): 
        scaled_radius = radius * 10
        super().__init__(name, texture, position, velocity, acceleration, mass=mass, radius=scaled_radius)
    def body_type(self):
        return "Planet" 

class BlackHole(Body):

    def __init__(self, name, position, mass, color):

        super().__init__(name, None, position, [0,0,0], [0,0,0], mass=mass, radius=0)
        self.radius = (2*G*self.mass)/C**2  #schwarzchild radius 
        self.color = color

        # Make it look cooler
        self.visual.emissive = False

    def body_type(self):
        return "BlackHole"


# Convert hex color to RGB vector to easily customize colors
"""def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return vector(
        int(hex_color[0:2],16)/255,       # Red
        int(hex_color[2:4],16)/255,       # Green
        int(hex_color[4:6],16)/255        # Blue
    )"""


Sun = Star("Sun","https://upload.wikimedia.org/wikipedia/commons/c/cb/Solarsystemscope_texture_2k_sun.jpg", [0, 0, 0], [0, 0, 0], [0, 0, 0], mass=1.989e30, radius=0.2) 
Sun.visual.emissive = True
local_light(pos=Sun.position * SCALE, color=color.white)

# NOTE: The missing [0, 0, 0] acceleration vector was added to the planets and meteor below to prevent the previous crash!
Mercury = Planet("Mercury", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRazoRKaLCrMI7lURGR9xv8mKxPThr38wRkjQ&s", [0.39*AU,0,0.01*AU], [0,47.4*KM,0], [0,0,0], mass=3.30e23, radius=0.0007)
Venus   = Planet("Venus", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRE7q_NoC49WiU1JYZAZdMEHD5sl_Bli3TiOw&s", [0.72*AU,0,-0.015*AU], [0,35.0*KM,0], [0,0,0], mass=4.87e24, radius=0.00174)
Earth   = Planet("Earth", "https://t3.ftcdn.net/jpg/03/64/91/04/360_F_364910470_DCjyTv7AlFX0or7TGEcJWkz7JDLnCE5G.jpg", [1.00*AU,0,0.02*AU], [0,29.8*KM,0], [0,0,0], mass=5.97e24, radius=0.00183)
Mars    = Planet("Mars","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQc0ELDdWdnToVXeznMHPNmZPjB9-jKy1p68Q&s", [1.52*AU,0,-0.01*AU], [0,24.1*KM,0], [0,0,0], mass=6.42e23, radius=0.00097)
Jupiter = Planet("Jupiter","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_ABVh6X-rxANutcMkEqX0Q6fQtFt7ERZPkQ&s", [5.20*AU,0,0.03*AU], [0,13.1*KM,0], [0,0,0], mass=1.898e27, radius=0.02010)
Saturn  = Planet("Saturn","https://upload.wikimedia.org/wikipedia/commons/1/1e/Solarsystemscope_texture_8k_saturn.jpg", [9.58*AU,0,-0.025*AU], [0,9.7*KM,0], [0,0,0], mass=5.683e26, radius=0.01674)
Uranus  = Planet("Uranus","https://upload.wikimedia.org/wikipedia/commons/9/95/Solarsystemscope_texture_2k_uranus.jpg", [19.22*AU,0,0.015*AU], [0,6.8*KM,0], [0,0,0], mass=8.681e25, radius=0.00729)
Neptune = Planet("Neptune","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5m6I1cNvdxJo1hMYBzgmMzcD1viyiItRiyg&s", [30.05*AU,0,-0.02*AU], [0,5.4*KM,0], [0,0,0], mass=1.024e26, radius=0.00708)
Pluto   = Planet("Pluto","https://planetpixelemporium.com/download/download.php?plutomap2k.jpg", [39.48*AU,0,0.01*AU], [0,4.7*KM,0], [0,0,0], mass=1.309e22, radius=0.00034)

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
    global selected_target
    click_pos = evt.pos 
    
    closest_body = None
    min_diff = float('inf')
    
    for b in bodies:
        diff = mag(click_pos - b.visual.pos) 
        
        if diff < min_diff:
            min_diff = diff
            closest_body = b
            
    if min_diff < 0.3: # 0.3 AU visual hitbox
        selected_target = closest_body
        if closest_body.name in planet_facts:
            new_text = f"{closest_body.name}\nType: {closest_body.body_type()}\n{planet_facts[closest_body.name]}"
            
            if info_board.visible and info_board.text == new_text:
                info_board.visible = False
            else:
                info_board.text = new_text
                info_board.visible = True  
    else:
        selected_target = None
        info_board.visible = False     


scene.bind('mousedown', on_mouse_click)

# ========================================= BLACK HOLE & METEOR ==========================================================

black_hole = None
is_black_hole = False
selected_target = None
pending_bodies = []

def toggle_black_hole(b):
    global Sun, black_hole, is_black_hole, bodies

    if not is_black_hole:
        Sun.visual.visible = False

        # Create Black Hole
        black_hole = BlackHole("BlackHole", Sun.position, Sun.mass*10, color.black)

        # Replace Sun in bodies list
        bodies[0] = black_hole

        is_black_hole = True

    else:
        # Remove Black Hole
        if black_hole:
            black_hole.visual.visible = False

        # Bring Sun back
        Sun.visual.visible = True

        # light 
        local_light(pos=Sun.position * SCALE, color=color.white)

        # Replace back
        bodies[0] = Sun

        is_black_hole = False

def spawn_meteor(target):
    global pending_bodies
    
    # Spawn the meteor roughly 1.5 AU away in a random direction
    offset_dir = vector(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-0.1, 0.1)).norm()
    spawn_pos = target.position + (offset_dir * AU * 1.5)
    
    # Calculate a velocity aimed right at the target
    direction = (target.position - spawn_pos).norm()
    speed = 80 * KM 
    
    vel = (direction * speed) + target.velocity 
    
    new_meteor = Meteor(
    name=f"Meteor_{random.randint(100,999)}",
    texture = None, 
    position=spawn_pos,
    velocity=vel,
    acceleration=[0,0,0],
    mass=1e15,
    radius=0.005
    )

    new_meteor.visual.color = color.white 
    new_meteor.visual.trail_color = color.red  
    
    pending_bodies.append(new_meteor)
    print(f"Meteor spawned targeting {target.name}!") 
    

#========================================== RESET BUTTON ======================================================
def reset_simulation():
    global bodies, Sun, black_hole, is_black_hole, pending_bodies, selected_target

    # Clear all visuals
    for b in bodies:
        if b.visual:
            b.visual.visible = False

    # Reset flags
    black_hole = None
    is_black_hole = False
    pending_bodies.clear()
    selected_target = None
    info_board.visible = False

    # Recreate Sun
    Sun.position = vector(0,0,0)
    Sun.velocity = vector(0,0,0)
    Sun.visual.visible = True
    Sun.visual.clear_trail()

    # Recreate planets (IMPORTANT: reset lại đúng initial)
    Mercury.position = vector(0.39*AU,0,0.01*AU)
    Mercury.velocity = vector(0,47.4*KM,0)

    Venus.position = vector(0.72*AU,0,-0.015*AU)
    Venus.velocity = vector(0,35.0*KM,0)

    Earth.position = vector(1.00*AU,0,0.02*AU)
    Earth.velocity = vector(0,29.8*KM,0)

    Mars.position = vector(1.52*AU,0,-0.01*AU)
    Mars.velocity = vector(0,24.1*KM,0)

    Jupiter.position = vector(5.20*AU,0,0.03*AU)
    Jupiter.velocity = vector(0,13.1*KM,0)

    Saturn.position = vector(9.58*AU,0,-0.025*AU)
    Saturn.velocity = vector(0,9.7*KM,0)

    Uranus.position = vector(19.22*AU,0,0.015*AU)
    Uranus.velocity = vector(0,6.8*KM,0)

    Neptune.position = vector(30.05*AU,0,-0.02*AU)
    Neptune.velocity = vector(0,5.4*KM,0)

    Pluto.position = vector(39.48*AU,0,0.01*AU)
    Pluto.velocity = vector(0,4.7*KM,0)

    # Reset trails + visuals
    for p in planets:
        p.visual.visible = True
        p.visual.clear_trail()
        p.update_visual()

    Sun.update_visual()

    # Reset bodies list
    bodies = [Sun] + planets

    # Re-add light
    local_light(pos=Sun.position * SCALE, color=color.white)

    print("Simulation reset!")


# ========================================= KEY INPUT ========================================================
def key_input(evt):
    if evt.key.lower() == 'b':
        toggle_black_hole(None)
    elif evt.key.lower() == 'm':
        if selected_target is not None:
            spawn_meteor(selected_target)
    elif evt.key.lower() == 'r':   
        reset_simulation()

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
        
    return total_acc


t = 0
dt = 3600 # 1 hour per frame 
while True:
    rate(50)
    
    if pending_bodies:
        bodies.extend(pending_bodies)
        pending_bodies.clear()
        
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