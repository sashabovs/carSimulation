import shapely
from map import Map
import numpy as np


class Car:
    def __init__(self, x: float, y: float, speed: int, max_speed: int, d_x: float, d_y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.d_x: float = d_x
        self.d_y: float = d_y
        self.car_angle: float = 0

        self.speed: int = speed
        self.max_speed = max_speed
        self.desired_speed = max_speed

        self.cur_track = 0
        self.cur_chunk = 0

    def move(self) -> None:
        self.x = self.x + np.cos(self.car_angle)[0] * self.speed
        self.y = self.y + np.sin(self.car_angle)[0] * self.speed

    def rotateLeft(self, angle:float) -> None:
        # self.d_x = self.d_x * np.cos(np.pi / 18) - self.d_y * np.sin(np.pi / 18)
        # self.d_y = self.d_x * np.sin(np.pi / 18) + self.d_y * np.cos(np.pi / 18)
        self.car_angle -= angle


    def rotateRight(self, angle:float) -> None:
        # self.d_x = self.d_x * np.cos(-np.pi / 18) - self.d_y * np.sin(-np.pi / 18)
        # self.d_y = self.d_x * np.sin(-np.pi / 18) + self.d_y * np.cos(-np.pi / 18)
        self.car_angle += angle

    def speedUp(self):
        if self.max_speed < self.speed + 10:
            self.speed = self.max_speed
        else:
            self.speed += 10

    def speedDown(self):
        if self.speed < 10:
            self.speed = 0
        else:
            self.speed -= 10

    def changeTrackUp(self):
        self.cur_track += 1

    def changeTrackDown(self):
        self.cur_track -= 1

    def maintain_speed(self):
        if self.speed > self.desired_speed:
            self.speedDown()
        elif self.speed < self.desired_speed:
            self.speedUp()

    def calcNextStep(self, map: Map) -> None:

        # get closest line segment
        distances = [segment.distance([shapely.Point(self.x, self.y)]) for segment in map.track_lines[self.cur_track]]
        dist = min(distances)
        nearest_line = map.track_lines[self.cur_track][distances.index(dist)]


        car_vector = [np.cos(self.car_angle), np.sin(self.car_angle)]

        temp = map.track_lines[self.cur_track][self.cur_chunk].xy
        line_vector = [temp[0][1] - temp[0][0], temp[1][1] - temp[1][0]]

        line_start_to_car = [self.x - temp[0][0], self.y - temp[1][0]]


        len_of_vec = (line_start_to_car[0]**2+line_start_to_car[1]**2)**.5*(line_vector[0]**2+line_vector[1]**2)**.5
        angle_cos = (line_start_to_car[0]*line_vector[0] + line_start_to_car[1]*line_vector[1])/(len_of_vec)
        angle_sin = (line_start_to_car[0]*line_vector[1] - line_start_to_car[1]*line_vector[0])/(len_of_vec)

        len2 = (car_vector[0] ** 2 + car_vector[1] ** 2) ** .5 * (
                    line_vector[0] ** 2 + line_vector[1] ** 2) ** .5
        angle_sin_2 = (car_vector[0]*line_vector[1] - car_vector[1]*line_vector[0])/(len2)


        if angle_sin_2 > 0:
            self.rotateRight(0.1)
        else:
            self.rotateLeft(0.1)

        if angle_sin > 0:
            self.rotateRight(min(dist*np.pi/200, np.pi/4))
        else:
            self.rotateLeft(min(dist*np.pi/200, np.pi/4))

        if (temp[0][1] - self.x)**2 + (temp[1][1] - self.y)**2 < 100:
            self.cur_chunk += 1
            if self.cur_chunk >= len(map.track_lines[self.cur_track]):
                self.cur_chunk = 0



        self.maintain_speed()