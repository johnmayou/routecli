from pathlib import Path
from typing import cast
import map

class Xml:
  def parse(self, path: str) -> tuple[map.Bounds, list[map.Node], list[map.Edge]]:
    bounds = {}
    nodes: list[map.Node] = []
    edges: list[map.Edge] = []
    
    with open(path, "r") as file:
      line = file.readline()
      while line:
        line = line.strip()
        if line.startswith("<bounds "):
          for part in line.split(" "):
            if part.startswith("minlat"): bounds["minlat"] = float(part[8:-1])
            elif part.startswith("minlon"): bounds["minlng"] = float(part[8:-1])
            elif part.startswith("maxlat"): bounds["maxlat"] = float(part[8:-1])
            elif part.startswith("maxlon"): bounds["maxlng"] = float(part[8:-3]) # /> at the end
        elif line.startswith("<node "):          
          node = cast(map.Node, {})
          for part in line.split(" "):
            if part.startswith("id"):
              node["id"] = int(part[4:-1])
            elif part.startswith("lat"):
              node["lat"] = float(part[5:-1])
            elif part.startswith("lon"):
              node["lng"] = float(part[5:-1])
              break # should be last of what we need
          if not node["id"] or not node["lat"] or not node["lng"]:
            raise RuntimeError(f"Invalid node: {line}")
          nodes.append(node)
        elif line.startswith("<way "):
          edge = cast(map.Edge, {"name": "", "node_ids": []})
          for part in line.split(" "):
            if part.startswith("id"):
              edge["id"] = int(part[4:-1])
              break
          line = file.readline()
          routable = False
          while line:
            line = line.strip()
            if "footway" in line or "highway" in line:
              routable = True
            if line.startswith("<nd ref=\"") and line.endswith("\"/>"):
              edge["node_ids"].append(int(line[9:-3]))
            if line.startswith("<tag k=\"name\""):
              start = 0
              while True:
                if line[start] == "v":
                  start += 3
                  break
                start += 1
              end = start
              while True:
                if line[end+1] == "\"":
                  break
                end += 1
              edge["name"] = line[start:end+1]
            elif line.startswith("</way>"):
              break
            line = file.readline()
          if routable:
            edges.append(edge)
        line = file.readline()
        
    if not bounds["minlat"] or not bounds["minlng"] or not bounds["maxlat"] or not bounds["maxlng"]:
      raise RuntimeError(f"Invalid bounds: {bounds}")
          
    return (cast(map.Bounds, bounds), nodes, edges)
  
if __name__ == "__main__":
  bounds, nodes, edges = Xml().parse(str(Path(__file__).resolve().parent / 'map.xml'))
  print("Bounds:")
  print(bounds)
  print(f"Nodes: {len(nodes)}")
  print(nodes[0])
  print(f"Edges: {len(edges)}")
  print(edges[0])