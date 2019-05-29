import collections
import copy
import math

import prettytable
import argparse


def check_colour(graph, permutation):
    for vertex in graph.keys():
        for neighbour in graph[vertex]:
            if permutation[neighbour] == permutation[vertex]:
                return False
    return True


def minimize_colour(permutation):
    min_colour = {}
    cnt = 1
    result_permutation = []
    for e in permutation:
        if e not in min_colour:
            min_colour[e] = cnt
            cnt += 1
        result_permutation.append(min_colour[e])
    return result_permutation


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


def chromatic_number(graph, graph_girth):
    if graph_girth == math.inf:
        return 2
    n = len(graph)
    if graph_girth % 2 == 0:
        start = 2
    else:
        start = 3
    for cn in range(start, 99):
        permutation = [1 for _ in range(n)]
        i = len(permutation) - 1
        while i >= 0:
            while permutation[i] <= cn:
                if minimize_colour(permutation) >= permutation:
                    if check_colour(graph, permutation):
                        return cn
                permutation[i] += 1
            while permutation[i] >= cn:
                permutation[i] = 1
                i -= 1
            if i >= 0:
                permutation[i] += 1
                i = len(permutation) - 1


def analyse_graph():
    main_table = prettytable.PrettyTable()
    main_table.field_names = ["Graph6", "Number of vertexes", "Number of edges", "Girth",
                              "Chromatic number"]
    result_girth = {}
    result_chromatic_number = {}
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default=None, help="Read graphs from file")
    args = parser.parse_args()
    if args.file is None:
        try:
            str_graph = input()
            while str_graph != "":
                graph = parse_graph6(str_graph)
                result_girth[str_graph] = girth(graph)
                result_chromatic_number[str_graph] = chromatic_number(graph, result_girth[str_graph])
                number_of_vertexes = len(graph)
                number_of_edges = 0
                for vertex in graph.keys():
                    number_of_edges += len(graph[vertex])
                result_to_table = [str_graph, number_of_vertexes, number_of_edges//2, result_girth[str_graph],
                                   result_chromatic_number[str_graph]]
                main_table.add_row(result_to_table)
                str_graph = input()
        except EOFError:
            count_girths = {}
            count_chromatic_number = {}

            for key, value in result_girth.items():
                count_girths[value] = count_girths.setdefault(value, 0) + 1
            count_girths = dict(sorted(count_girths.items(), key=lambda girth: girth[0]))

            for key, value in result_chromatic_number.items():
                count_chromatic_number[value] = count_chromatic_number.setdefault(value, 0) + 1
            count_chromatic_number = dict(
                sorted(count_chromatic_number.items(), key=lambda chromatic_number: chromatic_number[0]))

            girth_stat_table = prettytable.PrettyTable()
            girth_stat_table.field_names = ["Girth", "Number of graph with this girth"]
            for key, value in count_girths.items():
                girth_stat_table.add_row([key, value])

            chromatic_stat_table = prettytable.PrettyTable()
            chromatic_stat_table.field_names = ["Chromatic number", "Number of graph with this chromatic number"]
            for key, value in count_chromatic_number.items():
                chromatic_stat_table.add_row([key, value])

            with open("main_info.txt", "w") as out_main:
                out_main.write(main_table.get_string())

            with open("girth_stat.txt", "w") as out_girth_stat:
                out_girth_stat.write(girth_stat_table.get_string())

            with open("chromatic_number_stat.txt", "w") as out_chromatic_number_stat:
                out_chromatic_number_stat.write(chromatic_stat_table.get_string())
        finally:
            print("Analyse of graphs was finished!\n")
    else:
        with open(args.file, "r") as graph_file:
            for str_graph in graph_file:
                str_graph = str_graph.rstrip()
                graph = parse_graph6(str_graph)
                result_girth[str_graph] = girth(graph)
                result_chromatic_number[str_graph] = chromatic_number(graph, result_girth[str_graph])
                number_of_vertexes = len(graph)
                number_of_edges = 0
                for vertex in graph.keys():
                    number_of_edges += len(graph[vertex])
                result_to_table = [str_graph, number_of_vertexes, number_of_edges//2, result_girth[str_graph],
                                   result_chromatic_number[str_graph]]
                main_table.add_row(result_to_table)

            count_girths = {}
            count_chromatic_number = {}

            for key, value in result_girth.items():
                count_girths[value] = count_girths.setdefault(value, 0) + 1
            count_girths = dict(sorted(count_girths.items(), key=lambda girth: girth[0]))

            for key, value in result_chromatic_number.items():
                count_chromatic_number[value] = count_chromatic_number.setdefault(value, 0) + 1
            count_chromatic_number = dict(sorted(count_chromatic_number.items(), key=lambda chromatic_number: chromatic_number[0]))

            girth_stat_table = prettytable.PrettyTable()
            girth_stat_table.field_names = ["Girth", "Number of graph with this girth"]
            for key, value in count_girths.items():
                girth_stat_table.add_row([key, value])

            chromatic_stat_table = prettytable.PrettyTable()
            chromatic_stat_table.field_names = ["Chromatic number", "Number of graph with this chromatic number"]
            for key, value in count_chromatic_number.items():
                chromatic_stat_table.add_row([key, value])

            with open("main_info.txt", "w") as out_main:
                out_main.write(main_table.get_string())

            with open("girth_stat.txt", "w") as out_girth_stat:
                out_girth_stat.write(girth_stat_table.get_string())

            with open("chromatic_number_stat.txt", "w") as out_chromatic_number_stat:
                out_chromatic_number_stat.write(chromatic_stat_table.get_string())


if __name__ == '__main__':
    analyse_graph()
