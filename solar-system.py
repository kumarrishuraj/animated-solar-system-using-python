import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


planets = [
    {"name": "Mercury", "orbit_radius": 0.39, "color": "gray", "speed": 4.15, "moons": []},
    {"name": "Venus", "orbit_radius": 0.72, "color": "yellow", "speed": 1.62, "moons": []},
    {"name": "Terravita", "orbit_radius": 0.85, "color": "purple", "speed": 1.28, "moons": []},
    {"name": "Earth", "orbit_radius": 1.0, "color": "blue", "speed": 1.0, "moons": ["Moon"]},
    {"name": "Mars", "orbit_radius": 1.52, "color": "red", "speed": 0.53, "moons": ["Phobos", "Deimos"]},
    {"name": "Jupiter", "orbit_radius": 5.2, "color": "orange", "speed": 0.084, "moons": ["Io", "Europa", "Ganymede", "Callisto"]},
    {"name": "Saturn", "orbit_radius": 9.58, "color": "gold", "speed": 0.034, "moons": ["Titan", "Enceladus"]},
    {"name": "Uranus", "orbit_radius": 19.22, "color": "lightblue", "speed": 0.011, "moons": ["Miranda", "Ariel"]},
    {"name": "Neptune", "orbit_radius": 30.05, "color": "darkblue", "speed": 0.006, "moons": ["Triton"]},
]


num_asteroids = 300
asteroid_radii = np.random.uniform(2.0, 3.5, num_asteroids)
asteroid_angles = np.random.uniform(0, 2 * np.pi, num_asteroids)


fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect("equal")
ax.set_facecolor("black")
ax.set_xlim(-35, 35)
ax.set_ylim(-35, 35)
ax.axis("on")


num_stars = 1000
stars_x = np.random.uniform(-35, 35, num_stars)
stars_y = np.random.uniform(-35, 35, num_stars)
ax.scatter(stars_x, stars_y, color="white", s=0.5, zorder=1)


asteroid_x = asteroid_radii * np.cos(asteroid_angles)
asteroid_y = asteroid_radii * np.sin(asteroid_angles)
ax.scatter(asteroid_x, asteroid_y, color="white", s=np.random.uniform(5, 20, num_asteroids), zorder=2)


for planet in planets:
    orbit_x = planet["orbit_radius"] * np.cos(np.linspace(0, 2 * np.pi, 500))
    orbit_y = planet["orbit_radius"] * np.sin(np.linspace(0, 2 * np.pi, 500))
    ax.plot(orbit_x, orbit_y, color="white", linestyle="--", linewidth=0.5, zorder=2)


ax.scatter(0, 0, color="yellow", s=500, zorder=3)

planet_scatters = []
planet_labels = []
moon_scatters = {}
moon_labels = {}

for planet in planets:
    scatter = ax.scatter([], [], color=planet["color"], s=planet["orbit_radius"] * 50, zorder=4)
    label = ax.text(0, 0, planet["name"], color=planet["color"], fontsize=8, zorder=5, ha="center")
    planet_scatters.append(scatter)
    planet_labels.append(label)
    for moon in planet["moons"]:
        moon_scatter = ax.scatter([], [], color="white", s=10, zorder=5)
        moon_label = ax.text(0, 0, moon, color="white", fontsize=6, zorder=6, ha="center")
        moon_scatters[moon] = moon_scatter
        moon_labels[moon] = moon_label


def init():
    for scatter, label in zip(planet_scatters, planet_labels):
        scatter.set_offsets(np.array([[], []]).T)
        label.set_position((0, 0))
    for scatter, label in zip(moon_scatters.values(), moon_labels.values()):
        scatter.set_offsets(np.array([[], []]).T)
        label.set_position((0, 0))
    return planet_scatters + list(moon_scatters.values()) + planet_labels + list(moon_labels.values())


def update(frame):
    for i, planet in enumerate(planets):
        angle = frame * planet["speed"]
        x = planet["orbit_radius"] * np.cos(angle)
        y = planet["orbit_radius"] * np.sin(angle)
        planet_scatters[i].set_offsets(np.array([[x, y]]))
        planet_labels[i].set_position((x, y + 0.2))  # Position label slightly above the planet
        
        for j, moon in enumerate(planet["moons"]):
            moon_angle = frame * planet["speed"] * (2 + j * 0.5)
            moon_x = x + 0.1 * (j + 1) * np.cos(moon_angle)
            moon_y = y + 0.1 * (j + 1) * np.sin(moon_angle)
            moon_scatters[moon].set_offsets(np.array([[moon_x, moon_y]]))
            moon_labels[moon].set_position((moon_x, moon_y + 0.1))
    return planet_scatters + list(moon_scatters.values()) + planet_labels + list(moon_labels.values())


ani = FuncAnimation(
    fig, update, frames=np.linspace(0, 2 * np.pi, 360),
    init_func=init, blit=True, interval=50, save_count=360
)


plt.show()