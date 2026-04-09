from abc import ABC, abstractmethod
import math
import random
from typing import Any, Sequence

from vpython import canvas, color, dot, label, local_light, mag, rate, sphere, vector


AU = 1.496e11
KM = 1_000
G = 6.67e-11
SCALE = 1 / AU
C = 3e8


def to_vector(value: vector | Sequence[float], name: str) -> vector:
    """Convert supported vector inputs into a VPython vector."""
    if isinstance(value, vector):
        return value
    if not isinstance(value, Sequence) or len(value) != 3:
        raise TypeError(f"{name} must be a VPython vector or a 3-item sequence")
    return vector(float(value[0]), float(value[1]), float(value[2]))


class Body(ABC):
    """Abstract celestial body with state, rendering, and update behavior."""

    def __init__(
        self,
        name: str,
        texture: str | None,
        position: vector | Sequence[float] = (0.0, 0.0, 0.0),
        velocity: vector | Sequence[float] = (0.0, 0.0, 0.0),
        acceleration: vector | Sequence[float] = (0.0, 0.0, 0.0),
        mass: float = 1.0,
        radius: float = 0.05,
    ) -> None:
        self.name = name
        self.mass = float(mass)
        self.radius = float(radius)
        self.texture = texture
        self._position = to_vector(position, "position")
        self._velocity = to_vector(velocity, "velocity")
        self._acceleration = to_vector(acceleration, "acceleration")

        self.visual = sphere(
            pos=self._position * SCALE,
            radius=self.radius,
            texture=self.texture,
            make_trail=True,
            trail_color=color.white,
        )

    @property
    def position(self) -> vector:
        return self._position

    @position.setter
    def position(self, value: vector | Sequence[float]) -> None:
        self._position = to_vector(value, "position")

    @property
    def velocity(self) -> vector:
        return self._velocity

    @velocity.setter
    def velocity(self, value: vector | Sequence[float]) -> None:
        self._velocity = to_vector(value, "velocity")

    @property
    def acceleration(self) -> vector:
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value: vector | Sequence[float]) -> None:
        self._acceleration = to_vector(value, "acceleration")

    def update_visual(self) -> None:
        self.visual.pos = self._position * SCALE

    @abstractmethod
    def body_type(self) -> str:
        """Return a body category name for behavior routing."""


class Star(Body):
    def body_type(self) -> str:
        return "Star"


class Meteor(Body):
    def body_type(self) -> str:
        return "Meteor"


class Planet(Body):
    def __init__(
        self,
        name: str,
        texture: str,
        position: vector | Sequence[float],
        velocity: vector | Sequence[float],
        acceleration: vector | Sequence[float],
        mass: float,
        radius: float,
        semi_major_axis: float,
        eccentricity: float,
    ) -> None:
        super().__init__(
            name=name,
            texture=texture,
            position=position,
            velocity=velocity,
            acceleration=acceleration,
            mass=mass,
            radius=radius * 10,
        )
        self.semi_major_axis = float(semi_major_axis)
        self.eccentricity = float(eccentricity)

    def body_type(self) -> str:
        return "Planet"


class BlackHole(Body):
    def __init__(self, name: str, position: vector | Sequence[float], mass: float) -> None:
        radius_scene_units = (2 * G * float(mass) / (C**2)) * SCALE
        super().__init__(
            name=name,
            texture=None,
            position=position,
            velocity=(0.0, 0.0, 0.0),
            acceleration=(0.0, 0.0, 0.0),
            mass=mass,
            radius=max(radius_scene_units, 0.01),
        )
        self.visual.color = color.black
        self.visual.emissive = False

    def body_type(self) -> str:
        return "BlackHole"


