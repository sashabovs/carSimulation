import numpy as np

from car import Car
from map import Map
import shapely
import tkinter
from shapely.geometry.point import Point

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tkinter.Canvas.create_circle = _create_circle
class Visualisation:
    def __init__(self, map: Map, car: Car) -> None:
        self.window = tkinter.Tk()
        self.window.geometry("1000x1000")
        self.canvas = tkinter.Canvas(self.window, background='white')
        self.canvas.pack(fill="both", expand=True)

        self.car: Car = car
        self.map: Map = map
        self.traffic_lights = map.traffic_lights

        for track in self.map.tracks:
            flattened = [a for x in track.coords for a in x]
            self.canvas.create_line(*flattened)
        self.canvas_car = None
        self.canvas_lights = None

    def draw(self) -> None:
        self.canvas.delete(self.canvas_car)
        self.canvas.delete(self.canvas_lights)

        k = 7
        m = 4
        d_x = np.cos(self.car.car_angle)[0]
        d_y = np.sin(self.car.car_angle)[0]
        x_1 = self.car.x + d_x * k + d_y * m
        y_1 = self.car.y + d_y * k - d_x * m

        x_2 = self.car.x + d_x * k - d_y * m
        y_2 = self.car.y + d_y * k + d_x * m

        x_4 = self.car.x - d_x * k + d_y * m
        y_4 = self.car.y - d_y * k - d_x * m

        x_3 = self.car.x - d_x * k - d_y * m
        y_3 = self.car.y - d_y * k + d_x * m

        self.canvas_lights = []
        for track_lights in self.traffic_lights:
            for pos, light in track_lights.items():
                fill = "black"
                if light < 50:
                    fill = "#38761D"
                elif light < 60:
                    fill = "#ddb321"
                else:
                    fill = "#B7410E"
                self.canvas_lights.append(self.canvas.create_circle(pos[0], pos[1], 4, fill=fill))

        self.canvas_car = self.canvas.create_polygon(x_1,y_1,x_2,y_2,x_3,y_3,x_4,y_4)


