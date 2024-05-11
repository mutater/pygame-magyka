from .common import *

class Serializable:
    def serialize(self) -> str | None:
        pass

    def deserialize(self, json_data: str) -> Self:
        return self
