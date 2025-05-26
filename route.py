from typing import TypedDict, cast
import requests
import math
import map
import os

class Coordinates(TypedDict):
  lat: float
  lng: float

class Route:
  @classmethod
  def get_start_coordinates(cls, bounds: map.Bounds) -> Coordinates:
    return cls._prompt_adr_and_fetch_coordinates("What is your current address: ", bounds)
                
  @classmethod
  def get_destination_coordinates(cls, bounds: map.Bounds) -> Coordinates:
    return cls._prompt_adr_and_fetch_coordinates("What is your destination address: ", bounds)
  
  @classmethod
  def closest_node(cls, coords: Coordinates, nodes: list[map.Node]) -> map.Node:
    if not nodes:
      raise RuntimeError("Must have at least one node in nodes")
    
    closest_node: map.Node = nodes[0]
    closest_dist: float = float('inf')
    
    for node in nodes:
      dist = math.sqrt((coords["lat"] - node["lat"])**2 + (coords["lng"] - node["lng"])**2)
      if dist < closest_dist:
        closest_node = node
        closest_dist = dist
      
    return closest_node
  
  @classmethod
  def _prompt_adr_and_fetch_coordinates(cls, prompt: str, bounds: map.Bounds) -> Coordinates:
    while True:
      response = requests.get(
        "https://api.opencagedata.com/geocode/v1/json",
        params={
          "q": input(prompt),
          "key": os.getenv("OPEN_CAGE_DATA_API_KEY")
        }
      )
      if response.status_code == 200:
        places = response.json()["results"]
        if len(places) == 0:
          print("No place was found for that address, please try again.")
          continue
        
        for place in places:
          placetype = place["components"]["_type"]
          if placetype != "building":
            print(f"Skipping place of type: {placetype}")
            continue
            
          coords = cast(Coordinates, place["geometry"])
          if not cls._within_bounds(coords, bounds):
            print(f"Found a building, but it was not within bounds:\n  bounds: {bounds}\n  coords: {coords}")
            continue
            
          return coords
      else:
        print(f"Address lookup error, please try again: {response.status_code} - {response.text}")
  
  @classmethod
  def _within_bounds(cls, coords: Coordinates, bounds: map.Bounds) -> bool:
    return (
      bounds["minlat"] <= coords["lat"] <= bounds["maxlat"] and
      bounds["minlng"] <= coords["lng"] <= bounds["maxlng"]
    )