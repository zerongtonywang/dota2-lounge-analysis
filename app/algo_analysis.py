from app.simulation import Simulation

for i in range(15):
    TRAIN_PERIOD = i
    s = Simulation()
    s.simulate()
