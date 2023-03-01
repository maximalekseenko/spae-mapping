from engine import Scene
import math
import pygame
from application import application



class Scene_Map(Scene):
    def On_Init(self) -> None:
        from .window import Window_Map
        self.act:Window_Map


    def On_Open(self) -> None:
        self.camera_pos = [application.data['axis'][0] / 2, application.data['axis'][1] / 2]
        self.camera_rot = 0
        self.camera_rad_z = math.radians(45)
        self.camera_rad = 0
        self.camera_scale = 1
        self.camera_2d = False

        self.camera_movement = [False, False, False, False]
        '''Does camera moves [`left`, `right`, `up`, `down`].'''

        self.Update()


    def On_Close(self) -> None:
        return super().On_Close()

    
    def On_Tick(self) -> None:
        self._Camera_Move()


    def On_Handle(self, event: pygame.event.Event) -> None:

        # rotate camera
        if event.type == pygame.MOUSEMOTION and event.buttons[2]: self._Camera_Rotate(event.rel[0])

        # scale camera
        elif event.type == pygame.MOUSEWHEEL: self._Camera_Scale(event.y)

        # move camera
        elif event.type == pygame.KEYDOWN:
            if   event.key == pygame.K_a or event.key == pygame.K_LEFT:  self.camera_movement[0] = True
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT: self.camera_movement[1] = True
            elif event.key == pygame.K_w or event.key == pygame.K_UP:    self.camera_movement[2] = True
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:  self.camera_movement[3] = True
        elif event.type == pygame.KEYUP:
            if   event.key == pygame.K_a or event.key == pygame.K_LEFT:  self.camera_movement[0] = False
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT: self.camera_movement[1] = False
            elif event.key == pygame.K_w or event.key == pygame.K_UP:    self.camera_movement[2] = False
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:  self.camera_movement[3] = False

        # 2d camera
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT: self.camera_2d = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT: self.camera_2d = False

    def _Camera_Rotate(self, dx):
        # degrees
        self.camera_rot = (self.camera_rot - dx * self.act.scene_settings.camera_rot_speed) % 360
        self.camera_rad = math.radians(self.camera_rot)


    def _Camera_Scale(self, dy):
        self.camera_scale += dy / 100

    
    def _Camera_Move(self):
        if self.camera_movement[0]: # left
            self.camera_pos[0] += math.cos(self.camera_rad + math.pi) * self.act.scene_settings.camera_move_speed
            self.camera_pos[1] -= math.sin(self.camera_rad + math.pi) * self.act.scene_settings.camera_move_speed
        if self.camera_movement[1]: # right
            self.camera_pos[0] += math.cos(self.camera_rad) * self.act.scene_settings.camera_move_speed
            self.camera_pos[1] -= math.sin(self.camera_rad) * self.act.scene_settings.camera_move_speed
        if self.camera_movement[2]: # up
            self.camera_pos[0] += math.cos(self.camera_rad + math.pi / 2) * self.act.scene_settings.camera_move_speed
            self.camera_pos[1] -= math.sin(self.camera_rad + math.pi / 2) * self.act.scene_settings.camera_move_speed
        if self.camera_movement[3]: # down
            self.camera_pos[0] += math.cos(self.camera_rad - math.pi / 2) * self.act.scene_settings.camera_move_speed
            self.camera_pos[1] -= math.sin(self.camera_rad - math.pi / 2) * self.act.scene_settings.camera_move_speed


    def On_Render(self) -> None:
        self._Render_Background()
        self._Render_Bounds()
        self._Render_CameraCenter()
        self._Render_Stars()
        self._Render_Compass()
        self._Render_Debug()

        
    def _Render_Background(self):
        self.surface.fill("#0a0a0a")


    def _Render_Bounds(self):
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


    def _Render_CameraCenter(self):
        CROSSHALDWIDTH = 5
        pygame.draw.line(self.surface, "#ffffff", 
            (self.surface.get_width() / 2 - CROSSHALDWIDTH, self.surface.get_height() / 2 - CROSSHALDWIDTH), 
            (self.surface.get_width() / 2 + CROSSHALDWIDTH, self.surface.get_height() / 2 + CROSSHALDWIDTH),
        )
        pygame.draw.line(self.surface, "#ffffff", 
            (self.surface.get_width() / 2 - CROSSHALDWIDTH, self.surface.get_height() / 2 + CROSSHALDWIDTH), 
            (self.surface.get_width() / 2 + CROSSHALDWIDTH, self.surface.get_height() / 2 - CROSSHALDWIDTH),
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


    
    def _Point_To_Cam(self, *__point:tuple[int, int]|tuple[int, int, int]) -> tuple[int, int]:
        # Extract X Y Z
        ## __point is [X Y Z]
        if len(__point) == 3:  
            __x, __y, __z = __point
        ## __point is [X Y]
        if len(__point) == 2:  
            __x, __y = __point
            __z = 0
        ## __point is point
        if len(__point) == 1:  
            return self._Point_To_Cam(*__point[0])

        # Modify
        ## 2D
        if self.camera_2d: 
            ## camera position
            __x -= self.camera_pos[0]
            __y -= self.camera_pos[1]
            ## camera rotation
            __x, __y, __z = (
                __x * math.cos(self.camera_rad) - __y * math.sin(self.camera_rad),
                __x * math.sin(self.camera_rad) + __y * math.cos(self.camera_rad),
                0)
            ## scale
            __x *= self.camera_scale
            __y *= self.camera_scale
            ## screen center
            __x += self.surface.get_width() / 2
            __y += self.surface.get_height() / 2

        ## 3D
        else: 
            ## camera position
            __x -= self.camera_pos[0]
            __y -= self.camera_pos[1]
            ## camera rotation
            __cos = math.cos(self.camera_rad)
            __sin = math.sin(self.camera_rad)
            ### X rotation
            # __x, __y, __z = (
            #     + __x *   1   - __y *   0   + __z *   0  ,
            #     + __x *   0   + __y * __cos - __z * __sin,
            #     + __x *   0   + __y * __sin + __z * __cos)
            # ### Y rotation
            # __x, __y, __z = (
            #     + __x * __cos - __y *   0   + __z * __sin,
            #     + __x *   0   + __y *   1   + __z *   0  ,
            #     - __x * __sin + __y *   0   + __z * __cos)
            ### Z rotation
            __x, __y, __z = (
                + __x * __cos - __y * __sin + __z *   0  ,
                + __x * __sin + __y * __cos + __z *   0  ,
                + __x *   0   + __y *   0   + __z *   1  )
            ## scale
            __x *= self.camera_scale
            __y *= self.camera_scale
            __z *= self.camera_scale
            ## screen center
            __x += self.surface.get_width() / 2
            __y += self.surface.get_height() / 2

        # Return
        ## __point is [X Y Z]
        if len(__point) == 3: 
            return (__x, __y, __z)
        ## __point is [X Y]
        if len(__point) == 2: 
            return (__x, __y)