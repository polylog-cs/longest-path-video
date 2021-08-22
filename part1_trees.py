from manim import *
from manim.utils import tex
import numpy as np
import math
import textwrap

import solarized
import tree_data
from util import *

class TheBook(Scene):
    def construct(self):

        text_color = solarized.BASE00
        erdos_img = ImageMobject("img/erdos.jpg")  # wiki
        erdos_img.height = 4
        erdos_desc = Tex(r"Paul Erd\H{o}s", color=text_color)
        erdos = Group(erdos_img, erdos_desc).arrange(DOWN)

        erdos.shift(5 * LEFT)
        erdos.shift(1.5 * UP)

        erdos_img_wink = ImageMobject("img/erdos_wink.jpg")  # wiki
        erdos_img_wink.height = erdos_img.height
        erdos_img_wink.align_to(erdos_img, LEFT)
        erdos_img_wink.align_to(erdos_img, UP)

        self.play(FadeIn(erdos))
        self.wait(1)

        #################################################################

        # book reveal
        offset = np.array((2.0, -0.5, -1))
        offset_start = np.array((5.0, -2.0, -1))
        offset_finish = offset_start - np.array((10, 0.5, 0))
        book_height_large = 6.0
        book_height_small = 2.5
        book = OSVGMobject("img/open-book.svg", height=book_height_small)
        # http://www.clker.com/cliparts/I/O/x/x/4/8/open-book.svg
        book.move_to(offset_start)

        self.play(FadeIn(book))

        self.play(
            ApplyMethod(
                book.move_and_resize, offset, book_height_large / book_height_small
            )
        )
        # book travel

        # first square

        a = 5.0
        b = 12.0
        scale = 0.5 * book_height_large / (a + b)
        a *= scale
        b *= scale
        c = math.sqrt(a * a + b * b)

        # nejdriv vnejsi ctverce
        outer_shift = np.array((0.28 * book_height_large, 0.0 * book_height_large, 0))
        outer_color = solarized.GREEN
        outer_square = Square(side_length=(a + b), color=outer_color)
        outer_square.move_to(np.array(offset) - outer_shift)

        outer_square2 = outer_square.copy()
        outer_square2.move_to(np.array(offset) + outer_shift)

        # self.wait(1)

        # pak vnitrni
        inner_color = solarized.BLUE
        inner_square = Square(side_length=c, color=inner_color)
        inner_square.set_fill(inner_color, opacity=1.0)
        inner_square.rotate(math.asin(a / c))
        inner_square.align_to(outer_square, LEFT)
        inner_square.align_to(outer_square, DOWN)

        self.play(FadeIn(outer_square), FadeIn(outer_square2), FadeIn(inner_square))

        # self.wait(1)

        # pak trojuhelniky
        tr_color = solarized.RED

        pointedness = 0.00

        tr_botleft = RotPolygon([0, 0, 0], [a, 0, 0], [0, b, 0], color=tr_color)
        tr_botleft.align(outer_square, LEFT, DOWN)

        tr_botright = RotPolygon([0, 0, 0], [0, a, 0], [-b, 0, 0], color=tr_color)
        tr_botright.align(outer_square, RIGHT, DOWN)

        tr_topright = RotPolygon([0, 0, 0], [-a, 0, 0], [0, -b, 0], color=tr_color)
        tr_topright.align(outer_square, RIGHT, UP)

        tr_topleft = RotPolygon([0, 0, 0], [0, -a, 0], [b, 0, 0], color=tr_color)
        tr_topleft.align(outer_square, LEFT, UP)

        self.play(
            Create(tr_botleft),
            Create(tr_botright),
            Create(tr_topright),
            Create(tr_topleft),
        )
        # self.wait(1)

        # pak se presunou
        self.play(
            ApplyMethod(tr_botleft.align_and_rotate, outer_square2, LEFT, DOWN, 0),
            ApplyMethod(
                tr_botright.align_and_rotate,
                outer_square2,
                LEFT,
                DOWN,
                math.pi / 2,
                pointedness * UP,
            ),
            ApplyMethod(
                tr_topright.align_and_rotate, outer_square2, RIGHT, UP, -math.pi / 2
            ),
            ApplyMethod(
                tr_topleft.align_and_rotate,
                outer_square2,
                RIGHT,
                UP,
                0,
                pointedness * LEFT,
            ),
        )
        # self.play(MoveToTarget(tr_botright))

        # nakonec male ctverce
        thickness = 0.04
        a_square = Square(side_length=a - thickness, color=inner_color)
        a_square.align_to(outer_square2, LEFT)
        a_square.align_to(outer_square2, UP)
        a_square.shift((0, 0, -1))
        a_square.set_fill(inner_color, opacity=1.0)
        b_square = Square(side_length=b - thickness, color=inner_color)
        b_square.align_to(outer_square2, RIGHT)
        b_square.align_to(outer_square2, DOWN)
        a_square.shift((0, 0, 1))
        b_square.set_fill(inner_color, opacity=1.0)

        self.play(FadeIn(a_square), FadeIn(b_square))

        pythagoras = OGroup(
            outer_square,
            outer_square2,
            inner_square,
            tr_botright,
            tr_botleft,
            tr_topleft,
            tr_topright,
            a_square,
            b_square,
        )

        math_book = OGroup(book, pythagoras)

        ########################################################
        # erdos mluvi, knizka zaleze
        ########################################################


        bubble = SVGMobject(file_name = "img/Chat_bubble.svg").stretch(1.1, 0).stretch(0.8, 1)
        bubble.set_fill(solarized.BASE1)

        straight = Tex(r"Straight from the Book!", color=solarized.BASE02)

        bublina = Group(bubble, straight)
        straight.align_to(bubble, LEFT)
        straight.align_to(bubble, UP)
        straight.shift(0.4*DOWN+0.4*RIGHT)
        bublina.shift(3 * UP+0.4*LEFT)

        self.play(Create(bubble), Write(straight))
        # self.play(FadeOut(erdos), FadeOut(straight))

        self.play(
            ApplyMethod(
                math_book.move_and_resize,
                offset_finish,
                book_height_small / book_height_large,
            )
        )

        ########################################################
        # objevi se druha knizka, naleze doprostred, udela se v ni animace
        ########################################################

        # kniha
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
        highlight_color = solarized.RED

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

        self.play(ex_tree.animate.set_path_color(a, a, solarized.GREEN))
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

        ###########################################
        # erdos winks
        ###########################################

        wink_time = 0.3

        #zakomentovany flash
        #self.play(FadeIn(erdos_img_wink), Flash(5.2*LEFT + 2.1*UP), run_time=wink_time)
        self.play(ex_tree2.animate.change_layout(b_hanging), run_time=wink_time)
        self.play(FadeOut(erdos_img_wink), run_time=wink_time)

        self.play(ex_tree2.animate.change_layout(b_hanging), run_time=0.5)

        # TODO: animace s našimi jmény - Vašek ® a Václav (V),
        #   pokud bude separátní channel, tak jméno channelu,
        #   naznačit že mluví vašek v?, taky někde napsáno SoME challenge

        ################################################################
        # everything fades out, then names are displayed
        ################################################################

        self.play(FadeOut(Group(math_book, book2, erdos, ex_tree, ex_tree2, bubble, straight)))

        """            
        self.play(
            FadeOut(book2),
            FadeOut(ex_tree),
            FadeOut(erdos),
            FadeOut(math_book),
            FadeOut(straight),
            FadeOut(ex_tree2),            
        )"""

        volhejn = Tex(r"Václav Volhejn", color=text_color)
        rozhon = Tex(r"Václav Rozhoň", color=text_color)
        names = Group(rozhon, volhejn).arrange(DOWN)
        names.shift(2 * DOWN + 4 * RIGHT)
        volhejn.align_to(names, RIGHT)
        rozhon.align_to(names, RIGHT)

        some_highlight_color = solarized.RED
        some_challenge = MarkupText(
            f'<span fgcolor="{some_highlight_color}">S</span>ummer <span fgcolor="{some_highlight_color}">o</span>f <span fgcolor="{some_highlight_color}">M</span>ath<span fgcolor="{some_highlight_color}"> E</span>xposition <span fgcolor="{some_highlight_color}">1</span>',
            color=text_color,
            size=0.7,
        )
        some_challenge.shift(3 * LEFT + 2 * DOWN)
        channel_name = Tex(r"polylog", color=text_color)
        channel_name.shift(1 * UP)

        run_time = Write(channel_name).run_time
        self.play(
            Write(volhejn, run_time=run_time),
            Write(rozhon, run_time=run_time),
            Write(channel_name, run_time=run_time),
            Write(some_challenge, run_time=run_time),
        )

        self.wait(1)

        self.play(
            Unwrite(volhejn),
            Unwrite(rozhon),
            Unwrite(some_challenge),
            Unwrite(channel_name),
            run_time=1,
        )
        self.wait(1)


