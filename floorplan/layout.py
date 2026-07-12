from collections import defaultdict

import networkx as nx

from .embedding import rotation_system, outer_boundary
from .segment_tree import SegmentTree


def split_hull(boundary, rs):
    """Boundary walk with each node's interior neighbours inserted after it (as strings)."""
    ring = boundary[:-1]
    out = []
    for i in range(len(ring)):
        out.append(ring[i])
        nbrs = rs[ring[i]][::-1]
        k = nbrs.index(ring[(i - 1) % len(ring)])
        nbrs = nbrs[k + 1:] + nbrs[:k]
        for v in nbrs[:-1]:
            out.append(str(v))
    return out


def _row_heights(grid, ring, inset, n):
    """Stack rooms on row `ring` to their needed heights; returns grid and the next ring index."""
    spans = defaultdict(list)
    st = SegmentTree([1] * n, max, 0)
    heights = [1] * n
    for i in range(inset + 1, n - inset * 2 - 1):
        room = grid[ring][i]
        if len(spans[room]) == 0:
            spans[room].append([i, i])
        elif spans[room][-1][1] == i - 1:
            spans[room][-1][1] = i
            heights[i] = heights[i - 1]
            st.update(i, heights[i])
        else:
            new_h = max(st.query(spans[room][-1][1] + 1, i + 1) + 1,
                        heights[spans[room][-1][1]])
            spans[room].append([i, i])
            for lo, hi in spans[room]:
                for c in range(lo, hi + 1):
                    heights[c] = new_h
                    st.update(c, new_h)
    for j in range(inset + 1, n - inset * 2 - 1):
        for i in range(1, heights[j]):
            grid[i][j] = grid[i - 1][j]
    for i in range(max(heights) - 1, 0, -1):
        last = grid[i][inset]
        for j in range(inset + 1, n - inset * 2 - 1):
            if grid[i][j] != 0:
                last = grid[i][j]
            else:
                grid[i][j] = last
    return grid, ring + max(heights), inset, n


def _peel_size(boundary, ring, inset, n):
    """The grid size the next ring works over, once this ring's border is filled in."""
    if inset < n - inset:
        return n - inset - 1
    if ring + 1 < n - ring:
        return n - ring - 1
    return boundary[-2]


def build_layout(split, boundary, labels, grid, ring, col, inset, n, g, pos):
    """Paint one ring of the floorplan, drop its edges, and recurse on what remains."""
    if ring != 0:
        split = split + [split[0]]
        col = inset

    prev = split[0]
    k = boundary[-2]
    if ring == 0:
        grid[ring][inset] = labels[(k, int(split[-2]))]

    if ring == 0:
        rooms = sum(1 for x in split if not isinstance(x, int))
    else:
        rooms = sum(1 for x in split if isinstance(x, int))
    width = max((n - 2 * inset) // rooms, 1)

    dropped = []
    for x in split:
        if isinstance(x, int):
            dropped.append((prev, x) if ring == 0 else (x, prev))
            prev = x
        else:
            room = labels[(prev, int(x))]
            dropped.append((prev, int(x)))
            for c in range(width):
                grid[ring][col + c] = room
            col += width

    for j in range(n):
        if grid[ring][j] == 0:
            fill = grid[ring][j - 1]
            for c in range(j, n - inset):
                grid[ring][c] = fill
            break

    border = grid[ring][inset]
    for r in range(ring + 1, n - ring):
        grid[r][inset] = border
        grid[r][n - inset - 1] = border
    for c in range(inset, n - inset):
        grid[n - inset - 1][c] = border

    for e in dropped[1:]:
        if (e[0], e[1]) in g.edges():
            g.remove_edge(e[0], e[1])
    remaining = list(g.edges())
    g = nx.Graph()
    g.add_edges_from(remaining)
    pos = {v: pos[v] for v in pos if v in g.nodes()}

    grid, ring, inset, n = _row_heights(grid, ring, inset,
                                        _peel_size(boundary, ring, inset, n))
    inset += 1
    if len(g.edges()) == 0:
        return grid
    rs = rotation_system(g, pos)
    boundary = outer_boundary(g, pos, rs)
    split = split_hull(boundary, rs)
    return build_layout(split, boundary, labels, grid, ring, col, inset, n, g, pos)


def flood_fill(grid):
    """Fill leftover empty cells from a filled neighbour, sweeping up, down, left, right."""
    h, w = len(grid), len(grid[0])
    for i in range(h):
        for j in range(w):
            if grid[i][j] == 0 and grid[i - 1][j] != -1:
                grid[i][j] = grid[i - 1][j]
    for i in range(h - 1, 0, -1):
        for j in range(w):
            if grid[i][j] == 0 and i + 1 < h and grid[i + 1][j] != -1:
                grid[i][j] = grid[i + 1][j]
    for i in range(h):
        for j in range(w):
            if grid[i][j] == 0 and grid[i][j - 1] != -1:
                grid[i][j] = grid[i][j - 1]
    for i in range(h - 1, 0, -1):
        for j in range(w):
            if grid[i][j] == 0 and j + 1 < w and grid[i][j + 1] != -1:
                grid[i][j] = grid[i][j + 1]
    for i in range(h):
        for j in range(w - 1, -1, -1):
            if grid[i][j] == 0 and j + 1 < w:
                grid[i][j] = grid[i][j + 1]
    return grid
