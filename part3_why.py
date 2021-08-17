from manim import *

import solarized
import tree_data
from util import Tree
from util import OScene

class Misof(OScene):
    def construct(self):
        self.outline(3)

        cover = ImageMobject("img/forisek_steinova.jpg").scale(1.5)
        text = Tex(r"Michal Forišek\\Monika Steinová", color=solarized.BASE00)
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
        hanging = self.g.hanging_position(b1, c1, shift=2 * UP, scale=1.0)
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

        self.play(self.g.animate.set_colors_all())
        self.wait()


class Proof(Scene):
    def construct(self):
        # va, vb, vc = 61, 80, 46
        va, vb, vc = 62, 21, 64

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
            # labels=True,
        )

        hanging = self.g.hanging_position(vb, vc, shift=2 * UP, scale=1.0)
        self.g.change_layout(hanging)

        self.play(Create(self.g))
        # self.play(DrawBorderThenFill(self.g))
        self.wait()

        scale_factor = 3.0

        self.wait()
        self.play(self.g[va].animate.scale(scale_factor))

        # So, recall that we start by finding some node farthest away from a.
        # Let's think about where this farthest node can be. We start computing
        # distances from a to other nodes. Let us pause the algorithm now, just
        # one step before we reach the leftmost node.
        v_layers, e_layers, _ = self.g.bfs(va)
        # v_layers.pop()
        # e_layers[-1] = []
        anim1, anim2 = self.g.bfs_animation(va, override_layers=(v_layers, e_layers))

        self.play(anim1)
        self.wait(1)
        self.play(anim2)

        # By this time, we have already reached all nodes on the left side,
        # except the nodes lying on the edge of the triangle.
        # self.highlight_left_edge()

        # We have also reached the node on the right that is closest to the
        # bottom tip of the triangle. That means we already reached all the
        # nodes in the right side of the triangle to the left of a.

        # self.play(self.g[va].animate.scale(1 / scale_factor))
        self.wait()

        vd = 60
        top = self.g[vd].get_center()
        line1 = Line(top, top, color=solarized.GREEN)
        line2 = Line(top, top, color=solarized.GREEN)
        self.add(line1, line2)

        v_layers, e_layers, _ = self.g.bfs(va)
        v_layers.pop()
        e_layers[-1] = []
        anim11, anim12 = self.g.bfs_animation(
            va, override_layers=(v_layers[:2], e_layers[:2])
        )
        anim21, anim22 = self.g.bfs_animation(
            va, override_layers=(v_layers[2:], e_layers[2:])
        )

        self.play(anim11)
        square = Square(side_length=0.5, color=solarized.GREEN).move_to(
            self.g[vd].get_center()
        )
        self.play(Create(square))
        self.wait()
        self.play(Uncreate(square))

        dist = 6.5
        self.play(
            AnimationGroup(
                line1.animate(rate_func=linear).put_start_and_end_on(
                    top + LEFT * dist, top + DOWN * dist
                ),
                line2.animate(rate_func=linear).put_start_and_end_on(
                    top + RIGHT * dist, top + DOWN * dist
                ),
                run_time=anim21.get_run_time(),
            ),
            anim21,
        )
        self.wait()

        self.play(anim12, anim22)


    def highlight_left_edge(self):
        v_edge_top = 21
        v_edge_bot = 46
        dy = self.g[v_edge_top].get_center()[1] - self.g[v_edge_bot].get_center()[1]
        padding = 0.5
        top = self.g[v_edge_top].get_center()

        poly = Polygon(
            top + 2 * LEFT * padding + UP * padding,
            top + UP * padding,
            top + np.array((dy + 2 * padding, -dy - padding, 0.0)),
            top + np.array((dy, -dy - padding, 0.0)),
            color=solarized.GREEN,
        )
        self.play(Create(poly))
        self.wait(1)
        self.play(Uncreate(poly))


class EvenCase(Scene):
    def construct(self):
        pass
        self.g = Tree(
            tree_data.even_example_vertices,
            tree_data.even_example_edges,
            layout="kamada_kawai",
            layout_scale=3.5,
            vertex_config={
                # "radius": 0.2,
                "color": solarized.BASE00
            },
            edge_config={"color": solarized.BASE00},
            # labels=True,
        )

        hanging = self.g.hanging_position(1, 5, shift=UP, scale=1.0)
        self.g.change_layout(hanging)

        self.play(Create(self.g))
        # self.play(DrawBorderThenFill(self.g))
        self.wait()

        square = Rectangle(height=0.5, width=1.0, color=solarized.GREEN).move_to(
            self.g[33].get_center()
        )
        self.play(Create(square))
        self.wait()
        self.play(Uncreate(square))

        self.play(self.g.animate.set_path_color(32, 34))
        self.wait()
