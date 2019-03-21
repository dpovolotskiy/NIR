import collections
import copy
import math
import prettytable


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
    d, visited, queue = [0 for _ in range(len(new_graph))], set(), collections.deque([root])
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


def analyse_graph():
    result = {}
    try:
        str_graph = input()
        while str_graph != "":
            graph = parse_graph6(str_graph)
            result[str_graph] = girth(graph)
            str_graph = input()
    except EOFError:
        result_str = ""
        count_girths = {}
        for key, value in result.items():
            count_girths[value] = count_girths.setdefault(value, 0) + 1
            result_str += "Girth of graph: {}, equals: {};\n".format(key, value)
        count_girths = dict(sorted(count_girths.items(), key=lambda girth: girth[1]))
        x = prettytable.PrettyTable()
        x.field_names = ["Girth", "Number of graph with this girth"]
        for key, value in count_girths.items():
            x.add_row([key, value])
        with open("girth_of_graphs.txt", "w") as output:
            output.write(result_str)
            output.write(x.get_string())
    finally:
        print("Analyse of graphs was finished!\n")


def main():
    analyse_graph()


if __name__ == '__main__':
    main()
