from car import Car
from map import Map
from folder1.visualisation import Visualisation
import shapely
import tkinter


class Simulation:

    def __init__(self, first_car: Car, map: Map) -> None:
        self.map = map
        self.first_car: Car = first_car
        self.visualisation = Visualisation(map=map, car=first_car)

    def loop(self) -> None:
        self.first_car.calcNextStep(self.map)
        self.first_car.move()

    def main(self) -> None:
        self.loop()
        self.visualisation.draw()
        self.visualisation.window.after(100, self.main)


if __name__ == '__main__':
    sim = Simulation(first_car=Car(x=40, y=40, speed=5,max_speed=100, d_x=1, d_y=0),
                     map=Map([shapely.LinearRing(
                         [(35, 50), (270, 45), (440, 130), (525, 235)]),shapely.LinearRing(
                         [(70, 55), (265, 55), (430, 135), (490, 205)])]))
    sim.visualisation.window.after(10, sim.main)
    sim.visualisation.window.mainloop()
