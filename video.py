from manim import *

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


def bfs(g: Graph, start):
    adj = dict([(v, []) for v in g.vertices])
    for v1, v2 in g.edges:
        adj[v1].append(v2)
        adj[v2].append(v1)

    res_vertices = [[start]]
    res_edges = [[]]
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

        if cur_vertices:
            res_vertices.append(cur_vertices)
            res_edges.append(cur_edges)
        else:
            break

    return res_vertices, res_edges


class MovingVertices(Scene):
    def play_bfs(self, start):
        v_layers, e_layers = bfs(self.g, start)
        e_layers.append([])

        def vertex_on(v):
            v.set_fill(RED)
            v.scale(1.5)
            return v

        def vertex_off(v):
            v.set_fill(RED)
            v.scale(1 / 1.5)
            return v

        all_anims = []
        for i in range(len(v_layers) + 1):
            anims = []

            if i < len(v_layers):
                # + [self.g[v].animate.set_radius(0.2) for v in vs]

                def make_progress_line(v1, dummy):
                    def get_progress_line():
                        return Line(
                            self.g[v1].get_center(),
                            dummy.get_center(),
                            color=RED,
                            stroke_width=DEFAULT_STROKE_WIDTH * 1.1,
                        )

                    return get_progress_line

                for (v1, v2) in e_layers[i]:
                    dummy = Dot(self.g[v1].get_center(), fill_opacity=0)

                    # def get_progress_line():
                    #     print("Getting", v1, dummy)
                    #     return Line(
                    #         self.g[v1], dummy, color=RED
                    #     )

                    progress_line = always_redraw(make_progress_line(v1, dummy))
                    self.add(dummy, progress_line)

                    # anims.append(self.g.edges[tuple(sorted((v1, v2)))].animate.set_stroke(RED))
                    anims.append(
                        dummy.animate(rate_func=linear).move_to(self.g[v2].get_center())
                    )

                anims += [
                    Succession(
                        ApplyFunction(vertex_on, self.g[v]),
                        ApplyFunction(vertex_off, self.g[v]),
                    )
                    for v in v_layers[i]
                ]
                for v in v_layers[i]:
                    self.bring_to_front(self.g[v])

            # if i > 0:
            #     anims += [ApplyFunction(vertex_off, self.g[v]) for v in v_layers[i - 1]]

            # self.play(
            #     *anims,
            #     run_time=0.3,
            # )
            # self.wait()

            # if i == 1:
            #     break
            all_anims.append(AnimationGroup(*anims, run_time=1))

        self.play(AnimationGroup(*all_anims, lag_ratio=0.4))

    def construct(self):
        # vertices = [1, 2, 3, 4]
        # edges = [(3, 2), (3, 4), (1, 3), (1, 4)]
        self.g = Graph(
            example_vertices,
            example_edges,
            layout="kamada_kawai",
            layout_scale=4.0,
            # vertex_config={"radius": 0.2},
        )

        self.play(Create(self.g))
        # self.wait()
        # self.play(
        #     g[1].animate.move_to([1, 1, 0]),
        #     g[2].animate.move_to([-1, 1, 0]),
        #     g[3].animate.move_to([1, -1, 0]),
        #     g[4].animate.move_to([-1, -1, 0]),
        # )
        # self.wait()

        self.play_bfs(1)

        line = Line(ORIGIN, ORIGIN).set_color(WHITE)
        dot = Dot(fill_opacity=0)

        def updater():
            line.set_start_and_end_attrs(ORIGIN, dot)

        line.add_updater(updater)
        self.play(dot.animate.shift(LEFT))

        self.wait()


class LineTest(Scene):
    def construct(self):
        dot = Dot(fill_opacity=1)

        self.add(dot)

        self.t_offset = 0

        def go_around_circle(mob, dt):
            self.t_offset += dt

        dot.add_updater(go_around_circle)

        def get_line_to_curve():
            return Line(ORIGIN, dot.get_center(), color=YELLOW_A, stroke_width=2)

        dot_to_curve_line = always_redraw(get_line_to_curve)

        self.add(dot_to_curve_line)
        self.play(dot.animate.shift(UP))

        self.wait()