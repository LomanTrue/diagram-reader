from dataclasses import dataclass
from typing import List

@dataclass
class Node:
    id: str
    type: str
    text: str
    bbox: list

@dataclass
class Edge:
    source: str
    target: str

@dataclass
class DiagramGraph:
    nodes: List[Node]
    edges: List[Edge]
