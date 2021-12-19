"""
This module allows to colourize a graph in three colors (red, blue and green).
"""

from __future__ import unicode_literals
import doctest

# 2-sat find solution implementation


def dfs_type_1(graph):
    """
    First DFS used for typological sort.
    """

    order = []
    visited = set()

    for start in range(len(graph)):
        if start not in visited:
            stack = [(False, start)]
            visited.add(start)

            while stack:
                logical, vertex = stack.pop()
                if logical:
                    order.append(vertex)
                    continue

                stack.append((True, vertex))

                for child in graph[vertex]:
                    if child not in visited:
                        visited.add(child)
                        stack.append((False, child))

    return order


def dfs_type_2(start, color, components, graph):
    """
    Second DFS used for finding components in the graph.
    """

    stack = [start]
    components[start] = color

    while stack:
        vertex = stack.pop()

        for child in graph[vertex]:
            if components[child] == -1:
                components[child] = color
                stack.append(child)


def find_2_sat(graph):
    num_vertices = len(graph)
    components = [-1 for _ in range(num_vertices)]

    order = dfs_type_1(graph)

    color = 0
    for vertex in range(num_vertices):
        idx = order[num_vertices - vertex - 1]
        if components[idx] == -1:
            dfs_type_2(idx, color, components, graph)
            color += 1

    for vertex in range(0, num_vertices, 2):
        if components[vertex] == components[vertex + 1]:
            return None

    assigned_values = []
    for vertex in range(0, num_vertices, 2):
        assigned_values.append(components[vertex] > components[vertex + 1])

    return assigned_values

# Main function that was used for testing 2-SAT algorithm.

# def main():
#     num_vertices, num_edges = map(int, input().split())

#     graph = [[] for _ in range(num_vertices)]
#     for _ in range(num_edges):
#         a, b = map(int, input().split())
#         graph[b].append(a)

#     solution = find_2_sat(graph)
#     print(solution)


# Creating an graph of implications.

def vertex_idx(vertex, color, opp, num_colors):
    """
    Calculates a position of given vertex with specific color.

    >>> vertex_idx(1, 1, 1, 3)
    9
    """

    position = vertex * num_colors * 2
    position += color * 2 + opp

    return position


def build_implications_graph(initial_graph, initial_colors, num_colors):
    init_graph_sz = len(initial_graph)
    num_vertecies = init_graph_sz * num_colors * 2

    implications_graph = [[] for _ in range(num_vertecies)]

    # Type 1 clauses

    for edge in initial_graph:
        u_ver, v_ver = edge

        for color in range(num_colors):
            if color in (initial_colors[u_ver], initial_colors[v_ver]):
                continue

            implications_graph[vertex_idx(u_ver, color, 0, num_colors)].append(
                vertex_idx(v_ver, color, 1, num_colors))
            implications_graph[vertex_idx(v_ver, color, 0, num_colors)].append(
                vertex_idx(u_ver, color, 1, num_colors))

    # Type 2 & 3 clauses

    for vertex in range(init_graph_sz):
        for color1 in range(num_colors):
            for color2 in range(color1 + 1, num_colors):
                if initial_colors[vertex] in (color1, color2):
                    continue

                # Type 2 clauses

                implications_graph[vertex_idx(vertex, color1, 1, num_colors)].append(
                    vertex_idx(vertex, color2, 0, num_colors))
                implications_graph[vertex_idx(vertex, color2, 1, num_colors)].append(
                    vertex_idx(vertex, color1, 0, num_colors))

                # Type 3 clauses

                implications_graph[vertex_idx(vertex, color1, 0, num_colors)].append(
                    vertex_idx(vertex, color2, 1, num_colors))
                implications_graph[vertex_idx(vertex, color2, 0, num_colors)].append(
                    vertex_idx(vertex, color1, 1, num_colors))

    # Reversing implications graph because 2-SAT solver needs it

    reversed_graph = [[] for _ in range(num_vertecies)]
    for u_ver in range(num_vertecies):
        for v_ver in implications_graph[u_ver]:
            reversed_graph[v_ver].append(u_ver)

    return reversed_graph

# Main function that was used for testing Constructing implications graph algorithm.

# def main():
#     num_vertices, num_edges = map(int, input().split())

#     graph = []
#     for _ in range(num_edges):
#         a, b = map(int, input().split())
#         graph.append((a, b))

#     colors = [int(val) for val in input().split()]

#     solution = build_implications_graph(graph, colors, 3)
    
#     print(find_2_sat(solution))


if __name__ == "__main__":
    main()

# doctest.testmod()
