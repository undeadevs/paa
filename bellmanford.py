from typing import List, Tuple, Any
from tabulate import tabulate
import math
import time

class BellmanFord():

    # Constructor to initiliaze bellman-ford
    def __init__(self, nodes: List[str], adj_mat: List[int], src: str):
        self.nodes = nodes
        self.adj_mat = adj_mat
        self.src = src
        self.dist = [[float("inf"), None] for _ in range(len(nodes))]
        src_index = nodes.index(src)
        self.dist[src_index] = [0, src_index]

    # Executes bellman-ford
    def execute(self) -> List[List[Any]]:
        history = []
        # Append initial state (0th iteration) to history
        history.append(self.dist.copy())
        # Iterate V-1 times
        for _ in range(0,len(self.nodes)-1):
            # Iterate through all edges
            for i, weight in enumerate(self.adj_mat):
                u = math.floor(i / len(self.nodes))
                v = i % len(self.nodes)
                if weight==0:
                    continue
                # Relax edges
                if self.dist[u][0]+weight < self.dist[v][0]:
                    self.dist[v] = [self.dist[u][0]+weight, u]
            # Append current iteration to history
            history.append(self.dist.copy())

        # Check negative cycles by iterating through all edges
        for i, weight in enumerate(self.adj_mat):
            u = math.floor(i / len(self.nodes))
            v = i % len(self.nodes)
            if weight==0:
                continue
            if self.dist[u][0]+weight < self.dist[v][0]:
                self.dist[v] = [float("-inf"), u]
        history.append(self.dist.copy())

        return history

    # Builds path from source to destination
    def construct_path(self, dest: str) -> Tuple[List[int], List[int]] | None:
        src_index = self.nodes.index(src)
        dest_index = self.nodes.index(dest)
        nodes_len = len(self.nodes)
        path = []
        path_dist = []
        # Insert path destination by node index
        path.insert(0, dest_index)
        prev_node_index = self.dist[dest_index][1]
        # If there's no previous node on destination then there's no path from source
        if prev_node_index is None:
            return None
        # Insert path distance
        path_dist.insert(0, self.adj_mat[prev_node_index*nodes_len + dest_index])
        while prev_node_index is not src_index:
            temp = prev_node_index
            # Insert path by node index
            path.insert(0, prev_node_index)
            prev_node_index = self.dist[prev_node_index][1]
            # Insert path distance
            path_dist.insert(0, self.adj_mat[prev_node_index*nodes_len + temp])
        # Insert path source by node index
        path.insert(0, src_index)
        # Insert path distance
        path_dist.insert(0, self.adj_mat[prev_node_index*nodes_len + src_index])
        return (path, path_dist)

if __name__ == "__main__":
    # Initialize nodes
    nodes = ["R Main", "RA", "RB", "RC", "R Lab"]
    # Initialize adjacent matrix
    adj_mat = [
        0, 3, 10, 4, 5,
        3, 0, 6, 0, 0,
        10, 6, 0, 12, 0,
        4, 0, 12, 0, 0,
        5, 0, 0, 0, 0,
    ]
    # Initialize source
    src = "RB"
    # Initialize destination
    dest = "R Lab"
    # Initialize BellmanFord class
    newBellmanFord = BellmanFord(nodes, adj_mat, src)
    # History table for table printing
    history_table = []
    # Store starting time
    start = time.time() * 1000
    # Execute dijkstra and get history
    history = newBellmanFord.execute()
    # Store ending time
    end = time.time() * 1000
    # Format history to history_table
    for i, history_item in enumerate(history):
        history_row = [str(i)]
        for history_node in history_item:
            if history_node[1] is not None:
                history_row.append(str(history_node[0])+"_"+nodes[history_node[1]])
            else:
                history_row.append(str(history_node[0]))
        history_table.append(history_row)

    # Print history_table
    print(tabulate(history_table, headers=["i", *nodes], tablefmt="simple_grid"))

    # Print execution time
    print(f"Execution time: {end-start}ms")

    # Construct path to destination
    path = newBellmanFord.construct_path(dest)
    if path is None:
        # Tell the user if there's no path to get to the destination
        print(f"There exists no path from {src} to {dest}")
    else:
        # Print the shortest path
        print(f"Shortest path from {src} to {dest}:")
        print(" + ".join([str(dist) for i, dist in enumerate(path[1]) if i > 0]) + " = " + str(sum(path[1])))
        print(" -> ".join([nodes[node_i] for node_i in path[0]]))

