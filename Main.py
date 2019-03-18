import collections
import copy
import math


def parse_graph6(str_graph):
    byte = str_graph.encode('UTF-8')
    n = byte[0] - 63
    graph = {i: [] for i in range(n)}
    code_string = ""
    for i in range(1, len(byte)):
        code_string += format(byte[i] - 63, '06b')
    counter = 0
    for i in range(1, n):
        for j in range(i):
            if code_string[counter] == "1":
                graph[j].append(i)
                graph[i].append(j)
            counter += 1
    return graph


def breadth_first_search(graph, root):
    new_graph = copy.deepcopy(graph)
    d, visited, queue = [0 for i in range(len(new_graph))], set(), collections.deque([root])
    visited.add(root)
    while queue:
        vertex = queue.popleft()
        for neighbour in new_graph[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
                if vertex in new_graph[neighbour]:
                    new_graph[neighbour].remove(vertex)
                d[neighbour] = d[vertex] + 1
            else:
                return d[vertex] + d[neighbour] + 1
    return math.inf


def girth(graph):
    len_of_cycles = []
    for vertex in graph.keys():
        len_of_cycles.append(breadth_first_search(graph, vertex))
    return min(len_of_cycles)


def main():
    str_graph = input()
    graph = parse_graph6(str_graph)
    with open("grith_of_graphs.txt", "w") as output:
        output.write("Обхват графа {}: {};\n".format(str_graph, girth(graph)))


if __name__ == '__main__':
    main()
