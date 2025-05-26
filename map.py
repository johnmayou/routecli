from typing import TypedDict

class Node(TypedDict):
  id: int
  lat: float
  lng: float

class Edge(TypedDict):
  id: int
  name: str
  node_ids: list[int]
  
class Bounds(TypedDict):
  minlat: float
  minlng: float
  maxlat: float
  maxlng: float