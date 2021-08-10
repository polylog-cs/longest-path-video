from manim import *
import numpy as np
import math
from scipy.optimize import linprog

import solarized
import tree_data


def parse_bacteria_tree():
    L = 100.0
    rot = (90.0) / (2 * math.pi)
    cycle_center = [279.847 / L, 427.013 / L, 0]
    cycle_radius = 273.232 / L
    positions = {}
    leaves = tree_data.bacteria_leaves
    pos_to_vertex = {}
    edges = []
    data = [
        (
            float(d.split(" ")[0]) / L - cycle_center[0],
            float(d.split(" ")[1]) / L - cycle_center[1],
            0.0,
        )
        for d in tree_data.bacteria_data.splitlines()
    ]

    for i in range(
        int(len(data) / 2) - 2
    ):  # last 2 lines are to distinguish a and b (bad hack)
        pos_u = data[2 * i]
        pos_v = data[2 * i + 1]
        if pos_u == pos_v:
            continue
        for pos in (pos_u, pos_v):
            if not pos in pos_to_vertex:
                node_id = len(pos_to_vertex)
                positions[node_id] = pos
                pos_to_vertex[pos] = node_id
                # if math.dist((0,0,0), pos) > 0.95 * cycle_radius:
                #    leaves.append(node_id)
        edges.append((pos_to_vertex[pos_u], pos_to_vertex[pos_v]))

    pos_a = data[-4]
    pos_b = data[-2]
    a = pos_to_vertex[pos_a]
    b = pos_to_vertex[pos_b]

    for pos in positions:
        positions[pos] = (
            math.cos(rot) * positions[pos][0] + math.sin(rot) * positions[pos][1],
            math.cos(rot) * positions[pos][1] - math.sin(rot) * positions[pos][0],
            0.0,
        )
        # positions[pos] = (positions[pos][0], positions[pos][1], 0)

    for k, v in positions.items():
        positions[k] = np.asarray(v)

    return range(len(positions)), edges, positions, a, b, leaves


def parse_tree_tree():
    L = 80.0
    positions = {}
    pos_to_vertex = {}
    edges = []
    data = [
        (float(d.split(" ")[0]) / L, float(d.split(" ")[1]) / L, 0)
        for d in tree_data.tree_data.splitlines()
    ]

    for i in range(int(len(data) / 2)):
        pos_u = data[2 * i]
        pos_v = data[2 * i + 1]
        if pos_u == pos_v:
            continue
        for pos in (pos_u, pos_v):
            if not pos in pos_to_vertex:
                node_id = len(pos_to_vertex)
                positions[node_id] = pos
                pos_to_vertex[pos] = node_id

        edges.append((pos_to_vertex[pos_u], pos_to_vertex[pos_v]))

    for k, v in positions.items():
        positions[k] = np.asarray(v)

    return range(len(positions)), edges, positions


def get_adjacency_list(g):
    adj = dict([(v, []) for v in g.vertices])
    for v1, v2 in g.edges:
        adj[v1].append(v2)
        adj[v2].append(v1)

    return adj


def bfs(g: Graph, start):
    adj = get_adjacency_list(g)

    res_vertices = [[start]]
    res_edges = [[]]
    res_parents = {start: None}
    seen = set([start])

    while True:
        cur_vertices = []
        cur_edges = []

        for v1 in res_vertices[-1]:
            for v2 in adj[v1]:
                if v2 not in seen:
                    cur_vertices.append(v2)
                    seen.add(v2)
                    cur_edges.append((v1, v2))
                    res_parents[v2] = v1

        if cur_vertices:
            res_vertices.append(cur_vertices)
            res_edges.append(cur_edges)
        else:
            break

    return res_vertices, res_edges, res_parents


def get_path(g: Graph, start, end):
    _, _, parents = bfs(g, end)
    path = [start]

    while path[-1] != end:
        path.append(parents[path[-1]])

    return path


def hanging_position(g: Graph, start, end, shift=(0.0, 0.0, 0.0), Delta=0.3, scale=0.5):
    positions = {}
    top = get_path(g, start, end)

    adj = get_adjacency_list(g)
    weights = {}
    level_order = {}
    pi = {}
    parent = {}
    i = 0
    for u in g.vertices:
        pi[u] = i
        i = i + 1

    def weight(v, parents, depth):
        w = 1
        for v2 in adj[v]:
            if v2 not in parents:
                w += weight(v2, [v], depth + 1)
        weights[v] = w
        if depth > 0:
            parent[v] = parents[0]
            positions[v] = np.array([0.0, -depth, 0])
            if not depth in level_order:
                level_order[depth] = []
            level_order[depth].append(v)
        return w

    for i, v1 in enumerate(top):
        positions[v1] = np.array([i * 1.0 - len(top) / 2.0 + 0.5, 0.0, 0.0])
        weight(v1, top, 0)

    # LP
    # variably:    n* x_i ... pozice na x-ove ose
    #              n* c_i ... rozdil na x-ove ose me a meho otce
    #              vektor promennych je konkatenace x_i a c_i
    # constrainty: pro rooty je x_i = jejich pozice
    #              jinak kdyz x_i a x_j vedle sebe tak x_j > x_i + Delta
    #              a nakonec c_i >= |x_i - x_p(i)|
    # MIN sum w_i * c_i kde w_i je velikost podstromu

    n = len(g.vertices)
    num_var = 2 * n

    A = []
    b = []
    c = np.zeros(num_var)

    for u in g.vertices:
        if u in top:  # je-li to root tak x_i = současná pozice i
            l = np.zeros(num_var)
            l[pi[u]] = 1
            A.append(l)
            A.append(-l)
            b.append(positions[u][0])
            b.append(-positions[u][0])
        else:  # jinak c_i >= |x_i - x_p(i)|
            c[n + pi[u]] = weights[u]
            l = np.zeros(num_var)
            l[pi[u]] = 1
            l[pi[parent[u]]] = -1
            l[n + pi[u]] = -1
            A.append(l)
            l = -l
            l[n + pi[u]] = -1
            A.append(l)
            b.append(0)
            b.append(0)

    for i in level_order:
        lev = level_order[i]
        for i in range(1, len(lev)):  # pro ty vedle plati x_j > x_i + Delta
            l = np.zeros(num_var)
            l[pi[lev[i]]] = -1
            l[pi[lev[i - 1]]] = 1

            A.append(l)
            b.append(-Delta)

    constraints = []
    for i in range(num_var):
        constraints.append((None, None))

    res = linprog(c, A_ub=A, b_ub=b, bounds=constraints)

    for u in g.vertices:
        positions[u][0] = 1.0 * res.x[pi[u]]

    for k in positions:
        positions[k] *= scale
        positions[k] += shift

    return positions


