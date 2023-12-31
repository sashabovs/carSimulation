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