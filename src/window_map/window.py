from engine import Window
from application import application
import pygame
import math



class Window_Map(Window):
    def __init__(self) -> None:
        super().__init__()

        from .scene_map import Scene_Map
        self.scene_map = Scene_Map(self)

        from .scene_edit import Scene_Edit
        self.scene_edit = Scene_Edit(self)

        from .scene_settings import Scene_Settings
        self.scene_settings = Scene_Settings(self)


    def On_Open(self) -> None:
        self.scene_settings.Close()
        self.scene_edit.Close()
        self.scene_map.Open()


    def On_Render(self) -> None:
        self.scene_map.Render()
        self.scene_settings.Render()
        self.scene_edit.Render()


    def On_Handle(self, event: pygame.event.Event) -> None:
        self._Handle_Shortcuts(event)

        self.scene_settings.Handle(event)
        self.scene_edit.Handle(event)
        self.scene_map.Handle(event)


    def _Handle_Shortcuts(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:

            # Open settings
            if event.key == application.keybindings["quicksettings"]:
                self.scene_settings.Toggle()


    def On_Tick(self) -> None:
        self.scene_map.Tick()