class Intro(Scene):
    def construct(self):
        erdos = ImageMobject("img/erdos.jpg")
        straight = Text("Straight from the Book!")
        erdos.shift(5 * RIGHT)
        self.add(erdos)
        self.add(straight)
        self.wait(1)
        self.remove(erdos, straight)


# https://illustoon.com/?dl=383
class DefiniceStromu(Scene):
    def construct(self):
        tree = ImageMobject("img/tree.png")
        self.add(tree)
        self.wait(1)

        vertices, edges, positions = parse_tree_tree()

        self.g = Graph(
            vertices,
            edges,
            layout="kamada_kawai",
            labels=False,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
        )

        self.play(Create(self.g))

        self.wait(1)

        vec = tree.get_center() - tree.get_start()
        delta = positions[0] - tree.get_center() - np.array([0.0, 0.8 * vec[1], 0.0])
        # (-2.5, -6.0, 0.0)
        for k, v in positions.items():
            v -= delta

        self.play(self.g.animate.change_layout(positions))

        self.wait(1)

        self.g.add_edges((6, 22))

        self.wait(1)

        self.g.remove_edges((1, 8))

        self.wait(10)


class KutaleciStrom(Scene):
    def construct(self):
        self.g = Graph(tree_data.example_vertices, tree_data.example_edges)
        sh = (-2, 3, 0)
        hanging1 = hanging_position(self.g, 4, 4, shift=sh)
        self.g = Graph(
            tree_data.example_vertices,
            tree_data.example_edges,
            layout="kamada_kawai",
            layout_scale=2,
            labels=False,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
        )

        self.play(Create(self.g))
        self.wait(1)

        delta = (-2.0, 0.0, 0.0)
        for k, v in hanging1.items():
            v += delta

        self.play(self.g.animate.change_layout(hanging1))
        self.wait(1)

        hanging2 = hanging_position(self.g, 4, 9, shift=sh)
        delta = hanging1[4] - hanging2[4]
        for k, v in hanging2.items():
            v += delta

        self.play(self.g.animate.change_layout(hanging2))

        self.wait(1)

        hanging3 = hanging_position(self.g, 9, 9)
        delta = hanging2[9] - hanging3[9]
        for k, v in hanging3.items():
            v += delta

        self.play(self.g.animate.change_layout(hanging3))

        self.wait(1)

        hanging4 = hanging_position(self.g, 9, 0)
        delta = hanging3[9] - hanging4[9]
        for k, v in hanging4.items():
            v += delta

        self.play(self.g.animate.change_layout(hanging4))

        self.wait(1)

        self.wait(1)


class LongestPath(Scene):
    def construct(self):

        self.g = Graph(
            tree_data.example_vertices,
            tree_data.example_edges,
            layout="kamada_kawai",
            layout_scale=4.0,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
        )

        self.play(Create(self.g))

        self.wait(1)

        sh = (0, 1, 0)
        hanging1 = hanging_position(self.g, 0, 9, shift=sh)

        self.play(self.g.animate.change_layout(hanging1))

        self.wait(1)

        tleft = hanging1[0]
        tright = hanging1[9]
        tmid = (tleft + tright) / 2.0
        tbot = tmid - [(tmid - tleft)[1], (tmid - tleft)[0], 0]

        ltop = Line(tleft, tright)
        lleft = Line(tleft, tbot)
        lright = Line(tbot, tright)
        self.add(ltop)
        self.add(lleft)
        self.add(lright)

        self.wait(1)

        self.remove(ltop, lleft, lright)

        self.wait(1)

        self.play(
            self.g.animate.change_layout(hanging_position(self.g, 44, 65, shift=sh))
        )

        self.wait(1)


class Bacteria(Scene):
    def construct(self):

        vertices, edges, positions, a, b, leaves = parse_bacteria_tree()
        vconfig = {"color": solarized.BASE00}

        self.g = Graph(
            vertices,
            edges,
            layout=positions,  # "kamada_kawai",
            vertex_config=vconfig,
            edge_config={"color": solarized.BASE00},
        )

        longest = get_path(self.g, a, b)

        for u in longest:
            vconfig[u] = {"fill_color": RED}
        for u in leaves:
            vconfig[u] = {"fill_color": GREEN}

        self.play(Create(self.g))

        self.wait(1)

        self.remove(self.g)

        self.g = Graph(
            vertices,
            edges,
            layout=positions,  # "kamada_kawai",
            layout_scale=4.0,
            # labels = True,
            vertex_config=vconfig,
            edge_config={"color": solarized.BASE00},
        )

        self.play(self.g.animate.change_layout("kamada_kawai"))

        self.wait(1)
