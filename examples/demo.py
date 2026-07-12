"""Reproduce the floorplan for the example adjacency graph end to end."""
import networkx as nx
import numpy as np

from floorplan import (
    rotation_system, outer_boundary, label_faces,
    split_hull, build_layout, flood_fill,
)

# Example room-adjacency graph: nodes are rooms, edges mean "should be adjacent".
POS = {1: (0, 0), 2: (1, 1), 3: (1, 2), 4: (2, 2), 5: (3, 3), 6: (2, 1),
       7: (3, 1), 8: (4, 2), 9: (5, 3), 10: (0, 4), 11: (4, 4), 12: (3, 0), 13: (2, 3)}
EDGES = [(1, 2), (1, 12), (1, 10), (2, 3), (2, 6), (6, 4), (6, 7), (3, 10),
         (3, 4), (4, 5), (4, 6), (5, 8), (5, 11), (8, 9), (9, 11), (7, 8),
         (9, 12), (7, 12), (10, 13), (13, 11), (1, 6)]


def build(edges=EDGES, pos=POS, size=7):
    """Run the full pipeline and return the filled room grid."""
    g = nx.Graph()
    g.add_edges_from(edges)

    rs = rotation_system(g, pos)
    boundary = outer_boundary(g, pos, rs)
    labels = label_faces(g, rs, boundary)
    split = split_hull(boundary, rs)
    split.append(boundary[0])

    grid = np.zeros((size, size))
    build_layout(split, boundary, labels, grid, 0, 1, 0, size, g, pos)
    return flood_fill(grid).astype(int)


if __name__ == "__main__":
    grid = build()
    print("Room grid (each integer is a room):\n")
    print(grid)
