from ..common import *

from . import Point
from . import Cardinal

class Widget():
    def __init__(self, parent: Self | None = None):
        self.name: str = ""
        """This widget's name."""
        self.children: list[Self] = []
        """This widget's children."""

        self.rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        """This widget's bounding box."""
        self.children_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        """This widget's childrens' bounding box."""

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

        self.is_focussed: bool = False
        """Whether or not this widget has keyboard focus."""
        self.focus_allowed: bool = False
        """Whether or not this widget is allowed to have keyboard focus."""

        self.is_visible: bool = False
        """Whether or not this widget is visible."""

        self.align: str = "topleft"
        """
        This widget's alignment.
        
        Valid alignments are:
        ```
        topleft,    midtop,    topright,
        midleft,    center,    midright,
        bottomleft, midbottom, bottomright
        ```
        """

        self.margins: Cardinal = Cardinal(0, 0, 0, 0)

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

    # --------------------------------------------------------------------------------------------

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