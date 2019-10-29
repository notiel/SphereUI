from dataclasses import dataclass
from typing import  List

@dataclass
class group:
    name: str
    leds: List[int]
    effects: List[str]

    def __init__(self, name: str, leds: List[int]):
        self.name = name
        self.leds = leds
        self.effects = list()
