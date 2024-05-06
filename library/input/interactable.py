import pygame

from library.common import *
from library.input.inputCode import InputCode, InputCodeValue

class EventCallable(Protocol):
    def __call__(self, event: pygame.event.Event) -> None:
        pass

CallbackValue = Tuple[str, EventCallable]

class Interactable:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)

        self.next: Interactable | None = None
        self.prev: Interactable | None = None

        self.color = pygame.Color("white")
        self.color_disabled = pygame.Color("darkgray")
        self.color_normal = pygame.Color("white")
        self.color_selected = pygame.Color("lightblue")
        self.color_pressed = pygame.Color("gray")

        self._enabled = True
        self._pressed = False
        self._selected = False

        def empty(event: pygame.event.Event):
            pass

        self.callbacks: Dict[str, EventCallable] = {"main": empty}

        self.esc_cancels = True
        
        self.keys: List[InputCode] = []
        self.buttons: List[InputCode] = []
    
    # Getters / Setters

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

    # Methods

    def _add_input_code(self, input_code_list: List[InputCode], input_code: InputCodeValue):
        if type(input_code) is Tuple:
            input_code_list.append(InputCode(input_code[0], to_list(input_code[1])))
        else:
            input_code_list.append(InputCode(input_code)) # type: ignore

    def add_key(self, key: InputCodeValue):
        self._add_input_code(self.keys, key)

    def add_keys(self, keys: List[InputCodeValue]):
        for key in keys:
            self.add_key(key)

    def set_keys(self, keys: List[InputCodeValue]):
        self.keys.clear()
        self.add_keys(keys)

    def add_button(self, button: InputCodeValue):
        self._add_input_code(self.buttons, button)
    
    def add_buttons(self, buttons: List[InputCodeValue]):
        for button in buttons:
            self.add_button(button)

    def set_buttons(self, buttons: List[InputCodeValue]):
        self.buttons.clear()
        self.add_buttons(buttons)

    def clear_pressed(self):
        for key in self.keys:
            key.pressed = False
        
        for button in self.buttons:
            button.pressed = False
        
        self.pressed = False
    
    def add_callback(self, callback: CallbackValue):
        self.callbacks[callback[0]] = callback[1]
    
    def add_callbacks(self, callbacks: List[CallbackValue]):
        for callback in callbacks:
            self.add_callback(callback)

    def set_callbacks(self, callbacks: List[CallbackValue]):
        self.callbacks.clear()
        self.add_callbacks(callbacks)

    def _call_callbacks(self, event: pygame.event.Event, input_code: InputCode):
        for k in self.callbacks:
            if input_code.has_callback(k):
                self.callbacks[k](event)
        
        self.clear_pressed()

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            for key in self.keys:
                if event.key == key.code:
                    key.pressed = True
                    self.pressed = True
                    break

            if self.esc_cancels and event.key == pygame.K_ESCAPE:
                self.clear_pressed()
        
        elif event.type == pygame.KEYUP:
            for key in self.keys:
                if event.key == key.code:
                    self._call_callbacks(event, key)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if event.button == button.code:
                    button.pressed = True
                    self.pressed = True
                    break
        
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in self.buttons:
                if event.button == button.code and self.rect.collidepoint(event.pos):
                    self._call_callbacks(event, button)
        
        elif event.type == pygame.MOUSEMOTION:
            self.selected = self.rect.collidepoint(event.pos)
    
    def update(self, events: List[pygame.event.Event]):
        for event in events:
            self.on_event(event)

    def draw(self, surface: pygame.Surface, offset: Coordinate = (0, 0)):
        pass
