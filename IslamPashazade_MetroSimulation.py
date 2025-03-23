from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Station:
    def __init__(self, idx: str, name: str, line: str):
        self.idx = idx
        self.name = name
        self.line = line
        self.neighbors: List[Tuple['Station', int]] = []  # (station, time) tuples

    def add_neighbor(self, station: 'Station', time: int):
        self.neighbors.append((station, time))

class MetroNetwork:
    def __init__(self):
        self.stations: Dict[str, Station] = {}
        self.lines: Dict[str, List[Station]] = defaultdict(list)

    def add_station(self, idx: str, name: str, line: str) -> None:
        """Add a station to the metro network."""
        if idx not in self.stations:
            station = Station(idx, name, line)
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
        A* Algorithm: Finds the fastest route.
        """
        if start_id not in self.stations or target_id not in self.stations:
            print("Error: One or both stations do not exist.")
            return None

        start = self.stations[start_id]
        target = self.stations[target_id]

        # Priority queue for A* and a dictionary to store the shortest time for each station
        pq = [(0, id(start), start, [start])]
        shortest_time = {start: 0}

        while pq:
            current_time, _, current_station, path = heapq.heappop(pq)

            # If we reach the target, return the path and the total time
            if current_station == target:
                return (path, current_time)

            # Check the neighbors
            for neighbor, time in current_station.neighbors:
                new_time = current_time + time

                # If a shorter time is found, add it to the queue
                if neighbor not in shortest_time or new_time < shortest_time[neighbor]:
                    shortest_time[neighbor] = new_time
                    heapq.heappush(pq, (new_time, id(neighbor), neighbor, path + [neighbor]))

        return None  # Return None if no route is found

# Tests
if __name__ == "__main__":
    metro = MetroNetwork()

    # Add stations
    for idx, name, line in [
        ("A1", "Kızılay", "Red Line"),
        ("A2", "Ulus", "Red Line"),
        ("A3", "Sıhhiye", "Blue Line"),
        ("A4", "Aşti", "Blue Line"),
        ("A5", "Batıkent", "Green Line"),
        ("A6", "Demetevler", "Green Line"),
        ("A7", "Keçiören", "Orange Line"),
        ("A8", "Gar", "Blue Line"),
        ("A9", "Airport", "Orange Line"),
        ("A10", "Beşevler", "Red Line")
    ]:
        metro.add_station(idx, name, line)

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
