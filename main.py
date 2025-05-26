from collections import defaultdict
from directions import humanized
from pathlib import Path
from route import Route
import parser
import dotenv
import astar

dotenv.load_dotenv()

def main():
  bounds, nodes, edges = parser.Xml().parse(str(Path(__file__).resolve().parent / 'map.xml'))
  
  # each tuple is (neighbor_id, edge_id)
  adj_list: dict[int, list[tuple[int, int]]] = defaultdict(list)
  for edge in edges:
    for i in range(len(edge["node_ids"])-1):
      a, b = edge["node_ids"][i], edge["node_ids"][i+1]
      adj_list[a].append((b, edge["id"]))
      adj_list[b].append((a, edge["id"]))

  routable_nodes = [node for node in nodes if node["id"] in adj_list]      
  node_map = {node["id"]: node for node in routable_nodes}
  edge_map = {edge["id"]: edge for edge in edges}
  
  path = astar.astar(
    node_map,
    adj_list,
    start_id=Route.closest_node(Route.get_start_coordinates(bounds), routable_nodes)["id"],
    goal_id=Route.closest_node(Route.get_destination_coordinates(bounds), routable_nodes)["id"]
  )
  
  miles, directions = humanized(path, node_map, edge_map)
  print("\nDirections:")
  for i, direction in enumerate(directions):
    print(f"  {i}. {direction}")
  print(f"\nTotal Miles: {miles}\n")

if __name__ == "__main__":
  main()