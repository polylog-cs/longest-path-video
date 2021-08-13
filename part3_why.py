from manim import *

import solarized
import tree_data
from util import Tree


class Misof(Scene):
    def construct(self):
        # TODO: osnova: Why it works

        cover = ImageMobject("img/forisek_steinova.jpg").scale(1.5)
        text = Text("Michal Forišek\nMonika Steinová", color=solarized.BASE00)
        cover.shift(3 * LEFT)
        text.shift(2 * RIGHT)
        self.play(FadeIn(cover))
        self.play(Create(text))
        self.wait(1)


class PhysicalModel(Scene):
    def construct(self):
        pass
        # [fyzická demonstrace odteď dál, bude to ten stejný strom a run algoritmu jako předtím,
        #   jen fyzicky, klidně vedle toho může být obrázek té původní animace aby to šlo srovnat]

        # Pokud chceme, muzeme dat tuhle animaci k fyzickemu modelu
        scale_factor = 3.0
        self.g = Tree(
            tree_data.example_vertices,
            tree_data.example_edges,
            layout="kamada_kawai",
            layout_scale=3.5,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
            # labels=True
        )
        self.play(Create(self.g))

        va = 52
        self.wait()
        self.play(self.g[va].animate.scale(scale_factor))
        anim1, anim2 = self.g.bfs_animation(va, turn_furthest_off=False)

        self.play(anim1)
        self.play(anim2)
        self.wait(1)

        hanging = self.g.hanging_position(va, va, shift=(-4, 3, 0))
        self.play(self.g.animate.change_layout(hanging))
        self.wait(1)


class Triangle(Scene):
    def construct(self):
        pass
        b1, c1 = 21, 64
        b2, c2 = 46, 80

        self.g = Tree(
            tree_data.example_vertices,
            tree_data.example_edges,
            layout="kamada_kawai",
            layout_scale=3.5,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
            # labels=True,
        )
        hanging = self.g.hanging_position(b1, c1, shift=UP, scale=1.0)
        self.g.change_layout(hanging)

        self.play(Create(self.g))
        self.wait()

        tleft = hanging[b1]
        tright = hanging[c1]
        tmid = (tleft + tright) / 2.0
        tbot = tmid - [(tmid - tleft)[1], (tmid - tleft)[0], 0]

        def flash_triangle():
            ltop = Line(tright, tleft, color=solarized.GREEN)
            lleft = Line(tleft, tbot, color=solarized.GREEN)
            lright = Line(tbot, tright, color=solarized.GREEN)
            self.play(Create(ltop), Create(lleft), Create(lright), time=2)
            self.play(Uncreate(ltop), Uncreate(lleft), Uncreate(lright), time=2)
            self.wait(1)

        flash_triangle()

        self.play(self.g.animate.set_path_color(b2, c2))
        self.wait(1)

        self.play(
            self.g.animate.change_layout(
                self.g.hanging_position(b2, c2, shift=UP, scale=1.0)
            )
        )

        self.wait(1)
        self.play(self.g.animate.set_colors_all())

        flash_triangle()

        # animace, zvýraznit třetí vrchol horní cesty a pak vzdálenost k levému
        #   kraji a ke spodku podstromu (vzdálenost je stejná)
        b3, c3 = 64, 80
        v_layers = [[6], [60, 7], [61, 8], [64, 80]]
        e_layers = [[(6, 60), (6, 7)], [(60, 61), (7, 8)], [(61, 64), (8, 80)], []]
        anim1, anim2 = self.g.bfs_animation(6, override_layers=(v_layers, e_layers))
        self.play(anim1)
        self.wait(1)
        self.play(anim2)
        self.wait(1)

        self.play(self.g.animate.set_colors_all())

        b4, c4 = 64, 100
        # důkaz trojúhelníkovosti sporem - animace sporné cesty
        self.play(
            self.g.animate.add_vertices(
                c4,
                positions={c4: self.g[b4].get_center() + DOWN},
                vertex_config={"color": solarized.RED},
            ),
            self.g.animate.add_edges(
                (b4, c4),
                edge_config={"color": solarized.RED},
            ),
        )
        self.play(Flash(self.g[c4], color=solarized.RED))
        self.wait()

        self.play(self.g.animate.set_path_color(b2, c4))

        self.wait()


class Proof(Scene):
    def construct(self):
        pass
        # TODO: animace, ukázat trojúhelník, zvýrazit a

        # So, recall that we start by finding some node farthest away from a.
        # Let's think about where this farthest node can be. We start computing
        # distances from a to other nodes. Let us pause the algorithm now, just
        # one step before we reach the leftmost node. By this time, we have
        # already reached all nodes on the left side, except the nodes lying on
        # the edge of the triangle. We have also reached the node on the right
        # that is closest to the bottom tip of the triangle. That means we
        # already reached all the nodes in the right side of the triangle to the
        # left of a. Finally, we have reached all the nodes to the right of a,
        # because the furthest one, in the right tip of the triangle, is
        # definitely strictly closer than the node in the furthest left tip.
        # TODO: animace toho, jak algoritmus postupuje, stopne krok před cílem, pak
        #   se tam občas objeví nějaké čáry, když se porovnávají vzdálenosti

        # TODO: nějak se vyznačí vrcholy na levé hraně trojúhelníka

        # TODO: animace ohne cestu co jsme našli na tu horní, aby se ukázalo, že jsou
        #   stejně dlouhé


class EvenCase(Scene):
    def construct(self):
        pass
        # TODO: obrázek druhého casu, bude napravo od prvního (příprava na nadcházející animaci)
        # TODO: nechat to viewera rozdejchat


class OtherUses(Scene):
    def construct(self):
        pass
        # This is not the only thing the picture is useful for. For example, it
        # also shows that all longest paths in a tree will either share their
        # middle edge, if the diameter is even, or they share the middle node if
        # the diameter is odd. This middle edge or a node is called the center
        # of the tree and it is also the only place in the tree from which you
        # can reach all other nodes in smallest number of steps, namely half of
        # the tree’s diameter. Or to be precise, its half of the tree’s
        # diameter, rounded up  [+1 u sudých]

        # TODO: animace - běhají různé nejdelší cesty, uprostřed je highlightnutá
        #   hrana (nalevo) nebo vrchol (napravo), vyznačí se centrum  a z něj se
        #   spustí bfs
