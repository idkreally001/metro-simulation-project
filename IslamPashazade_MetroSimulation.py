from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Station:
    def __init__(self, idx: str, name: str, line: str, x: float = 0, y: float = 0):
        self.idx = idx
        self.name = name
        self.line = line
        self.x = x  # x-coordinate for heuristic
        self.y = y  # y-coordinate for heuristic
        self.neighbors: List[Tuple['Station', int]] = []  # (station, time) tuples

    def add_neighbor(self, station: 'Station', time: int):
        self.neighbors.append((station, time))

    def distance_to(self, other: 'Station') -> float:
        """Euclidean distance to another station for heuristic."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

class MetroNetwork:
    def __init__(self):
        self.stations: Dict[str, Station] = {}
        self.lines: Dict[str, List[Station]] = defaultdict(list)

    def add_station(self, idx: str, name: str, line: str, x: float = 0, y: float = 0) -> None:
        """Add a station to the metro network."""
        if idx not in self.stations:
            station = Station(idx, name, line, x, y)
            self.stations[idx] = station
            self.lines[line].append(station)

    def add_connection(self, station1_id: str, station2_id: str, time: int) -> None:
        """Add a connection between two stations."""
        try:
            station1 = self.stations[station1_id]
            station2 = self.stations[station2_id]
            station1.add_neighbor(station2, time)
            station2.add_neighbor(station1, time)
        except KeyError as e:
            print(f"Error: One of the stations does not exist. Missing station ID: {e}")

    def find_least_transfers(self, start_id: str, target_id: str) -> Optional[List[Station]]:
        """
        BFS Algorithm: Finds the route with the least transfers.
        """
        if start_id not in self.stations or target_id not in self.stations:
            print("Error: One or both stations do not exist.")
            return None

        start = self.stations[start_id]
        target = self.stations[target_id]

        # Queue and visited set for BFS
        queue = deque([(start, [start])])
        visited = set()

        while queue:
            current_station, path = queue.popleft()

            # If we reach the target, return the path
            if current_station == target:
                return path

            # Check the neighbors
            for neighbor, _ in current_station.neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None  # Return None if no route is found

    def find_fastest_route(self, start_id: str, target_id: str) -> Optional[Tuple[List[Station], int]]:
        """
        A* Algorithm: Finds the fastest route with a heuristic.
        """
        if start_id not in self.stations or target_id not in self.stations:
            print("Error: One or both stations do not exist.")
            return None

        start = self.stations[start_id]
        target = self.stations[target_id]

        # Priority queue for A* and a dictionary to store the shortest time for each station
        pq = [(0, 0, start, [start])]  # (total_time, heuristic, current_station, path)
        shortest_time = {start: 0}

        while pq:
            current_time, current_heuristic, current_station, path = heapq.heappop(pq)

            # If we reach the target, return the path and the total time
            if current_station == target:
                return (path, current_time)

            # Check the neighbors
            for neighbor, time in current_station.neighbors:
                new_time = current_time + time
                heuristic = neighbor.distance_to(target)

                # If a shorter time is found, add it to the queue
                if neighbor not in shortest_time or new_time < shortest_time[neighbor]:
                    shortest_time[neighbor] = new_time
                    total_time = new_time + heuristic  # Total time with heuristic
                    heapq.heappush(pq, (new_time, heuristic, neighbor, path + [neighbor]))

        return None  # Return None if no route is found

# Tests
if __name__ == "__main__":
    metro = MetroNetwork()

    # Add stations (with hypothetical coordinates for heuristic purposes)
    for idx, name, line, x, y in [
        ("A1", "Kızılay", "Red Line", 1, 1),
        ("A2", "Ulus", "Red Line", 1, 2),
        ("A3", "Sıhhiye", "Blue Line", 2, 3),
        ("A4", "Aşti", "Blue Line", 3, 4),
        ("A5", "Batıkent", "Green Line", 4, 5),
        ("A6", "Demetevler", "Green Line", 5, 5),
        ("A7", "Keçiören", "Orange Line", 6, 6),
        ("A8", "Gar", "Blue Line", 7, 7),
        ("A9", "Airport", "Orange Line", 8, 8),
        ("A10", "Beşevler", "Red Line", 9, 9)
    ]:
        metro.add_station(idx, name, line, x, y)

    # Add connections
    for station1, station2, time in [
        ("A1", "A2", 5), ("A1", "A3", 3), ("A3", "A4", 7),
        ("A5", "A6", 4), ("A7", "A8", 6), ("A8", "A9", 8),
        ("A1", "A10", 2), ("A2", "A6", 9), ("A4", "A9", 10)
    ]:
        metro.add_connection(station1, station2, time)

    # Test scenarios
    tests = [
        ("A1", "A7"),("A1", "A10"),("A2", "A6"),
        ("A3", "A9"),("A5", "A7"),("A8", "A10"),
        ("A1", "A1"),("A1", "A4"),("A3", "A2"),
        ("A5", "A8"),("A6", "A9"),("A10", "A1"),
    ]

    for start, target in tests:
        # Least transfer route
        transfer_route = metro.find_least_transfers(start, target)
        
        # Fastest route
        fastest_route = metro.find_fastest_route(start, target)
        
        # Calculate total time for the least transfer route (transfer_route)
        if transfer_route:
            total_time_transfer = 0
            for i in range(len(transfer_route) - 1):
                for neighbor, time in transfer_route[i].neighbors:
                    if neighbor == transfer_route[i + 1]:
                        total_time_transfer += time
                        break
        else:
            total_time_transfer = 0

        # If both routes are the same, print only one
        if transfer_route == fastest_route[0]:
            print(f"Least transfer route ({start} -> {target}):")
            print(" -> ".join(station.name for station in transfer_route))
            print(f"Total time: {total_time_transfer} minutes")
            print(f"Number of transfers: {len(transfer_route) - 1}")
            print(f"Total stations visited: {len(transfer_route)}")
            print("The fastest route and least transfer route are the same.\n")
        else:
            # If the routes are different, print both
            print(f"Least transfer route ({start} -> {target}):")
            if transfer_route:
                print(" -> ".join(station.name for station in transfer_route))
                print(f"Total time: {total_time_transfer} minutes")
                print(f"Number of transfers: {len(transfer_route) - 1}")
                print(f"Total stations visited: {len(transfer_route)}")
            else:
                print("Route not found.")
            
            print(f"\nFastest route ({start} -> {target}):")
            if fastest_route:
                print(" -> ".join(station.name for station in fastest_route[0]))
                print(f"Total time: {fastest_route[1]} minutes")
                print(f"Number of transfers: {len(fastest_route[0]) - 1}")
                print(f"Total stations visited: {len(fastest_route[0])}")
            else:
                print("Route not found.")
