from ..common import *

class EventCallback(Protocol):
    def __call__(self, event: Event) -> None:
        pass

EventCallbackOrList = EventCallback | list[EventCallback]

class Action:
    def __init__(self, callbacks: EventCallbackOrList, mods: IntOrList = []):
        self.pressed = False
        self._callbacks: list[EventCallback] = []

        self.mods = to_list(mods)

        self._callbacks = to_list(callbacks)
    
    def add_mods(self, mods: IntOrList) -> Self:
        for modifier in to_list(mods):
            self.mods.append(modifier)

        return self

    def has_mods(self) -> bool:
        return len(self.mods) > 0

    def mods_pressed(self):
        if not self.has_mods():
            return True
        
        mods = pygame.key.get_mods()
        for mod in self.mods:
            if not mods & mod:
                return False
        
        return True

    def exact_mods_pressed(self):
        mods = pygame.key.get_mods()
        for mod in self.mods:
            if not mods & mod:
                return False
        
        for mod in [pygame.KMOD_CTRL, pygame.KMOD_ALT, pygame.KMOD_SHIFT]:
            if mods & mod and mod not in self.mods:
                return False
        
        return True

    def callbacks(self, event: Event):
        if self.mods_pressed:
            for callback in self._callbacks:
                callback(event)
            
            self.pressed = False
    
    def add_callbacks(self, callbacks: EventCallbackOrList) -> Self:
        for callback in to_list(callbacks):
            self._callbacks.append(callback)
        
        return self

_ActionDict = dict[int, list[Action]]

class Interact:
    def __init__(self):
        self.rect = pygame.Rect(0.0, 0.0, 0.0, 0.0)

        self.next: Interact | None = None
        self.prev: Interact | None = None
        self.parent: Interact | None = None
        self.name = ""

        self._enabled = True
        self._pressed = False
        self._selected = False
        self._highlighted = False

        self._key_actions: _ActionDict = {}
        self._button_actions: _ActionDict = {}
    
    def named(self, name: str) -> Self:
        self.name = name
        return self
    
    # Getters / Setters

    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool):
        if self._enabled != value:
            self._on_enabled(None) if value else self._on_disabled(None)

        self._enabled = value
    
    @property
    def pressed(self):
        return self._pressed
    
    @pressed.setter
    def pressed(self, value: bool):
        if self._pressed != value:
            self._on_pressed(None) if value else self._on_released(None)
        
        self._pressed = value
    
    @property
    def selected(self):
        return self._selected
    
    @selected.setter
    def selected(self, value: bool):
        if self._selected != value:
            self._on_selected(None) if value else self._on_unselected(None)
        
        self._selected = value
    
    @property
    def highlighted(self):
        return self._highlighted
    
    @highlighted.setter
    def highlighted(self, value: bool):
        if self._highlighted != value:
            self._on_highlighted(None) if value else self._on_unhighlighted(None)
        
        self._highlighted = value
    
    # Events

    def _on_enabled(self, event: Event):
        self.send_event("_on_enabled", event)
    
    def _on_disabled(self, event: Event):
        self.send_event("_on_disabled", event)
        
        self.pressed = False
        self.selected = False
        self.highlighted = False

    def _on_pressed(self, event: Event):
        self.send_event("_on_pressed", event)
    
    def _on_released(self, event: Event):
        self.send_event("_on_released", event)

    def _on_selected(self, event: Event):
        self.send_event("_on_selected", event)
    
    def _on_unselected(self, event: Event):
        self.send_event("_on_unselected", event)

    def _on_highlighted(self, event: Event):
        self.send_event("_on_highlighted", event)
        
    def _on_unhighlighted(self, event: Event):
        self.send_event("_on_unhighlighted", event)

    def _on_key_event(self, event: Event):
        if event == None or event.type not in [pygame.KEYDOWN, pygame.KEYUP]:
            return

        if event.key not in self._key_actions:
            return

        if event.type == pygame.KEYDOWN:
            for action in self._key_actions[event.key]:
                if action.exact_mods_pressed():
                    action.callbacks(event)
                    self.pressed = True
        
        else:
            if event.key in self._key_actions:
                self.pressed = False
    
    def _on_button_event(self, event: Event):
        if event == None or event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            return
        
        if event.button not in self._button_actions:
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for action in self._button_actions[event.button]:
                if action.mods_pressed():
                    action.pressed = True

                    if action.has_mods():
                        for other_action in self._button_actions[event.button]:
                            if other_action != action:
                                other_action.pressed = False
                        break
            
            self.pressed = True
        
        else:
            if self.rect.collidepoint(event.pos):
                for action in self._button_actions[event.button]:
                    if action.pressed:
                        action.callbacks(event)
            
            self.pressed = False

    def _on_event(self, event: Event):
        if not self.enabled or event == None:
            return
        
        if event.type == pygame.MOUSEMOTION:
            self.highlighted = self.rect.collidepoint(event.pos)
        
        if self.selected:
            self._on_key_event(event)
        
        if self.highlighted:
            self._on_button_event(event)

    def receive_event(self, interact: Self, event_name: str, event: Event):
        pass

    def send_event(self, event_name: str, event: Event):
        if self.parent != None:
            self.parent.receive_event(self, event_name, event)

    # Methods

    def _add_actions(self, action_code: int, action_dict: _ActionDict, callbacks: EventCallbackOrList, mods: IntOrList = []) -> Self:
        if action_code in action_dict:
            action_dict[action_code].append(Action(callbacks, mods))
        else:
            action_dict[action_code] = [Action(callbacks, mods)]
        
        return self

    def add_key(self, keys: IntOrList, callbacks: EventCallbackOrList, mods: IntOrList = []) -> Self:
        for key in to_list(keys):
            self._add_actions(key, self._key_actions, callbacks, mods)

        return self

    def clear_keys(self):
        self._key_actions.clear()

    def add_button(self, buttons: IntOrList, callbacks: EventCallbackOrList, mods: IntOrList = []) -> Self:
        for button in to_list(buttons):
            self._add_actions(button, self._button_actions, callbacks, mods)

        return self

    def clear_buttons(self):
        self._button_actions.clear()
    
    def update(self, dt: float, events: list[Event]):
        for event in events:
            self._on_event(event)
