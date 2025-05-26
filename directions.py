from typing import Optional
import astar
import math
import map

def humanized(
  steps: list[astar.Step],
  node_map: dict[int, map.Node],
  edge_map: dict[int, map.Edge]
) -> tuple[float, list[str]]:
  total_miles = 0
  directions: list[str] = []
  curr: list[tuple[astar.Step, Optional[str]]] = []
  for step in steps:
    if not curr:
      curr.append((step, None))
      continue
    
    direction = calc_direction(
      prev_node=node_map[step["from_id"]],
      curr_node=node_map[step["to_id"]]
    )
    
    prev_edge = edge_map[curr[-1][0]["edge_id"]]
    curr_edge = edge_map[step["edge_id"]]
    
    if (
      (curr[-1][1] != None and direction != curr[-1][1]) # new direction
      or (prev_edge["id"] != curr_edge["id"] and prev_edge["name"] != curr_edge["name"]) # new street / path
    ):
      miles = round(sum([miles_between_nodes(node_map[step["from_id"]], node_map[step["to_id"]]) for step, _ in curr]), 2)
      total_miles += miles
      directions.append(f"{direction} {miles} miles on {curr_edge["name"]}")
      curr.clear()
      continue
    
    curr.append((step, direction))
      
  return (round(total_miles, 2), directions)

DIRECTIONS = ["E", "N", "W", "S"]

def calc_direction(prev_node: map.Node, curr_node: map.Node) -> str:
  dx = curr_node["lng"] - prev_node["lng"]
  dy = curr_node["lat"] - prev_node["lat"]
  angle = math.atan2(dy, dx)
  return DIRECTIONS[round((math.degrees(angle) % 360) / 90) % 4]

# Haversine formula: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def miles_between_nodes(n1: map.Node, n2: map.Node):
  # convert decimal degrees to radians
  lat1 = math.radians(n1["lat"])
  lng1 = math.radians(n1["lng"])
  lat2 = math.radians(n2["lat"])
  lng2 = math.radians(n2["lng"])

  # haversine formula
  dlat = lat2 - lat1
  dlng = lng2 - lng1
  a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
  c = 2 * math.asin(math.sqrt(a))
  r = 3956
  return c * r