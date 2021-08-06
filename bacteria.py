from manim import *
import solarized


bacteria_data = """47.8968 301.269 m
203.398 321.238 l
60.6783 278.841 m
151.258 292.205 l
76.3443 256.66 m
149.48 267.32 l
95.7957 234.426 m
125.78 243.028 l
125.78 243.028 m
119.703 212.651 l
125.78 243.028 m
149.48 244.213 l
149.48 244.213 m
140.305 197.542 l
149.48 244.213 m
149.48 267.32 l
149.48 267.32 m
151.258 292.205 l
151.258 292.205 m
200.435 285.688 l
200.435 285.688 m
203.398 321.238 l
200.435 285.688 m
229.468 224.66 l
229.468 224.66 m
185.623 211.033 l
185.623 211.033 m
155.717 188.032 l
185.623 211.033 m
175.049 177.972 l
229.468 224.66 m
242.503 197.406 l
242.503 197.406 m
197.976 168.428 l
242.503 197.406 m
252.575 176.076 l
252.575 176.076 m
225.32 160.069 l
252.575 176.076 m
257.452 154.074 l
203.398 321.238 m
231.838 338.42 l
231.838 338.42 m
279.772 152.203 l
231.838 338.42 m
260.277 356.788 l
260.277 356.788 m
317.75 201.553 l
317.75 201.553 m
308.27 173.113 l
317.75 201.553 m
364.6 161.939 l
308.27 173.113 m
300.116 152.093 l
308.27 173.113 m
330.283 154.734 l
260.277 356.788 m
275.09 378.71 l
275.09 378.71 m
394.068 171.972 l
275.09 378.71 m
311.825 439.145 l
311.825 439.145 m
96.748 371.008 l
96.748 371.008 m
41.5514 314.621 l
96.748 371.008 m
61.1981 389.375 l
61.1981 389.375 m
29.3687 347.802 l
61.1981 389.375 m
21.9003 380.258 l
311.825 439.145 m
305.9 478.842 l
305.9 478.842 m
182.66 472.325 l
182.66 472.325 m
151.85 471.14 l
151.85 471.14 m
63.5681 425.517 l
63.5681 425.517 m
18.6799 408.685 l
63.5681 425.517 m
18.3662 435.244 l
151.85 471.14 m
132.89 497.802 l
132.89 497.802 m
106.228 478.842 l
106.228 478.842 m
20.1282 457.748 l
106.228 478.842 m
94.378 507.282 l
94.378 507.282 m
56.4581 500.172 l
56.4581 500.172 m
25.8107 489.305 l
56.4581 500.172 m
33.5049 515.404 l
94.378 507.282 m
47.5799 548.479 l
132.89 497.802 m
151.258 548.165 l
151.258 548.165 m
58.2691 567.664 l
151.258 548.165 m
153.035 572.457 l
153.035 572.457 m
73.0143 589.375 l
153.035 572.457 m
149.48 605.044 l
149.48 605.044 m
94.8894 615.013 l
149.48 605.044 m
129.648 645.386 l
182.66 472.325 m
162.809 666.261 l
305.9 478.842 m
343.227 476.472 l
343.227 476.472 m
426.15 187.486 l
343.227 476.472 m
367.52 490.1 l
367.52 490.1 m
458.172 334.273 l
458.172 334.273 m
452.247 305.24 l
452.247 305.24 m
445.762 199.727 l
452.247 305.24 m
478.909 304.648 l
478.909 304.648 m
535.748 302.891 l
478.909 304.648 m
474.762 282.133 l
474.762 282.133 m
522.328 279.126 l
474.762 282.133 m
470.614 257.84 l
470.614 257.84 m
474.413 222.291 l
470.614 257.84 m
497.658 245.97 l
458.172 334.273 m
523.939 357.38 l
523.939 357.38 m
550.811 339.348 l
523.939 357.38 m
558.082 365.661 l
367.52 490.1 m
364.557 529.797 l
364.557 529.797 m
227.69 643.557 l
227.69 643.557 m
259.721 696.575 l
227.69 643.557 m
202.805 657.184 l
202.805 657.184 m
180.515 674.901 l
202.805 657.184 m
218.803 672.589 l
218.803 672.589 m
204.456 684.212 l
218.803 672.589 m
230.954 691.646 l
364.557 529.797 m
397.737 531.575 l
397.737 531.575 m
282.653 698.278 l
397.737 531.575 m
423.807 530.982 l
423.807 530.982 m
371.075 621.042 l
371.075 621.042 m
363.372 654.222 l
363.372 654.222 m
324.267 674.959 l
324.267 674.959 m
312.658 697.592 l
324.267 674.959 m
338.76 694.285 l
363.372 654.222 m
387.072 648.889 l
387.072 648.889 m
362.018 689.139 l
387.072 648.889 m
410.18 647.704 l
410.18 647.704 m
413.688 669.532 l
410.18 647.704 m
436.055 656.994 l
371.075 621.042 m
457.067 642.476 l
423.807 530.982 m
450.469 490.1 l
450.469 490.1 m
531.049 398.262 l
531.049 398.262 m
561.545 384.143 l
531.049 398.262 m
564.379 413.121 l
450.469 490.1 m
465.282 514.392 l
465.282 514.392 m
451.654 604.452 l
451.654 604.452 m
467.682 633.957 l
451.654 604.452 m
485.189 617.818 l
465.282 514.392 m
487.204 497.21 l
487.204 497.21 m
528.087 454.55 l
528.087 454.55 m
564.542 432.685 l
528.087 454.55 m
561.748 464.867 l
487.204 497.21 m
497.869 522.687 l
497.869 522.687 m
502.086 599.177 l
497.869 522.687 m
526.309 508.467 l
526.309 508.467 m
518.014 543.425 l
518.014 543.425 m
523.106 570.011 l
518.014 543.425 m
538.057 542.756 l
526.309 508.467 m
538.752 484.767 l
538.752 484.767 m
557.619 486.753 l
538.752 484.767 m
552.918 504.374 l
"""

def parse_bacteria_tree():
	positions = []
	pos_to_vertex = {}
	edges = []
	data = [(float(d.split(" ")[0]), float(d.split(" ")[1])) for d in bacteria_data.splitlines()]

	for i in range(int(len(data)/2)):
		pos_u = data[2*i]
		pos_v = data[2*i+1]
		if pos_u == pos_v:
			continue
		for pos in (pos_u, pos_v):
			if not pos in pos_to_vertex:
				positions.append(pos)
				pos_to_vertex[pos] = len(pos_to_vertex)
		edges.append((pos_to_vertex[pos_u], pos_to_vertex[pos_v]))
	print(positions)

	return range(len(positions)), edges, positions



####################################################################


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


config.background_color = solarized.BASE2


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

        vertices, edges, positions = parse_bacteria_tree()

        self.g = Graph(
            vertices,
            edges,
            layout=positions,
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
        '''
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
		'''
        self.wait()
