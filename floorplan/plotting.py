"""Optional matplotlib helpers for looking at graphs and finished floorplans."""
import matplotlib.pyplot as plt
import networkx as nx


def draw_graph(g, pos, title=None):
    """Draw a graph at the given node positions."""
    nx.draw(g, pos, with_labels=True, node_color="lightblue", edge_color="black")
    if title:
        plt.title(title)


def show_floorplan(grid, title="Floorplan"):
    """Render the room grid as a coloured image, one colour per room."""
    plt.imshow(grid, cmap="tab20")
    plt.title(title)
    plt.axis("off")
