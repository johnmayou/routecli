from typing import TypedDict
import heapq
import math
import map

class Step(TypedDict):
  from_id: int
  to_id: int
  edge_id: int
  edge_len: float

# Based on pseudocode at https://en.wikipedia.org/wiki/A*_search_algorithm
def astar(
  node_map: dict[int, map.Node],
  adj_list: dict[int, list[tuple[int, int]]], # each tuple is (neighbor_id, edge_id)
  start_id: int,
  goal_id: int
) -> list[Step]:
  # Use euclidian distance as heuristic since it's the straight line path to the goal. Since we're using a map with a small bounding box, we can get away with not using something like Haversine.
  def heuristic(curr_node: map.Node) -> float:
    return euclidian(curr_node, node_map[goal_id])
  
  # Set of discovered nodes that need to be processed, implemented with a min-heap.
  open_set: list[tuple[float, int]] = [(heuristic(node_map[start_id]), start_id)]
  heapq.heapify(open_set)
  
  # came_from[n] is the node immediately preceding it on the shortest path from the start (of known paths).
  came_from: dict[int, Step] = {}
  
  # g_score[n] is the currently known cost of the shortest path from start to n.
  g_score: dict[int, float] = {start_id: 0}
  
  while open_set:
    _, curr_id = heapq.heappop(open_set)
    if curr_id == goal_id:
      path: list[Step] = []
      while curr_id in came_from:
        step = came_from[curr_id]
        path.append(step)
        curr_id = step["from_id"]
      path.reverse()
      return path
    
    curr_node = node_map[curr_id]
    for nei_id, edge_id in adj_list[curr_id]:
      edge_len = euclidian(curr_node, node_map[nei_id])
      nei_g_score = g_score[curr_id] + edge_len
      if nei_id not in g_score or nei_g_score < g_score[nei_id]:
        # This path to neighbor is better than any previous one, override it.
        came_from[nei_id] = {
          "from_id": curr_id,
          "to_id": nei_id,
          "edge_id": edge_id,
          "edge_len": edge_len
        }
        g_score[nei_id] = nei_g_score
        heapq.heappush(open_set, (nei_g_score + heuristic(node_map[nei_id]), nei_id))

  raise RuntimeError("Could not reach destination.")

def euclidian(n1: map.Node, n2: map.Node) -> float:
  return math.sqrt((n1["lat"] - n2["lat"])**2 + (n1["lng"] - n2["lng"])**2)