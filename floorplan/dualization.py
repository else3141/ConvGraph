"""Experimental: turn an arbitrary planar graph into a triangulated one.

This is the unfinished on-ramp to the pipeline. The idea is to triangulate a
sparse adjacency graph so it becomes a maximal planar graph, from which a
rectangular dual (the input the layout stage actually expects) can be derived.
The triangulation itself works; deriving the dual from it is not done yet, so
nothing in the layout stage depends on this module.
"""
import networkx as nx
import numpy as np
import triangle as tr


def _triangle_input(g):
    """Pack a graph into the {vertices, segments} dict the Triangle library wants."""
    pos = nx.planar_layout(g)
    nodes = list(g.nodes())
    idx = {v: i for i, v in enumerate(nodes)}
    vertices = np.array([pos[v] for v in nodes])
    segments = np.array([(idx[u], idx[v]) for u, v in g.edges()])
    return {"vertices": vertices, "segments": segments}, pos


def triangulate(g):
    """Return a triangulated copy of g plus the layout used, via Shewchuk's Triangle."""
    data, pos = _triangle_input(g)
    result = tr.triangulate(data, "pq0")
    nodes = list(g.nodes())
    out = nx.Graph()
    out.add_edges_from(g.edges())
    for a, b, c in result["triangles"]:
        out.add_edge(nodes[a], nodes[b])
        out.add_edge(nodes[b], nodes[c])
        out.add_edge(nodes[c], nodes[a])
    return out, pos