class TreeIntro(OScene):
    def construct(self):
        va1 = 34
        va2 = 7
        vc1 = 35 # 35
        vd1 = 20
        root = 33
        base_color = solarized.BASE00
        node_radius = 0.2

        self.outline(1)

        # https://illustoon.com/?dl=383
        tree = ImageMobject("img/tree.png")
        tree.shift(np.array((100, 0, 0)))
        self.add(tree)

        # tree.set_opacity(0.5)
        vertices, edges, positions = parse_tree_tree()

        self.T = Tree(
            vertices,
            edges,
            layout="kamada_kawai",
            #labels=True,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
            # Passed to:
            # https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.kamada_kawai_layout.html
            layout_config={"center": (-4, 0)},
        ).scale(1.2)

        # for k,v in self.T.positions:
        #    self.T.layout[k] = v * 0.5 + np.array((3,0,0))

        self.play(DrawBorderThenFill(self.T))

        self.wait(1)

        tree.shift(np.array((-100 + 3, 0, 0)))
        self.play(FadeIn(tree))

        self.wait(1)

        vec = tree.get_center() - tree.get_start()
        delta = positions[0] - tree.get_center() - np.array([0.0, 0 * 0.8 * vec[1], 0.0])-0.1*LEFT-0.1*DOWN
        # (-2.5, -6.0, 0.0)
        for k, v in positions.items():
            v -= delta

        self.play(self.T.animate.change_layout(positions))
        self.play(self.T.animate.change_layout(positions), run_time=3)

        self.play(FadeOut(tree), run_time=1)

        self.wait()
        # ted se prida hrana

        extra_edge = Line(
            self.T[vc1].get_center(), self.T[vd1].get_center(), color=solarized.RED
        )

        self.play(
            self.T.animate.set_colors_and_enlarge(
                {vc1: solarized.RED, vd1: solarized.RED}, sc=2
            )
        )
        self.wait(1)
        self.play(Create(extra_edge))
        self.wait(1)

        self.wait()
        self.wait(1)
        anim1, anim2 = self.T.path_animation(vc1, vd1, time_per_step=0.3)
        self.play(anim1)
        self.wait()
        self.play(anim2)
        # self.play(anim2)
        # self.play(self.T.animate.set_path_color(6, 22, solarized.RED))

        self.play(
            Uncreate(extra_edge),
            self.T.animate.set_colors_and_enlarge(
                {vc1: solarized.BASE00, vd1: solarized.BASE00}, sc=1.0 / 2
            ),
        )
        self.wait(1)

        # ted se odeberou vrcholy
        self.play(
            self.T.animate.set_colors_and_enlarge(
                vertex_colors={va1: solarized.BLUE, va2: solarized.BLUE}, sc=2
            )
        )
        self.wait(1)
        self.play(self.T.animate.remove_edges((va1, va2)))

        self.wait(1)
        self.play(
            self.T.animate.set_colors_and_enlarge(
                vertex_colors={va1: solarized.BASE00, va2: solarized.BASE00}, sc=0.5
            )
        )
        self.wait(1)
        self.play(FadeOut(self.T))
        self.wait(1)


