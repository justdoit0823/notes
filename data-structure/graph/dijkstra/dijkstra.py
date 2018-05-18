
"""Dijkstra algorithm."""

from collections import deque


class Edge:
    """Graph's edge."""

    def __init__(self, from_vertex, to_vertex, weight):
        self._weight = weight
        self._from = from_vertex
        self._to = to_vertex

    @property
    def weight(self):
        return self._weight

    @property
    def up(self):
        return self._from

    @property
    def to(self):
        return self._to


class Vertex:
    """Graph's vertex."""

    def __init__(self, identity):
        self._id = identity
        self._neighbors = []

    def __str__(self):
        return '<vertex>.<{0}>'.format(self._id)

    def __add__(self, edge):
        if edge not in self._neighbors:
            self._neighbors.append(edge)

    @property
    def id(self):
        return self._id

    @property
    def neighbors(self):
        return self._neighbors


def shortest_path(from_vertex, to_vertex):
    """Search for the shortest path from vertex a to vertex b."""
    vertex_queue = deque()
    vertex_queue.append((None, from_vertex))

    weight_map = {from_vertex: (0, None)}

    while vertex_queue:
        cur_vertex = vertex_queue.popleft()[1]

        for edge in cur_vertex.neighbors:
            next_vertex = edge.to
            to_weight = edge.weight
            cur_weight = weight_map[cur_vertex][0]
            new_weight = cur_weight + to_weight

            try:
                cur_next_weight = weight_map[next_vertex][0]
            except KeyError:
                weight_map[next_vertex] = (new_weight, cur_vertex)
            else:
                if new_weight < cur_next_weight:
                    weight_map[next_vertex] = (new_weight, cur_vertex)

            if next_vertex != to_vertex:
                vertex_queue.append((cur_vertex, next_vertex))

    path = []
    last_vertex = weight_map[to_vertex][1]
    while last_vertex is not None:
        path.insert(0, last_vertex)
        last_vertex = weight_map[last_vertex][1]

    return path


def main():

    a_vertex = Vertex('A')

    b_vertex = Vertex('B')
    edge_a_b = Edge(a_vertex, b_vertex, 7)
    a_vertex + edge_a_b

    c_vertex = Vertex('C')

    edge_a_c = Edge(a_vertex, c_vertex, 9)
    a_vertex + edge_a_c

    edge_b_c = Edge(b_vertex, c_vertex, 10)
    b_vertex + edge_b_c

    d_vertex = Vertex('D')

    edge_a_d = Edge(a_vertex, d_vertex, 14)
    a_vertex + edge_a_d

    edge_c_d = Edge(c_vertex, d_vertex, 2)
    c_vertex + edge_c_d

    e_vertex = Vertex('E')

    edge_b_e = Edge(b_vertex, e_vertex, 15)
    b_vertex + edge_b_e

    edge_c_e = Edge(c_vertex, e_vertex, 11)
    c_vertex + edge_c_e

    f_vertex = Vertex('F')

    edge_e_f = Edge(e_vertex, f_vertex, 6)
    e_vertex + edge_e_f

    edge_d_f = Edge(d_vertex, f_vertex, 9)
    d_vertex + edge_d_f

    path = shortest_path(a_vertex, f_vertex)
    total_weight = 0
    for idx, vertex in enumerate(path):
        vertex = path[idx]
        if idx == len(path) - 1:
            next_vertex = f_vertex
        else:
            next_vertex = path[idx + 1]

        for edge in vertex.neighbors:
            if edge.to == next_vertex:
                total_weight += edge.weight
                continue

    print('shortest path', ' -> '.join(map(lambda v: v.id, path)), 'total weight', total_weight)


if __name__ == '__main__':
    main()
