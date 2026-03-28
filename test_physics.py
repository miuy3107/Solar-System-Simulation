from vpython import *
from abc import ABC, abstractmethod
import random 

# ========================================= BACKGROUND ==========================================================

scene = canvas(title="Solar System Simulation (Adjusted View)", width=1280, height=720, center=vector(0,0,0), background=color.black)

NUM_STARS = 200

for _ in range(NUM_STARS):
    x = random.uniform(-100, 100) # Phóng to không gian sao
    y = random.uniform(-100, 100)
    z = random.uniform(-100, 100)

    sphere(
        pos=vector(x, y, z),
        radius=random.uniform(0.01, 0.2), # Sao to hơn
        color=color.white,
        emissive=True  # self-glowed 
    )

# ========================================= SOLAR SYSTEM CONSTANTS ==========================================================
AU = 1.496e11      # meters (vật lý)
KM = 1000          # meters
G = 6.67e-11       # gravitational constant
SCALE = 1/AU       # 1 unit in VPython = 1 AU (giữ nguyên tỷ lệ khoảng cách)
C = 3e8            # m/s    

# ========================================= SCALING MULTIPLIERS (CHỈ ĐỂ HIỂN THỊ) =========================================================
# LÀM CHO CHÚNG TO LÊN ĐỂ CÓ THỂ NHÌN THẤY
# Số này càng lớn, hành tinh trông càng to
PLANET_SCALE_MULTIPLIER = 1000.0   # Phóng đại các hành tinh 1000 lần so với bán kính bạn nhập
SUN_SCALE_MULTIPLIER = 10.0      # Phóng đại Mặt Trời 10 lần so với bán kính bạn nhập

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
        self.radius = radius                      # radius [đơn vị tùy ý, không rõ]
        self.color = color                        # color
        
        # Determine visual radius based on type and multiplier
        self.visual_radius = radius # Mặc định
        if isinstance(self, Star):
            # Với bán kính Sun bạn nhập là 0.2, nó đã khá to. 
            # Multiplier này làm nó to thêm một chút.
            self.visual_radius = radius * SUN_SCALE_MULTIPLIER
        elif isinstance(self, Planet):
            # Các hành tinh có bán kính siêu nhỏ (0.000... hoặc 0.01...).
            # Chúng cần một hệ số cực lớn để có thể nhìn thấy trên nền hàng chục AU.
            self.visual_radius = radius * PLANET_SCALE_MULTIPLIER

        # 3D visual object
        self.visual = sphere(
            pos=self.position * SCALE,
            radius=self.visual_radius, # DÙNG BÁN KÍNH PHÓNG ĐẠI ĐỂ HIỂN THỊ
            color=color,
            make_trail=True,
            # Tăng độ mượt của khối cầu để trông đẹp hơn
            rings=24 if isinstance(self, Planet) else 12 
        )
    
    def update_visual(self):
        if self.visual:
            self.visual.pos = self.position * SCALE
    

class Star(Body):
    pass

class Planet(Body):
    pass

class Meteor(Body): 
    pass 

class BlackHole(Body):
    def __init__(self, name, position, mass):
        # Ta cần một bán kính nền để tạo vật thể visual.
        # Một khối cầu có bán kính 0.2 đơn vị là đủ to.
        # Chúng ta sẽ tính Schwarzschild radius nhưng sau đó ép nó phải to để nhìn thấy.
        
        # Radius nhỏ (0.1) cho constructor cha, để BlackHole không bị auto-scale quá lớn
        super().__init__(name, position, [0,0,0], [0,0,0], mass=mass, radius=0.1, color=color.black)
        
        # Calculate Schwarzschild radius in meters (Bán kính vật lý)
        rs_meters = (2*G*self.mass)/C**2  
        
        # Convert to units of AU for visual representation (Rất rất nhỏ)
        rs_units = rs_meters * SCALE
        
        # **SỬA LỖI:** Nếu Black Hole nhỏ hơn một khối cầu 0.1 đơn vị, 
        # hãy ép nó có bán kính 0.1 để có thể nhìn thấy.
        final_visual_radius = rs_units
        if rs_units < 0.1:
            final_visual_radius = 0.1
        
        # Cập nhật bán kính hiển thị
        self.visual.radius = final_visual_radius
        
        # Black Hole không phát sáng
        self.visual.emissive = False

