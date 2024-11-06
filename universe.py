import cv2
import numpy as np
import logging
import datetime

# Set up logging
logging.basicConfig(filename='universe.log', level=logging.INFO)

# Define classes for the universe
class LifeFormAI:
    def __init__(self, name):
        self.name = name
        self.intelligence = 1
        self.complexity = 1
        self.generation = 1

    def evolve(self):
        self.intelligence *= 1.19
        self.complexity *= 1.19
        self.generation += 1
        logging.info(f"{self.name} has evolved to Generation {self.generation}: Intelligence={self.intelligence}, Complexity={self.complexity}")

class Planet:
    def __init__(self, name, distance, star_mass):
        self.name = name
        self.distance = distance
        self.life_forms = []
        self.star_mass = star_mass

    def add_life(self, life_form):
        self.life_forms.append(life_form)
        logging.info(f"Life form '{life_form.name}' added to planet '{self.name}'.")

class Star:
    def __init__(self, name, mass):
        self.name = name
        self.mass = mass
        self.planets = []

    def add_planet(self, planet):
        self.planets.append(planet)
        logging.info(f"Planet '{planet.name}' added to star '{self.name}'.")

class Galaxy:
    def __init__(self, name):
        self.name = name
        self.stars = []

    def add_star(self, star):
        self.stars.append(star)
        logging.info(f"Star '{star.name}' added to galaxy '{self.name}'.")

    def destroy_star(self, star_name):
        for star in self.stars:
            if star.name == star_name:
                self.stars.remove(star)
                logging.info(f"Star '{star.name}' has been destroyed.")
                return True
        return False

class Universe:
    def __init__(self):
        self.galaxies = []
        self.video_writer = None
        self.initialize_video()

    def initialize_video(self):
        self.video_writer = cv2.VideoWriter('universe_simulation.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (640, 480))

    def create_galaxy(self, name):
        galaxy = Galaxy(name)
        self.galaxies.append(galaxy)
        logging.info(f"Galaxy '{name}' has been created.")

    def create_star(self, galaxy_name, star_name, mass):
        for galaxy in self.galaxies:
            if galaxy.name == galaxy_name:
                star = Star(star_name, mass)
                galaxy.add_star(star)
                return True
        return False

    def create_planet(self, star_name, planet_name, distance):
        for galaxy in self.galaxies:
            for star in galaxy.stars:
                if star.name == star_name:
                    planet = Planet(planet_name, distance, star.mass)
                    star.add_planet(planet)
                    return True
        return False

    def add_life_to_planet(self, planet_name, life_name):
        for galaxy in self.galaxies:
            for star in galaxy.stars:
                for planet in star.planets:
                    if planet.name == planet_name:
                        life_form = LifeFormAI(life_name)
                        planet.add_life(life_form)
                        return True
        return False

    def simulate(self, time_steps):
        for step in range(time_steps):
            logging.info(f"Simulating time step {step + 1}/{time_steps}...")
            for galaxy in self.galaxies:
                for star in galaxy.stars:
                    for planet in star.planets:
                        for life in planet.life_forms:
                            life.evolve()
            self.visualize_universe()
            self.save_video_frame()

    def visualize_universe(self):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        for galaxy in self.galaxies:
            for star in galaxy.stars:
                for planet in star.planets:
                    cv2.circle(frame, (320, 240), int(planet.distance / 1e10), (255, 255, 255), -1)  # Simplified representation
        cv2.imshow('Universe Simulation', frame)
        cv2.waitKey(1)  # Wait for a short moment

    def save_video_frame(self):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self.video_writer.write(frame)

    def close_video(self):
        if self.video_writer:
            self.video_writer.release()

    def observe_universe(self):
        logging.info("Current state of the universe:")
        for galaxy in self.galaxies:
            print(f"Galaxy '{galaxy.name}' with {len(galaxy.stars)} stars.")
            for star in galaxy.stars:
                print(f"  Star '{star.name}' with {len(star.planets)} planets.")
                for planet in star.planets:
                    life_names = ', '.join([life.name for life in planet.life_forms])
                    print(f"    Planet '{planet.name}', has life: {life_names if life_names else 'None'}")

    def destroy_star(self, star_name):
        for galaxy in self.galaxies:
            if galaxy.destroy_star(star_name):
                return True
        return False

    def destroy_galaxy(self, galaxy_name):
        for galaxy in self.galaxies:
            if galaxy.name == galaxy_name:
                self.galaxies.remove(galaxy)
                logging.info(f"Galaxy '{galaxy.name}' has been destroyed.")
                return True
        return False

# Command line interface
def main():
    universe = Universe()
    print("Universe Simulation Commands:")
    print("  create_galaxy <galaxy_name>")
    print("  create_star <galaxy_name> <star_name> <mass>")
    print("  create_planet <star_name> <planet_name> <distance>")
    print("  add_life <planet_name> <life_name>")
    print("  simulate <time_steps>")
    print("  observe")
    print("  destroy_star <star_name>")
    print("  destroy_galaxy <galaxy_name>")
    print("  exit to quit")
    
    while True:
        command = input("Enter a command: ")
        parts = command.split()
        
        if not parts:
            continue
        
        if parts[0] == "create_galaxy" and len(parts) == 2:
            universe.create_galaxy(parts[1])
        
        elif parts[0] == "create_star" and len(parts) == 4:
            galaxy_name, star_name, mass = parts[1], parts[2], float(parts[3])
            if not universe.create_star(galaxy_name, star_name, mass):
                print(f"Galaxy '{galaxy_name}' not found.")
        
        elif parts[0] == "create_planet" and len(parts) == 4:
            star_name, planet_name, distance = parts[1], parts[2], float(parts[3])
            if not universe.create_planet(star_name, planet_name, distance):
                print(f"Star '{star_name}' not found.")
        
        elif parts[0] == "add_life" and len(parts) == 3:
            planet_name, life_name = parts[1], parts[2]
            if not universe.add_life_to_planet(planet_name, life_name):
                print(f"Planet '{planet_name}' not found.")
        
        elif parts[0] == "simulate" and len(parts) == 2:
            time_steps = int(parts[1])
            universe.simulate(time_steps)
        
        elif parts[0] == "observe":
            universe.observe_universe()
        
        elif parts[0] == "destroy_star" and len(parts) == 2:
            if universe.destroy_star(parts[1]):
                print(f"Star '{parts[1]}' has been destroyed.")
            else:
                print(f"Star '{parts[1]}' not found.")
        
        elif parts[0] == "destroy_galaxy" and len(parts) == 2:
            if universe.destroy_galaxy(parts[1]):
                print(f"Galaxy '{parts[1]}' has been destroyed.")
            else:
                print(f"Galaxy '{parts[1]}' not found.")
        
        elif parts[0] == "exit":
            universe.close_video()
            cv2.destroyAllWindows()
            print("Exiting universe simulation.")
            break
        
        else:
            print("Invalid command. Please check the syntax.")

if __name__ == '__main__':
    main()
