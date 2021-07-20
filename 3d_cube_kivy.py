
####### DONE #######

# import

from math import sin, cos
from kivy.config import Config
from kivy.graphics import Ellipse, Color,Line
Config.set('graphics', 'resizable', True)
from kivy.properties import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
from kivy.core.window import Window
Window.clearcolor = (1,1,1,1)
import numpy as np


class Main(RelativeLayout):

    # vertices of a cube
    vertices = []
    vertices.append(np.matrix([[-200], [-200], [200]]))
    vertices.append(np.matrix([[200], [-200], [200]]))
    vertices.append(np.matrix([[200], [200], [200]]))
    vertices.append(np.matrix([[-200], [200], [200]]))
    vertices.append(np.matrix([[-200], [-200], [-200]]))
    vertices.append(np.matrix([[200], [-200], [-200]]))
    vertices.append(np.matrix([[200], [200], [-200]]))
    vertices.append(np.matrix([[-200], [200], [-200]]))

    vertices = np.array(vertices)

    projection_matrix = np.matrix([
        [1, 0, 0],
        [0, 1, 0]
    ])

    ellipse = [i for i in range(8)]
    line = [ p for p in range(12)]
    projected_point = list()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.pos_hint= {"center_x":0.95, "center_y":1}
        self.draw_vertices() 
        Clock.schedule_interval(self.rotate_obj, 1.0/60.0)
        
    # func for displaying vertices of obj
    def draw_vertices(self):

        # generating x,y cordinates  
        for index, vertic in enumerate(self.vertices):
            two_d = self.projection_matrix * vertic
            x, y = np.array(two_d).flatten()
            self.projected_point.append([x, y])

            # drawing a circle at the vertices of obj 
            with self.canvas:
                Color(1, 0, 0, 1)
                self.ellipse[index] = Ellipse(pos=(x,y), size=(8, 8))

        # genarating line cordinates and displaying line
        line_cordinate = self.genarate_line_cordinate()
        self.draw_line(line_cordinate)

    # func for genarating new line cordinates according to obj rotation
    def genarate_line_cordinate(self):
        line_point = list()
        for i in range(4):
            x1,y1 = self.projected_point[i]
            x2,y2 = self.projected_point[(i+1)%4]
            l1 = [x1,y1,x2,y2 ]
            line_point.append(list(np.add(l1,2)))

        for i in range(4):
            x1,y1 = self.projected_point[i]
            x2,y2 = self.projected_point[i+4]
            l2 = [x1,y1,x2,y2 ]
            line_point.append(list(np.add(l2,2)))

        for i in range(4):
            x1,y1 = self.projected_point[i+4]
            x2,y2 = self.projected_point[((i+1)%4) + 4]
            l3 = [x1,y1,x2,y2 ]
            line_point.append(list(np.add(l3,2)))

        return line_point

    # func for drawing line
    def draw_line(self,line_cordinate):
        for index,point in enumerate(line_cordinate):
            with self.canvas:
                Color(0,0,0,1)
                self.line[index]= Line(points = point)

    def rotate_obj(self, dt):

        ## formula of rotation 
        theta = 0.01
        rotation_z = np.matrix([
            [cos(theta), -sin(theta), 0],
            [sin(theta), cos(theta), 0],
            [0, 0, 1]
        ])
        rotation_y = np.matrix([
            [cos(theta), 0, sin(theta)],
            [0, 1, 0],
            [-sin(theta), 0, cos(theta)]
        ])
        rotation_X = np.matrix([
            [1,0,0],
            [0 , cos(theta),-sin(theta)],
            [0,sin(theta), cos(theta)]
        ])
        vertic_point = list()
        new_projected_point = list()

        # Rotating obj
        for index, vertic in enumerate(self.vertices):
            rotated_2d = rotation_X * rotation_y * rotation_z * vertic
            vertic_point.append(rotated_2d)
            tow_d = self.projection_matrix * rotated_2d
            x, y = np.array(tow_d).flatten()
            self.ellipse[index].pos = (x,y)
            new_projected_point.append([x, y])

        theta += 0.01

        # updating vertices and projected_point
        self.vertices = np.array(vertic_point)
        self.projected_point = new_projected_point

        # genarating new line cordinate according to the rotation of obj
        line_cordinate = self.genarate_line_cordinate()
        for index,cordinate in enumerate(line_cordinate):
            self.line[index].points = cordinate

class MainApp(App):
    def build(self):
        return Main()


MainApp().run()