# Convert hex color to RGB vector to easily customize colors
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return vector(
        int(hex_color[0:2],16)/255,       # Red
        int(hex_color[2:4],16)/255,       # Green
        int(hex_color[4:6],16)/255        # Blue
    )

# GIỮ NGUYÊN BÁN KÍNH BẠN ĐÃ NHẬP. CODE SẼ TỰ ĐỘNG CHỈNH SỬA KÍNH HIỂN THỊ TRONG BODY
Sun = Star("Sun", [0, 0, 0], [0, 0, 0], [0, 0, 0], mass=1.989e30, radius=0.2, color=color.yellow) 
Sun.visual.emissive = True
local_light(pos=Sun.position * SCALE, color=color.white)

# NOTE: The missing [0, 0, 0] acceleration vector was added to the planets and meteor below to prevent the previous crash!
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

# --- TỰ ĐỘNG CHỈNH CAMERA (ZOOOM) ĐỂ BAO QUÁT HỆ MẶT TRỜI ---
# Điểm xa nhất trong hệ mặt trời là Pluto (gần 40 AU).
# Chúng ta sẽ đặt camera cách Mặt Trời khoảng 45 đơn vị để nhìn thấy mọi thứ.
scene.range = 45 

# ========================================= INTERACTIVE FEATURE ==========================================================

planet_facts = {
    "Sun": "Sun\nType: Star\nTemperature: 5778 K\nFun fact: Contains 99.86% of the Solar System's mass",
    "Mercury": "Mercury\nType: Terrestrial\nMoons: 0\nFun fact: A day is longer than a year (176 vs 88 Earth days)",
    "Venus": "Venus\nType: Terrestrial\nMoons: 0\nFun fact: Rotates backwards and is hotter than Mercury",
    "Earth": "Earth\nType: Terrestrial\nMoons: 1\nFun fact: The only known planet with life",
    "Mars": "Mars\nType: Terrestrial\nMoons: 2\nFun fact: Home to Olympus Mons, the largest volcano",
    "Jupiter": "Jupiter\nType: Gas Giant\nMoons: 95\nFun fact: Great Red Spot storm has lasted over 300 years",
    "Saturn": "Saturn\nFamous for its complex and beautiful ring system.",
    "Uranus": "Uranus\nAn ice giant that rotates on its side.",
    "Neptune": "Neptune\nThe farthest known planet from the Sun.",
    "Pluto": "Pluto\nA famous dwarf planet in the Kuiper belt.",
    "Meteor1": "Meteor1\nA rogue space rock wandering through!",
    "BlackHole": "BlackHole\nA massive distortion in space-time!"
}

# Create the hidden 2D pop-up board
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
            
    # Nới lỏng một chút vùng click (0.3 -> 0.4) do vật thể to lên
    if min_diff < 0.4: 
        if closest_body.name in planet_facts:
            new_text = planet_facts[closest_body.name]
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
        # Hide Sun
        Sun.visual.visible = False

        # Create Black Hole
        black_hole = BlackHole("BlackHole", Sun.position, Sun.mass*10)

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

        # Tránh lỗi chia cho 0 khi các vật thể ở rất gần nhau
        if dist < 1e-10: 
            continue

        total_acc += -G * other.mass * r_vec / dist**3   #newton gravitational law 

    return total_acc


t = 0
dt = 3600

print("Bắt đầu mô phỏng. Hãy dùng con lăn chuột để zoom in/out.")
print("Dùng chuột phải để xoay camera.")
print("Bấm phím 'B' để bật/tắt Black Hole.")

# Vòng lặp mô phỏng chính
while True: # Cho chạy vô tận
    rate(200) # Tăng tốc độ mô phỏng lên một chút (200) so với 50 cũ

    
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