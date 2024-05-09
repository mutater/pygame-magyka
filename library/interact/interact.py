from library.common import *
from library.draw.draw import Draw

class EventCallback(Protocol):
    def __call__(self, event: pygame.event.Event) -> None:
        pass

EventCallbackValue = EventCallback | List[EventCallback]

class Action:
    def __init__(self, callbacks: EventCallbackValue, modifiers: List[int] = []):
        self.is_pressed = False
        self._callbacks: List[EventCallback] = []
        self.modifiers: List[int] = []

        if not isinstance(callbacks, list):
            self._callbacks = [callbacks]
        else:
            self._callbacks = callbacks
    
    def add_modifiers(self, modifiers: int | List[int]):
        if not isinstance(modifiers, list):
            modifiers = [modifiers]

        for modifier in modifiers:
            self.modifiers.append(modifier)

    def modifiers_pressed(self):
        if len(self.modifiers) == 0:
            return True
        
        keys = pygame.key.get_pressed()
        for modifier in self.modifiers:
            if modifier not in keys:
                return False
        
        return True

    def callbacks(self, event: pygame.event.Event):
        if self.modifiers_pressed:
            for callback in self._callbacks:
                callback(event)
    
    def add_callbacks(self, callbacks: EventCallbackValue):
        if not isinstance(callbacks, list):
            callbacks = [callbacks]
        
        for callback in callbacks:
            self._callbacks.append(callback)
        

class Interact:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)

        self.next: Interact | None = None
        self.prev: Interact | None = None

        self._enabled = True
        self._pressed = False
        self._selected = False
        self._highlighted = False

        self.keyActions: Dict[int, Action] = {}
        self.buttonActions: Dict[int, Action] = {}
    
    # Getters / Setters

    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool):
        if self._enabled != value:
            self.on_enabled() if value else self.on_disabled()

        self._enabled = value
    
    def on_enabled(self):
        pass
    
    def on_disabled(self):
        self.pressed = False
        self.selected = False
        self.highlighted = False

    @property
    def pressed(self):
        return self._pressed
    
    @pressed.setter
    def pressed(self, value: bool):
        if self._pressed != value:
            self.on_pressed() if value else self.on_released()
        
        self._pressed = value

    def on_pressed(self):
        pass
    
    def on_released(self):
        pass

    @property
    def selected(self):
        return self._selected
    
    @selected.setter
    def selected(self, value: bool):
        if self._selected != value:
            self.on_selected() if value else self.on_unselected()
        
        self._selected = value

    def on_selected(self):
        pass
    
    def on_unselected(self):
        pass

    @property
    def highlighted(self):
        return self._highlighted
    
    @highlighted.setter
    def highlighted(self, value: bool):
        if self._highlighted != value:
            self.on_highlighted() if value else self.on_unhighlighted()
        
        self._highlighted = value
    
    def on_highlighted(self):
        pass
        
    def on_unhighlighted(self):
        pass

    # Methods

    def add_key(self, key: int, callbacks: EventCallbackValue, modifiers: int | List[int] = []):
        if key in self.keyActions:
            self.keyActions[key].add_callbacks(callbacks)
        else:
            self.keyActions[key] = Action(callbacks)
        
        self.keyActions[key].add_modifiers(modifiers)

    def add_keys(self, keys: List[int], callbacks: EventCallbackValue):
        for key in keys:
            self.add_key(key, callbacks)

    def clear_keys(self):
        self.keyActions.clear()

    def add_button(self, button: int, callbacks: EventCallbackValue):
        if button in self.buttonActions:
            self.buttonActions[button].add_callbacks(callbacks)
        else:
            self.buttonActions[button] = Action(callbacks)
    
    def add_buttons(self, buttons: List[int], callbacks: EventCallbackValue):
        for button in buttons:
            self.add_button(button, callbacks)

    def clear_buttons(self):
        self.buttonActions.clear()

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
            self.highlighted = self.rect.collidepoint(event.pos)
        
        if self.selected:
            self.on_key_event(event)
        
        if self.highlighted:
            self.on_button_event(event)
    
    def update(self, events: List[pygame.event.Event]):
        for event in events:
            self.on_event(event)
