from math import sqrt
import argparse

# Not done by me.

def parse_inputfile(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                points.append(tuple(map(int, line.split(','))))
    return points

def get_shortest_connections(points, num_connections):
    connections = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = sqrt(sum((points[i][k] - points[j][k]) ** 2 for k in range(3)))
            connections.append((i, j, dist))
    connections.sort(key=lambda x: x[2])
    return connections

def group_connected(points, connections):
    # Union-Find (Disjoint Set) to group connected circuits
    parent = list(range(len(points)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[py] = px

    for i, j, _ in connections:
        union(i, j)

    # Build groups
    groups = {}
    for idx in range(len(points)):
        root = find(idx)
        groups.setdefault(root, []).append(idx)
        
    return groups

def min_connections_to_connect_all(points):
    connections = get_shortest_connections(points, None)  # get all possible connections, sorted
    parent = list(range(len(points)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[py] = px
            return True
        return False

    count = 0
    used_connections = []
    for i, j, dist in connections:
        if union(i, j):
            used_connections.append((i, j, dist))
            count += 1
            # When we've connected all points, we have N-1 connections
            if count == len(points) - 1:
                break
    return count, used_connections

def main():
    parser = argparse.ArgumentParser(description="Parse file lines with a character and a number.")
    parser.add_argument("filename", help="Input file to parse")
    parser.add_argument("connections", help="number of connections to generate before the product is generated", type=int)
    args = parser.parse_args()
    points = parse_inputfile(args.filename)
    count, used_connections = min_connections_to_connect_all(points)
    print(f"Minimum number of connections to connect all circuits: {count}")
    print("Connections used:")
    for i, j, dist in used_connections:
        print(f"  {points[i]} <-> {points[j]} (distance {dist:.2f})")

    last_a, last_b, dist = used_connections[-1]
    product = points[last_a][0] * points[last_b][0]
    print(f"Last connection made: {points[last_a]} <-> {points[last_b]} = {product})") 
if __name__ == "__main__":
    main()