class SolarSystemSimulation:
    def __init__(self) -> None:
        self.scene = canvas(
            title="Solar System Simulation",
            width=1280,
            height=720,
            center=vector(0, 0, 0),
            background=color.black,
        )

        self._build_starfield(1_000)
        self._build_asteroid_belt(500)

        self.sun, self.planets = self._create_main_bodies()
        self.bodies: list[Body] = [self.sun, *self.planets]

        self.planet_facts: dict[str, str] = {
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

        self.info_board = label(
            visible=False,
            xoffset=60,
            yoffset=50,
            space=30,
            height=25,
            border=4,
            font="sans",
        )

        self.active_explosions: list[Any] = []
        self.pending_bodies: list[Body] = []
        self.selected_target: Body | None = None
        self.black_hole: BlackHole | None = None
        self.is_black_hole = False

        self._initial_states: dict[str, tuple[vector, vector]] = {
            p.name: (vector(p.position.x, p.position.y, p.position.z), vector(p.velocity.x, p.velocity.y, p.velocity.z))
            for p in self.planets
        }

        self.sun.visual.emissive = True
        local_light(pos=self.sun.position * SCALE, color=color.white)

        self._initialize_elliptic_orbits()

        self.scene.bind("mousedown", self.on_mouse_click)
        self.scene.bind("keydown", self.on_key_input)

    def run(self, dt: float = 3600.0) -> None:
        while True:
            rate(50)
            self._step(dt)

    def on_mouse_click(self, evt: Any) -> None:
        click_pos = evt.pos
        closest: Body | None = None
        min_diff = float("inf")

        for body in self.bodies:
            diff = mag(click_pos - body.visual.pos)
            if diff < min_diff:
                min_diff = diff
                closest = body

        if closest is not None and min_diff < 0.3:
            self.selected_target = closest
            if closest.name in self.planet_facts:
               new_text = (
                    f"{closest.name}\n"
                    f"Type: {closest.body_type()}\n"
                    f"{self.planet_facts[closest.name]}"
                )
            if self.info_board.visible and self.info_board.text == new_text:
                    self.info_board.visible = False
            else:
                    self.info_board.text = new_text
                    self.info_board.visible = True
            return

        self.selected_target = None
        self.info_board.visible = False

    def on_key_input(self, evt: Any) -> None:
        key = str(evt.key).lower()
        if key == "b":
            self.toggle_black_hole()
        elif key == "m" and self.selected_target is not None:
            self.spawn_meteor(self.selected_target)
        elif key == "r":
            self.reset_simulation()

    def toggle_black_hole(self) -> None:
        if not self.is_black_hole:
            self.sun.visual.visible = False
            self.black_hole = BlackHole("BlackHole", self.sun.position, self.sun.mass * 10)
            self.bodies[0] = self.black_hole
            self.is_black_hole = True
            return

        if self.black_hole is not None:
            self.black_hole.visual.visible = False

        self.sun.visual.visible = True
        local_light(pos=self.sun.position * SCALE, color=color.white)
        self.bodies[0] = self.sun
        self.black_hole = None
        self.is_black_hole = False

    def _calculate_interception(self, target: Body, spawn_pos: vector, meteor_speed: float) -> vector:
        from math import sqrt
        
        p_t = target.position
        v_t = target.velocity
        p_m = spawn_pos
        s_m = meteor_speed
        
        dp = p_t - p_m
        
        A = mag(v_t)**2 - s_m**2
        B = 2 * dot(dp, v_t)
        C = mag(dp)**2
        
        delta = B**2 - 4*A*C
        if delta < 0:
            return p_t
            
        t1 = (-B - sqrt(delta)) / (2*A)
        t2 = (-B + sqrt(delta)) / (2*A)
        
        if t1 > 0 and t2 > 0:
            t = min(t1, t2)
        elif t1 > 0:
            t = t1
        elif t2 > 0:
            t = t2
        else:
            return p_t
            
        return p_t + v_t * t

    def spawn_meteor(self, target: Body) -> None:
        spawn_radius = max(3 * AU, mag(target.position) + 2 * AU)
        raw_dir = vector(
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            random.uniform(-0.1, 0.1),
        )
        if mag(raw_dir) < 1e-8:
            raw_dir = vector(1, 0, 0)

        spawn_pos = raw_dir.norm() * spawn_radius
        meteor_speed = 1000 * KM
        
        future_pos = self._calculate_interception(target, spawn_pos, meteor_speed)
        
        direction = (future_pos - spawn_pos).norm()

        meteor = Meteor(
            name=f"Meteor_{random.randint(100, 999)}",
            texture=None,
            position=spawn_pos,
            velocity=direction * meteor_speed,
            acceleration=(0.0, 0.0, 0.0),
            mass=1e12,
            radius=0.01,
        )
        meteor.visual.color = color.white
        meteor.visual.trail_color = color.red
        meteor.visual.emissive = True
        meteor.visual.retain = 2_000

        self.pending_bodies.append(meteor)
        print(f"Meteor calculated intercept trajectory for {target.name}!")

    def reset_simulation(self) -> None:
        for body in self.bodies:
            body.visual.visible = False

        self.black_hole = None
        self.is_black_hole = False
        self.pending_bodies.clear()
        self.selected_target = None
        self.info_board.visible = False

        self.sun.position = (0.0, 0.0, 0.0)
        self.sun.velocity = (0.0, 0.0, 0.0)
        self.sun.visual.visible = True
        self.sun.visual.clear_trail()

        for planet in self.planets:
            initial_pos, initial_vel = self._initial_states[planet.name]
            planet.position = initial_pos
            planet.velocity = initial_vel
            planet.acceleration = (0.0, 0.0, 0.0)
            planet.visual.visible = True
            planet.visual.clear_trail()
            planet.update_visual()

        self.sun.update_visual()
        self.bodies = [self.sun, *self.planets]
        local_light(pos=self.sun.position * SCALE, color=color.white)
        print("Simulation reset!")

    def _build_starfield(self, count: int) -> None:
        for _ in range(count):
            sphere(
                pos=vector(
                    random.uniform(-100, 100),
                    random.uniform(-100, 100),
                    random.uniform(-100, 100),
                ),
                radius=random.uniform(0.001, 0.1),
                color=color.white,
                emissive=True,
            )

    def _build_asteroid_belt(self, count: int) -> None:
        inner_radius = 2.2 * AU
        outer_radius = 3.2 * AU

        for _ in range(count):
            r = random.uniform(inner_radius, outer_radius)
            theta = random.uniform(0, 2 * math.pi)
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            z = random.uniform(-0.05 * AU, 0.05 * AU)
            sphere(
                pos=vector(x, y, z) * SCALE,
                radius=random.uniform(0.002, 0.008),
                color=color.gray(0.7),
                emissive=False,
            )

    def _create_main_bodies(self) -> tuple[Star, list[Planet]]:
        sun = Star(
            "Sun",
            "https://upload.wikimedia.org/wikipedia/commons/c/cb/Solarsystemscope_texture_2k_sun.jpg",
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
            mass=1.989e30,
            radius=0.2,
        )

        planets = [
            Planet(
                "Mercury",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRazoRKaLCrMI7lURGR9xv8mKxPThr38wRkjQ&s",
                (0.39 * AU, 0, 0.01 * AU),
                (0, 47.4 * KM, 0),
                (0, 0, 0),
                mass=3.30e23,
                radius=0.0007,
                semi_major_axis=0.387,
                eccentricity=0.2056,
            ),
            Planet(
                "Venus",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRE7q_NoC49WiU1JYZAZdMEHD5sl_Bli3TiOw&s",
                (0.72 * AU, 0, -0.015 * AU),
                (0, 35.0 * KM, 0),
                (0, 0, 0),
                mass=4.87e24,
                radius=0.00174,
                semi_major_axis=0.723,
                eccentricity=0.0068,
            ),
            Planet(
                "Earth",
                "https://t3.ftcdn.net/jpg/03/64/91/04/360_F_364910470_DCjyTv7AlFX0or7TGEcJWkz7JDLnCE5G.jpg",
                (1.00 * AU, 0, 0.02 * AU),
                (0, 29.8 * KM, 0),
                (0, 0, 0),
                mass=5.97e24,
                radius=0.00183,
                semi_major_axis=1.0,
                eccentricity=0.0167,
            ),
            Planet(
                "Mars",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQc0ELDdWdnToVXeznMHPNmZPjB9-jKy1p68Q&s",
                (1.52 * AU, 0, -0.01 * AU),
                (0, 24.1 * KM, 0),
                (0, 0, 0),
                mass=6.42e23,
                radius=0.00097,
                semi_major_axis=1.524,
                eccentricity=0.0934,
            ),
            Planet(
                "Jupiter",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_ABVh6X-rxANutcMkEqX0Q6fQtFt7ERZPkQ&s",
                (5.20 * AU, 0, 0.03 * AU),
                (0, 13.1 * KM, 0),
                (0, 0, 0),
                mass=1.898e27,
                radius=0.02010,
                semi_major_axis=5.204,
                eccentricity=0.0485,
            ),
            Planet(
                "Saturn",
                "https://upload.wikimedia.org/wikipedia/commons/1/1e/Solarsystemscope_texture_8k_saturn.jpg",
                (9.58 * AU, 0, -0.025 * AU),
                (0, 9.7 * KM, 0),
                (0, 0, 0),
                mass=5.683e26,
                radius=0.01674,
                semi_major_axis=9.582,
                eccentricity=0.0555,
            ),
            Planet(
                "Uranus",
                "https://upload.wikimedia.org/wikipedia/commons/9/95/Solarsystemscope_texture_2k_uranus.jpg",
                (19.22 * AU, 0, 0.015 * AU),
                (0, 6.8 * KM, 0),
                (0, 0, 0),
                mass=8.681e25,
                radius=0.00729,
                semi_major_axis=19.201,
                eccentricity=0.0463,
            ),
            Planet(
                "Neptune",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5m6I1cNvdxJo1hMYBzgmMzcD1viyiItRiyg&s",
                (30.05 * AU, 0, -0.02 * AU),
                (0, 5.4 * KM, 0),
                (0, 0, 0),
                mass=1.024e26,
                radius=0.00708,
                semi_major_axis=30.047,
                eccentricity=0.0090,
            ),
            Planet(
                "Pluto",
                "https://planetpixelemporium.com/download/download.php?plutomap2k.jpg",
                (39.48 * AU, 0, 0.01 * AU),
                (0, 4.7 * KM, 0),
                (0, 0, 0),
                mass=1.309e22,
                radius=0.00034,
                semi_major_axis=39.482,
                eccentricity=0.2488,
            ),
        ]
        return sun, planets

    def _initialize_elliptic_orbits(self) -> None:
        for planet in self.planets:
            a_meters = planet.semi_major_axis * AU
            e = planet.eccentricity
            r_peri = a_meters * (1 - e)
            v_peri = math.sqrt((G * self.sun.mass / a_meters) * ((1 + e) / (1 - e)))
            planet.position = (r_peri, 0.0, 0.0)
            planet.velocity = (0.0, v_peri, 0.0)
            planet.visual.clear_trail()

    def _step(self, dt: float) -> None:
        if self.pending_bodies:
            self.bodies.extend(self.pending_bodies)
            self.pending_bodies.clear()
        self._animate_explosions()
        self._handle_collisions(dt)  
        self._cleanup_far_meteors()
        self._integrate_bodies(dt)

    def _animate_explosions(self) -> None:
        for explosion in self.active_explosions[:]:
            explosion.radius += 0.015
            explosion.opacity -= 0.015
            if explosion.opacity <= 0:
                explosion.visible = False
                self.active_explosions.remove(explosion)

    def _handle_collisions(self, dt: float) -> None:
        meteors_to_destroy: list[Meteor] = []
        target_types = {"Planet", "Star", "BlackHole"}

        for body in self.bodies:
            if body.body_type() != "Meteor":
                continue

            meteor = body
            for target in self.bodies:
                if target is meteor or target.body_type() not in target_types:
                    continue
                distance = mag(meteor.position - target.position)
                            
                target_physical_radius = target.radius / SCALE
                meteor_physical_radius = meteor.radius / SCALE                            
                dynamic_hitbox = target_physical_radius + meteor_physical_radius + (mag(meteor.velocity) * dt)               
                if distance < dynamic_hitbox:
                    self._trigger_explosion(target.position)
                    meteors_to_destroy.append(meteor)
                    break

        for meteor in meteors_to_destroy:
            if meteor in self.bodies:
                meteor.visual.visible = False
                meteor.visual.clear_trail()
                self.bodies.remove(meteor)

    def _cleanup_far_meteors(self) -> None:
        for body in self.bodies[:]:
            if body.body_type() == "Meteor" and mag(body.position) > 20 * AU:
                body.visual.visible = False
                body.visual.make_trail = False
                body.visual.clear_trail()
                self.bodies.remove(body)

    def _integrate_bodies(self, dt: float) -> None:
        for body in self.bodies:
            body.acceleration = self._compute_acceleration(body)

        for body in self.bodies:
            body.position = body.position + body.velocity * dt + 0.5 * body.acceleration * (dt**2)

        new_accelerations = [self._compute_acceleration(body) for body in self.bodies]
        for index, body in enumerate(self.bodies):
            body.velocity = body.velocity + 0.5 * (body.acceleration + new_accelerations[index]) * dt
            body.acceleration = new_accelerations[index]
            body.update_visual()

    def _compute_acceleration(self, body: Body) -> vector:
        # [CẬP NHẬT MỚI]: Bỏ qua trọng lực đối với thiên thạch để nó bay thẳng theo đường toán học
        if body.body_type() == "Meteor":
            return vector(0, 0, 0)
            
        total_acc = vector(0, 0, 0)
        for other in self.bodies:
            if body is other:
                continue
            r_vec = body.position - other.position
            dist = mag(r_vec)
            if dist < 1e-5:
                continue
            total_acc += -G * other.mass * r_vec / (dist**3)
        return total_acc

    def _trigger_explosion(self, hit_position: vector) -> None:
        explosion = sphere(
            pos=hit_position * SCALE,
            radius=0.1,
            color=vector(1, 0.5, 0),
            emissive=True,
            opacity=1.0,
        )
        self.active_explosions.append(explosion)
        print("BOOM! Collision detected!")


if __name__ == "__main__":
    simulation = SolarSystemSimulation()
    simulation.run()