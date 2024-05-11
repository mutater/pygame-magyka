from library.common import *

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
        self.rect = pygame.Rect(0, 0, 0, 0)

        self.next: Interact | None = None
        self.prev: Interact | None = None

        self._enabled = True
        self._pressed = False
        self._selected = False
        self._highlighted = False

        self._key_actions: _ActionDict = {}
        self._button_actions: _ActionDict = {}
    
    # Getters / Setters

    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool):
        if self._enabled != value:
            self._on_enabled() if value else self._on_disabled()

        self._enabled = value
    
    def _on_enabled(self):
        pass
    
    def _on_disabled(self):
        self.pressed = False
        self.selected = False
        self.highlighted = False

    @property
    def pressed(self):
        return self._pressed
    
    @pressed.setter
    def pressed(self, value: bool):
        if self._pressed != value:
            self._on_pressed() if value else self._on_released()
        
        self._pressed = value

    def _on_pressed(self):
        pass
    
    def _on_released(self):
        pass

    @property
    def selected(self):
        return self._selected
    
    @selected.setter
    def selected(self, value: bool):
        if self._selected != value:
            self._on_selected() if value else self._on_unselected()
        
        self._selected = value

    def _on_selected(self):
        pass
    
    def _on_unselected(self):
        pass

    @property
    def highlighted(self):
        return self._highlighted
    
    @highlighted.setter
    def highlighted(self, value: bool):
        if self._highlighted != value:
            self._on_highlighted() if value else self._on_unhighlighted()
        
        self._highlighted = value
    
    def _on_highlighted(self):
        pass
        
    def _on_unhighlighted(self):
        pass

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

    def on_key_event(self, event: Event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key not in self._key_actions:
            return

        for action in self._key_actions[event.key]:
            if action.exact_mods_pressed():
                action.callbacks(event)
    
    def on_button_event(self, event: Event):
        if event.type != pygame.MOUSEBUTTONDOWN and event.type != pygame.MOUSEBUTTONUP:
            return
        
        if event.button not in self._button_actions:
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            modifier_found = False

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

    def on_event(self, event: Event):
        if not self.enabled:
            return
        
        if event.type == pygame.MOUSEMOTION:
            self.highlighted = self.rect.collidepoint(event.pos)
        
        if self.selected:
            self.on_key_event(event)
        
        if self.highlighted:
            self.on_button_event(event)
    
    def update(self, dt: float, events: list[Event]):
        for event in events:
            self.on_event(event)
