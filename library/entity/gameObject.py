import json

from ..common import *
from ..serializable import Serializable

from ..component import *

class GameObject(Serializable):
    def __init__(self):
        self.info = Info()

        self.components: list[Component] = [self.info]
    
    def update(self, dt: float, events: list[Event]):
        pass
    
    def serialize(self) -> str | None:
        data = {
            "components": {}
        }

        for component in self.components:
            component_data = component.serialize()

            if component_data != None:
                data["components"][component.__class__.__name__.lower()] = component_data
        
        return json.dumps(data)
    
    def deserialize(self, json_data: str) -> Self:
        data = json.loads(json_data)

        for name, component_data in data.get("components", {}):
            component = component_from_name(name)

            if component != None:
                self.components.append(component().deserialize(component_data))
        
        return self
