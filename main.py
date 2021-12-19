"""
This module allows to colourize a graph in three colors (red, blue and green).
"""

import numpy as np

# 2-sat find solution implementation


def dfs_type_1(graph):
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


def main():
    num_vertices, num_edges = map(int, input().split())

    graph = [[] for _ in range(num_vertices)]
    for _ in range(num_edges):
        a, b = map(int, input().split())
        graph[b].append(a)

    solution = find_2_sat(graph)
    print(solution)


if __name__ == "__main__":
    main()
