from manim import *

import solarized
import tree_data
from util import Tree
from util import OScene


class Naive(OScene):
    def construct(self):
        self.outline(2)

        #vytvori prvni strom a ukaze bfs

        a = 4
        main_g = Tree(
                    tree_data.example_vertices,
                    tree_data.example_edges,
                    layout="kamada_kawai",
                    # layout_scale=3.5,
                    layout_scale=3.5,
                    vertex_config={
                        "color": solarized.BASE00,
                        "radius": 0.20,
                    },
                    edge_config={"color": solarized.BASE00},
                    # labels=True
                )

        self.play(DrawBorderThenFill(main_g))
        self.wait()

        
        self.play(main_g.animate.set_colors_and_enlarge(vertex_colors = {a: solarized.RED}, sc = 1.5))
        self.wait()

        txt = Tex(r"Breadth First Search", color = solarized.BASE00)
        txt.shift(4*RIGHT+3*UP)

        anim1, high_anim, anim2 = main_g.bfs_animation(a, time_per_step=1, annotations=True, 
            final_highlight = 5, 
            custom_angles = {10: (180, 1), 56: (0, 1)})
        self.play(anim1)
        self.wait()
        self.play(Write(txt))
        self.wait()
        self.play(*high_anim)
        self.wait()
        self.play(anim2)
        self.wait()

        anim1, anim2 = main_g.path_animation(a, 65)
        self.play(anim1)
        self.wait()
        self.play(anim2, Uncreate(main_g), Unwrite(txt))
        self.wait()

        # animace nkrát zkopírovaného grafu (už je to náš příkladový graf),
        #   na každém běží bfs z jednoho vrcholu, důležité, aby jednotlivá bfs
        #   běžela sekvenčně a každé bfs běželo sekvenčně
        scale_factor = 2.0
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
                        "radius": 0.20,
                    },
                    edge_config={"color": solarized.BASE00},
                    # labels=True
                ).scale(g_scale_factor)
                for _ in range(int(len(vertices)))
            ]
        )
        # buff = padding (rows, cols)
        gs.arrange_in_grid(cols=8, buff=(0.25, 0.4)).shift(DOWN * 0.25)
        self.play(FadeIn(gs))
        self.wait()

        rng: np.random.Generator = np.random.default_rng(seed=127)
        rng.shuffle(vertices)
        

        self.play(
            *[
                g[va].animate.scale(scale_factor)
                for va, g in zip(vertices, gs)
            ]
        )
        
        num_before = 5
        i = 0
        nines = []
        all_texts = []
        for va, g in zip(vertices, gs):
            v_layers, e_layers, _ = g.bfs(va)
            vb = rng.choice(v_layers[-1])

            
            run_time = 0.1
            if i < num_before:
                anim1, anim2 = g.bfs_animation(va, time_per_step=0.3, annotations=False)
                self.play(anim1)
                self.play(anim2)
                run_time = 0.5
            txt = Tex(
                        f"Length: {len(v_layers) - 1}",
                        color=solarized.BASE00#font="Helvetica Neue",weight="SEMIBOLD",
                    ).scale(0.4).move_to(g.get_top() + UP * 0.2)

            all_texts.append(txt)
            if len(v_layers) - 1 == 9:
                nines.append(txt)

            self.play(
                Create(txt),
                g.animate.set_path_color(va, vb),
                run_time=run_time,
            )
            i += 1

        self.wait()

        self.play(*[Indicate(txt) for txt in nines])

        self.wait()

        # (animace, jak vašek klikne v terminálu na enter, pak se zapne TQDM progress bar
        #   a bude vidět na pozadí při mluvení, aby se ukázalo, jak pomalé to je)

        # After waiting for like an hour, our calculation seems to be about right.
        # TODO: animace výpočtu nxn/10^6 = …, pak jak vypadá tqdm bar po hodině?

        self.play(*[Uncreate(txt) for txt in all_texts])
        self.play(gs.animate.shift(4*LEFT+2*DOWN).scale(0.3))
        

        main_g = Tree(
                    tree_data.example_vertices,
                    tree_data.example_edges,
                    layout="kamada_kawai",
                    # layout_scale=3.5,
                    layout_scale=1.5,
                    vertex_config={
                        "color": solarized.BASE00,
                        "radius": 0.08,
                    },
                    edge_config={"color": solarized.BASE00},
                    # labels=True
                )
        main_g.shift(4*LEFT + 1*UP)
        self.play(DrawBorderThenFill(main_g))


        txt11 = Tex(r"$n$ computations", color = solarized.BASE00).scale(0.7)
        txt12 = Tex(r"per starting node", color = solarized.BASE00).scale(0.7)
        txt11.shift(1*RIGHT+2*UP)
        txt1 = Group(txt11, txt12).arrange(DOWN)
        txt12.align_to(txt11, LEFT)
        txt1.shift(1*UP)

        anim1, anim2 = main_g.bfs_animation(a, time_per_step=1, annotations=True, annotations_scale = 0.35)
        self.play(anim1, Write(txt11), Write(txt12))
        self.wait()
        self.play(anim2)
        self.wait()

        txt2 = Tex(r"$n$ starting nodes", color = solarized.BASE00).scale(0.7)
        txt2.shift(0*RIGHT + 2*DOWN)
        self.play(Write(txt2))
        self.wait()

        txts = Group(txt1, txt2)
        txt3 = Tex(r"$n^2$ operations in total", color = solarized.BASE00).scale(0.7)
        br = Brace(txts, direction = RIGHT, color = solarized.BASE00)
        txt3.align_to(br, LEFT)
        txt3.shift([0.4, br.get_center()[1], 0])
        self.play(Write(txt3), Create(br))
        self.wait()


        txt_mil1 = Tex(r"If $n = 1\,000\,000$,", color = solarized.BASE00)
        txt_mil2= Tex(r"then $n^2 = 1\,000\,000\,000\,000$", color = solarized.BASE00)


        txt_mil = Group(txt_mil1, txt_mil2).arrange(DOWN)
        txt_mil1.align_to(txt_mil, RIGHT)
        txt_mil.move_to(3.8*RIGHT + 2.6*DOWN)

        self.play(Write(txt_mil1))
        self.wait()
        self.play(Write(txt_mil2))
        self.wait()
        self.play(Unwrite(txt_mil1), Unwrite(txt_mil2), Uncreate(main_g), Unwrite(txt11), Unwrite(txt12), Unwrite(txt2), Unwrite(txt3), Uncreate(br), Uncreate(gs))
        self.wait()


        self.wait(10)


class Algorithm(Scene):
    def construct(self):
        pass
        # Fortunately, there is a much faster algorithm whose number of steps is about 2n.
        # Here is how it works. We start by picking one node in our tree, it doesn't matter which one. We call it, say, a.
        # Next, we find the distance from it to all other nodes.

        # TODO (VV): přidat labely "a", "b". Možná i "c"
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
        self.play(DrawBorderThenFill(self.g))

        config = [(52, 21, 64, solarized.RED), (40, 80, 46, solarized.BLUE)]

        for va, vb, vc, color in config:
            scale_factor = 3.0

            self.wait()
            self.play(self.g[va].animate.scale(scale_factor))
            self.play(Create(Text("a", color=solarized.BASE2).move_to(self.g[va].get_center())))

            anim1, anim2 = self.g.bfs_animation(va, turn_furthest_off=False)

            self.play(anim1)
            self.play(anim2)
            self.wait(1)

            self.wait()

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