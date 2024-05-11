from .component import Component
from .health import Health

_name_to_component: dict[str, type[Component]] = {
    "component": Component,
    "health": Health,
}

def component_from_name(name: str) -> type[Component] | None:
    return _name_to_component.get(name, None)
