from .component import Component
from .life import Life
from .mana import Mana
from .experience import Experience
from .level import Level
from .info import Info

_name_to_component: dict[str, type[Component]] = {
    "component": Component,
    "health": Life,
    "mana": Mana,
    "experience": Experience,
    "level": Level,
}

def component_from_name(name: str) -> type[Component] | None:
    return _name_to_component.get(name, None)
