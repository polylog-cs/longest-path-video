from manim import *

import solarized
from util import Tree

example_vertices = list(range(1, 22))
example_edges = [
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (8, 9),
    (9, 10),
    (3, 11),
    (4, 12),
    (4, 13),
    (5, 14),
    (6, 15),
    (8, 16),
    (13, 17),
    (14, 18),
    (16, 19),
    (17, 20),
    (17, 21),
]


def get_adjacency_list(g):
    adj = dict([(v, []) for v in g.vertices])
    for v1, v2 in g.edges:
        adj[v1].append(v2)
        adj[v2].append(v1)

    return adj


class LongestPath(Scene):
    # CONFIG = {"camera_config": {"background_color": solarized.BASE2}}

    def make_triangle(self, start, end):
        padding = 0.7
        start_pos = self.g[start].get_center() + np.array([-padding, 0, 0])
        end_pos = self.g[end].get_center() + np.array([padding, 0, 0])
        distance = end_pos[0] - start_pos[0]

        mid_pos = np.array(
            [(start_pos[0] + end_pos[0]) / 2, start_pos[1] - distance / 2, 0]
        )

        line_left = Line(start_pos, mid_pos, color=solarized.CYAN)
        line_right = Line(end_pos, mid_pos, color=solarized.CYAN)

        self.play(Create(line_left), Create(line_right), time=2)

    def construct(self):
        self.g = Tree(
            example_vertices,
            example_edges,
            layout="kamada_kawai",
            layout_scale=4.0,
            vertex_config={
                # "radius": 0.2,
                "color": solarized.BASE00
            },
            edge_config={"color": solarized.BASE00},
        )

        self.play(Create(self.g))

        pos = self.g.hanging_position(10, 1, shift=np.array([0, 2, 0]))

        self.wait()
        self.play(self.g[1].animate.scale(1.5))
        self.play(self.g.bfs_animation(1, turn_furthest_off=False))
        self.wait(1)
        self.play(self.g.animate.change_layout(pos))

        self.play(
            self.g[1].animate.scale(1 / 1.5),
            self.g[10].animate.scale(1.5),
        )
        self.play(self.g.animate.set_colors_all(solarized.BASE00))
        self.play(self.g.bfs_animation(10, turn_furthest_off=False))

        self.wait()
