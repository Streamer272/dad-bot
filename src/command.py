from typing import List, Callable
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Argument:
    index: int
    example: str
    description: str
    # TODO: make these actually work
    is_string: bool
    required: bool


@dataclass(frozen=True, order=True)
class Command:
    name: str
    description: str
    arguments: List[Argument]
    callback: Callable
