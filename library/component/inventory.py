from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..entity import Item

from enum import Enum

from ..common import *
from ..fonts import *

from . import Component

class Inventory(Component):
    class Slot():
        def __init__(self, item: Item, quantity: int = 1):
            self.item = item
            self.quantity = quantity
    
    SortStyle = Literal[
        "name",
        "quantity",
        "value",
        "rarity",
    ]

    def __init__(self):
        super().__init__()

        self.slots: list[Inventory.Slot] = []
        self.sort_style: Inventory.SortStyle = "name"
    
    def __contains__(self, item: Slot | Item | str):
        name = self.name_of(item)

        for slot in self.slots:
            if self.name_of(slot) == name:
                return True
        
        return False

    # Getters / Setters

    def name_of(self, obj: Slot | Item | str) -> str:
        if isinstance(obj, Inventory.Slot):
            return obj.item.info.name
        elif isinstance(obj, Item):
            return obj.info.name
        else:
            return obj

    def get_slot(self, item: Slot | Item | str) -> Slot | None:
        name = self.name_of(item)

        for slot in self.slots:
            if self.name_of(slot) == name:
                return slot
    
    def get_slots(self, item: Slot | Item | str) -> list[Slot]:
        name = self.name_of(item)
        slots = []

        for slot in self.slots:
            if self.name_of(slot) == name:
                slots.append(slot)
        
        return slots
    
    def get_index(self, item: Slot | Item | str) -> int:
        name = self.name_of(item)

        for i in range(len(self.slots)):
            if self.slots[i].item.name == name:
                return i
        
        return -1
    
    def get_indices(self, item: Slot | Item | str) -> list[int]:
        name = self.name_of(item)

        indices = []

        for i in range(len(self.slots)):
            if self.slots[i].item.name == name:
                indices.append(i)
        
        return indices

    # Methods

    def add(self, item: Item, quantity: int = 1):
        if quantity <= 0:
            return
        
        if item.stackable:
            slot = self.get_slot(item)

            if slot != None:
                slot.quantity += quantity
            else:
                self.slots.append(Inventory.Slot(item, quantity))
        else:
            for i in range(quantity):
                self.slots.append(Inventory.Slot(item, 1))
            
        self.sort()
    
    def remove(self, item: Item | str, quantity: int = 1):
        if quantity <= 0:
            return False
        
        first = self.get_slot(item)

        if first == None:
            return
        
        if first.item.stackable:
            first.quantity -= quantity

            if first.quantity <= 0:
                self.slots.pop(self.get_index(first))
        else:
            for i in self.get_indices(first):
                self.slots.pop(i)
    
    def quantity(self, item: Slot | Item | str):
        return sum([slot.quantity for slot in self.get_slots(item)])
    
    def sort(self):
        match self.sort_style:
            case "name":
                self.slots.sort(key = lambda x: x.item.info.name)
            
            case "quantity":
                self.slots.sort(key = lambda x: x.quantity)
            
            case "value":
                pass

            case "rarity":
                pass
