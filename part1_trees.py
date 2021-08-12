from manim import *
import numpy as np
import math

import solarized
import tree_data
from util import Tree


class TheBook(Scene):
    def construct(self):
        # TODO: obrázek knížky?
        erdos = ImageMobject("img/erdos.jpg")
        straight = Text("Straight from the Book!", color=solarized.BASE00)
        erdos.shift(5 * LEFT)
        self.play(FadeIn(erdos))
        self.play(Create(straight))
        self.wait(1)

        # TODO: animace s našimi jmény - Vašek ® a Václav (V),
        #   pokud bude separátní channel, tak jméno channelu,
        #   naznačit že mluví vašek v?, taky někde napsáno SoME challenge


class TreeIntro(Scene):
    def construct(self):
        # TODO: vyznačí se osnova TREES, THE ALGORITHM, WHY IT WORKS?, zvýrazní se TREES

        # https://illustoon.com/?dl=383
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
            # Passed to:
            # https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.kamada_kawai_layout.html
            layout_config={"center": (-5, 0)},
        )

        # TODO: vytvorit v puvodnim layoutu napred vedle (bio)stromu, ne pres nej
        self.play(Create(self.g))

        self.wait(1)

        vec = tree.get_center() - tree.get_start()
        delta = positions[0] - tree.get_center() - np.array([0.0, 0.8 * vec[1], 0.0])
        # (-2.5, -6.0, 0.0)
        for k, v in positions.items():
            v -= delta

        self.play(self.g.animate.change_layout(positions))
        self.wait(1)
        # TODO: vyresit ze hrany (abstraktniho) stromu jsou za vetvemi skutecneho
        #   a problikavaji
        # self.bring_to_back(tree)
        self.play(FadeOut(tree))

        # This means that in a tree, you can walk from every node to every other node
        # using the connections between nodes,
        # but there is always just one way of doing that.
        # TODO: animace typu vyznačí se dva vrcholy a pak cesta mezi nimi

        extra_edge = Line(
            self.g[6].get_center(), self.g[22].get_center(), color=solarized.RED
        )

        self.play(Create(extra_edge))
        self.wait(1)

        # TODO: vyznacit vytvoreny cyklus

        self.play(Uncreate(extra_edge))
        self.wait(1)

        # TODO: animace disconnected grafu


class Filesystem(Scene):
    def construct(self):
        # TODO: labely u vrcholu? reprezentativnejsi subset?
        #   mozna by bylo lepsi udelat nejakej umelej priklad jako
        #   ~/, ~/Documents, ~/Documents/school/thesis.tex, ~/Documents/manim/,
        #   ~/Pictures/vacation/...
        #   etc a ukazat to podobne jako to dela prikaz `tree`
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


class Bacteria(Scene):
    def construct(self):
        vertices, edges, positions, a, b, leaves = parse_bacteria_tree()
        vconfig = {"color": solarized.BASE00}

        # labels = dict((v, Text(str(v), fill_color=BLACK, size=0.15)) for v in vertices)
        g = Tree(
            vertices,
            edges,
            layout=positions,  # "kamada_kawai",
            vertex_config=vconfig,
            edge_config={"color": solarized.BASE00},
            # labels=labels,
        )

        self.play(Create(g))
        self.wait(1)

        self.play(g.animate.set_colors(dict((v, solarized.GREEN) for v in leaves)))
        self.wait(1)

        self.play(g.animate.set_path_color(a, b))
        self.wait(1)

        a2 = 117
        b2 = 6
        self.play(g.animate.set_path_color(a2, b2, solarized.BLUE))

        self.wait(1)


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
