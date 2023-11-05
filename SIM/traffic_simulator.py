from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random

class Car(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.speed = 5
        self.max_speed = 5

    def step(self):
        self.move()

    def move(self):
        x, y = self.pos
        # Verifica si el semáforo permite el movimiento
        semaphore = self.model.semaphore
        if semaphore.state == 2:  # Verde
            # Mueve el carro hacia adelante
            new_pos = y - self.speed
            if new_pos >= 0:
                self.model.grid.move_agent(self, (x, new_pos))
            else:
                # Si el carro llega a un borde, muévelo al borde opuesto
                new_pos = self.model.grid.height - 1  # Posición del borde opuesto en y
                self.model.grid.move_agent(self, (x, new_pos))

class Semaphore(Agent):
    def __init__(self, unique_id, model, position, green_duration, red_duration):
        super().__init__(unique_id, model)
        self.state = 0  # 0: Rojo, 1: Amarillo, 2: Verde
        self.green_duration = green_duration
        self.red_duration = red_duration
        self.steps = 0
        self.position = position

    def step(self):
        self.steps += 1
        if self.state == 0 and self.steps >= self.red_duration:
            self.steps = 0
            self.state = 1
        elif self.state == 1 and self.steps >= self.green_duration:
            self.steps = 0
            self.state = 2
        elif self.state == 2 and self.steps >= self.red_duration:
            self.steps = 0
            self.state = 0

class TrafficModel(Model):
    def __init__(self, width, height, N, green_duration, red_duration):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.semaphore = Semaphore(0, self, position=(5, 5), green_duration=green_duration, red_duration=red_duration)
        self.running = True
        self.datacollector = DataCollector(
            {"Cars": lambda m: self.count_type(m, Car), "Green Duration": lambda m: m.semaphore.green_duration},
        )
        # Coloca el semáforo en la posición especificada
        x, y = self.semaphore.position
        self.grid.place_agent(self.semaphore, (x, y))
        self.schedule.add(self.semaphore)

        # Coloca los carros en posiciones aleatorias en la grilla
        for i in range(self.num_agents):
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            while (x, y) == (self.semaphore.position):
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
            a = Car(i + 2, self)
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def count_type(self, model, agent_type):
        return len([agent for agent in model.schedule.agents if isinstance(agent, agent_type)])