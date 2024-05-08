from library.common import *
from library.draw.draw import Draw

class EventCallback(Protocol):
    def __call__(self, event: pygame.event.Event) -> None:
        pass

EventCallbackValue = EventCallback | List[EventCallback]

class Action:
    def __init__(self, callbacks: EventCallbackValue):
        self.is_pressed = False
        self._callbacks: List[EventCallback] = []

        if not isinstance(callbacks, list):
            self._callbacks = [callbacks]
        else:
            self._callbacks = callbacks
    
    def callbacks(self, event: pygame.event.Event):
        for callback in self._callbacks:
            callback(event)
    
    def append(self, callbacks: EventCallbackValue):
        if not isinstance(callbacks, list):
            callbacks = [callbacks]
        
        for callback in callbacks:
            self._callbacks.append(callback)
        

class Interact:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)

        self.next: Interact | None = None
        self.prev: Interact | None = None

        self.color = pygame.Color("white")
        self.color_disabled = pygame.Color("darkgray")
        self.color_normal = pygame.Color("white")
        self.color_selected = pygame.Color("lightblue")
        self.color_pressed = pygame.Color("gray")

        self.draws: List[Draw] = []

        self._enabled = True
        self._pressed = False
        self._selected = False

        self.keyActions: Dict[int, Action] = {}
        self.buttonActions: Dict[int, Action] = {}
    
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

    def add_draw(self, draw: Draw):
        self.draws.append(draw)
    
    def add_draws(self, draws: List[Draw]):
        for draw in draws:
            self.add_draw(draw)
    
    def set_draws_color(self, color: ColorValue):
        for draw in self.draws:
            draw.color = pygame.Color(color)

    def add_key(self, key: int, callbacks: EventCallbackValue):
        if key in self.keyActions:
            self.keyActions[key].append(callbacks)
        else:
            self.keyActions[key] = Action(callbacks)

    def add_keys(self, keys: List[int], callbacks: EventCallbackValue):
        for key in keys:
            self.add_key(key, callbacks)

    def add_button(self, button: int, callbacks: EventCallbackValue):
        if button in self.buttonActions:
            self.buttonActions[button].append(callbacks)
        else:
            self.buttonActions[button] = Action(callbacks)
    
    def add_buttons(self, buttons: List[int], callbacks: EventCallbackValue):
        for button in buttons:
            self.add_button(button, callbacks)

    def clear_pressed(self):
        for _, action in self.keyActions.items():
            action.is_pressed = False
        
        for _, action in self.buttonActions.items():
            action.is_pressed = False
        
        self.pressed = False

    def on_key_event(self, event: pygame.event.Event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key not in self.keyActions:
            return

        self.keyActions[event.key].callbacks(event)
    
    def on_button_event(self, event: pygame.event.Event):
        if event.type != pygame.MOUSEBUTTONDOWN and event.type != pygame.MOUSEBUTTONUP:
            return
        
        if event.button not in self.buttonActions:
            return
        
        action = self.buttonActions[event.button]

        if event.type == pygame.MOUSEBUTTONDOWN:
            action.is_pressed = True
            self.pressed = True
        
        elif action.is_pressed:
            self.clear_pressed()
            if self.rect.collidepoint(event.pos):
                action.callbacks(event)

    def on_event(self, event: pygame.event.Event):
        if not self.enabled:
            return
        
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.selected = True
            return
        
        if self.selected:
            self.on_key_event(event)
            self.on_button_event(event)
    
    def update(self, events: List[pygame.event.Event]):
        for event in events:
            self.on_event(event)
    
    def draw(self, surface: pygame.surface.Surface):
        for draw in self.draws:
            draw.draw(surface)
