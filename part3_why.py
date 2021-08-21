from manim import *
import math
import solarized
import tree_data
from util import *


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
        self.play(DrawBorderThenFill(self.g))

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
        b1, c1 = 64, 0
        b2, c2 = 21, 9

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

        self.play(DrawBorderThenFill(self.g))
        self.play(self.g.animate.set_path_color(b1, c1, solarized.RED))
        self.wait()

        eps = 0.1
        tleft = hanging[b1] + 2 * eps * LEFT + eps * UP
        tright = hanging[c1] + 2 * eps * RIGHT + eps * UP
        tmid = (tleft + tright) / 2.0
        tbot = (
            tmid
            - [(tmid - tleft)[1], (tmid - tleft)[0], 0]
            + (4 / 1.4 - 1) * eps * DOWN
        )

        def flash_triangle():
            ltop = Line(tright, tleft, color=solarized.GREEN)
            lleft = Line(tleft, tbot, color=solarized.GREEN)
            lright = Line(tbot, tright, color=solarized.GREEN)
            self.play(
                Create(ltop),
                Create(lleft),
                Create(lright),
                self.g.animate.set_path_color(b1, c1, solarized.RED),
                time=2,
            )
            self.wait(1)
            self.play(Uncreate(ltop), Uncreate(lleft), Uncreate(lright), time=2)
            self.wait(1)

        flash_triangle()

        self.play(
            self.g.animate.change_layout("kamada_kawai", layout_scale=1.5).scale(2)
        )
        self.wait(1)

        self.play(self.g.animate.set_path_color(b1, c1, solarized.BASE00))

        self.wait(1)
        self.play(self.g.animate.set_path_color(b2, c2))
        self.wait(1)

        self.play(
            self.g.animate.scale(0.5).change_layout(
                self.g.hanging_position(b2, c2, shift=2 * UP, scale=1.0)
            )
        )

        self.wait(1)
        self.play(self.g.animate.set_colors_all())
        self.wait(1)

        # tenhle trojuhelnik uz tu nechame dyl
        # flash_triangle()
        ltop = Line(tright, tleft, color=solarized.GREEN)
        lleft = Line(tleft, tbot, color=solarized.GREEN)
        lright = Line(tbot, tright, color=solarized.GREEN)
        self.play(Create(ltop), Create(lleft), Create(lright), time=2)
        self.wait(1)

        # animace, zvýraznit třetí vrchol horní cesty a pak vzdálenost k levému
        #   kraji a ke spodku podstromu (vzdálenost je stejná)
        b3, c3 = 64, 80
        v_layers = [[6], [60, 7], [61, 8], [64, 9]]
        e_layers = [[(6, 60), (6, 7)], [(60, 61), (7, 8)], [(61, 64), (8, 9)], []]
        anim1, anim2 = self.g.bfs_animation(6, override_layers=(v_layers, e_layers), custom_angles = {64: (-70, 1.5), 61: (180, 1), 9: (90, 1)})
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

        # rotace sporné cesty

        Grot = Tree(
            [6, 60, 61, 64, 100],
            [(6, 60), (60, 61), (61, 64), (64, 100)],
            layout={
                6: self.g.vertices[6].get_center(),
                60: self.g.vertices[60].get_center(),
                61: self.g.vertices[61].get_center(),
                64: self.g.vertices[64].get_center(),
                100: self.g.vertices[100].get_center(),
            },
            # layout_scale=3.5,
            vertex_config={"color": solarized.RED},
            edge_config={"color": solarized.RED},
            labels=False,
        )

        self.play(Create(Grot), run_time=0.1)
        self.play(Rotate(Grot, math.pi / 2, about_point=Grot.vertices[6].get_center()))
        self.wait()
        self.play(Rotate(Grot, -math.pi / 2, about_point=Grot.vertices[6].get_center()))
        self.wait()

        self.play(self.g.animate.remove_edges((64, 100)))
        self.play(self.g.animate.remove_vertices(100), run_time=0.1)
        self.play(
            self.g.animate.set_colors_all(),
            Uncreate(ltop),
            Uncreate(lleft),
            Uncreate(lright),
            Uncreate(Grot),
        )
        self.wait()


