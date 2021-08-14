from manim import *

import solarized
import tree_data
from util import Tree
from util import OScene


class Naive(OScene):
    def construct(self):
        self.outline(2)

        # TODO: osnova: Algorithm
        
        # animace nkrát zkopírovaného grafu (už je to náš příkladový graf),
        #   na každém běží bfs z jednoho vrcholu, důležité, aby jednotlivá bfs
        #   běžela sekvenčně a každé bfs běželo sekvenčně
        scale_factor = 3.0
        g_scale_factor = 0.21

        vertices = tree_data.example_vertices

        gs = VGroup(
            *[
                Tree(
                    vertices,
                    tree_data.example_edges,
                    layout="kamada_kawai",
                    # layout_scale=3.5,
                    layout_scale=3.5,
                    vertex_config={
                        "color": solarized.BASE00,
                        # "radius": 0.08 * g_scale_factor,
                    },
                    edge_config={"color": solarized.BASE00},
                    # labels=True
                ).scale(g_scale_factor)
                for _ in range(len(vertices))
            ]
        )
        # buff = padding (rows, cols)
        gs.arrange_in_grid(cols=8, buff=(0.25, 0.4)).shift(DOWN * 0.25)
        self.play(Create(gs))
        self.wait()

        rng: np.random.Generator = np.random.default_rng(seed=127)
        rng.shuffle(vertices)

        self.play(
            *[
                g[va].animate.scale(scale_factor)
                for va, g in zip(vertices, gs)
            ]
        )

        for va, g in zip(vertices, gs[:7]):
            v_layers, e_layers, _ = g.bfs(va)
            vb = rng.choice(v_layers[-1])

            anim1, anim2 = g.bfs_animation(va, time_per_step=0.2, annotations=False)
            self.play(anim1)
            self.play(anim2)
            self.play(
                Create(
                    Text(
                        f"Length: {len(v_layers) - 1}",
                        color=solarized.BASE00,
                        font="Helvetica Neue",
                        weight="SEMIBOLD",
                    )
                    .scale(0.4)
                    .move_to(g.get_top() + UP * 0.2)
                ),
                g.animate.set_path_color(va, vb),
                run_time=0.5,
            )
            
        self.wait()

        # (animace, jak vašek klikne v terminálu na enter, pak se zapne TQDM progress bar
        #   a bude vidět na pozadí při mluvení, aby se ukázalo, jak pomalé to je)

        # After waiting for like an hour, our calculation seems to be about right.
        # TODO: animace výpočtu nxn/10^6 = …, pak jak vypadá tqdm bar po hodině?


class QuadraticVsLinear(Scene):
    def construct(self):
        pass
        # TODO: animace lineární a kvadratické křivky: n^2 vs n vs 10n


class Algorithm(Scene):
    def construct(self):
        pass
        # Fortunately, there is a much faster algorithm whose number of steps is about 2n.
        # Here is how it works. We start by picking one node in our tree, it doesn't matter which one. We call it, say, a.
        # Next, we find the distance from it to all other nodes.

        # TODO: animace toho, jak se vybere a a jede bfs
        # TODO: přidat labely "a", "b". Možná i "c"
        self.g = Tree(
            tree_data.example_vertices,
            tree_data.example_edges,
            layout="kamada_kawai",
            layout_scale=3.5,
            vertex_config={
                # "radius": 0.2,
                "color": solarized.BASE00
            },
            edge_config={"color": solarized.BASE00},
            # labels=True
        )
        self.play(Create(self.g))

        config = [(52, 21, 64, solarized.RED), (40, 80, 46, solarized.BLUE)]

        # TODO: druhou iteraci prehrat rychleji
        for va, vb, vc, color in config:
            scale_factor = 3.0

            self.wait()
            self.play(self.g[va].animate.scale(scale_factor))
            anim1, anim2 = self.g.bfs_animation(va, turn_furthest_off=False)

            self.play(anim1)
            self.play(anim2)
            self.wait(1)

            self.play(
                self.g[va].animate.scale(1 / scale_factor),
                self.g[vb].animate.scale(scale_factor),
            )
            self.play(self.g.animate.set_colors_all(solarized.BASE00))
            anim1, anim2 = self.g.bfs_animation(vb, turn_furthest_off=False)
            self.play(anim1)
            self.play(anim2)

            self.wait()
            self.play(self.g[vc].animate.scale(scale_factor))
            self.play(self.g.animate.set_colors_all(solarized.BASE00))

            self.play(self.g.animate.set_path_color(vb, vc, color))
            self.wait(2)

            self.play(
                self.g[vb].animate.scale(1 / scale_factor),
                self.g[vc].animate.scale(1 / scale_factor),
            )
            self.play(self.g.animate.set_colors_all(solarized.BASE00))

        self.play(
            self.g.animate.set_path_color(config[0][1], config[0][2], config[0][3])
        )
        self.wait(2)

        # TODO: animace terminálu, kde vašek klikne a hned vidí výsledek