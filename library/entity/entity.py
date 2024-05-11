import json

from ..common import *
from ..serializable import Serializable

from ..component import *

class Entity(Serializable):
    def __init__(self):
        self.components: dict[str, Component] = {}

        self.health: Health
    
    def __getattr__(self, name: str) -> Component | None:
        if name in self.components:
            return self.components[name]

    def add_component(self, components: Component | list[Component]):
        for component in to_list(components):
            self.components[component.name] = component
    
    def update(self, dt: float, events: list[Event]):
        for _, component in self.components.items():
            component.update(dt, events)
    
    def draw(self, surface: Surface):
        for _, component in self.components.items():
            component.draw(surface)
    
    def serialize(self) -> str | None:
        data = {
            "components": {}
        }

        for name, component in self.components.items():
            component_data = component.serialize()

            if component_data != None:
                data["components"][name] = component_data
        
        return json.dumps(data)
    
    def deserialize(self, json_data: str) -> Self:
        data = json.loads(json_data)

        for name, component_data in data.get("components", {}):
            component = component_from_name(name)

            if component != None:
                self.add_component(component().deserialize(component_data))
        
        return self