class TreeExamples(Scene):
    def construct(self):
        # x = Dot()
        # self.add(x)

        # def foo(a):
        #     a.shift(RIGHT)
        #     a.scale(4)
        #     return a

        # self.play(ApplyFunction(foo, x))

        # self.play(x.animate.shift(RIGHT).scale(4))
        # self.play(x.animate)
        # self.wait()
        # return

        text_color = solarized.BASE00
        edges = tree_data.parse_linux_tree("fictional_filesystem.txt")

        vertices = set()
        for edge in edges:
            vertices.add(edge[0])
            vertices.add(edge[1])

        # vertex order influences layout
        vertices = sorted(list(vertices))
        # import os
        # seed = int(os.environ["seed"])
        # self.add(Text(str(seed), color=RED))
        """
        # seed search (Fish shell):
        for seed in (seq 100)
            env seed={$seed} manim -pql part1_trees.py TreeExamples -s
            sleep 1
        end
        """
        seed = 1
        rng: np.random.Generator = np.random.default_rng(seed=seed)
        rng.shuffle(vertices)

        file_tree = Tree(
            vertices,
            edges,
            layout="kamada_kawai",
            layout_scale=3,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
            # labels=labels,
            vertex_type=ExternalLabeledDot,
            labels=True,
            label_class=Tex,
        )

        for v in file_tree.vertices:
            file_tree[v].reposition_label(file_tree, v)

        # self.play(DrawBorderThenFill(Gbacteria))
        self.play(DrawBorderThenFill(file_tree))
        self.wait(1)

        self.play(file_tree.animate.shift(LEFT * 4).scale(0.6))

        filesystem_str = textwrap.dedent(
            """
            ├── Documents
            │   ├── Books
            │   ├── ETH
            │   │   ├── Notes
            │   │   └── Thesis
            │   └── SoME1
            ├── Downloads
            ├── Movies
            └── Pictures
            """
        )

        filesystem_text = (
            Text(filesystem_str, color=solarized.BASE00).scale(0.8).shift(RIGHT * 3)
        )

        self.wait()
        self.play(Create(filesystem_text))
        self.wait(3)

        self.play(Uncreate(filesystem_text))
        self.wait()

        # bacteria

        bacteria_mid_point = np.array((3.5, 0, 0))
        vertices, edges, positions, a, b, a2, b2, leaves = parse_bacteria_tree(
            shift=bacteria_mid_point
        )
        base_color = solarized.BASE00
        bac_highlight_color = solarized.RED
        node_radius = 0.05
        # labels = dict((v, Text(str(v), fill_color=BLACK, size=0.15)) for v in vertices)
        Gbacteria = Tree(
            vertices,
            edges,
            layout=positions,  # "kamada_kawai",
            labels=False,
            vertex_config={"radius": node_radius, "color": base_color},
            edge_config={"color": base_color},
        )

        self.play(DrawBorderThenFill(Gbacteria))
        self.wait(1)

        c = 67
        d = 68

        self.wait(1)

        sc = 1.8

        # bakterii se zvetsi listy
        self.play(
            Gbacteria.animate.set_colors_and_enlarge(
                dict((v, solarized.GREEN) for v in leaves), sc=sc
            )
        )
        self.wait(1)
        self.play(
            Gbacteria.animate.set_colors_and_enlarge(
                dict((v, base_color) for v in leaves), sc=1.0 / sc
            )
        )

        # highlightnou se dva podobne vrcholy
        self.play(
            Gbacteria.animate.set_colors_and_enlarge(
                {c: bac_highlight_color, d: bac_highlight_color}, sc=sc
            )
        )

        self.play(Gbacteria.animate.set_path_color(c, d, bac_highlight_color))
        self.wait()

        self.play(Gbacteria.animate.set_path_color(c, d, base_color))
        self.play(
            Gbacteria.animate.set_colors_and_enlarge(
                {c: base_color, d: base_color}, sc=1.0 / sc
            )
        )
        self.wait()

        # ted se zobrazi number of nodes

        txt_n_file = Tex(r"\# of nodes = 10", color=solarized.BASE00)
        txt_n_file.move_to(5 * LEFT + 2.5 * UP)
        txt_n_bacteria = Tex(r"\# of nodes = 114", color=solarized.BASE00)
        txt_n_bacteria.move_to(0.1 * LEFT + 3 * UP)

        self.play(Write(txt_n_file), Write(txt_n_bacteria))
        self.wait()
        self.play(Unwrite(txt_n_file), Unwrite(txt_n_bacteria))
        self.wait()

        # zobrazi se nejdelsi cesta a strom se orotuje
        self.wait(1)
        self.play(Gbacteria.animate.set_path_color(a, b))
        self.wait(1)

        self.play(
            Gbacteria.animate.rot(bacteria_mid_point, 47.0 / 360.0 * (2 * math.pi))
        )

        sc = 0.3
        dlt = 0.3
        self.wait(1)
        bact_hanging_position = Gbacteria.hanging_position(
            start=a, end=b, shift=bacteria_mid_point, delta=dlt, scale=sc
        )
        self.play(Gbacteria.animate.change_layout(bact_hanging_position), run_time=2)
        self.wait(1)

        txt_diameter = Tex(r"Diameter", color=text_color)
        txt_diameter.move_to(np.array((3.5, 2, 0)))
        txt_21 = Tex(r" = 21", color=text_color)
        txt_21.align_to(txt_diameter, RIGHT)
        txt_21.move_to(np.array((1, 0, 0)))
        # txt_21.move_to(np.array((3 + txt_diameter.get_end()-txt_diameter.get_start(), 1.5, 0)))

        seg_mid = Line(
            Gbacteria.vertices[a].get_center() + np.array((0, 1, 0)),
            Gbacteria.vertices[b].get_center() + np.array((0, 1, 0)),
            color=text_color,
        )
        l = 0.3
        seg_left = Line(
            seg_mid.get_start() + np.array((0, l, 0)),
            seg_mid.get_start() + np.array((0, -l, 0)),
            color=text_color,
        )
        seg_right = Line(
            seg_mid.get_end() + np.array((0, l, 0)),
            seg_mid.get_end() + np.array((0, -l, 0)),
            color=text_color,
        )
        seg = Group(seg_left, seg_mid, seg_right)

        self.play(Write(txt_diameter), FadeIn(seg))

        self.wait()
        self.play(Gbacteria.animate.set_path_color(a2, b2, solarized.BLUE))

        # bakterie se prevesi do druhe pozice, napise se co je diameter
        self.wait(1)
        bact_hanging_position2 = Gbacteria.hanging_position(
            start=a2, end=b2, shift=bacteria_mid_point, delta=dlt, scale=sc
        )
        self.play(Gbacteria.animate.change_layout(bact_hanging_position2), run_time=2)
        self.wait()
        # self.play(Write(txt_21))
        self.wait()

        file_a = "/Documents/ETH/Thesis"
        file_b = "/Downloads"
        # nejdelsi cesta ve file tree
        anim1, anim2 = file_tree.path_animation(
            file_a, file_b, color=solarized.RED, time_per_step=1.0
        )
        self.play(anim1)
        self.wait(1)

        txt_d_file = Tex(r"Diameter = 4", color=solarized.BASE00)
        txt_d_file.move_to(4 * LEFT + 2.5 * UP)
        self.play(Write(txt_d_file))
        self.wait()
        self.play(anim2, Unwrite(txt_d_file))

        self.wait(1)
        self.play(
            FadeOut(Gbacteria), FadeOut(file_tree), FadeOut(txt_diameter), FadeOut(seg)
        )
        self.wait(1)


