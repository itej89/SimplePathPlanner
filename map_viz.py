import numpy as np
import cv2 as cv

import pyclipper

from obstacle_model import *

class map_viz:
    
    def point_at_a_distance_on_line(self, point1, point2, dt):
        d = np.linalg.norm(np.array(point1) - np.array(point2))
        t = (dt+d)/d

        return ((1-t)*point2[0]+t*point1[0], (1-t)*point2[1]+t*point1[1])
    
    def inflate_polygon(self, vertices, radius):
        pco = pyclipper.PyclipperOffset()
        pco.AddPath(vertices, pyclipper.PT_CLIP, pyclipper.ET_CLOSEDPOLYGON)
        vertices_inflated = pco.Execute(radius)
        vertices_inflated = [tuple(x) for x in vertices_inflated[0]]
        return vertices_inflated

    def __init__(self, height, width) -> None:
        self.map = np.ones((height, width)) * 240

        self.boundary_model = obstacle_model([
            [(600,0), (600,250), (0,250), (0,0)]
            ])
        
        self.inflated_boundary_model = obstacle_model([
            self.inflate_polygon([(600,0), (600,250), (0,250), (0,0)], -5),
            ])
        
        self.original_obstacle_model = obstacle_model([
            [(150,0), (150,100), (100,100), (100,0)],
            [(150,150), (150,250), (100,250), (100,150)],
            [(360,87), (360,163), (300,200), (240,163), (240,87), (300,50)],
            [(510,125), (460,225), (460,25) ],
        ])


        self.inflated_obstacle_model = obstacle_model([
            self.inflate_polygon([(150,0), (150,100), (100,100), (100,0)], 5),
            self.inflate_polygon([(150,150), (150,250), (100,250), (100,150)], 5),
            self.inflate_polygon([(360,87), (360,163), (300,200), (240,163), (240,87), (300,50)], 5),
            self.inflate_polygon([(510,125), (460,225), (460,25) ], 5),
        ])


    
    def create_map(self):
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                if self.original_obstacle_model.check_obstacle((j,i)):
                    self.map[i,j] = 0
                elif self.inflated_obstacle_model.check_obstacle((j,i)):
                    self.map[i,j] = 120
                elif not self.inflated_boundary_model.check_obstacle((j,i)):
                    self.map[i,j] = 120

    def show_map(self):
        cv.imshow("map", self.map.astype('uint8'))
        cv.waitKey(0)


if __name__ == "__main__":
    _map_viz = map_viz(250, 600)
    _map_viz.create_map()
    _map_viz.show_map()