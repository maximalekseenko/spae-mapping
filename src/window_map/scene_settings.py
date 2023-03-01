from engine import Scene
import math
import pygame
from application import application



class Scene_Settings(Scene):
    def On_Init(self) -> None:
        self.use_2d_default = False
        self.camera_move_speed = 2
        self.camera_rot_speed = 2

    def On_Render(self) -> None:
        self.surface.fill("#000000")