from core import Simulation
from visualizer import Window

sim = Simulation()

# sim.create_segment((0, 0), (50, 0))
sim.create_quadratic_bezier_curve((0, 0), (50, 0), (50, 50))
sim.create_vehicle(path=[0])

win = Window(sim)
win.show()
