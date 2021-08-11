from manim import *
import numpy as np
import math
from scipy.optimize import linprog

import solarized
import tree_data
from util import Tree


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
        g = Tree(
            tree_data.example_vertices,
            tree_data.example_edges,
            layout="kamada_kawai",
            layout_scale=2,
            labels=False,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
        )

        hanging1 = g.hanging_position(4, 4, shift=(-4, 3, 0))

        self.play(Create(g))
        self.wait(1)

        self.play(g.animate.change_layout(hanging1))
        self.wait(1)

        hanging2 = g.hanging_position(4, 9, pinned_vertex=4)
        self.play(g.animate.change_layout(hanging2))
        self.wait(1)

        hanging3 = g.hanging_position(9, 9, pinned_vertex=9)
        self.play(g.animate.change_layout(hanging3))
        self.wait(1)

        hanging4 = g.hanging_position(9, 0, pinned_vertex=9)
        self.play(g.animate.change_layout(hanging4))
        self.wait(1)


class Triangle(Scene):
    def construct(self):

        g = Tree(
            tree_data.example_vertices,
            tree_data.example_edges,
            layout="kamada_kawai",
            layout_scale=4.0,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
        )

        self.play(Create(g))
        self.wait(1)

        sh = (0, 1, 0)
        hanging1 = g.hanging_position(0, 9, shift=sh)
        self.play(g.animate.change_layout(hanging1))

        self.wait(1)

        tleft = hanging1[0]
        tright = hanging1[9]
        tmid = (tleft + tright) / 2.0
        tbot = tmid - [(tmid - tleft)[1], (tmid - tleft)[0], 0]

        ltop = Line(tright, tleft)
        lleft = Line(tleft, tbot)
        lright = Line(tbot, tright)
        self.play(Create(ltop), Create(lleft), Create(lright), time=2)
        self.wait(1)

        self.play(Uncreate(ltop), Uncreate(lleft), Uncreate(lright), time=2)
        self.wait(1)

        self.play(g.animate.change_layout(g.hanging_position(44, 65, shift=sh)))

        self.wait(1)


class Bacteria(Scene):
    def construct(self):
        vertices, edges, positions, a, b, leaves = parse_bacteria_tree()
        vconfig = {"color": solarized.BASE00}

        g = Tree(
            vertices,
            edges,
            layout=positions,  # "kamada_kawai",
            vertex_config=vconfig,
            edge_config={"color": solarized.BASE00},
        )

        longest = g.get_path(a, b)

        self.play(Create(g))
        self.wait(1)

        self.play(g.animate.set_path_color(a, b))
        self.play(g.animate.set_colors(dict((v, solarized.GREEN) for v in leaves)))
        self.wait(1)

        self.play(g.animate.change_layout("kamada_kawai"))

        self.wait(1)


class Filesystem(Scene):
    def construct(self):
        edges = tree_data.parse_linux_tree("vv_filesystem_L2_edited.txt")

        vertices = set()
        for edge in edges:
            vertices.add(edge[0])
            vertices.add(edge[1])

        # labels = dict((v, Text(v, fill_color=solarized.ORANGE)) for v in vertices)
        # labels["/Applications"] = Text("/Applications", fill_color=solarized.ORANGE)

        g = Tree(
            vertices,
            edges,
            layout="kamada_kawai",
            layout_scale=3,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
            # labels=labels,
        )

        # self.play(DrawBorderThenFill(g))
        self.play(Create(g))
        self.wait(1)
