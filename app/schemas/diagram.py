from pydantic import BaseModel
from typing import List

class Node(BaseModel):
    id: str
    type: str
    text: str
    bbox: List[int]

class Edge(BaseModel):
    source: str
    target: str

class DiagramResponse(BaseModel):
    graph: dict
    description: str
