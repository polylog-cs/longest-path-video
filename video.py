from manim import *

import solarized

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


def hanging_position(g: Graph, start, end, shift=None):
    positions = {}
    top = get_path(g, start, end)

    adj = get_adjacency_list(g)

    def hang(v1, parents):
        n_sons = 0
        for v2 in adj[v1]:
            if v2 not in parents:
                n_sons += 1

        delta = -n_sons / 2 + 0.5
        for v2 in adj[v1]:
            if v2 not in parents:
                positions[v2] = positions[v1] + np.array([delta * 0.3, -1, 0])
                # (pos[0] + delta * 0.2, pos[1] + 1, 0)
                hang(v2, [v1])
                delta += 1

    for i, v1 in enumerate(top):
        positions[v1] = np.array([i - len(top) / 2 + 0.5, 0, 0])

        hang(v1, top)

    if shift is not None:
        for k in positions:
            positions[k] += shift

    return positions



class LongestPath(Scene):
    # CONFIG = {"camera_config": {"background_color": solarized.BASE2}}

    def play_bfs(self, start, turn_furthest_off=True):
        v_layers, e_layers, _ = bfs(self.g, start)
        e_layers.append([])

        def vertex_on(v: Dot):
            v.set_fill(solarized.RED)
            # v.scale(1.5)
            return v

        def vertex_off(v):
            v.set_fill(solarized.RED)
            # v.scale(1 / 1.5)
            return v

        all_progress_lines = []

        all_anims = []
        to_unhighlight = []

        for i in range(len(v_layers)):
            anims = []

            def make_progress_line(v1, dummy):
                def get_progress_line():
                    return Line(
                        self.g[v1].get_center(),
                        dummy.get_center(),
                        color=solarized.RED,
                        stroke_width=DEFAULT_STROKE_WIDTH * 1.1,
                    )

                return get_progress_line

            for (v1, v2) in e_layers[i]:
                dummy = Dot(self.g[v1].get_center(), fill_opacity=0)

                progress_line = always_redraw(make_progress_line(v1, dummy))
                self.add(dummy, progress_line)
                all_progress_lines.append(progress_line)

                # anims.append(self.g.edges[tuple(sorted((v1, v2)))].animate.set_stroke(solarized.RED))
                anims.append(
                    dummy.animate(rate_func=linear).move_to(self.g[v2].get_center())
                )

            for v in v_layers[i]:
                if v != start:
                    if i == len(v_layers) - 1 and not turn_furthest_off:
                        # Do not turn these off.
                        anims.append(ApplyFunction(vertex_on, self.g[v]))
                    else:
                        to_unhighlight.append(v)
                        anims.append(
                            Succession(
                                ApplyFunction(vertex_on, self.g[v]),
                                ApplyFunction(vertex_off, self.g[v]),
                                run_time=1,
                            )
                        )

            all_anims.append(AnimationGroup(*anims, run_time=0.5))

        for v in self.g.vertices:
            self.bring_to_front(self.g[v])

        self.play(AnimationGroup(*all_anims, lag_ratio=0.95))

        self.play(
            *(
                [FadeOut(l) for l in all_progress_lines]
                + [self.g[v].animate.set_fill(solarized.BASE00) for v in to_unhighlight]
            )
        )

        self.remove(*all_progress_lines)

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
        self.g = Graph(
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

        # pos = hanging_position(self.g, 10, 1, shift=np.array([0, 2, 0]))
        # self.play(*[self.g[v].animate.move_to(k) for v, k in pos.items()])

        # self.play(
        #     g[1].animate.move_to([1, 1, 0]),
        #     g[2].animate.move_to([-1, 1, 0]),
        #     g[3].animate.move_to([1, -1, 0]),
        #     g[4].animate.move_to([-1, -1, 0]),
        # )
        # self.wait()
        # self.make_triangle(10, 1)

        self.wait()
        self.play(self.g[1].animate.scale(1.5))
        self.play_bfs(1, turn_furthest_off=False)
        self.wait()
        self.play(
            self.g[1].animate.scale(1 / 1.5),
            self.g[10].animate.scale(1.5),
        )
        self.play(
            *[self.g[v].animate.set_fill(solarized.BASE00) for v in self.g.vertices]
        )
        self.play_bfs(10, turn_furthest_off=False)

        self.wait()
