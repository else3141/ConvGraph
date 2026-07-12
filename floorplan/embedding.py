from .geometry import orientation, distance


def rotation_system(g, pos):
    """Neighbours of each node in CCW angular order."""
    rs = {}
    for u in g.nodes():
        rs[u] = sorted(
            g.neighbors(u),
            key=lambda v: (orientation(pos[u], pos[v]), distance(pos[u], pos[v]), v),
        )
    return rs


def outer_boundary(g, pos, rs):
    """Outer face as a closed CCW walk of nodes (starts and ends at the same node)."""
    start = min(g.nodes(), key=lambda u: (pos[u][1], pos[u][0]))
    hull = [start, rs[start][0]]
    while hull[-1] != start:
        u, prev = hull[-1], hull[-2]
        i = rs[u].index(prev)
        hull.append(rs[u][(i + 1) % len(rs[u])])
    return hull


def label_faces(g, rs, boundary):
    """Number the bounded faces; returns {directed edge: room id}."""
    darts = [(u, v) for u, v in g.edges()] + [(v, u) for u, v in g.edges()]
    for i in range(len(boundary) - 1):
        darts.remove((boundary[i], boundary[i + 1]))
    labels = {}
    room = 0
    while darts:
        u, v = darts.pop()
        room += 1
        labels[(u, v)] = room
        start = u
        while v != start:
            i = rs[v].index(u)
            w = rs[v][(i + 1) % len(rs[v])]
            darts.remove((v, w))
            labels[(v, w)] = room
            u, v = v, w
    return labels
