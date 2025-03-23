
# Metro Route Optimization Project

This project simulates a metro network and provides functionality to find optimal routes between stations based on different criteria. It implements two pathfinding algorithms: Breadth-First Search (BFS) for finding the route with the fewest transfers, and the A* search algorithm for finding the fastest route.

## Technologies and Libraries Used

* **Python:** The project is implemented in Python.
* **collections.deque:** Used for implementing the queue in the BFS algorithm. [cite: 29]
* **heapq:** Used for implementing the priority queue in the A* algorithm. [cite: 30]

## Algorithm Details

### BFS Algorithm

The Breadth-First Search (BFS) algorithm is used to find the route with the least number of transfers between two metro stations. [cite: 29, 30, 31]

1. The algorithm starts at the source station and explores its neighbors.
   
2. It then explores the neighbors of those neighbors, and so on, layer by layer.
   
3. A queue data structure is used to keep track of the stations to be visited. [cite: 29]
   
4. The algorithm keeps track of visited stations to avoid loops. [cite: 29]
   
5. By exploring the graph in this manner, the first path found to the destination station is guaranteed to be one of the paths with the fewest transfers. [cite: 29]

### A* Algorithm

The A* algorithm is used to find the fastest route between two metro stations. [cite: 30, 31]

1. A* is an informed search algorithm that uses a heuristic to guide its search. [cite: 30, 31]
   
2. It maintains a priority queue of paths, ordered by their cost. [cite: 30]
   
3. The cost of a path is the sum of the actual cost from the start station to the current station and an estimated cost (heuristic) from the current station to the goal station. [cite: 30, 31]
   
4. The algorithm repeatedly selects the path with the lowest cost from the priority queue and explores its neighbors. [cite: 30]
   
5. It keeps track of the shortest time taken to reach each station. [cite: 30]
   
6. By using the heuristic, A* efficiently finds the shortest path. [cite: 30, 31]

### Why These Algorithms Were Chosen

* BFS is well-suited for finding the shortest path in terms of the number of "hops" or transfers, as it explores all paths equally in each layer. [cite: 29, 30, 31]
   
* A* is an efficient algorithm for finding the shortest path in terms of cost (in this case, time), as it uses a heuristic to guide its search and prioritize paths that are likely to lead to the goal. [cite: 30, 31]

## Usage Example and Test Results

To use the simulation:

1. Add stations to the metro network using the `add_station` method.
   
2. Connect stations using the `add_connection` method, specifying the travel time between them.
   
3. Use the `find_least_transfers` method to find the route with the fewest transfers.
   
4. Use the `find_fastest_route` method to find the fastest route.

### Example Test Results:

**Least transfer route (A1 -> A7):**
```
A1 -> A3 -> A8 -> A7
Total time: 16 minutes
Number of transfers: 3
Total stations visited: 4
```

**Fastest route (A1 -> A7):**
```
A1 -> A3 -> A8 -> A7
Total time: 16 minutes
Number of transfers: 3
Total stations visited: 4
```

**Least transfer route (A1 -> A10):**
```
A1 -> A10
Total time: 2 minutes
Number of transfers: 1
Total stations visited: 2
```

**Fastest route (A1 -> A10):**
```
A1 -> A10
Total time: 2 minutes
Number of transfers: 1
Total stations visited: 2
```

... (Add other test results here)

## Future Development Ideas

* Implement a graphical user interface (GUI) for visualizing the metro network and the routes. [cite: 26]
* Add real-time data integration to simulate dynamic changes in the metro network (e.g., delays, closures). [cite: 26]
* Incorporate more sophisticated heuristics for the A* algorithm to improve its performance. [cite: 26]
* Extend the simulation to consider other factors such as ticket prices or platform waiting times. [cite: 26]