def parse_tree_tree():
    L = 80.0
    positions = {}
    pos_to_vertex = {}
    edges = []
    data = [
        (float(d.split(" ")[0]) / L, float(d.split(" ")[1]) / L, 0)
        for d in tree_data.tree_data.splitlines()
    ]

    for i in range(int(len(data) / 2)):
        pos_u = data[2 * i]
        pos_v = data[2 * i + 1]
        if pos_u == pos_v:
            continue
        for pos in (pos_u, pos_v):
            if not pos in pos_to_vertex:
                node_id = len(pos_to_vertex)
                positions[node_id] = pos
                pos_to_vertex[pos] = node_id

        edges.append((pos_to_vertex[pos_u], pos_to_vertex[pos_v]))

    for k, v in positions.items():
        positions[k] = np.asarray(v)

    return range(len(positions)), edges, positions


def parse_bacteria_tree(rot=0.0, shift=np.array((0, 0, 0))):
    a = 6
    b = 111
    a2 = 16
    b2 = 105
    L = 90.0
    cycle_center = [279.847 / L, 427.013 / L, 0]
    cycle_radius = 273.232 / L
    positions = {}
    leaves = tree_data.bacteria_leaves
    pos_to_vertex = {}
    edges = []
    data = [
        (
            float(d.split(" ")[0]) / L - cycle_center[0],
            float(d.split(" ")[1]) / L - cycle_center[1],
            0.0,
        )
        for d in tree_data.bacteria_data.splitlines()
    ]

    for i in range(int(len(data) / 2)):
        pos_u = data[2 * i]
        pos_v = data[2 * i + 1]
        if pos_u == pos_v:
            continue
        for pos in (pos_u, pos_v):
            if not pos in pos_to_vertex:
                node_id = len(pos_to_vertex)
                positions[node_id] = pos
                pos_to_vertex[pos] = node_id
                # if math.dist((0,0,0), pos) > 0.95 * cycle_radius:
                #    leaves.append(node_id)
        edges.append((pos_to_vertex[pos_u], pos_to_vertex[pos_v]))

    """    
    leaves = []
    for k, v in positions.items():
        if math.dist((0,0,0), v) - cycle_radius > -0.2:
            leaves.append(k)
    print(leaves)
    """

    """
    for pos in positions:
        positions[pos] = (
            math.cos(rot) * positions[pos][0] + math.sin(rot) * positions[pos][1],
            math.cos(rot) * positions[pos][1] - math.sin(rot) * positions[pos][0],
            0.0,
        )
        # positions[pos] = (positions[pos][0], positions[pos][1], 0)
    """

    for k, v in positions.items():
        positions[k] = np.asarray(v) + shift

    return range(len(positions)), edges, positions, a, b, a2, b2, leaves
