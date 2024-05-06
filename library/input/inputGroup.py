import pygame

from library.common import *
from library.input.interactable import Interactable

class InputGroup(Interactable):
    def __init__(self, dest: Coordinate):
        super().__init__()
        self.dest = dest
        self.interactables: List[Interactable] = []
        self.head: Interactable | None = None
        self.tail: Interactable | None = None
        self.selected: Interactable | None = None

        self.add_keys([
            (pygame.K_DOWN, "next"),
            (pygame.K_UP, "prev")
        ])

        self.add_callbacks([
            ("next", self.select_next),
            ("prev", self.select_prev)
        ])
    
    def add_interactable(self, interactable: Interactable):
        if self.head == None or self.tail == None:
            self.head = interactable
            self.tail = interactable
        interactable.next = self.head
        interactable.prev = self.tail
        self.tail.next = interactable
        self.head.prev = interactable
        self.tail = interactable
    
    def select_next(self, event: pygame.event.Event):
        if self.selected != None:
            self.selected = self.selected.next
        else:
            self.selected = self.head
    
    def select_prev(self, event: pygame.event.Event):
        if self.selected != None:
            self.selected = self.selected.prev
        else:
            self.selected = self.tail

    def on_event(self, event: pygame.event.Event):
        i = self.head

        while i != None:
            i.on_event(event)

            i = i.next

            if i == self.head:
                break
    
    def draw(self, surface: pygame.Surface, offset: Coordinate = (0, 0)):
        i = self.head

        while i != None:
            i.draw(surface, add_coords(self.dest, offset))

            i = i.next

            if i == self.head:
                break
