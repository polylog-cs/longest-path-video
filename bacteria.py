from manim import *
import numpy as np
import math

import solarized
import tree_data
from util import Tree


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