class Proof(Scene):
    def construct(self):
        # va, vb, vc = 61, 80, 46
        # va, vb, vc = 62, 21, 64
        # va, vb, vc = 45, 65, 0
        # va, vb, vc = 45, 21, 64
        va, vb, vc = 45, 21, 9

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
            # label_class=Text,
        )

        hanging = self.g.hanging_position(vb, vc, shift=2 * UP, scale=1.0)
        self.g.change_layout(hanging)

        self.play(DrawBorderThenFill(self.g))
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

        custom_angles = {42: (180, 1), 21: (90, 1), 9: (90, 1), 
            61: (180, 1), 63: (-90, 1), 64: (-90, 1), 
            54: (180, 1), 60: (180, 1), 62: (0, 1)}

        anim1, anim2 = self.g.bfs_animation(va, override_layers=(v_layers, e_layers), custom_angles = custom_angles)

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

        for v, vd, steps_first_part in [(va, 4, 3), (65, 6, 4)]:
            top = self.g[vd].get_center()
            line1 = Line(top, top, color=solarized.GREEN)
            line2 = Line(top, top, color=solarized.GREEN)
            self.add(line1, line2)

            if v != va:
                self.play(
                    self.g[v].animate.scale(scale_factor),
                    self.g[va].animate.scale(1 / scale_factor),
                )

            v_layers, e_layers, _ = self.g.bfs(v)
            # v_layers.pop()
            # e_layers[-1] = []
            e_layers.append([])
            anim11, anim12 = self.g.bfs_animation(
                va,
                override_layers=(
                    v_layers[:steps_first_part],
                    e_layers[:steps_first_part],
                ),
                custom_angles = custom_angles
            )

            uncreate_anims = [anim12]

            self.play(anim11)
            square = Square(side_length=0.5, color=solarized.GREEN).move_to(
                self.g[vd].get_center()
            )
            self.play(Create(square))
            self.wait()
            self.play(Uncreate(square))

            for i in range(steps_first_part, len(v_layers)):
                anim21, anim22 = self.g.bfs_animation(
                    va,
                    override_layers=(
                        v_layers[i : i + 1],
                        e_layers[i : i + 1],
                    ),
                    distance_offset=i,
                    turn_furthest_off=(i == len(v_layers) - 1),
                    custom_angles = custom_angles,
                )
                uncreate_anims.append(anim22)

                if i == 5:
                    #rectangle okolo začínajícího podstromu
                    rect = Rectangle(
                        height = (self.g.vertices[40].get_center() - self.g.vertices[46].get_center())[1] + 1,
                        width = 1.5, 
                        color = solarized.GREEN 
                    )
                    rect.move_to(self.g.vertices[40].get_center()/2 
                        + self.g.vertices[46].get_center()/4 
                        + self.g.vertices[44].get_center()/4
                        + 0.1* LEFT + 0.2*DOWN)
                    self.play(Create(rect))
                    self.wait()
                    self.play(Uncreate(rect))

                dist = i - steps_first_part + 1.5
                self.play(
                    AnimationGroup(
                        # line1.animate(rate_func=linear)
                        line1.animate.put_start_and_end_on(
                            top + LEFT * dist, top + DOWN * dist
                        ),
                        line2.animate.put_start_and_end_on(
                            top + RIGHT * dist, top + DOWN * dist
                        ),
                        run_time=anim21.get_run_time(),
                    ),
                    anim21,
                )
                self.wait()

            self.play(FadeOut(line1), FadeOut(line2))
            self.wait()
            self.play(*uncreate_anims)
            self.wait()

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

        self.play(DrawBorderThenFill(self.g))
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


