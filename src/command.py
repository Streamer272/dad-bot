from typing import List, Callable
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Argument:
    index: int
    example: str
    description: str


@dataclass(frozen=True, order=True)
class Command:
    name: str
    description: str
    arguments: List[Argument]
    callback: Callable
