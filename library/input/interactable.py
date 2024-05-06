import pygame

from library.common import *
from library.input.inputCode import InputCode

class Interactable:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)

        self.color = pygame.Color("white")
        self.color_disabled = pygame.Color("white")
        self.color_normal = pygame.Color("white")
        self.color_selected = pygame.Color("white")
        self.color_pressed = pygame.Color("white")

        self._enabled = True
        self._pressed = False
        self._selected = False

        self.callbacks: List[Callable[[pygame.event.Event]]] = []

        self.esc_cancels = True
        
        self.keys: List[InputCode] = []
        self.buttons: List[InputCode] = []
    
    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
        self.color = self.color_disabled if value else self.color_normal
    
    @property
    def pressed(self):
        return self._pressed
    
    @pressed.setter
    def pressed(self, value: bool):
        self._pressed = value
        if self.enabled:
            self.color = self.color_pressed if value else (self.color_selected if self.selected else self.color_normal)

    @property
    def selected(self):
        return self._selected
    
    @selected.setter
    def selected(self, value: bool):
        self._selected = value
        if self.enabled and not self.pressed:
            self.color = self.color_selected if value else self.color_normal

    def set_keys(self, keys: Tuple[InputCode]):
        
        self.keys.clear()
        for key in keys:
            self.keys.append(key)
    
    def add_key(self, key: int, callback_id: List[int] | None = None):
        self.keys.append((key, callback_id))

    def set_buttons(self, buttons: List[Tuple[int, List[int] | None]]):
        self.buttons.clear()
        for button in buttons:
            self.add_button(button[0], button[1])
    
    def add_button(self, button: int, callback_id: List[int] | None = None):
        self.buttons.append((button, callback_id))
    
    def set_callbacks(self, callbacks: List[Callable[[pygame.event.Event]]]):
        self.callbacks.clear()
        for callback in callbacks:
            self.add_callback(callback)
    
    def add_callback(self, callback: Callable[[pygame.event.Event]]):
        self.callbacks.append(callback)

    def call_callbacks(self, event: pygame.event.Event, input_code: Tuple[int, List[int] | None]):
        for i in range(len(self.callbacks)):
            if input_code[1] != None and i in input_code[1]:
                self.callbacks[i](event)
        
        if event.type == pygame.KEYDOWN:
            self.keys_pressed[input_code[0]] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.buttons_pressed[input_code[0]] = False
        
        self.pressed = any(self.keys_pressed.items()) or any(self.buttons_pressed.items())

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            for button in self.keys:
                if event.key == button[0]:
                    self.keys_pressed[event.key] = True
                    break

            if self.esc_cancels and event.key == pygame.K_ESCAPE:
                self.keys_pressed.clear()
                self.buttons_pressed.clear()
        elif event.type == pygame.KEYUP:
            if self.keys_pressed.get(event.key, False):
                self.call_callbacks
                self.keys_pressed[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if event.button == button[0]:
                    self.buttons_pressed[event.button] = True
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.buttons_pressed.get(event.button, False) and self.rect.collidepoint(event.pos):
                self.call_callbacks(event)
                self.buttons_pressed[event.button] = False
        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.selected = True
        
        self.pressed = any(self.keys_pressed.items()) or any(self.buttons_pressed.items())
    
    def draw(self, surface: pygame.Surface):
        pass
