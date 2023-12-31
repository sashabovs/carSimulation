import shapely
from typing import List
from shapely.geometry import Point, LineString

class Map:
    def __init__(self, tracks: List[shapely.LinearRing]):
        self.tracks: List[shapely.LinearRing] = tracks

        self.track_lines = []
        self.lines = []
        n = 0
        for track in self.tracks:
            self.track_lines.append([])
            for c1, c2 in zip(track.coords, track.coords[1:]):
                self.lines.append(LineString([c1, c2]))
                self.track_lines[n].append(LineString([c1, c2]))
            n += 1



        #traffic light
        #0 > 50 > 60 > 110
        #r > y > g > r
        self.traffic_lights = [{(270,45): 0 , (150,94): 0 }, {(265,55): 0 , (150,84): 0 }]

    def incr_light(self):
        for track_lights in self.traffic_lights:
            for pos,light in track_lights.items():
                track_lights[pos] += 1
                if light > 110:
                    track_lights[pos] = 0