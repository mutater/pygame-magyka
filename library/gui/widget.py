import pygame

from typing import Self

from . import Cardinal, Event, Point, Signal

class Widget():
    def __init__(self, parent: Self | None = None, name: str = "", size: tuple[int, int] | Point = (0, 0),
                 align: str = "topleft"):
        self.name: str = name
        """This widget's name."""
        self.children: list[Self] = []
        """This widget's children."""

        self.rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        """This widget's bounding box."""
        self.size: Point = Point(size)
        """This widget's size."""

        self.cursor = None
        """
        The cursor for when the item is hovered.
        
        Valid cursors are:
        ```
        pygame.SYSTEM_CURSOR_ARROW      arrow
        pygame.SYSTEM_CURSOR_IBEAM      i-beam
        pygame.SYSTEM_CURSOR_WAIT       wait
        pygame.SYSTEM_CURSOR_CROSSHAIR  crosshair
        pygame.SYSTEM_CURSOR_NO         slashed circle or crossbones
        pygame.SYSTEM_CURSOR_HAND       hand
        ```
        """

        self.is_visible: bool = False
        """Whether or not this widget is visible."""
        self.is_enabled: bool = True
        """Whether or not this widget is enabled."""

        self.is_focussed: bool = False
        """Whether or not this widget has keyboard focus."""
        self.can_focus: bool = False
        """Whether or not this widget can have keyboard focus."""
        self.is_selected: bool = False
        """Whether or not this widget is selected by the keyboard."""
        self.can_select: bool = True
        """Whether or not this widget can be selected by the keyboard."""
        self.is_hovered: bool = False
        """Whether or not this widget is hovered with the mouse."""
        self.can_hover: bool = False
        """Whether or not this widget can be hovered by the mouse."""
        self.is_pressed: bool = False
        """Whether or not this widget is pressed by the mouse."""
        self.can_press: bool = False
        """Whether or not this widget can be pressed by the mouse."""

        self.align: str = align
        """
        This widget's alignment.
        
        Valid alignments are:
        ```
        topleft,    midtop,    topright,
        midleft,    center,    midright,
        bottomleft, midbottom, bottomright
        ```
        """

        self._parent = None
        self.parent = parent

        # TODO: self.font: Font = default_font
        # """This widget's font used for drawing."""
    
    # - Getters / Setters ------------------------------------------------------------------------

    @property
    def parent(self) -> Self:
        """This widget's parent."""
        return self.parent
    
    @parent.setter
    def parent(self, value: Self | None):
        if value != self._parent:
            if self._parent:
                self._parent.children.remove(self)
            
            if value:
                value.children.append(self)
            
            self._parent = value
    
    @property
    def pos(self) -> Point:
        """The widget's anchor pos based on its alignment."""
        return Point(*getattr(self.rect, self.align))
    
    @pos.setter
    def pos(self, value: tuple[int, int] | Point):
        if isinstance(value, Point):
            value = value.as_tuple()
        
        setattr(self.rect, self.align, value)

    # - General Methods --------------------------------------------------------------------------

    def find_child(self, name: str, recursive: bool = False) -> Self | None:
        for child in self.children:
            if child.name == name:
                return child
            elif recursive:
                grandchild = child.find_child(name, True)

                if grandchild:
                    return grandchild
        
        return None
    
    def find_children(self, name: str, recursive: bool = False) -> list[Self]:
        children: list[Self] = []

        for child in self.children:
            if child.name == name:
                children.append(child)
            
            if recursive:
                grandchildren = child.find_children(name, True)
                children += grandchildren
        
        return children

    def collidepoint(self, point: Point) -> bool:
        """Returns True if a point is inside this widget's rect."""
        return self.rect.collidepoint(point.x, point.y)

    # - Signals ----------------------------------------------------------------------------------

    def _get_signal(self, name: str) -> Signal:
        signal = getattr(self, name, None)

        if signal == None:
            raise AttributeError(f"Widget has no signal '{signal}'")
        
        return signal

    def connect(self, name: str, connection: callable):
        self._get_signal(name).connect(connection)
    
    def disconnect(self, name: str, connection: callable):
        self._get_signal(name).disconnect(connection)
    
    def emit(self, name: str, args):
        self._get_signal(name).emit(args)
    
    def _silent_emit(self, name: str, args):
        try:
            self.emit(name, args)
        except AttributeError:
            pass

    # - Events -----------------------------------------------------------------------------------

    def handle_event(self, event: Event):
        if event.is_handled or not self.is_enabled:
            return
        
        match event.type:
            case Event.Type.KeyDown:
                self.key_down_event(event)
            
            case Event.Type.KeyUp:
                self.key_up_event(event)
            
            case Event.Type.MouseMove:
                self.mouse_move_event(event)

            case Event.Type.MouseDown:
                self.mouse_down_event(event)
            
            case Event.Type.MouseUp:
                self.mouse_up_event(event)

        for child in self.children:
            child.handle_event(event)

            if event.is_handled:
                return

    def key_down_event(self, event: Event):
        if self.is_selected or self.is_focussed:
            self._silent_emit("key_down", event.key, event.mods)
            event.is_handled = True

    def key_up_event(self, event: Event):
        if self.is_selected or self.is_focussed:
            self._silent_emit("key_up", event.key, event.mods)
            event.is_handled = True

    def mouse_move_event(self, event: Event):
        if self.collidepoint(event.pos):
            if self.can_hover:
                self.is_hovered = True
            
            self._silent_emit("mouse_move", event.pos, event.buttons)
            event.is_handled = True
        else:
            if self.is_hovered:
                self.is_hovered = False
    
    def mouse_down_event(self, event: Event):
        if self.collidepoint(event.pos):
            if self.can_focus:
                self.is_focussed = True
                self._silent_emit("focus_gained", event.pos, event.button)
            
            if self.can_pressed:
                self.is_pressed = True
            
            self._silent_emit("mouse_down", event.pos, event.button)
            event.is_handled = True
        else:
            if self.can_focus:
                self.is_focussed = False
                self._silent_emit("focus_lost", event.pos, event.button)

    def mouse_up_event(self, event: Event):
        if self.collidepoint(event.pos):
            if self.is_pressed:
                self.is_pressed = False
                self._silent_emit("clicked", event.pos, event.button)
            
            self._silent_emit("mouse_up", event.pos, event.button)
            event.is_handled = True
        else:
            if self.is_pressed:
                self.is_pressed = False
