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
    return connections[:num_connections]

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

def main():
    parser = argparse.ArgumentParser(description="Parse file lines with a character and a number.")
    parser.add_argument("filename", help="Input file to parse")
    parser.add_argument("connections", help="number of connections to generate before the product is generated", type=int)
    args = parser.parse_args()
    points = parse_inputfile(args.filename)
    connections = get_shortest_connections(points, args.connections)
    groups = group_connected(points, connections)

    print(f"Total groups: {len(groups)}")
    for group_id, indices in groups.items():
        print(f"Group {group_id}: {len(indices)} circuits")
        for idx in indices:
            print(f"  {points[idx]}")
        print()

    # sort the grops by size
    sorted_groups = sorted(groups.values(), key=len, reverse=True)
    largest_group = sorted_groups[0]

    product = len(sorted_groups[0])
    product *= len(sorted_groups[1])
    product *= len(sorted_groups[2])
    print(f"Product of top 3: {product}")

if __name__ == "__main__":
    main()