class Outro(Scene):
    def construct(self):
        base_color = solarized.BASE00

        # jeste jednou kniha
        offset = np.array((2.0, -0.5, -1))
        offset_start = np.array((5.0, -2.0, -1))
        offset_final = np.array((8, -3, 0))
        book_height_large = 6.0
        book_height_small = 2.5

        offset2_start = offset_start
        book2 = OSVGMobject("img/open-book.svg", height=book_height_small)
        # http://www.clker.com/cliparts/I/O/x/x/4/8/open-book.svg
        book2.move_to(offset2_start)
        self.play(FadeIn(book2))

        offset2 = offset + np.array((0, 0, 0))
        self.play(
            ApplyMethod(
                book2.move_and_resize, offset2, book_height_large / book_height_small
            )
        )

        # strom
        time_scale = 2.0
        tree_scale = 2.0
        edge_scale = 0.5
        node_radius = 0.1
        base_color = solarized.BASE00
        highlight_color = RED

        ex_tree = Tree(
            tree_data.misof_example_vertices,
            tree_data.misof_example_edges,
            layout="kamada_kawai",
            layout_scale=tree_scale,
            vertex_config={"radius": node_radius, "color": base_color},
            labels=False,
            edge_config={"color": base_color}
            # labels=True
        )

        # self.add_foreground_mobjects(ex_tree)
        offset2_tree_start = offset2 + np.array((-0.45 * book_height_large, 0.3, 0))
        ex_tree.move_to(offset2_tree_start)
        ex_tree.rot(offset2_tree_start, math.pi / 2.0)
        ex_tree.shift(1 * RIGHT)

        # self.play(Create(ex_tree))
        self.play(DrawBorderThenFill(ex_tree))

        a = 5
        b = 10
        c = 20

        self.play(ex_tree.animate.set_path_color(a, a, GREEN))
        a_hanging = ex_tree.hanging_position(
            a,
            a,
            shift=offset2
            + np.array((-0.3 * book_height_large, 0.2 * book_height_large, 0)),
            scale=edge_scale,
            delta=5 * node_radius,
            custom_layers={2: [12, 3, 13, 7, 15, 18]},
        )

        self.play(ex_tree.animate.change_layout(a_hanging), run_time=time_scale)
        self.play(ex_tree.animate.set_path_color(b, b, highlight_color))

        ex_tree2 = ex_tree.copy()
        b_hanging = ex_tree.hanging_position(
            b,
            b,
            shift=offset2
            + np.array((+0.26 * book_height_large, 0.46 * book_height_large, 0)),
            scale=edge_scale,
            delta=5 * node_radius,
            custom_layers={},
        )

        # takle se to asi nema delat?
        self.play(ex_tree2.animate.set_path_color(a, a, base_color), run_time=0)
        self.play(ex_tree2.animate.set_path_color(b, b, highlight_color), run_time=0)
        self.play(ex_tree2.animate.change_layout(b_hanging), run_time=time_scale)
        # self.play(ex_tree2.animate.set_path_color(c, c, highlight_color))
        self.play(ex_tree2.animate.set_path_color(b, c, highlight_color))

        whole_book = Group(book2, ex_tree, ex_tree2)



        #######################################################
        # kniha odjede
        self.play(
            whole_book.animate.scale(0.2).move_to(offset_final)            
        )



        ###############################################################################
        # pak oba stromy
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

        self.play(DrawBorderThenFill(self.g), run_time=0.1)
        self.wait()

        va, vb = 65, 21
        self.g2 = Tree(
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

        hanging = self.g2.hanging_position(
            va, vb, shift=3 * RIGHT + 0 * DOWN, scale=0.7
        )
        self.g2.change_layout(hanging)

        self.play(
            ApplyMethod(self.g.shift, 4 * LEFT + 1 * DOWN),
            DrawBorderThenFill(self.g2),
            run_time=1,
        )

        # rectangles appear

        l_c = 3
        r_c = [4, 5]

        rec1 = Rectangle(height=0.5, width=1.0, color=solarized.GREEN).move_to(
            self.g[l_c].get_center()
        )
        rec2 = Rectangle(height=0.5, width=1.5, color=solarized.GREEN).move_to(
            (self.g2[r_c[0]].get_center() + self.g2[r_c[1]].get_center()) / 2.0
        )
        self.play(Create(rec1), Create(rec2))

        # paths are lighting up

        txt = Tex(r"In the middle of all longest paths", color=base_color)
        txt.shift(2 * UP)

        st = np.array((-3, 2, 0))
        en = np.array((-4, 0.1, 0))
        st2 = np.array((2, 2, 0))
        en2 = np.array((3, 0.1, 0))
        ar1 = Arrow(start=st, end=en, color=base_color)
        ar2 = Arrow(start=st2, end=en2, color=base_color)
        self.play(Create(txt), Create(ar1), Create(ar2))

        even_paths = [(1, 5), (32, 34), (5, 20), (33, 1)]
        odd_paths = [(65, 21), (56, 46), (10, 64), (44, 80)]
        for i in range(len(even_paths)):
            t = 0.1
            anim_l1, anim_l2 = self.g.path_animation(
                even_paths[i][0],
                even_paths[i][1],
                time_per_step=t * 1.9,
                color=RED,
                rect=(l_c, rec1, rec2),
            )
            anim_r1, anim_r2 = self.g2.path_animation(
                odd_paths[i][0], odd_paths[i][1], time_per_step=t, color=RED
            )

            self.play(anim_l1, anim_r1)
            self.wait()
            self.play(anim_l2, anim_r2)

        self.wait()
        self.play(
            Uncreate(txt),
            Uncreate(self.g),
            Uncreate(self.g2),
            Uncreate(ar1),
            Uncreate(ar2),
            Uncreate(rec1),
            Uncreate(rec2),
        )

        txt_fs = Tex(r"The actual longest path in Vaclav's filesystem", color = base_color)
        txt_fs.shift(2*UP)
        self.play(Write(txt_fs))

        self.wait()
        self.play(Unwrite(txt_fs))
        self.wait()
        txt_th1 = Tex(r"Big thanks to: ", color = base_color)
        txt_th21 = Tex(r"3blue1brown", color = base_color)
        txt_th22 = Tex(r"\& LeiosOS", color = base_color)
        img_3b1b = ImageMobject("img/3b1b.jpg")
        img_3b1b.height = 0.7
        img_leios= ImageMobject("img/leios.jpg")
        img_leios.height = 0.7
        txt_th2 = Group(txt_th21, img_3b1b, txt_th22, img_leios).arrange(RIGHT)
        txt_th3 = Tex(r"manim community", color = base_color)
        txt_th4 = Tex(r"Tom Gavenčiak, Mohsen Ghaffari, Filip Hlásek", color = base_color)
        txt_th5 = Tex(r"Mirek Olšák, Hanka Rozhoňová", color = base_color)
        txt_th = Group(txt_th1, txt_th2, txt_th3, txt_th4, txt_th5).arrange(DOWN)
        txt_th1.align_to(txt_th, LEFT)
        txt_th2.align_to(txt_th, LEFT)
        txt_th3.align_to(txt_th, LEFT)
        txt_th4.align_to(txt_th, LEFT)
        txt_th5.align_to(txt_th, LEFT)
        
        self.play(Write(txt_th1))
        self.wait()
        self.play(Write(txt_th21), FadeIn(img_3b1b), Write(txt_th22), FadeIn(img_leios))
        self.wait()
        self.play(Write(txt_th3))
        self.play(ApplyWave(
            txt_th3,
            rate_func=linear,
            ripples=3
        ))
        self.wait()

        self.play(Write(txt_th4), Write(txt_th5))

        self.wait()
        self.play(Unwrite(txt_th1), Unwrite(txt_th21), FadeOut(img_3b1b), Unwrite(txt_th22), FadeOut(img_leios), 
            Unwrite(txt_th3), Unwrite(txt_th4), Unwrite(txt_th5))
        self.wait(10)
