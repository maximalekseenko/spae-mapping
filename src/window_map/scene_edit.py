from engine import Scene
import math
import pygame
from application import application



class Scene_Edit(Scene):
    def On_Init(self) -> None:
        self.selected_id = -1


    def On_Open(self) -> None:
        self.Update()


    def On_Close(self) -> None:
        self.selected_id = -1

    
    def On_Tick(self) -> None:
        self._Camera_Move()


    def On_Handle(self, event: pygame.event.Event) -> None:
        pass

    def _Camera_Rotate(self, dx):
        __SPEED = 1
        # degrees
        self.camera_rot = (self.camera_rot + dx * __SPEED) % 360
        self.camera_rad = math.radians(self.camera_rot)


    def _Camera_Scale(self, dy):
        self.camera_scale += dy / 100

    
    def _Camera_Move(self):
        __SPEED = 2
        if self.camera_movement[0]: # left
            self.camera_pos[0] += math.cos(self.camera_rad + math.pi) * __SPEED
            self.camera_pos[1] -= math.sin(self.camera_rad + math.pi) * __SPEED
        if self.camera_movement[1]: # right
            self.camera_pos[0] += math.cos(self.camera_rad) * __SPEED
            self.camera_pos[1] -= math.sin(self.camera_rad) * __SPEED
        if self.camera_movement[2]: # up
            self.camera_pos[0] += math.cos(self.camera_rad + math.pi / 2) * __SPEED
            self.camera_pos[1] -= math.sin(self.camera_rad + math.pi / 2) * __SPEED
        if self.camera_movement[3]: # down
            self.camera_pos[0] += math.cos(self.camera_rad - math.pi / 2) * __SPEED
            self.camera_pos[1] -= math.sin(self.camera_rad - math.pi / 2) * __SPEED


    def On_Render(self) -> None:
        self._Render_Background()
        self._Render_bounds()
        self._Render_Stars()
        self._Render_Compass()
        self._Render_Debug()

        
    def _Render_Background(self):
        self.surface.fill("#0a0a0a")


    def _Render_bounds(self):
        # X
        pygame.draw.line(self.surface, "#ff000050", 
            self._Point_To_Cam(0,                           0), 
            self._Point_To_Cam(application.data['axis'][0], 0)
        )
        pygame.draw.line(self.surface, "#ff000050", 
            self._Point_To_Cam(0,                           application.data['axis'][1]), 
            self._Point_To_Cam(application.data['axis'][0], application.data['axis'][1])
        )
        # Y
        pygame.draw.line(self.surface, "#00ff0050", 
            self._Point_To_Cam(application.data['axis'][0], 0), 
            self._Point_To_Cam(application.data['axis'][0], application.data['axis'][1])
        )
        pygame.draw.line(self.surface, "#00ff0050", 
            self._Point_To_Cam(0,                           application.data['axis'][1]), 
            self._Point_To_Cam(0,                           0)
        )

    
    def _Render_Stars(self):
        __BASE_RADIUS_X = 10
        __BASE_RADIUS_Y = 5
        __STAR_RADIUS = 5
        for star in application.data['stars']:

            __x, __y, __z = self._Point_To_Cam(star['pos'])

            # render base
            # TODO colors
            pygame.draw.ellipse(
                self.surface, 
                "#a0a0a0",
                (
                    __x - __BASE_RADIUS_X / 2,
                    __y - __BASE_RADIUS_Y / 2,
                    __BASE_RADIUS_X,
                    __BASE_RADIUS_Y
                ),
                1
            )

            # render height line
            pygame.draw.line(
                self.surface,
                "#a0a0a0",
                (__x, __y),
                (__x, __y - __z)
            )

            # draw star
            pygame.draw.circle(
                self.surface, 
                "#aaaaaa", 
                (__x, __y - __z), 
                __STAR_RADIUS
            )


    def _Render_Compass(self):
        __LENGTH = 25
        __CENTER = (
            __LENGTH,
            self.surface.get_height() - __LENGTH
        )

        # render X axis line
        pygame.draw.line(
            self.surface,
            "#ff0000",
            __CENTER,
            (
                __CENTER[0] + math.cos(self.camera_rad) * __LENGTH,
                __CENTER[1] + math.sin(self.camera_rad) * __LENGTH / 2,
            )
        )
        # render Y axis line
        pygame.draw.line(
            self.surface,
            "#00ff00",
            __CENTER,
            (
                __CENTER[0] - math.cos(self.camera_rad + math.pi / 2) * __LENGTH,
                __CENTER[1] - math.sin(self.camera_rad + math.pi / 2) * __LENGTH / 2,
            )
        )
        # render Z axis line
        pygame.draw.line(
            self.surface,
            "#0000ff",
            __CENTER,
            (
                __CENTER[0],
                __CENTER[1] - __LENGTH / 2,
            )
        )
  

    def _Render_Debug(self):
        debug_text = [
            self.camera_pos,
            self.camera_rot,
        ]

        text_top = 0
        font = pygame.font.Font(None, 16)

        for text in debug_text:
            text_surf = font.render(str(text), 0, "#ffffff", "#000000")
            text_rect = text_surf.get_rect(top=text_top, left=0)
            self.surface.blit(text_surf, text_rect)
            text_top += text_rect.height





    def On_Update(self):
        return super().On_Update()


    
    def _Point_To_Cam(self, *point:tuple[int, int]|tuple[int, int, int]) -> tuple[int, int]:
        if len(point) == 3:
            __x, __y, __z = point
            __z /= 2
            __z *= self.camera_scale

        if len(point) == 2: 
            __x, __y = point

        if len(point) == 1: 
            return self._Point_To_Cam(*point[0])

        # X and Y
        ## camera position
        __x -= self.camera_pos[0]
        __y -= self.camera_pos[1]

        ## camera rotation
        __x, __y = (
            __x * math.cos(self.camera_rad) - __y * math.sin(self.camera_rad),
            __x * math.sin(self.camera_rad) + __y * math.cos(self.camera_rad),
        )

        ## scale
        __x *= self.camera_scale
        __y *= self.camera_scale

        ## screen center
        __x += self.surface.get_width() / 2
        __y += self.surface.get_height() / 2


        if len(point) == 3:
            return (__x, __y, __z)
        if len(point) == 2: 
            return (__x, __y)